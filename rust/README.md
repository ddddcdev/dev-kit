# Rust project standard

Reference configuration, not yet a copyable template. Same idea as the Python standard: one gate,
**`just check`**, for humans, agents, pre-commit and CI.

## Stack

| purpose | tool |
|---|---|
| toolchain | rustup, pinned per repo in `rust-toolchain.toml` (components `rustfmt`, `clippy`) |
| build, workspace | cargo (edition 2024, resolver 3, `[workspace.dependencies]`, `Cargo.lock` committed) |
| format | rustfmt (`cargo fmt --all --check`) |
| lint | clippy `all` + `pedantic` as warnings, run with `-D warnings` |
| tests | cargo-nextest, plus `cargo test --doc` (nextest skips doctests); insta for snapshots |
| dependency audit | cargo-deny (advisories, licenses, sources), cargo-machete (unused crates) |
| task runner | just (`justfile`) |
| errors | thiserror in libraries, anyhow in binaries |
| CLI | clap (derive) |
| logging | tracing + tracing-subscriber |

One-time tools: `cargo install --locked just cargo-nextest cargo-deny cargo-machete`.

## Files

`rust-toolchain.toml`:

```toml
[toolchain]
channel = "<latest stable, e.g. 1.99.1>"
components = ["rustfmt", "clippy"]
profile = "minimal"
```

`Cargo.toml` (workspace root):

```toml
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.package]
version = "0.1.0"
edition = "2024"
rust-version = "<MSRV>"
publish = false

[workspace.dependencies]
# every external crate is declared here once; member crates use `<name>.workspace = true`

[workspace.lints.rust]
unsafe_code = "forbid"
missing_debug_implementations = "warn"

[workspace.lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
module_name_repetitions = "allow"
missing_errors_doc = "allow"

[profile.release]
lto = "thin"
strip = true
```

Each member crate: `version.workspace = true`, `edition.workspace = true`, … and `[lints] workspace = true`.

`rustfmt.toml`: `edition = "2024"`.

`deny.toml`: `[advisories] yanked = "deny"`; `[licenses]` an explicit allow list of permissive licenses
(MIT, Apache-2.0, BSD-3-Clause, ISC, Unicode-3.0, Zlib, …), `private = { ignore = true }`;
`[bans] wildcards = "deny"`; `[sources] unknown-registry = "deny"`, `unknown-git = "deny"`.
Every `ignore` entry carries a `reason`.

`justfile`:

```just
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Everything CI runs. Run before pushing.
check: fmt-check lint test deny

fmt:
    cargo fmt --all

fmt-check:
    cargo fmt --all --check

lint:
    cargo clippy --workspace --all-targets -- -D warnings

test:
    cargo nextest run --workspace
    cargo test --workspace --doc

deny:
    cargo deny check
    cargo machete
```

`.pre-commit-config.yaml`: fast checks only (`cargo fmt --all --check`); the full gate is `just check`
and CI. Install with `GIT_CONFIG_GLOBAL=/dev/null pre-commit install` (see [git/setup.md](../git/setup.md)).

CI runs the same commands as `just check` with the toolchain version from `rust-toolchain.toml`
and a build cache (e.g. `Swatinem/rust-cache`).

## Conventions

- Bump the toolchain on purpose (edit `rust-toolchain.toml`), never float on `stable`.
- Pin a crate exactly (`=x.y.z`) only when its on-disk or wire format must match another program.
- `target/` is gitignored. Scratch output goes to `.scratch/`.
