#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Instant Messaging Encryption library with Whipsper System Sesame, Double Ratchet and X3DH protocols
Summary(pl.UTF-8):	Biblioteka szyfrowania komunikacji z protokołami Whipsper System Sesame, Double Ratchet oraz X3DH
Name:		lime
Version:	5.2.51
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/lime/-/tags
Source0:	https://gitlab.linphone.org/BC/public/lime/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	709f036e8c238b9797cf7a2d1aad0d6e
URL:		https://www.linphone.org/technical-corner/lime
# base+tester components
BuildRequires:	bctoolbox-devel >= 0.5.1
# for tester
BuildRequires:	belle-sip-devel
BuildRequires:	cmake >= 3.1
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libsoci-devel
BuildRequires:	libsoci-sqlite3-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LIME is an end-to-end encryption library for one-to-one and group
instant messaging, allowing users to exchange messages privately and
asynchronously. It uses modern ciphering curve X448 and double ratchet
algorithm for perfect forward secrecy.

LIME is composed of a portable client library coupled with a public
key server developed by Belledonne Communications to allow end-to-end
encryption for messaging, without having to exchange cryptographic
keys simultaneously.

%description -l pl.UTF-8
LIME to biblioteka szyfrowania transmisji między końcami połączenia
(end-to-end) na potrzeby komunikatorów osobistych i grupowych,
pozwalająca użytkownikom wymieniać wiadomości prywatnie i
asynchronicznie. Wykorzystuje nowoczesną krzywą szyfrującą X448 oraz
algorytm double ratchet w celu zapewnienia prywatności.

LIME składa się z przenośnej biblioteki klienckiej oraz serwera kluczy
publicznych, rozwijanych przez Belledonne Communications w celu
zapewnienia szyfrowania komunikacji między końcówkami bez potrzeby
jednoczesnej wymiany kluczy kryptograficznych.

%package devel
Summary:	Header files for LIME library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LIME
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bctoolbox-devel >= 0.5.1
Requires:	libsoci-devel
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for LIME library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LIME.

%package static
Summary:	Static LIME library
Summary(pl.UTF-8):	Statyczna biblioteka LIME
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LIME library.

%description static -l pl.UTF-8
Statyczna biblioteka LIME.

%package apidocs
Summary:	API documentation for LIME library
Summary(pl.UTF-8):	Dokumentacja API biblioteki LIME
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for LIME library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki LIME.

%prep
%setup -q

%build
install -d builddir
cd builddir
%cmake .. \
	-DENABLE_C_INTERFACE=ON \
	%{?with_apidocs:-DENABLE_DOC=ON} \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/lime/cmake/limeTargets.cmake

# omitted by cmake install
[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/lime.pc ] || exit 1
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -i -e 's,@CMAKE_INSTALL_PREFIX@,%{_prefix},' \
	-e 's,@PROJECT_NAME@,%{name},' \
	-e 's,@PROJECT_VERSION@,%{version},' \
	-e 's,@CMAKE_INSTALL_FULL_INCLUDEDIR@,%{_includedir},' \
	-e 's,@CMAKE_INSTALL_FULL_LIBDIR@,%{_libdir},' \
	-e 's,@LIBS_PRIVATE@,-lbctoolbox -lsoci_core,' \
	lime.pc.in >$RPM_BUILD_ROOT%{_pkgconfigdir}/lime.pc

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/lime-5.2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/lime_tester
%attr(755,root,root) %{_libdir}/liblime.so.0
%{_datadir}/lime_tester

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblime.so
%{_includedir}/lime
%{_pkgconfigdir}/lime.pc
%dir %{_datadir}/lime
%{_datadir}/lime/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblime.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc builddir/doc/html/*
%endif
