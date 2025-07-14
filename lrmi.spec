#
# Conditional build:
%bcond_without	klibc	# use klibc for initrd/initramfs purposes
#
Summary:	Library for calling real mode BIOS routines under Linux
Summary(pl.UTF-8):	Biblioteka do wywoływania funkcji BIOS w trybie rzeczywistym pod Linuksem
Name:		lrmi
Version:	0.10
Release:	6
License:	BSD-like/Public Domain (see source)
Group:		Libraries
Source0:	http://dl.sourceforge.net/lrmi/%{name}-%{version}.tar.gz
# Source0-md5:	fc1d9495e8f4563fca471bb65f34a5da
Patch0:		%{name}-update-v86d.patch
URL:		http://sourceforge.net/projects/lrmi/
%{?with_klibc:BuildRequires:	klibc-devel}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with klibc}
%define		_klibdir	%{_prefix}/%{_lib}/klibc
%define		_kincludedir	%{_prefix}/include/klibc
%endif

%description
LRMI is a library for calling real mode BIOS routines under Linux.

%description -l pl.UTF-8
LRMI to biblioteka do wywoływania funkcji BIOS w trybie rzeczywistym
pod Linuksem.

%package devel
Summary:	Header files for lrmi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lrmi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for lrmi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lrmi.

%package static
Summary:	Static lrmi library
Summary(pl.UTF-8):	Statyczna biblioteka lrmi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lrmi library.

%description static -l pl.UTF-8
Statyczna biblioteka lrmi.

%package klibc-devel
Summary:	Header files and static lrmi library for klibc
Summary(pl.UTF-8):	Pliki nagłówkowe i statyczna biblioteka lrmi dla klibc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description klibc-devel
Header files and static lrmi library for klibc.

%description klibc-devel -l pl.UTF-8
Pliki nagłówkowe i statyczna biblioteka lrmi dla klibc.

%prep
%setup -q
%patch -P0 -p1

%build
%if %{with klibc}
%{__make} liblrmi.a \
	CC="klcc" \
	CFLAGS="%{rpmcflags} -Os -static -Wall"

mkdir -p klibc
cp liblrmi.a klibc/
%{__make} clean
%endif

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"

# Make non-static version:
rm vbetest
%{__cc} %{rpmcflags} -Wall -o vbetest vbetest.c liblrmi.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_includedir}/%{name}}

install vbetest $RPM_BUILD_ROOT%{_bindir}
install *.so *.a $RPM_BUILD_ROOT%{_libdir}
install vbe.h lrmi.h $RPM_BUILD_ROOT%{_includedir}/%{name}

%if %{with klibc}
install -d $RPM_BUILD_ROOT{%{_klibdir},%{_kincludedir}/%{name}}
install klibc/*.a $RPM_BUILD_ROOT%{_klibdir}
install vbe.h lrmi.h $RPM_BUILD_ROOT%{_kincludedir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vbetest
%attr(755,root,root) %{_libdir}/liblrmi.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/liblrmi.a

%if %{with klibc}
%files klibc-devel
%defattr(644,root,root,755)
%{_kincludedir}/%{name}
%{_klibdir}/liblrmi.a
%endif
