%define	name	rss_glx
%define	oname	rss-glx
%define	fname	%{oname}_%{version}
%define	version	0.8.2
%define	release	%mkrel 5
%define	build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}


%if %build_plf
%define	distsuffix plf
%endif

Summary:	Really Slick Screensavers Port to GLX
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%fname.tar.bz2
Patch: rss-glx_0.8.1-desktopentry.patch
Patch2:		rss-glx_0.8.2-missing-header.patch
Patch3: rss-glx_0.8.2-format-strings.patch
License:	GPLv2
Group:		Graphical desktop/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://rss-glx.sourceforge.net/
BuildRequires:	libx11-devel
BuildRequires:	openal-devel
BuildRequires:	libxt-devel
BuildRequires:	libfreealut-devel
BuildRequires:	libglew-devel
BuildRequires:	libmesaglu-devel
BuildRequires:	bzip2-devel
BuildRequires:	imagemagick-devel >= 5.5.7
BuildRequires:	chrpath
Requires:	xscreensaver
Epoch:		1

%description
This is a collection of OpenGL screensavers for xscreensaver. They
require a hardware-accellerated GLX implementation.

You need to add them manually to your ~/.xscreensaver file as described
in README.xscreensaver

%if %build_plf
This package is in PLF, as it includes images that are similar to
those from the Matrix movies.
%endif

%package	matrixview
Summary:	Really Slick Screensavers Port to GLX - Matrixview 
Group:		Graphical desktop/Other
Requires:	xscreensaver

%description	matrixview
This is a collection of OpenGL screensavers for xscreensaver. They
require a hardware-accellerated GLX implementation.

This contains the matrixview screensaver. It is in PLF, as it includes
images that are similar to those from the Matrix movies.

%prep
%setup -q -n %fname
%patch -p1 -b .desktopentry
%patch2 -p1
%patch3 -p1
autoreconf -fi

%build
%configure2_5x \
 --with-configdir=%_datadir/xscreensaver/config \
 --bindir=%_libexecdir/xscreensaver \
 --with-kdessconfigdir=%_datadir/applnk/System/ScreenSavers/
%make CXXFLAGS="$RPM_OPT_FLAGS" CPPFLAGS="-I%_includedir/ImageMagick"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
# we don't need the static libs
rm -rf %buildroot%_libdir/lib*a
%if ! %build_plf
rm -f %buildroot%_libexecdir/xscreensaver/matrixview
rm -f %buildroot%_mandir/man1/matrixview.1
rm -f %buildroot%_datadir/xscreensaver/config/matrixview.xml
rm -f %buildroot%_datadir/applnk/System/ScreenSavers/matrixview.desktop
%endif
for screensaver in %buildroot%_libdir/xscreensaver/*;
 do fgrep -q ELF $screensaver && chrpath -d $screensaver
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README*
%_libexecdir/xscreensaver/*
%_mandir/man1/*
%_datadir/xscreensaver/config/*
%_datadir/applnk/System/ScreenSavers/*

%if %build_plf
%exclude %_libexecdir/xscreensaver/matrixview
%exclude %_mandir/man1/matrixview.1*
%exclude %_datadir/xscreensaver/config/matrixview.xml
%exclude %_datadir/applnk/System/ScreenSavers/matrixview.desktop
%endif

%if %build_plf
%files matrixview
%defattr(-,root,root)
%doc README*
%_libexecdir/xscreensaver/matrixview
%_mandir/man1/matrixview.1*
%_datadir/xscreensaver/config/matrixview.xml
%_datadir/applnk/System/ScreenSavers/matrixview.desktop
%endif


