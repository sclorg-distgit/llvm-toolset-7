%global scl_name_base llvm-toolset-
%global scl_name_version 7

%global scl %{scl_name_base}%{scl_name_version}

%scl_package %scl

%global dockerfiledir %{_datadir}/%{scl_prefix}dockerfiles

Summary: Package that installs %scl
Name: %scl_name
Version: 4.0.1
Release: 2%{?dist}
License: NCSA

# How to generate dockerfile tarbal:
# rhpkg clone llvm-toolset-7-docker
# cd llvm-toolset-7-docker
# git archive --prefix=llvm-toolset-7-docker/ -o llvm-toolset-7-docker-`git rev-parse --short HEAD`.tar.gz HEAD
Source0: llvm-toolset-7-docker-b49107f.tar.gz

Requires: %{scl_prefix}clang = %{version}

%ifarch %{arm} aarch64 %{ix86} x86_64
Requires: %{scl_prefix}lldb = %{version}
%endif

Requires: %{scl_prefix}llvm = %{version}
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

%package dockerfiles
Summary: Package shipping Dockerfiles for llvm-toolset

%description dockerfiles
This package provides a set of example Dockerfiles that can be used
with llvm-toolset.

%prep
%setup -c -T -a 0

%install
%scl_install

install -d %{buildroot}%{dockerfiledir}
install -d -p -m 755 %{buildroot}%{dockerfiledir}/rhel7
install -d -p -m 755 %{buildroot}%{dockerfiledir}/rhel7/llvm-toolset-7-docker
cp -a llvm-toolset-7-docker %{buildroot}%{dockerfiledir}/rhel7

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

%files dockerfiles
%{dockerfiledir}

%changelog
* Wed Aug 09 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-2
- Add docker file

* Wed Jun 21 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-1
- 4.0.1 Release.

* Wed Jun 21 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-6
- Fix Requires for lldb, this package is not built on all arches

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
