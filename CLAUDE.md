# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

Package the latest Ratty Linux binary release from https://github.com/orhun/ratty/releases into an RPM and publish it on Fedora Copr.

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): description`

Types: `feat`, `fix`, `docs`, `chore`, `ci`, `build`, `refactor`, `test`

## Build Commands

```bash
# Local RPM build (requires rpm-build, rpmdevtools)
rpmdev-setuptree
cp ratty.desktop ~/rpmbuild/SOURCES/
spectool -g -R ratty.spec
rpmbuild -bb ratty.spec

# Build SRPM only
rpmbuild -bs ratty.spec

# Clean chroot build via mock (Fedora 44)
rpmbuild -bs ratty.spec
mock -r fedora-44-x86_64 rebuild ~/rpmbuild/SRPMS/ratty-*.src.rpm

# Lint
rpmlint ratty.spec
```

## Architecture

- `ratty.spec` — RPM spec that repackages the upstream `ratty-x86_64-unknown-linux-gnu.tar.xz` (prebuilt Rust binary) into `/usr/bin/ratty` plus a desktop entry
- `.copr/Makefile` — Entry point for Copr custom source method; `make srpm outdir=<dir>` produces an SRPM
- `ratty.desktop` — Freedesktop desktop entry, referenced as Source1 in the spec

## Updating to a New Ratty Release

A GitHub Actions workflow (`.github/workflows/check-release.yml`) runs daily at 08:00 UTC and opens a PR when a new upstream release is detected. It can also be triggered manually via `workflow_dispatch`.

To update manually:
1. Update `Version:` in `ratty.spec`
2. Add a `%changelog` entry
3. Push — Copr rebuilds automatically
