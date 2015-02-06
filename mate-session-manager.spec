%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	The mate desktop programs for the MATE GUI desktop environment
Name:		mate-session-manager
Version:	1.8.1
Release:	3
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	startmate
Source2:	materc
Source3:	mate-lightdm.conf
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(pangox)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(xtrans)
Requires:	desktop-common-data
Requires:	mate-polkit
Requires:	mate-settings-daemon
Requires:	%{name}-bin >= %{EVRD}

%description
MATE (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.

The MATE Session Manager restores a set session (group of applications)
when you log into MATE.

%package bin
Group: %{group}
Summary: %{summary}

%description bin
This package contains the binaries for the MATE Session Manager, but 
no startup scripts. It is meant for applications such as GDM that use 
mate-session internally.

%prep
%setup -q
%apply_patches
NOCONFIGURE=yes ./autogen.sh

%build
%configure \
	--with-systemd

%make

%install
%makeinstall_std

# remove unneeded converter
rm -fr %{buildroot}%{_datadir}/MateConf
rm -f %{buildroot}%{_datadir}/doc/mate-session/dbus/mate-session.html

# wmsession session file
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/05MATE
NAME=MATE
ICON=mate
DESC=MATE Environment
EXEC=%{_bindir}/startmate
SCRIPT:
exec %{_bindir}/startmate
EOF

install -D -m 755 %{SOURCE1} %{buildroot}%{_bindir}/startmate
install -D -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/materc

# remove xsession file, it causes duplicate entries in GDM
rm -rf %{buildroot}%{_datadir}/xsessions/mate.desktop

# Pre-select MATE session in lightdm greeter when booting first time after install
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/50-mate.conf

%find_lang %{name}

%post
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
	sed -i -e "s|^DESKTOP=Mate$|DESKTOP=MATE|g" /etc/sysconfig/desktop
fi

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%config %{_sysconfdir}/X11/wmsession.d/*
%config(noreplace) %{_sysconfdir}/lightdm/lightdm.conf.d/50-mate.conf
%{_bindir}/mate-session-properties
%{_bindir}/mate-session-save
%{_bindir}/mate-wm
%{_datadir}/applications/*
%{_datadir}/mate-session-manager/gsm-inhibit-dialog.ui
%{_datadir}/mate-session-manager/session-properties.ui
#{_datadir}/xsessions/mate.desktop
%{_mandir}/man1/mate-session-properties.*
%{_mandir}/man1/mate-session-save.1.xz
%{_mandir}/man1/mate-wm.1.xz

%files bin
%{_sysconfdir}/materc
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_bindir}/mate-session
%{_bindir}/startmate
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/mate-session.*

