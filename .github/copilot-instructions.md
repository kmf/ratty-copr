# Copilot Instructions for ratty-copr

## Project Goal

This repository repackages the upstream prebuilt Ratty Linux binary from https://github.com/orhun/ratty/releases into an RPM and publishes it on Fedora Copr at https://copr.fedorainfracloud.org/coprs/kmf/ratty.

Ratty is a GPU-rendered terminal emulator with inline 3D graphics support.

## Architecture

This is a **binary repackaging project**, not a source build:

- **`ratty.spec`** — RPM spec file that downloads the upstream `ratty-x86_64-unknown-linux-gnu.tar.xz` release artifact, unpacks it, and installs:
  - `/usr/bin/ratty` (the precompiled binary)
  - `/usr/share/applications/ratty.desktop` (desktop entry)
  - License and documentation files
- **`.copr/Makefile`** — Entry point for Copr's "custom source" method. Running `make srpm outdir=<dir>` produces the SRPM that Copr builds into architecture-specific RPMs
- **`ratty.desktop`** — Freedesktop desktop entry, referenced as `Source1` in the spec
- **`.github/workflows/check-release.yml`** — Daily GitHub Actions workflow that checks for new upstream releases and opens a PR automatically

## Build Commands

```bash
# Local RPM build (requires rpm-build, rpmdevtools)
rpmdev-setuptree
cp ratty.desktop ~/rpmbuild/SOURCES/
spectool -g -R ratty.spec
rpmbuild -bb ratty.spec

# Build SRPM only
rpmbuild -bs ratty.spec

# Clean chroot build via mock (mirrors Copr behavior for Fedora 44)
rpmbuild -bs ratty.spec
mock -r fedora-44-x86_64 rebuild ~/rpmbuild/SRPMS/ratty-*.src.rpm

# Lint the spec file
rpmlint ratty.spec
```

## Release Update Workflow

### Automated (preferred)
- `.github/workflows/check-release.yml` runs daily at 08:00 UTC
- Detects new releases from upstream
- Opens a PR with updated spec and changelog
- Auto-merges the PR (using `--auto --squash`)
- Can be triggered manually via `workflow_dispatch`

### Manual update
1. Update `Version:` field in `ratty.spec`
2. Reset `Release:` to `1%{?dist}`
3. Add a `%changelog` entry with format:
   ```
   * Day Mon DD YYYY Name <email> - VERSION-RELEASE
   - Update to VERSION
   ```
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/): `build(spec): update to Ratty x.y.z`
5. Push to `main` — Copr rebuilds automatically

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): description`

Common types: `feat`, `fix`, `docs`, `chore`, `ci`, `build`, `refactor`, `test`

## Key Constraints

- **`ExclusiveArch: x86_64`** in the spec — only builds for x86_64 because that's the only arch upstream provides
- **No build phase** (`%build` is empty) — this is a binary repackage, not a source build
- **Source URL** in spec must match the exact upstream release artifact naming: `ratty-x86_64-unknown-linux-gnu.tar.xz`
- **Desktop file** must be copied to `~/rpmbuild/SOURCES/` before building locally (Copr handles this via `.copr/Makefile`)

## Copr Integration

Pushes to `main` trigger automatic rebuilds on Copr. The build process:
1. Copr clones the repo
2. Runs `.copr/Makefile` with `make srpm outdir=<dir>`
3. Builds the SRPM into RPMs for configured Fedora/EPEL chroots
4. Publishes to the Copr repository

Users install with:
```bash
sudo dnf copr enable kmf/ratty
sudo dnf install ratty
```
