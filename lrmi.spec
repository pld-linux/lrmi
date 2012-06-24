Summary:	Library for calling real mode BIOS routines under Linux
Summary(pl):	Biblioteka do wywo�ywania funkcji BIOS w trybie rzeczywistym pod Linuksem
Name:		lrmi
Version:	0.9
Release:	1
License:	BSD-like/Public Domain (see source)
Group:		Libraries
Source0:	http://dl.sourceforge.net/lrmi/%{name}-%{version}.tar.gz
# Source0-md5:	00c2d0e4f4848100c04d8f88591cb943
URL:		http://sourceforge.net/projects/lrmi/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LRMI is a library for calling real mode BIOS routines under Linux.

%description -l pl
LRMI to biblioteka do wywo�ywania funkcji BIOS w trybie rzeczywistym
pod Linuksem.

%package devel
Summary:	Header files for lrmi library
Summary(pl):	Pliki nag��wkowe biblioteki lrmi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for lrmi library.

%description devel -l pl
Pliki nag��wkowe biblioteki lrmi.

%package static
Summary:	Static lrmi library
Summary(pl):	Statyczna biblioteka lrmi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lrmi library.

%description static -l pl
Statyczna biblioteka lrmi.

%prep
%setup -q

%build
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
