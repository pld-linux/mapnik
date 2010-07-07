#
Summary:	Toolkit for developing GIS (Geographic Information Systems) applications
Name:		mapnik
Version:	0.7.1
Release:	1
License:	LGPL v2.1
Group:		Applications
Source0:	http://download.berlios.de/mapnik/%{name}-%{version}.tar.bz2
# Source0-md5:	8f65fda2a792518d6f6be8a85f62fc73
Patch0:		%{name}-boost_lib_names.patch
URL:		http://mapnik.org/
BuildRequires:	boost-devel
BuildRequires:	boost-python-devel
BuildRequires:	cairomm-devel
BuildRequires:	curl-devel
BuildRequires:	freetype-devel
BuildRequires:	gdal-devel
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libltdl-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	proj-devel
BuildRequires:	python-devel
BuildRequires:	python-pycairo-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	scons
BuildRequires:	sqlite3-devel
BuildRequires:	zlib-devel
Suggests:	fonts-TTF-DejaVu
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mapnik is a Free Toolkit for developing mapping applications. It's
written in C++ and there are Python bindings to facilitate fast-paced
agile development. It can comfortably be used for both desktop and web
development, which was something I wanted from the beginning.

Mapnik is about making beautiful maps. It uses the AGG library and
offers world class anti-aliasing rendering with subpixel accuracy for
geographic data. It is written from scratch in modern C++ and doesn't
suffer from design decisions made a decade ago.

%package -n python-%{name}
Summary:	Python bindings for Mapnik
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-%{name}
Python binding for Mapnik, the toolkit for developing GIS (Geographic
Information Systems) applications.

%package devel
Summary:	Header files for Mapnik
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Mapnik
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Mapnik.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Mapnik.

%package static
Summary:	Static Mapnik library
Summary(pl.UTF-8):	Statyczna biblioteka Mapnik
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Mapnik library.

%description static -l pl.UTF-8
Statyczna biblioteka Mapnik.

%prep
%setup -q
%patch0 -p1

%build
%scons \
	PREFIX=%{_prefix} \
	BOOST_TOOLKIT=gcc43 \
	INPUT_PLUGINS='raster,sqlite,osm,gdal,kismet,shape,postgis,ogr' \
	SYSTEM_FONTS=%{_datadir}/fonts/TTF

%install
rm -rf $RPM_BUILD_ROOT

%scons install \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT \
	SYSTEM_FONTS=%{_datadir}/fonts/TTF

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

## DejaVu fonts are available in a separate package
#rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG INSTALL README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/input
%attr(755,root,root) %{_libdir}/%{name}/input/*.input

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%dir %{py_sitedir}/%{name}/ogcserver
%{py_sitedir}/%{name}/ogcserver/*.py[co]
