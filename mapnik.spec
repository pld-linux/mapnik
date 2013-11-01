#
Summary:	Toolkit for developing GIS (Geographic Information Systems) applications
Name:		mapnik
Version:	2.0.0
Release:	14
License:	LGPL v2.1
Group:		Applications
Source0:	http://download.berlios.de/mapnik/%{name}-%{version}.tar.bz2
# Source0-md5:	499c6a61544014b9bc2a7c978f963ef3
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
	INPUT_PLUGINS='raster,rasterlite,sqlite,osm,gdal,kismet,shape,postgis,ogr,geos,occi' \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG INSTALL README
%attr(755,root,root) %{_bindir}/mapnik-config
%attr(755,root,root) %{_bindir}/mapnik-speed-check
%attr(755,root,root) %{_bindir}/shapeindex
%attr(755,root,root) %{_bindir}/upgrade_map_xml.py
%attr(755,root,root) %{_libdir}/libmapnik2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmapnik2.so.2.0
%dir %{_libdir}/mapnik2
%dir %{_libdir}/mapnik2/input
%attr(755,root,root) %{_libdir}/mapnik2/input/gdal.input
%attr(755,root,root) %{_libdir}/mapnik2/input/geos.input
%attr(755,root,root) %{_libdir}/mapnik2/input/kismet.input
%attr(755,root,root) %{_libdir}/mapnik2/input/ogr.input
%attr(755,root,root) %{_libdir}/mapnik2/input/osm.input
%attr(755,root,root) %{_libdir}/mapnik2/input/postgis.input
%attr(755,root,root) %{_libdir}/mapnik2/input/raster.input
%attr(755,root,root) %{_libdir}/mapnik2/input/shape.input
%attr(755,root,root) %{_libdir}/mapnik2/input/sqlite.input

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmapnik2.so
%{_includedir}/mapnik

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/mapnik2
%{py_sitedir}/mapnik2/*.py[co]
%attr(755,root,root) %{py_sitedir}/mapnik2/_mapnik2.so
%dir %{py_sitedir}/mapnik2/ogcserver
%{py_sitedir}/mapnik2/ogcserver/*.py[co]
