Name:           qtop
Version:        1.7
Release:        1%{?dist}
Summary:        A top-like job viewer for OpenPBS

License:        GPLv3
URL:            https://github.com/fnevgeny/qtop
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.0
BuildRequires:  gcc
BuildRequires:  ncurses-devel
BuildRequires:  openpbs-devel

%description
qtop aims to help in monitoring and analyzing performance of jobs on OpenPBS systems.
By default, it will list all your active (i.e., not finished) jobs.
It provides a top-like interface with metrics for memory, CPU utilization, 
and walltime, helping to identify misbehaving or inefficient jobs.

%prep
%autosetup -n %{name}-%{version}

%build
# 1. Disable the "Hardened Build" macro which injects the -pie flags automatically
%define _hardened_build 0

# 2. Manually overwrite flags to ensure NO PIE is used.
# We strip out the system defaults that include -specs=/usr/lib/rpm/redhat/...
export CFLAGS="-O2 -g -pipe -Wall -fno-PIE"
export CXXFLAGS="-O2 -g -pipe -Wall -fno-PIE"
export LDFLAGS="-no-pie"

%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/qtop
%{_mandir}/man1/qtop.1*

%changelog
* Wed Jan 28 2026 Gemini <gemini@google.com> - 1.7-1
- Initial RPM release for qtop 1.7
- Force disable PIE (Position Independent Executable) to fix linking against static libpbs.a
- Overwrote CFLAGS/LDFLAGS to remove conflicting RHEL hardening specs
