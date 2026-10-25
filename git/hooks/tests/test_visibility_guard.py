import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import visibility_guard as vg  # noqa: E402

POLICY = """
[defaults]
public = "allow"
on_error = "allow"
hosts = ["github.com"]
allow_public = ["alice/legacy-tool"]

[owners.alice]
public = "deny"

[owners.Acme-OSS]
public = "confirm"
on_error = "deny"
"""


def load(text):
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
        f.write(text)
    try:
        return vg.load_policy(f.name)
    finally:
        os.unlink(f.name)


def fetch_as(visibility):
    return lambda owner, repo: visibility


def no_resolve(alias):
    return alias


class ParseRemoteTest(unittest.TestCase):
    def test_forms(self):
        cases = {
            "git@github.com:alice/tool.git": ("github.com", "alice", "tool", True),
            "git@github-work:alice/tool.git": ("github-work", "alice", "tool", True),
            "https://github.com/alice/tool.git": ("github.com", "alice", "tool", False),
            "https://github.com/alice/tool": ("github.com", "alice", "tool", False),
            "ssh://git@github.com:22/alice/tool.git": ("github.com", "alice", "tool", True),
        }
        for url, expected in cases.items():
            self.assertEqual(vg.parse_remote(url), expected, url)

    def test_non_github_shapes(self):
        for url in ["/srv/git/repo.git", "../local", "file:///tmp/x.git", "https://host/a/b/c.git"]:
            self.assertIsNone(vg.parse_remote(url), url)


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.policy = load(POLICY)

    def check(self, url, visibility, allow_env=False, resolve=no_resolve):
        return vg.check(url, self.policy, allow_env, fetch=fetch_as(visibility), resolve=resolve)

    def test_deny_owner_public_blocked(self):
        ok, msg = self.check("git@github.com:alice/tool.git", "public")
        self.assertFalse(ok)
        self.assertIn("alice/tool", msg)

    def test_deny_owner_private_passes(self):
        self.assertEqual(self.check("git@github.com:alice/tool.git", "private"), (True, None))

    def test_allow_public_exception(self):
        self.assertTrue(self.check("git@github.com:alice/legacy-tool.git", "public")[0])

    def test_owner_case_insensitive(self):
        self.assertFalse(self.check("git@github.com:ALICE/tool.git", "public")[0])
        self.assertFalse(self.check("git@github.com:acme-oss/lib.git", "public")[0])

    def test_confirm_needs_env(self):
        self.assertFalse(self.check("https://github.com/acme-oss/lib.git", "public")[0])
        ok, msg = self.check("https://github.com/acme-oss/lib.git", "public", allow_env=True)
        self.assertTrue(ok)
        self.assertIn("PUBLIC", msg)

    def test_unknown_owner_allowed_without_lookup(self):
        def fail(owner, repo):
            raise AssertionError("should not fetch")

        ok, _ = vg.check("git@github.com:bob/x.git", self.policy, False, fetch=fail, resolve=no_resolve)
        self.assertTrue(ok)

    def test_on_error(self):
        self.assertTrue(self.check("git@github.com:alice/tool.git", None)[0])
        self.assertFalse(self.check("git@github.com:acme-oss/lib.git", None)[0])

    def test_ssh_alias_resolved(self):
        resolve = lambda alias: "github.com" if alias == "github-work" else alias  # noqa: E731
        self.assertFalse(self.check("git@github-work:alice/tool.git", "public", resolve=resolve)[0])
        self.assertTrue(self.check("git@gitlab.example:alice/tool.git", "public", resolve=resolve)[0])

    def test_https_other_host_not_resolved(self):
        def fail(alias):
            raise AssertionError("https hosts are not ssh aliases")

        self.assertTrue(self.check("https://gitlab.com/alice/tool.git", "public", resolve=fail)[0])


class LoadPolicyTest(unittest.TestCase):
    def test_invalid_mode(self):
        with self.assertRaises(vg.PolicyError):
            load('[owners.alice]\npublic = "block"\n')

    def test_invalid_toml(self):
        with self.assertRaises(vg.PolicyError):
            load("[defaults\n")

    def test_empty_policy_defaults(self):
        policy = load("")
        self.assertEqual(policy["hosts"], ["github.com"])
        self.assertEqual(vg.rule_for(policy, "x"), {"public": "allow", "on_error": "allow"})


if __name__ == "__main__":
    unittest.main()
