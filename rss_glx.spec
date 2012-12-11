%define	oname	rss-glx
%define	fname	%{oname}_%{version}

%define	build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

%if %build_plf
%define	distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

Summary:	Really Slick Screensavers Port to GLX
Name:		rss_glx
Version:	0.9.1
Release:	2%{?extrarelsuffix}
Epoch:		1
License:	GPLv2
Group:		Graphical desktop/Other
URL:		http://rss-glx.sourceforge.net/
Source0:	%{fname}.tar.bz2
Patch0:		rss-glx_0.9.1-linkage.patch
Patch1:		rss-glx_0.9.1-desktopentry.patch
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(quesoglc)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xt)
BuildRequires:	chrpath
Requires:	xscreensaver

%description
This is a collection of OpenGL screensavers for xscreensaver. They
require a hardware-accellerated GLX implementation.

You need to add them manually to your ~/.xscreensaver file as described
in README.xscreensaver

%if %{build_plf}
This package is in Restricted repository, as it includes images that
are similar to those from the Matrix movies.
%endif

%package	matrixview
Summary:	Really Slick Screensavers Port to GLX - Matrixview 
Group:		Graphical desktop/Other
Requires:	xscreensaver

%description	matrixview
This is a collection of OpenGL screensavers for xscreensaver. They
require a hardware-accellerated GLX implementation.

This contains the matrixview screensaver. It is in Restricted repository
as it includes images that are similar to those from the Matrix movies.

%prep
%setup -q -n %{fname}
%patch0 -p1
%patch1 -p1 -b .desktopentry

%build
%configure2_5x \
 --with-configdir=%{_datadir}/xscreensaver/config \
 --bindir=%{_libexecdir}/xscreensaver \
 --with-kdessconfigdir=%{_datadir}/applnk/System/ScreenSavers/
%make CXXFLAGS="%{optflags}" CPPFLAGS="-I%{_includedir}/ImageMagick"

%install
%makeinstall_std

# we don't need the static libs
rm -rf %{buildroot}%{_libdir}/lib*a
%if ! %{build_plf}
rm -f %{buildroot}%{_libexecdir}/xscreensaver/matrixview
rm -f %{buildroot}%{_mandir}/man1/matrixview.1
rm -f %{buildroot}%{_datadir}/xscreensaver/config/matrixview.xml
rm -f %{buildroot}%{_datadir}/applnk/System/ScreenSavers/matrixview.desktop
%endif

for screensaver in %{buildroot}%{_libdir}/xscreensaver/*;
 do fgrep -q ELF $screensaver && chrpath -d $screensaver
done

%files
%doc README*
%{_libexecdir}/xscreensaver/*
%{_mandir}/man1/*
%{_datadir}/xscreensaver/config/*
%{_datadir}/applnk/System/ScreenSavers/*

%if %{build_plf}
%exclude %{_libexecdir}/xscreensaver/matrixview
%exclude %{_mandir}/man1/matrixview.1*
%exclude %{_datadir}/xscreensaver/config/matrixview.xml
%exclude %{_datadir}/applnk/System/ScreenSavers/matrixview.desktop
%endif

%if %{build_plf}
%files matrixview
%doc README*
%{_libexecdir}/xscreensaver/matrixview
%{_mandir}/man1/matrixview.1*
%{_datadir}/xscreensaver/config/matrixview.xml
%{_datadir}/applnk/System/ScreenSavers/matrixview.desktop
%endif

