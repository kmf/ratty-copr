# ratty-copr

Fedora [Copr](https://copr.fedorainfracloud.org/) packaging for [Ratty](https://github.com/orhun/ratty) — a GPU-rendered terminal emulator with inline 3D graphics support.

Copr project: **https://copr.fedorainfracloud.org/coprs/kmf/ratty**

## What this repo does

This repo repackages the upstream prebuilt Linux binary from
[orhun/ratty releases](https://github.com/orhun/ratty/releases) into an RPM and
publishes it through Fedora Copr so it can be installed with `dnf`.

- `ratty.spec` — RPM spec that unpacks the upstream `ratty-x86_64-unknown-linux-gnu.tar.xz` and installs `/usr/bin/ratty` plus a desktop entry.
- `ratty.desktop` — Freedesktop entry, shipped as `Source1`.
- `.copr/Makefile` — Copr "custom source" entry point. `make srpm outdir=<dir>` builds an SRPM that Copr then turns into RPMs in its build chroots.
- `.github/workflows/check-release.yml` — Daily GitHub Actions check that opens a PR when a new upstream Ratty release appears.

Pushes to `main` trigger Copr to rebuild from the latest spec, so the published
repo follows upstream releases automatically.

## Installing Ratty from Copr

```bash
sudo dnf copr enable kmf/ratty
sudo dnf install ratty
```

To remove:

```bash
sudo dnf remove ratty
sudo dnf copr disable kmf/ratty
```

Only `x86_64` is published, matching the upstream binary release.

## Building locally

```bash
# Set up build tree and grab sources
rpmdev-setuptree
cp ratty.desktop ~/rpmbuild/SOURCES/
spectool -g -R ratty.spec

# Binary RPM
rpmbuild -bb ratty.spec

# SRPM only
rpmbuild -bs ratty.spec

# Clean chroot build via mock (mirrors what Copr does)
mock -r fedora-44-x86_64 rebuild ~/rpmbuild/SRPMS/ratty-*.src.rpm
```

Lint the spec:

```bash
rpmlint ratty.spec
```

## Updating to a new Ratty release

The daily workflow normally handles this. To do it by hand:

1. Bump `Version:` in `ratty.spec`.
2. Reset `Release:` to `1%{?dist}` and prepend a `%changelog` entry.
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
   (e.g. `build(spec): update to Ratty x.y.z`) and push to `main` — Copr will
   pick up the change and rebuild.

## License

Packaging files in this repo are MIT. Ratty itself is distributed under its own
license (see upstream).
