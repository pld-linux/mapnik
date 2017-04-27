# it's not possible to build this with debuginfo on 32bit archs due to
# memory constraints
%ifarch %{ix86} x32
%define		_enable_debug_packages		0
%endif
Summary:	Toolkit for developing GIS (Geographic Information Systems) applications
Name:		mapnik
Version:	3.0.12
Release:	1
License:	LGPL v2.1
Group:		Applications
Source0:	https://github.com/mapnik/mapnik/releases/download/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	221c1fa8e63f4cc93b3040e9382e3394
Patch0:		mapnik-boost_lib_names.patch
Patch1:		cxx.patch
Patch2:		icu59.patch
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
BuildRequires:	librasterlite-devel
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
Obsoletes:	python-mapnik < 3.0.9-1
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
%setup -q -n %{name}-v%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%scons configure \
	CUSTOM_CXXFLAGS="%{rpmcxxflags}" \
	CUSTOM_CFLAGS="%{rpmcflags}" \
	CUSTOM_LDFLAGS="%{rpmldflags}" \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	BOOST_TOOLKIT=gcc43 \
	INPUT_PLUGINS='csv,gdal,geojson,ogr,pgraster,postgis,raster,shape,sqlite,topojson' \
	SYSTEM_FONTS=%{_datadir}/fonts/TTF \
	LIBDIR_SCHEMA=%{_lib} \
	SVG2PNG=True

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md INSTALL.md README.md
%attr(755,root,root) %{_bindir}/mapnik-config
%attr(755,root,root) %{_bindir}/mapnik-index
%attr(755,root,root) %{_bindir}/mapnik-render
%attr(755,root,root) %{_bindir}/shapeindex
%attr(755,root,root) %{_libdir}/libmapnik.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmapnik.so.3.0
%dir %{_libdir}/mapnik
%dir %{_libdir}/mapnik/input
%attr(755,root,root) %{_libdir}/mapnik/input/csv.input
%attr(755,root,root) %{_libdir}/mapnik/input/gdal.input
%attr(755,root,root) %{_libdir}/mapnik/input/geojson.input
%attr(755,root,root) %{_libdir}/mapnik/input/ogr.input
%attr(755,root,root) %{_libdir}/mapnik/input/pgraster.input
%attr(755,root,root) %{_libdir}/mapnik/input/postgis.input
%attr(755,root,root) %{_libdir}/mapnik/input/raster.input
%attr(755,root,root) %{_libdir}/mapnik/input/shape.input
%attr(755,root,root) %{_libdir}/mapnik/input/sqlite.input
%attr(755,root,root) %{_libdir}/mapnik/input/topojson.input

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmapnik.so
%{_includedir}/mapnik
%{_libdir}/libmapnik-json.a
%{_libdir}/libmapnik-wkt.a
