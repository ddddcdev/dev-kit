"""Pre-push guard: refuse pushes to public GitHub repos according to a policy file.

Called as `visibility_guard.py <remote-name> <remote-url>` with the pre-push refs on stdin.
Visibility is looked up without authentication: 200 means public, 404 means private
(or nonexistent), so no token or account switching is needed.

Policy (TOML) at $VISIBILITY_GUARD_POLICY or ~/.config/git/visibility-policy.toml.
No policy file means the guard does nothing. See visibility-policy.example.toml.
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    tomllib = None

POLICY_ENV = "VISIBILITY_GUARD_POLICY"
DEFAULT_POLICY = "~/.config/git/visibility-policy.toml"
ALLOW_ENV = "ALLOW_PUBLIC_PUSH"
API_URL = "https://api.github.com/repos/{owner}/{repo}"

PUBLIC_MODES = ("allow", "confirm", "deny")
ERROR_MODES = ("allow", "deny")
DEFAULTS = {"public": "allow", "on_error": "allow", "hosts": ["github.com"], "allow_public": []}

SCP_RE = re.compile(r"^(?:[^@/]+@)?(?P<host>[^:/]+):(?!/)(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$")
URL_RE = re.compile(
    r"^(?P<scheme>ssh|https?|git)://(?:[^@/]+@)?(?P<host>[^/:]+)(?::\d+)?/"
    r"(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$"
)


class PolicyError(Exception):
    pass


def parse_remote(url):
    """Return (host, owner, repo, is_ssh) or None for URLs that are not owner/repo shaped."""
    m = URL_RE.match(url)
    if m:
        return m["host"], m["owner"], m["repo"], m["scheme"] == "ssh"
    m = SCP_RE.match(url)
    if m:
        return m["host"], m["owner"], m["repo"], True
    return None


def resolve_ssh_host(alias):
    """Map an ~/.ssh/config Host alias (e.g. github-work) to its HostName."""
    try:
        out = subprocess.run(
            ["ssh", "-G", alias], capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return alias
    for line in out.splitlines():
        key, _, value = line.partition(" ")
        if key == "hostname" and value:
            return value
    return alias


def load_policy(path):
    if tomllib is None:
        raise PolicyError("tomllib unavailable (needs Python 3.11+)")
    try:
        with open(path, "rb") as f:
            raw = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise PolicyError(f"invalid TOML in {path}: {e}") from e
    defaults = {**DEFAULTS, **raw.get("defaults", {})}
    owners = {k.lower(): v for k, v in raw.get("owners", {}).items()}
    for scope, rule in [("defaults", defaults), *owners.items()]:
        if rule.get("public", "allow") not in PUBLIC_MODES:
            raise PolicyError(f"{scope}.public must be one of {PUBLIC_MODES}")
        if rule.get("on_error", "allow") not in ERROR_MODES:
            raise PolicyError(f"{scope}.on_error must be one of {ERROR_MODES}")
    return {
        "defaults": defaults,
        "owners": owners,
        "hosts": [h.lower() for h in defaults["hosts"]],
        "allow_public": {r.lower() for r in defaults["allow_public"]},
    }


def rule_for(policy, owner):
    d = policy["defaults"]
    return {"public": d["public"], "on_error": d["on_error"], **policy["owners"].get(owner.lower(), {})}


def fetch_visibility(owner, repo, timeout=5):
    """Return "public", "private", or None when it cannot be determined."""
    req = urllib.request.Request(
        API_URL.format(owner=owner, repo=repo),
        headers={"Accept": "application/vnd.github+json", "User-Agent": "visibility-guard"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        return "private" if e.code == 404 else None
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return "private" if data.get("private") else "public"


def decide(rule, slug, visibility, allow_env):
    """Return (ok, message). message is None when there is nothing to say."""
    if visibility == "private":
        return True, None
    if visibility is None:
        if rule["on_error"] == "deny":
            return False, f"could not determine visibility of {slug}; policy denies on error"
        return True, f"could not determine visibility of {slug}; allowed by policy"
    mode = rule["public"]
    if mode == "allow":
        return True, None
    if mode == "confirm":
        if allow_env:
            return True, f"pushing to PUBLIC repo {slug} ({ALLOW_ENV}=1)"
        return False, f"{slug} is PUBLIC; push requires {ALLOW_ENV}=1"
    return False, f"{slug} is PUBLIC; policy forbids public repos under this owner"


def check(url, policy, allow_env, fetch=fetch_visibility, resolve=resolve_ssh_host):
    parsed = parse_remote(url)
    if parsed is None:
        return True, None
    host, owner, repo, is_ssh = parsed
    if host.lower() not in policy["hosts"] and is_ssh:
        host = resolve(host)
    if host.lower() not in policy["hosts"]:
        return True, None
    slug = f"{owner}/{repo}"
    if slug.lower() in policy["allow_public"]:
        return True, None
    rule = rule_for(policy, owner)
    if rule["public"] == "allow":
        return True, None
    return decide(rule, slug, fetch(owner, repo), allow_env)


def main(argv):
    if len(argv) < 3:
        return 0
    url = argv[2]
    if not sys.stdin.read().strip():
        return 0  # nothing to push
    path = os.path.expanduser(os.environ.get(POLICY_ENV) or DEFAULT_POLICY)
    if not os.path.exists(path):
        return 0
    try:
        policy = load_policy(path)
    except PolicyError as e:
        print(f"visibility-guard: {e}", file=sys.stderr)
        return 1
    ok, message = check(url, policy, os.environ.get(ALLOW_ENV) == "1")
    if message:
        print(f"visibility-guard: {message}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
