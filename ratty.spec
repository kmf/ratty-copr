%global debug_package %{nil}
%global upstream_arch x86_64-unknown-linux-gnu

Name:           ratty
Version:        0.3.0
Release:        1%{?dist}
Summary:        GPU-rendered terminal emulator with inline 3D graphics
License:        MIT
URL:            https://ratty-term.org
ExclusiveArch:  x86_64

Source0:        https://github.com/orhun/ratty/releases/download/v%{version}/%{name}-%{upstream_arch}.tar.xz
Source1:        ratty.desktop

%description
Ratty is a GPU-rendered terminal emulator with inline 3D graphics support.

%prep
%setup -q -n %{name}-%{upstream_arch}

%build
# Pre-compiled binary — nothing to build.

%install
install -Dm755 ratty %{buildroot}%{_bindir}/ratty
install -Dm644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/ratty.desktop

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/ratty
%{_datadir}/applications/ratty.desktop

%changelog
* Wed May 13 2026 Karl Fischer <karl@obsidian.co.za> - 0.3.0-1
- Update to 0.3.0

* Tue May 12 2026 Karl Fischer <karl@obsidian.co.za> - 0.2.0-1
- Initial package
