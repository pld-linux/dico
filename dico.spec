#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	GNU Dico - flexible implementation of DICT server
Summary(pl.UTF-8):	GNU Dico - elastyczna implementacja serwera DICT
Name:		dico
Version:	2.11
Release:	1
License:	GPL v3+
Group:		Applications/Text
Source0:	https://ftp.gnu.org/gnu/dico/%{name}-%{version}.tar.xz
# Source0-md5:	f55fe3917abeb6fd74eccd3b0327d0d7
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-info.patch
URL:		http://www.gnu.org/software/dico/
BuildRequires:	WordNet-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.15
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	gsasl-devel >= 0.2.5
BuildRequires:	guile-devel >= 5:2.2.0
BuildRequires:	libltdl-devel >= 2:2.4
BuildRequires:	libtool >= 2:2.4
BuildRequires:	ncurses-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dico is a flexible implementation of DICT server (RFC 2229). The
server is modular: the daemon itself (dicod) provides only the server
functionality, and knows nothing about database formats. Actual
searches are performed by functions supplied in loadable modules. A
single module can handle any number of database instances. 

The package includes several modules for searching in different
dictionary databases, such as dict.org, WordNet and others.

%description -l pl.UTF-8
Dico do elastyczna implementacja serwera DICT (RFC 2229). Serwer jest
modularny - sam demon (dicod) zapewnia jedynie funkcjonalność serwera,
natomiast nie zna żadnego formatu bazy danych. Właściwe wyszukiwanie
jest wykonywane przez funkcje dostarczane w ładowanych modułach.
Pojedynczy moduł może obsłużyć dowolną liczbę instancji bazy danych.

Pakiet zawiera kilka modułów do wyszukiwania w różnych bazach danych
słowników, takich jak dict.org, WordNet i inne.

%package libs
Summary:	GNU Dico shared library
Summary(pl.UTF-8):	Biblioteka współdzielona GNU Dico
Group:		Libraries

%description libs
GNU Dico shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona GNU Dico.

%package devel
Summary:	Header files for GNU Dico library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GNU Dico
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for GNU Dico library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GNU Dico.

%package static
Summary:	Static GNU Dico library
Summary(pl.UTF-8):	Statyczna biblioteka GNU Dico
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Statices for GNU Dico library.

%description static -l pl.UTF-8
Statyczna biblioteka GNU Dico.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4 -I am -I grecs/am -I gint -I imprimatur
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	WISH=/usr/bin/wish \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdico.la \
	$RPM_BUILD_ROOT%{_libdir}/dico/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/dico/*.a
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog* NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/dico
%attr(755,root,root) %{_bindir}/dicod
%attr(755,root,root) %{_bindir}/gcider
%attr(755,root,root) %{_libexecdir}/idxgcide
%dir %{_libdir}/dico
%attr(755,root,root) %{_libdir}/dico/dictorg.so
%attr(755,root,root) %{_libdir}/dico/echo.so
%attr(755,root,root) %{_libdir}/dico/gcide.so
%attr(755,root,root) %{_libdir}/dico/guile.so
%attr(755,root,root) %{_libdir}/dico/ldap.so
%attr(755,root,root) %{_libdir}/dico/metaphone2.so
%attr(755,root,root) %{_libdir}/dico/nprefix.so
%attr(755,root,root) %{_libdir}/dico/outline.so
%attr(755,root,root) %{_libdir}/dico/pam.so
%attr(755,root,root) %{_libdir}/dico/pcre.so
%attr(755,root,root) %{_libdir}/dico/python.so
%attr(755,root,root) %{_libdir}/dico/stratall.so
%attr(755,root,root) %{_libdir}/dico/substr.so
%attr(755,root,root) %{_libdir}/dico/word.so
%attr(755,root,root) %{_libdir}/dico/wordnet.so
%{_datadir}/dico
%{_infodir}/dico.info*
%{_mandir}/man1/dico.1*
%{_mandir}/man5/dicod.conf.5*
%{_mandir}/man8/dicod.8*

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdico.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdico.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdico.so
%{_includedir}/dico

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdico.a
%endif
