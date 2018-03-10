%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	The mate desktop programs for the MATE GUI desktop environment
Name:		mate-session-manager
Version:	1.18.2
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		https://mate-desktop.org
Source0:	https://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	startmate
Source2:	materc
Source3:	mate-lightdm.conf
Patch0:		https://patch-diff.githubusercontent.com/raw/mate-desktop/mate-session-manager/pull/138.patch

BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(pangox)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xtrans)
BuildRequires:	xmlto

Requires:	desktop-common-data
Requires:	mate-polkit >= %{url_ver}
Requires:	mate-settings-daemon >= %{url_ver}
Requires:	%{name}-bin >= %{EVRD}

%description
The MATE Desktop Environment is the continuation of GNOME 2. It provides an
intuitive and attractive desktop environment using traditional metaphors for
Linux and other Unix-like operating systems.

MATE is under active development to add support for new technologies while
preserving a traditional desktop experience.

The MATE Session Manager restores a set session (group of applications)
when you log into MATE.

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/lightdm/lightdm.conf.d/50-mate.conf
%{_bindir}/mate-session-properties
%{_bindir}/mate-session-save
%{_bindir}/mate-session-inhibit
%{_bindir}/mate-wm
%{_datadir}/applications/*
%dir %{_datadir}/mate-session-manager
%{_datadir}/mate-session-manager/gsm-inhibit-dialog.ui
%{_datadir}/mate-session-manager/session-properties.ui
%{_datadir}/xsessions/mate.desktop
%{_mandir}/man1/mate-session-inhibit.1*
%{_mandir}/man1/mate-session-properties.*
%{_mandir}/man1/mate-session-save.1*
%{_mandir}/man1/mate-wm.1*

#---------------------------------------------------------------------------

%package bin
Group: %{group}
Summary: %{summary}

%description bin
The MATE Desktop Environment is the continuation of GNOME 2. It provides an
intuitive and attractive desktop environment using traditional metaphors for
Linux and other Unix-like operating systems.

MATE is under active development to add support for new technologies while
preserving a traditional desktop experience.

This package contains the binaries for the MATE Session Manager, but 
no startup scripts. It is meant for applications such as GDM that use 
mate-session internally.

%files bin
%{_sysconfdir}/materc
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_bindir}/mate-session
%{_bindir}/startmate
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/mate-session.*

#---------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
#NOCONFIGURE=1 ./autogen.sh
%configure \
	--with-systemd \
	--disable-schemas-compile \
	%{nil}
%make

%install
%makeinstall_std

# install custom script
install -Dm 0755 %{SOURCE1} %{buildroot}%{_bindir}/startmate
install -Dm 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/materc

# Use custom startmate instead of default mate-session
sed -i -e "s|^Exec=mate-session|Exec=startmate|" %{buildroot}%{_datadir}/xsessions/mate.desktop

# Pre-select MATE session in lightdm greeter when booting first time after install
install -Dm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-mate.conf

# locales
%find_lang %{name} --with-gnome --all-name

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
	sed -i -e "s|^DESKTOP=Mate$|DESKTOP=MATE|g" /etc/sysconfig/desktop
fi

