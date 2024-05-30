#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Collection of C++ Data Structures, Algorithms, and Miscellaneous Helpers
Summary(pl.UTF-8):	Zbiór struktur danych, algorytmów i klas pomocniczych dla C++
Name:		tlx
Version:	0.6.1
Release:	1
License:	Boost v1.0
Group:		Libraries
#Source0Download: https://github.com/tlx/tlx/releases
Source0:	https://github.com/tlx/tlx/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3d92269e11e6f3c901df8f92152988d9
Patch0:		%{name}-library.patch
URL:		http://panthema.net/2018/0528-tlx-library/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tlx is a collection of C++ helpers and extensions universally needed,
but not found in the STL. The most important design goals and
conventions are:
 - high modularity with as little dependencies between modules as
   possible
 - attempt to never break existing interfaces
 - compile on all platforms with C++ - smartphones, supercomputers,
   windows, etc.
 - zero external dependencies: no additional libraries are required
 - warning and bug-freeness on all compilers
 - keep overhead down - small overall size such that is can be
   included without bloating applications.

%description -l pl.UTF-8
tlx to zbiór klas pomocniczych i rozszerzeń dla C++, które często są
potrzebne, ale nie ma ich w STL. Najważniejsze cele i konwencje
projektowe to:
 - duża modularność i możliwie mało zależności między modułami
 - próba nie łamania zgodności istniejących interfejsów
 - kompilacja na wszystkich platformach z C++ - telefonach,
   superkomputerach, okienkach itp.
 - brak zależności zewnętrznych: nie są potrzebne żadne dodatkowe
   biblioteki
 - brak ostrzeżeń i błędów na wszystkich kompilatorach
 - możliwie mały narzut - całkowity rozmiar mały na tyle, że
   włączenie nie rozdmucha aplikacji   

%package devel
Summary:	Header files of tlx library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tlx
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files of tlx library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tlx.

%package static
Summary:	Static tlx library
Summary(pl.UTF-8):	Statyczna biblioteka tlx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static tlx library.

%description static -l pl.UTF-8
Statyczna biblioteka tlx.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DTLX_BUILD_SHARED_LIBS=ON
	%{!?with_static_libs:-DTLX_BUILD_STATIC_LIBS=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{_libdir}/libtlx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtlx.so.0.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtlx.so
%{_includedir}/tlx
%{_pkgconfigdir}/tlx.pc
%{_libdir}/cmake/tlx

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtlx.a
%endif
