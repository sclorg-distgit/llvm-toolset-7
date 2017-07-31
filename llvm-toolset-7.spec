%global scl_name_base llvm-toolset-
%global scl_name_version 7

%global scl %{scl_name_base}%{scl_name_version}

%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 4.0.0
Release: 5%{?dist}
License: NCSA
Requires: %{scl_prefix}clang
Requires: %{scl_prefix}lldb
Requires: %{scl_prefix}llvm
Requires: %{scl_prefix}python-lit
BuildRequires: scl-utils-build
BuildRequires: python2-devel

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH="%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}"
export LD_LIBRARY_PATH="%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"
export MANPATH="%{_mandir}:\${MANPATH:-}"
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}"
export PYTHONPATH="%{?scl:%{_scl_root}}%{python2_sitelib}\${PYTHONPATH:+:\${PYTHONPATH}}"
EOF

%files

%files runtime -f filelist
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Mon Jun 05 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-5
- Remove scldevel package

* Mon Jun 05 2017 Tom Stellard <tstellar@rehat.com> - 4.0.0-4
- Remove unnecessary code

* Fri May 12 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-3
- Add clang, lldb, and python-lit to Requires

* Wed May 10 2017 Tilmann Scheller <tschelle@redhat.com> - 4.0.0-2
- Update PYTHONPATH to point to the scl's Python site-packages directory

* Mon Apr 24 2017 Tom Stellard <tstellar@redhat.com> 4.0.0-1
- Initial package
