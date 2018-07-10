%global scl_name_base llvm-toolset-
%global scl_name_version 7

%global scl %{scl_name_base}%{scl_name_version}

%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 5.0.1
Release: 4%{?dist}
License: NCSA

Requires: %{scl_prefix}clang = %{version}

%ifarch %{arm} aarch64 %{ix86} x86_64
Requires: %{scl_prefix}lldb = %{version}
%endif

Requires: %{scl_prefix}llvm = %{version}
Requires: %{scl_prefix}python-lit
BuildRequires: scl-utils-build
BuildRequires: python2-devel

Obsoletes: %{scl_prefix}dockerfiles < 5.0.0

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

# This allows users to build packages using LLVM Toolset.
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl} << EOF
%%enable_llvmtoolset7 %%global ___build_pre %%{___build_pre}; source scl_source enable %{scl} || :
EOF

%files

%files runtime -f filelist
%scl_files
%{_root_sysconfdir}/rpm/macros.%{scl}

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Fri Feb 23 2018 Tom Stellard <tstellar@redhat.com> - 5.0.1-4
- Obsolete llvm-toolset-7-dockerfiles

* Fri Feb 16 2018 Tilmann Scheller <tschelle@redhat.com> - 5.0.1-3
- Move %enable_llvmtoolset7 macro to the -build subpackage to avoid conflicts
  between multiple definitions of %scl when using llvm-toolset-7 to build a SCL

* Thu Feb 08 2018 Tilmann Scheller <tschelle@redhat.com> - 5.0.1-2
- Add %enable_llvmtoolset7 macro to make it easier to activate llvm-toolset-7
  during package builds.

* Wed Jan 17 2018 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- LLVM 5.0.1 release

* Wed Jan 17 2018 Tom Stellard <tstellar@redhat.com> - 4.0.1-5
- Drop dockerfiles package

* Wed Oct 04 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-4
- Update Dockerfile

* Wed Sep 20 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-3
- Update Dockerfile

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
