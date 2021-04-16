#global _rc 2
#global _beta 3

%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}

%global           _smp_mflags     -j1

%global           optflags        %{optflags} -Werror-implicit-function-declaration -DLUA_COMPAT_MODULE
%ifarch s390 %{arm} aarch64
%global           ldflags         -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%else
%global           ldflags         -m%{__isa_bits} -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags} -fPIC
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global           astvarrundir     /run/asterisk
%global           tmpfilesd        1
%else
%global           astvarrundir     %{_localstatedir}/run/asterisk
%global           tmpfilesd        0
%endif

%if 0%{?rhel} <= 6
%global           optflags        %{optflags} -std=c1x
%endif

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global           systemd    1
%else
%global           systemd    0
%endif

%global           apidoc     0
%global           mysql      1
%global           odbc       1
%global           postgresql 1
%global           radius     1
%global           snmp       1
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
%global           misdn      0
%else
%global           misdn      1
%endif
%global           ldap       1
%if 0%{?rhel} >= 8
%global           gmime      0
%global           radius     0
%else
%global           gmime      1
%global           radius     1
%endif
%global           corosync   1
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
%global           jack       0
%else
%global           jack       1
%endif

%global           makeargs        DEBUG= OPTIMIZE= DESTDIR=%{buildroot} ASTVARRUNDIR=%{astvarrundir} ASTDATADIR=%{_datadir}/asterisk ASTVARLIBDIR=%{_datadir}/asterisk ASTDBDIR=%{_localstatedir}/spool/asterisk NOISY_BUILD=1

Summary:          The Open Source PBX
Name:             asterisk
Version:          18.3.0
Release:          1%{?_rc:.rc%{_rc}}%{?_beta:.beta%{_beta}}%{?dist}
License:          GPLv2
Group:            Applications/Internet
URL:              http://www.asterisk.org/

Source0:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}.tar.gz
Source1:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}.tar.gz.asc
Source2:          asterisk18-logrotate
Source3:          asterisk18-menuselect.makedeps
Source4:          asterisk18-menuselect.makeopts
Source5:          asterisk18.service
Source6:          asterisk18-tmpfiles
Source7:          asterisk-addons-mp3-rev202.tar.gz
Source8:          pjproject-2.10.tar.bz2
Source9:          pjproject-2.10.md5
Source10:         jansson-2.12.tar.bz2
Source11:         codec_opus-18.0_1.3.0-x86_64.tar.gz
Source12:         codec_silk-18.0_1.0.3-x86_64.tar.gz
Source13:         codec_siren14-18.0_1.0.7-x86_64.tar.gz
Source14:         codec_siren7-18.0_1.0.7-x86_64.tar.gz


%if 0%{?fedora} > 0
Patch0:           gcc5.rc2.patch
%endif
Patch1:           asterisk18-init-path.patch
Patch2:           asterisk-addons-mp3.patch
%if 0%{?rhel} >= 8
Patch3:           asterisk18-python-to-python2.patch
%endif

BuildRoot:        %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires:    autoconf
BuildRequires:    automake

# core build requirements
BuildRequires:    openssl-devel
BuildRequires:    newt-devel
%if 0%{?fedora} <= 8
BuildRequires:    libtermcap-devel
%endif
BuildRequires:    ncurses-devel
BuildRequires:    libcap-devel
%if 0%{?gmime}
BuildRequires:    gtk2-devel
%endif
BuildRequires:    libsrtp-devel
BuildRequires:    popt-devel
%if %{systemd}
BuildRequires:    systemd-units
%endif

# for res_http_post
%if (0%{?fedora} > 0 || 0%{?rhel} >= 7) && 0%{?gmime}
BuildRequires:    gmime-devel
%endif

# for building docs
BuildRequires:    doxygen
BuildRequires:    graphviz
BuildRequires:    libxml2-devel
BuildRequires:    latex2html

# for building res_calendar_caldav
BuildRequires:    neon-devel
BuildRequires:    libical-devel
BuildRequires:    libxml2-devel

# for codec_speex
BuildRequires:    speex-devel >= 1.2
%if (0%{?fedora} > 0 || 0%{?rhel} >= 8)
BuildRequires:    speexdsp-devel >= 1.2
%endif

# for format_ogg_vorbis
BuildRequires:    libogg-devel
BuildRequires:    libvorbis-devel

# codec_gsm
BuildRequires:    gsm-devel

# additional dependencies
BuildRequires:    SDL-devel
#BuildRequires:    SDL_image-devel

# cli
BuildRequires:    libedit-devel

# codec_ilbc
BuildRequires:    ilbc-devel

# res_rtp_asterisk
BuildRequires:    libuuid-devel

%if 0%{?corosync}
BuildRequires:    corosynclib-devel
%endif

BuildRequires:    alsa-lib-devel
BuildRequires:    libcurl-devel
%if 0%{?fedora} > 0
BuildRequires:    dahdi-tools-devel >= 2.0.0
BuildRequires:    dahdi-tools-libs >= 2.0.0
%else
BuildRequires:    dahdi-linux-devel >= 2.0.0
BuildRequires:    libtonezone-devel
%endif

BuildRequires:    libpri-devel >= 1.4.12
BuildRequires:    libss7-devel >= 1.0.1
BuildRequires:    spandsp-devel >= 0.0.5-0.1.pre4
BuildRequires:    libtiff-devel
BuildRequires:    libjpeg-devel
BuildRequires:    lua-devel
%if 0%{?jack}
BuildRequires:    jack-audio-connection-kit-devel
%endif
BuildRequires:    libresample-devel
BuildRequires:    bluez-libs-devel
BuildRequires:    libtool-ltdl-devel
BuildRequires:    portaudio-devel >= 19
BuildRequires:    sqlite-devel
BuildRequires:    freetds-devel

%if 0%{?misdn}
BuildRequires:    mISDN-devel
%endif

%if 0%{?ldap}
BuildRequires:    openldap-devel
%endif

%if 0%{?mysql}
BuildRequires:    mysql-devel
%endif

%if 0%{?odbc}
BuildRequires:    libtool-ltdl-devel
BuildRequires:    unixODBC-devel
%endif

%if 0%{?postgresql}
BuildRequires:    postgresql-devel
%endif

%if 0%{?radius}
BuildRequires:    radiusclient-ng-devel
%endif

%if 0%{?snmp}
BuildRequires:    net-snmp-devel
BuildRequires:    lm_sensors-devel
%endif

%if 0%{?fedora} > 0 || 0%{?rhel} >= 7
BuildRequires:    uw-imap-devel
BuildRequires:    openssl-devel
%endif

#BuildRequires:    pjproject-devel
#BuildRequires:    jansson-devel
BuildRequires:    codec2-devel
BuildRequires:    fftw-devel

#BuildRequires:    xmlstarlet

%if 0%{?rhel} < 8
BuildRequires:    iksemel-devel
%endif

Requires(pre):    %{_sbindir}/useradd
Requires(pre):    %{_sbindir}/groupadd

%if 0%{?systemd}
Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units
%else
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Requires(preun):  /sbin/service
%endif

# asterisk-conference package removed since patch no longer compiles
Obsoletes:        asterisk-conference <= 1.6.0-0.14.beta9
Obsoletes:        asterisk-mobile <= 1.6.1-0.23.rc1
Obsoletes:        asterisk-firmware <= 1.6.2.0-0.2.rc1

# chan_usbradio was been removed in 10.4.0
Obsoletes:        asterisk-usbradio <= 10.3.1-1

# If upgrading from digium releases we need to handle the package format changes
Obsoletes:      asterisk-core <= %{version}-%{release}
Conflicts:      asterisk-core <= %{version}-%{release}
Provides:       asterisk-core = %{version}-%{release}
Obsoletes:      asterisk-configs <= %{version}-%{release}
Conflicts:      asterisk-configs <= %{version}-%{release}
Provides:       asterisk-configs = %{version}-%{release}
Obsoletes:      asterisk-doc <= %{version}-%{release}
Conflicts:      asterisk-doc <= %{version}-%{release}
Provides:       asterisk-doc = %{version}-%{release}

%description
Asterisk is a complete PBX in software. It runs on Linux and provides
all of the features you would expect from a PBX and more. Asterisk
does voice over IP in three protocols, and can interoperate with
almost all standards-based telephony equipment using relatively
inexpensive hardware.

%package ael
Summary: AEL (Asterisk Extension Logic) modules for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description ael
AEL (Asterisk Extension Logic) mdoules for Asterisk

%package alsa
Summary: Modules for Asterisk that use Alsa sound drivers
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description alsa
Modules for Asterisk that use Alsa sound drivers.

%if 0%{?apidoc}
%package apidoc
Summary: API documentation for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description apidoc
API documentation for Asterisk.
%endif

%package calendar
Summary: Calendar applications for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description calendar
Calendar applications for Asterisk.

%package compat
Summary: Metapackage to help transition Asterisk users to the new package split
Obsoletes: asterisk < 13.0.0
Requires: asterisk = %{version}-%{release}
Requires: asterisk-ael = %{version}-%{release}
Requires: asterisk-iax2 = %{version}-%{release}
Requires: asterisk-mgcp = %{version}-%{release}
Requires: asterisk-phone = %{version}-%{release}
Requires: asterisk-sip = %{version}-%{release}

%description compat
This package only exists to help transition Asterisk users to the new
package split. It will be removed after one distribution release
cycle, please do not reference it or depend on it in any way.

%if 0%{?corosync}
%package corosync
Summary: Modules for Asterisk that use Corosync
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description corosync
Modules for Asterisk that use Corosync.
%endif

%package curl
Summary: Modules for Asterisk that use cURL
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description curl
Modules for Asterisk that use cURL.

%package dahdi
Summary: Modules for Asterisk that use DAHDI
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires: dahdi-tools >= 2.0.0
Requires(pre): %{_sbindir}/usermod
Obsoletes: asterisk-zaptel <= 1.6.0-0.22.beta9
Provides: asterisk-zaptel = %{version}-%{release}

%description dahdi
Modules for Asterisk that use DAHDI.

%package devel
Summary: Development files for Asterisk
Group: Development/Libraries
Requires: asterisk = %{version}-%{release}

%description devel
Development files for Asterisk.

%package fax
Summary: FAX applications for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description fax
FAX applications for Asterisk

%package festival
Summary: Festival application for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires: festival

%description festival
Application for the Asterisk PBX that uses Festival to convert text to speech.

%package iax2
Summary: IAX2 channel driver for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description iax2
IAX2 channel driver for Asterisk

%package hep
Summary: Modules for capturing SIP traffic using Homer (HEPv3)
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description hep
Modules for capturing SIP traffic using Homer (HEPv3)

%if 0%{?fedora} || 0%{?rhel} >= 7
%package ices
Summary: Stream audio from Asterisk to an IceCast server
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires: ices

%description ices
Stream audio from Asterisk to an IceCast server.
%endif

%if 0%{?jack}
%package jack
Summary: JACK resources for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description jack
JACK resources for Asterisk.
%endif

%package lua
Summary: Lua resources for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description lua
Lua resources for Asterisk.

%if 0%{?ldap}
%package ldap
Summary: LDAP resources for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description ldap
LDAP resources for Asterisk.
%endif

%if 0%{?misdn}
%package misdn
Summary: mISDN channel for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires(pre): %{_sbindir}/usermod

%description misdn
mISDN channel for Asterisk.
%endif

%package mgcp
Summary: MGCP channel driver for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description mgcp
MGCP channel driver for Asterisk

%package mobile
Summary: Mobile (BlueTooth) channel for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires(pre): %{_sbindir}/usermod
Obsoletes: asterisk-addons-bluetooth <= %{version}-%{release}
Provides: asterisk-addons-bluetooth = %{version}-%{release}
Conflicts: asterisk-addons-bluetooth <= %{version}-%{release}

%description mobile
Mobile (BlueTooth) channel for Asterisk.

%package mp3
Summary: MP3 format support for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description mp3
MP3 format support for Asterisk (format_mp3 addon)

%package minivm
Summary: MiniVM applicaton for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description minivm
MiniVM application for Asterisk.

%package mwi-external
Summary: Support for developing external voicemail applications
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Conflicts: asterisk-voicemail = %{version}-%{release}
Conflicts: asterisk-voicemail-implementation = %{version}-%{release}

%description mwi-external
Support for developing external voicemail applications

%if 0%{?mysql}
%package mysql
Summary: Applications for Asterisk that use MySQL
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Obsoletes: asterisk-addons-mysql <= %{version}-%{release}
Provides: asterisk-addons-mysql = %{version}-%{release}
Conflicts: asterisk-addons-mysql <= %{version}-%{release}

%description mysql
Applications for Asterisk that use MySQL.
%endif

%if 0%{?odbc}
%package odbc
Summary: Applications for Asterisk that use ODBC (except voicemail)
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description odbc
Applications for Asterisk that use ODBC (except voicemail)
%endif

%package ooh323
Summary: H.323 channel for Asterisk using the Objective Systems Open H.323 for C library
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Obsoletes: asterisk-addons-ooh323 <= %{version}-%{release}
Provides: asterisk-addons-ooh323 = %{version}-%{release}
Conflicts: asterisk-addons-ooh323 <= %{version}-%{release}

%description ooh323
H.323 channel for Asterisk using the Objective Systems Open H.323 for C library.

%package oss
Summary: Modules for Asterisk that use OSS sound drivers
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description oss
Modules for Asterisk that use OSS sound drivers.

%if 0%{?rhel} < 8
%package phone
Summary: Channel driver for Quicknet Technologies, Inc.'s Telephony cards
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description phone
Quicknet Technologies, Inc.'s Telephony cards including the Internet
PhoneJACK, Internet PhoneJACK Lite, Internet PhoneJACK PCI, Internet
LineJACK, Internet PhoneCARD and SmartCABLE.
%endif

%package pjsip
Summary: SIP channel based upon the PJSIP library
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description pjsip
SIP channel based upon the PJSIP library

%package portaudio
Summary: Modules for Asterisk that use the portaudio library
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description portaudio
Modules for Asterisk that use the portaudio library.

%if 0%{?postgresql}
%package postgresql
Summary: Applications for Asterisk that use PostgreSQL
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Obsoletes: asterisk-pgsql <= %{version}-%{release}
Provides: asterisk-pgsql = %{version}-%{release}
Conflicts: asterisk-pgsql <= %{version}-%{release}

%description postgresql
Applications for Asterisk that use PostgreSQL.
%endif

%if 0%{?radius}
%package radius
Summary: Applications for Asterisk that use RADIUS
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description radius
Applications for Asterisk that use RADIUS.
%endif

%package skinny
Summary: Modules for Asterisk that support the SCCP/Skinny protocol
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description skinny
Modules for Asterisk that support the SCCP/Skinny protocol.

%package sip
Summary: Legacy SIP channel driver for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description sip
Legacy SIP channel driver for Asterisk

%if 0%{?snmp}
%package snmp
Summary: Module that enables SNMP monitoring of Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
# This subpackage depends on perl-libs, this Requires tracks versioning.
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description snmp
Module that enables SNMP monitoring of Asterisk.
%endif

%package sqlite
Summary: Sqlite modules for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Obsoletes: asterisk-sqlite3 <= %{version}-%{release}
Provides: asterisk-sqlite3 = %{version}-%{release}
Conflicts: asterisk-sqlite3 <= %{version}-%{release}

%description sqlite
Sqlite modules for Asterisk.

%package tds
Summary: Modules for Asterisk that use FreeTDS
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description tds
Modules for Asterisk that use FreeTDS.

%package unistim
Summary: Unistim channel for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}

%description unistim
Unistim channel for Asterisk

%package voicemail
Summary: Common Voicemail Modules for Asterisk and local storage
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Provides: asterisk-voicemail-implementation = %{version}-%{release}
Requires: /usr/bin/sox
Requires: /usr/sbin/sendmail
Conflicts: asterisk-mwi-external <= %{version}-%{release}

%description voicemail
Voicemail implementation for Asterisk that stores voicemail on the
local filesystem.

%if 0%{?fedora} > 0 || 0%{?rhel} >= 7
%package voicemail-imap
Summary: Store voicemail on an IMAP server
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires: asterisk-voicemail = %{version}-%{release}
Provides: asterisk-voicemail-implementation = %{version}-%{release}
Obsoletes: asterisk-voicemail-imapstorage <= %{version}-%{release}
Provides: asterisk-voicemail-imapstorage = %{version}-%{release}
Conflicts: asterisk-voicemail-imapstorage <= %{version}-%{release}

%description voicemail-imap
Voicemail implementation for Asterisk that stores voicemail on an IMAP
server.
%endif

%package voicemail-odbc
Summary: Store voicemail in a database using ODBC
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Requires: asterisk-voicemail = %{version}-%{release}
Provides: asterisk-voicemail-implementation = %{version}-%{release}
Obsoletes: asterisk-voicemail-odbcstorage <= %{version}-%{release}
Provides: asterisk-voicemail-odbcstorage = %{version}-%{release}
Conflicts: asterisk-voicemail-odbcstorage <= %{version}-%{release}

%description voicemail-odbc
Voicemail implementation for Asterisk that uses ODBC to store
voicemail in a database.

%if 0%{?rhel} < 8
%package xmpp
Summary: Jabber/XMPP resources for Asterisk
Group: Applications/Internet
Requires: asterisk = %{version}-%{release}
Obsoletes: asterisk-jabber < 13.0.0
Conflicts: asterisk-jabber < 13.0.0

%description xmpp
Jabber/XMPP resources for Asterisk.
%endif

%prep
%setup -q -n asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}
%setup -q -n asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}} -T -D -a 7
%if 0%{?fedora} > 0
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p0
%if 0%{?rhel} >= 8
%patch3 -p1
%endif


cp %{S:3} menuselect.makedeps
cp %{S:4} menuselect.makeopts

# Fixup makefile so sound archives aren't downloaded/installed
%{__perl} -pi -e 's/^all:.*$/all:/' sounds/Makefile
%{__perl} -pi -e 's/^install:.*$/install:/' sounds/Makefile

# convert comments in one file to UTF-8
mv main/fskmodem.c main/fskmodem.c.old
iconv -f iso-8859-1 -t utf-8 -o main/fskmodem.c main/fskmodem.c.old
touch -r main/fskmodem.c.old main/fskmodem.c
rm main/fskmodem.c.old

chmod -x contrib/scripts/dbsep.cgi

%if 0%{?rhel} == 8
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_motif/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_phone/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_xmpp/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_calendar_exchange/g' menuselect.makeopts
%endif

%if 0%{?rhel} == 6
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_http_post/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_voicemail_imap/g' menuselect.makeopts
%endif

%if 0%{?rhel} == 5
# Get the autoconf scripts working with 2.59
%{__perl} -pi -e 's/AC_PREREQ\(2\.60\)/AC_PREREQ\(2\.59\)/g' configure.ac
%{__perl} -pi -e 's/AC_USE_SYSTEM_EXTENSIONS/AC_GNU_SOURCE/g' configure.ac
%{__perl} -pi -e 's/AST_PROG_SED/SED=sed/g' autoconf/ast_prog_ld.m4
# kernel/glibc in RHEL5 does not support the timerfd
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_timing_timerfd/g' menuselect.makeopts
%endif

%if ! 0%{?corosync}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_corosync/g' menuselect.makeopts
%endif

%if ! 0%{?mysql}
%{__perl} -pi -e 's/^MENUSELECT_ADDONS=(.*)$/MENUSELECT_ADDONS=\1 res_config_mysql app_mysql cdr_mysql/g' menuselect.makeopts
%endif

%if ! 0%{?postgresql}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_config_pgsql/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CDR=(.*)$/MENUSELECT_CDR=\1 cdr_pgsql/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CEL=(.*)$/MENUSELECT_CEL=\1 cel_pgsql/g' menuselect.makeopts
%endif

%if ! 0%{?radius}
%{__perl} -pi -e 's/^MENUSELECT_CDR=(.*)$/MENUSELECT_CDR=\1 cdr_radius/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CEL=(.*)$/MENUSELECT_CEL=\1 cel_radius/g' menuselect.makeopts
%endif

%if ! 0%{?snmp}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_snmp/g' menuselect.makeopts
%endif

%if ! 0%{?misdn}
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_misdn/g' menuselect.makeopts
%endif

%if ! 0%{?jack}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_jack/g' menuselect.makeopts
%endif

%if ! 0%{?ldap}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_config_ldap/g' menuselect.makeopts
%endif

%if ! 0%{?gmime}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_http_post/g' menuselect.makeopts
%endif

%build

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS=" "
export JANSSON_CONFIGURE_OPTS="--with-pic"

./bootstrap.sh

pushd menuselect

%configure

popd

mkdir %{_tmppath}/dlcache
cp %{SOURCE8} %{_tmppath}/dlcache/
cp %{SOURCE9} %{_tmppath}/dlcache/
cp %{SOURCE10} %{_tmppath}/dlcache/

%if 0%{?fedora} > 0 || 0%{?rhel} >= 7
%configure --with-imap=system --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-srtp --with-jansson-bundled --with-download-cache=%{_tmppath}/dlcache LDFLAGS="%{ldflags}"
%else
%configure  --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-gmime=no --with-srtp --with-jansson-bundled --with-download-cache=%{_tmppath}/dlcache LDFLAGS="%{ldflags}"
%endif

make %{?_smp_mflags} menuselect-tree NOISY_BUILD=1
%{__perl} -n -i -e 'print unless /openr2/i' menuselect-tree

make %{?_smp_mflags} %{makeargs}

#rm apps/app_voicemail.o apps/app_directory.o
#mv apps/app_voicemail.so apps/app_voicemail_plain.so
#mv apps/app_directory.so apps/app_directory_plain.so

#%if 0%{?fedora} > 0 || 0%{?rhel} >= 7
#sed -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=IMAP_STORAGE/' menuselect.makeopts
#make %{?_smp_mflags} %{makeargs}
#
#rm apps/app_voicemail.o apps/app_directory.o
#mv apps/app_voicemail.so apps/app_voicemail_imap.so
#mv apps/app_directory.so apps/app_directory_imap.so
#%endif
#
#sed -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=ODBC_STORAGE/' menuselect.makeopts
#make %{?_smp_mflags} %{makeargs}
#
#rm apps/app_voicemail.o apps/app_directory.o
#mv apps/app_voicemail.so apps/app_voicemail_odbc.so
#mv apps/app_directory.so apps/app_directory_odbc.so
#
## so that these modules don't get built again
#touch apps/app_voicemail.o apps/app_directory.o
#touch apps/app_voicemail.so apps/app_directory.so

sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_mwi_external\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_mwi_external_ami\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_stasis_mailbox\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_APP=\(.*\)$/MENUSELECT_RES=\1 app_voicemail/g' menuselect.makeopts

make %{?_smp_mflags} %{makeargs}

%if 0%{?apidoc}
make %{?_smp_mflags} progdocs %{makeargs}

# fix dates so that we don't get multilib conflicts
find doc/api/html -type f -print0 | xargs --null touch -r ChangeLog
%endif

%install
rm -rf %{buildroot}

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS="%{optflags}"

make install %{makeargs}
make samples %{makeargs}
make install-headers %{makeargs}

%if 0%{?systemd}
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/asterisk.service
rm -f %{buildroot}%{_sbindir}/safe_asterisk
%else
mkdir -p %{buildroot}%{_initrddir}
build_tools/install_subst contrib/init.d/rc.redhat.asterisk %{buildroot}%{_initrddir}/asterisk
%endif
install -D -p -m 0644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/asterisk

#rm %{buildroot}%{_libdir}/asterisk/modules/app_directory.so
#rm %{buildroot}%{_libdir}/asterisk/modules/app_voicemail.so

%if 0%{?fedora} > 0 || 0%{?rhel} >= 7
#install -D -p -m 0755 apps/app_directory_imap.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_imap.so
install -D -p -m 0755 apps/app_voicemail_imap.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_imap.so
%endif
#install -D -p -m 0755 apps/app_directory_odbc.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_odbc.so
install -D -p -m 0755 apps/app_voicemail_odbc.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_odbc.so
install -D -p -m 0755 apps/app_directory.so %{buildroot}%{_libdir}/asterisk/modules/app_directory.so
install -D -p -m 0755 apps/app_voicemail.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail.so

# create some directories that need to be packaged
mkdir -p %{buildroot}%{_datadir}/asterisk/moh
mkdir -p %{buildroot}%{_datadir}/asterisk/sounds
mkdir -p %{buildroot}%{_localstatedir}/lib/asterisk
mkdir -p %{buildroot}%{_localstatedir}/log/asterisk/cdr-custom
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/festival
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/monitor
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/outgoing
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/uploads

# We're not going to package any of the sample AGI scripts
rm -f %{buildroot}%{_datadir}/asterisk/agi-bin/*

# Don't package the sample voicemail user
rm -rf %{buildroot}%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
rm -rf %{buildroot}%{_datadir}/asterisk/phoneprov/*

# these are compiled with -O0 and thus include unfortified code.
rm -rf %{buildroot}%{_sbindir}/hashtest
rm -rf %{buildroot}%{_sbindir}/hashtest2

# Don't include refcounter
rm -rf %{buildroot}%{_datadir}/asterisk/scripts/refcounter.*

#
rm -rf %{buildroot}%{_sysconfdir}/asterisk/app_skel.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/config_test.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/test_sorcery.conf

%if 0%{?rhel} == 8
# With iksemel gone and the xmpp package unavailable, we can't use the configs
rm -rf %{buildroot}%{_sysconfdir}/asterisk/motif.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/xmpp.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/phone.conf
%endif

%if 0%{?apidoc}
find doc/api/html -name \*.map -size 0 -delete
%endif

#rhel6 doesnt have 389 available, nor ices
%if 0%{?rhel} == 6
rm -rf %{buildroot}%{_sysconfdir}/dirsrv/schema/99asterisk.ldif
rm -rf %{buildroot}%{_libdir}/asterisk/modules/app_ices.so
%endif

%if %{tmpfilesd}
install -D -p -m 0644 %{SOURCE6} %{buildroot}/usr/lib/tmpfiles.d/asterisk.conf
mkdir -p %{buildroot}%{astvarrundir}
%endif

%if ! 0%{?mysql}
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_mysql.conf
%endif

%if ! 0%{?postgresql}
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_pgsql.conf
%endif

%if ! 0%{?misdn}
rm -f %{buildroot}%{_sysconfdir}/asterisk/misdn.conf
%endif

%if ! 0%{?snmp}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_snmp.conf
%endif

%if ! 0%{?ldap}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_ldap.conf
%endif

rm -f %{buildroot}%{_sysconfdir}/asterisk/cdr_beanstalkd.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/cel_beanstalkd.conf

# Manual codec opus
mkdir %{_tmppath}/extcodecstmp
tar xzf %{SOURCE11} --strip-components=1 -C %{_tmppath}/extcodecstmp
install -D -p -m 0755 %{_tmppath}/extcodecstmp/codec_opus.so %{buildroot}%{_libdir}/asterisk/modules/codec_opus.so
install -D -p -m 0755 %{_tmppath}/extcodecstmp/format_ogg_opus.so %{buildroot}%{_libdir}/asterisk/modules/format_ogg_opus.so
install -D -p -m 0755 %{_tmppath}/extcodecstmp/codec_opus_config-en_US.xml %{buildroot}%{_datadir}/asterisk/documentation/thirdparty/codec_opus_config-en_US.xml
cp %{_tmppath}/extcodecstmp/LICENSE ./codec_opus-LICENSE.txt
cp %{_tmppath}/extcodecstmp/README ./codec_opus-README.txt
rm -rf %{_tmppath}/extcodecstmp

# Manual codec silk
mkdir %{_tmppath}/extcodecstmp
tar xzf %{SOURCE12} --strip-components=1 -C %{_tmppath}/extcodecstmp
install -D -p -m 0755 %{_tmppath}/extcodecstmp/codec_silk.so %{buildroot}%{_libdir}/asterisk/modules/codec_silk.so
cp %{_tmppath}/extcodecstmp/LICENSE ./codec_silk-LICENSE.txt
rm -rf %{_tmppath}/extcodecstmp

# Manual codec siren14
mkdir %{_tmppath}/extcodecstmp
tar xzf %{SOURCE13} --strip-components=1 -C %{_tmppath}/extcodecstmp
install -D -p -m 0755 %{_tmppath}/extcodecstmp/codec_siren14.so %{buildroot}%{_libdir}/asterisk/modules/codec_siren14.so
cp %{_tmppath}/extcodecstmp/LICENSE ./codec_siren14-LICENSE.txt
rm -rf %{_tmppath}/extcodecstmp

# Manual codec siren7
mkdir %{_tmppath}/extcodecstmp
tar xzf %{SOURCE14} --strip-components=1 -C %{_tmppath}/extcodecstmp
install -D -p -m 0755 %{_tmppath}/extcodecstmp/codec_siren7.so %{buildroot}%{_libdir}/asterisk/modules/codec_siren7.so
cp %{_tmppath}/extcodecstmp/LICENSE ./codec_siren7-LICENSE.txt
rm -rf %{_tmppath}/extcodecstmp

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/groupadd -r asterisk &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d /var/lib/asterisk -M \
                               -c 'Asterisk User' -g asterisk asterisk &>/dev/null || :

%post
%if %{systemd}
if [ $1 -eq 1 ] ; then
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add asterisk
%endif

%preun
%if %{systemd}
if [ "$1" -eq "0" ]; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable asterisk.service > /dev/null 2>&1 || :
	/bin/systemctl stop asterisk.service > /dev/null 2>&1 || :
fi
%else
if [ "$1" -eq "0" ]; then
	# Package removal, not upgrade
        /sbin/service asterisk stop > /dev/null 2>&1 || :
        /sbin/chkconfig --del asterisk
fi
%endif

%if %{systemd}
%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart asterisk.service >/dev/null 2>&1 || :
fi

%triggerun -- asterisk < 1.8.2.4-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply asterisk
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save asterisk >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del asterisk >/dev/null 2>&1 || :
/bin/systemctl try-restart asterisk.service >/dev/null 2>&1 || :
%endif

%pre dahdi
%{_sbindir}/usermod -a -G dahdi asterisk

%if 0%{?misdn}
%pre misdn
%{_sbindir}/usermod -a -G misdn asterisk
%endif

%files
%defattr(-,root,root,-)
%doc README* *.txt ChangeLog BUGS CREDITS configs

%doc doc/asterisk.sgml

%if %{systemd}
%{_unitdir}/asterisk.service
%else
%{_initrddir}/asterisk
%endif

%{_libdir}/libasteriskssl.so.1
%{_libdir}/libasteriskssl.so
%{_libdir}/libasteriskpj.so.2
%{_libdir}/libasteriskpj.so

%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules

%{_libdir}/asterisk/modules/app_agent_pool.so
%{_libdir}/asterisk/modules/app_adsiprog.so
%{_libdir}/asterisk/modules/app_alarmreceiver.so
%{_libdir}/asterisk/modules/app_amd.so
%{_libdir}/asterisk/modules/app_attended_transfer.so
%{_libdir}/asterisk/modules/app_audiosocket.so
%{_libdir}/asterisk/modules/app_authenticate.so
%{_libdir}/asterisk/modules/app_blind_transfer.so
%{_libdir}/asterisk/modules/app_bridgeaddchan.so
%{_libdir}/asterisk/modules/app_bridgewait.so
%{_libdir}/asterisk/modules/app_cdr.so
%{_libdir}/asterisk/modules/app_celgenuserevent.so
%{_libdir}/asterisk/modules/app_chanisavail.so
%{_libdir}/asterisk/modules/app_channelredirect.so
%{_libdir}/asterisk/modules/app_chanspy.so
%{_libdir}/asterisk/modules/app_confbridge.so
%{_libdir}/asterisk/modules/app_controlplayback.so
%{_libdir}/asterisk/modules/app_db.so
%{_libdir}/asterisk/modules/app_dial.so
%{_libdir}/asterisk/modules/app_dictate.so
%{_libdir}/asterisk/modules/app_directed_pickup.so
%{_libdir}/asterisk/modules/app_disa.so
%{_libdir}/asterisk/modules/app_dumpchan.so
%{_libdir}/asterisk/modules/app_echo.so
%{_libdir}/asterisk/modules/app_exec.so
%{_libdir}/asterisk/modules/app_externalivr.so
%{_libdir}/asterisk/modules/app_followme.so
%{_libdir}/asterisk/modules/app_forkcdr.so
%{_libdir}/asterisk/modules/app_getcpeid.so
%{_libdir}/asterisk/modules/app_image.so
%{_libdir}/asterisk/modules/app_macro.so
%{_libdir}/asterisk/modules/app_milliwatt.so
%{_libdir}/asterisk/modules/app_mixmonitor.so
%{_libdir}/asterisk/modules/app_morsecode.so
%{_libdir}/asterisk/modules/app_nbscat.so
%{_libdir}/asterisk/modules/app_originate.so
#%{_libdir}/asterisk/modules/app_parkandannounce.so
%{_libdir}/asterisk/modules/app_playback.so
%{_libdir}/asterisk/modules/app_playtones.so
%{_libdir}/asterisk/modules/app_privacy.so
%{_libdir}/asterisk/modules/app_queue.so
%{_libdir}/asterisk/modules/app_readexten.so
#%{_libdir}/asterisk/modules/app_readfile.so
%{_libdir}/asterisk/modules/app_read.so
%{_libdir}/asterisk/modules/app_record.so
%{_libdir}/asterisk/modules/app_saycounted.so
#%{_libdir}/asterisk/modules/app_saycountpl.so
%{_libdir}/asterisk/modules/app_sayunixtime.so
%{_libdir}/asterisk/modules/app_senddtmf.so
%{_libdir}/asterisk/modules/app_sendtext.so
#%{_libdir}/asterisk/modules/app_setcallerid.so
%{_libdir}/asterisk/modules/app_sms.so
%{_libdir}/asterisk/modules/app_softhangup.so
%{_libdir}/asterisk/modules/app_speech_utils.so
%{_libdir}/asterisk/modules/app_stack.so
%{_libdir}/asterisk/modules/app_stasis.so
%{_libdir}/asterisk/modules/app_statsd.so
%{_libdir}/asterisk/modules/app_stream_echo.so
%{_libdir}/asterisk/modules/app_system.so
%{_libdir}/asterisk/modules/app_talkdetect.so
%{_libdir}/asterisk/modules/app_test.so
%{_libdir}/asterisk/modules/app_transfer.so
%{_libdir}/asterisk/modules/app_url.so
%{_libdir}/asterisk/modules/app_userevent.so
%{_libdir}/asterisk/modules/app_verbose.so
%{_libdir}/asterisk/modules/app_waitforring.so
%{_libdir}/asterisk/modules/app_waitforsilence.so
%{_libdir}/asterisk/modules/app_waituntil.so
%{_libdir}/asterisk/modules/app_while.so
%{_libdir}/asterisk/modules/app_zapateller.so
%{_libdir}/asterisk/modules/bridge_builtin_features.so
%{_libdir}/asterisk/modules/bridge_builtin_interval_features.so
%{_libdir}/asterisk/modules/bridge_holding.so
%{_libdir}/asterisk/modules/bridge_native_rtp.so
%{_libdir}/asterisk/modules/bridge_simple.so
%{_libdir}/asterisk/modules/bridge_softmix.so
%{_libdir}/asterisk/modules/cdr_csv.so
%{_libdir}/asterisk/modules/cdr_custom.so
%{_libdir}/asterisk/modules/cdr_manager.so
%{_libdir}/asterisk/modules/cdr_syslog.so
%{_libdir}/asterisk/modules/cel_custom.so
%{_libdir}/asterisk/modules/cel_manager.so
%{_libdir}/asterisk/modules/chan_audiosocket.so
%{_libdir}/asterisk/modules/chan_bridge_media.so
#%{_libdir}/asterisk/modules/chan_multicast_rtp.so
%{_libdir}/asterisk/modules/chan_rtp.so
%{_libdir}/asterisk/modules/codec_adpcm.so
%{_libdir}/asterisk/modules/codec_alaw.so
%{_libdir}/asterisk/modules/codec_a_mu.so
%{_libdir}/asterisk/modules/codec_codec2.so
%{_libdir}/asterisk/modules/codec_g722.so
%{_libdir}/asterisk/modules/codec_g726.so
%{_libdir}/asterisk/modules/codec_gsm.so
%{_libdir}/asterisk/modules/codec_ilbc.so
%{_libdir}/asterisk/modules/codec_lpc10.so
%{_libdir}/asterisk/modules/codec_opus.so
%{_libdir}/asterisk/modules/codec_resample.so
%{_libdir}/asterisk/modules/codec_silk.so
%{_libdir}/asterisk/modules/codec_siren7.so
%{_libdir}/asterisk/modules/codec_siren14.so
%{_libdir}/asterisk/modules/codec_speex.so
%{_libdir}/asterisk/modules/codec_ulaw.so
%{_libdir}/asterisk/modules/format_g719.so
%{_libdir}/asterisk/modules/format_g723.so
%{_libdir}/asterisk/modules/format_g726.so
%{_libdir}/asterisk/modules/format_g729.so
%{_libdir}/asterisk/modules/format_gsm.so
%{_libdir}/asterisk/modules/format_h263.so
%{_libdir}/asterisk/modules/format_h264.so
%{_libdir}/asterisk/modules/format_ilbc.so
#%{_libdir}/asterisk/modules/format_jpeg.so
%{_libdir}/asterisk/modules/format_ogg_opus.so
%{_libdir}/asterisk/modules/format_ogg_speex.so
%{_libdir}/asterisk/modules/format_ogg_vorbis.so
%{_libdir}/asterisk/modules/format_pcm.so
%{_libdir}/asterisk/modules/format_siren14.so
%{_libdir}/asterisk/modules/format_siren7.so
%{_libdir}/asterisk/modules/format_sln.so
%{_libdir}/asterisk/modules/format_vox.so
%{_libdir}/asterisk/modules/format_wav_gsm.so
%{_libdir}/asterisk/modules/format_wav.so
%{_libdir}/asterisk/modules/func_aes.so
#%{_libdir}/asterisk/modules/func_audiohookinherit.so
%{_libdir}/asterisk/modules/func_base64.so
%{_libdir}/asterisk/modules/func_blacklist.so
%{_libdir}/asterisk/modules/func_callcompletion.so
%{_libdir}/asterisk/modules/func_callerid.so
%{_libdir}/asterisk/modules/func_cdr.so
%{_libdir}/asterisk/modules/func_channel.so
%{_libdir}/asterisk/modules/func_config.so
%{_libdir}/asterisk/modules/func_cut.so
%{_libdir}/asterisk/modules/func_db.so
%{_libdir}/asterisk/modules/func_devstate.so
%{_libdir}/asterisk/modules/func_dialgroup.so
%{_libdir}/asterisk/modules/func_dialplan.so
%{_libdir}/asterisk/modules/func_enum.so
%{_libdir}/asterisk/modules/func_env.so
%{_libdir}/asterisk/modules/func_extstate.so
%{_libdir}/asterisk/modules/func_frame_trace.so
%{_libdir}/asterisk/modules/func_global.so
%{_libdir}/asterisk/modules/func_groupcount.so
%{_libdir}/asterisk/modules/func_hangupcause.so
%{_libdir}/asterisk/modules/func_holdintercept.so
%{_libdir}/asterisk/modules/func_iconv.so
%{_libdir}/asterisk/modules/func_jitterbuffer.so
%{_libdir}/asterisk/modules/func_lock.so
%{_libdir}/asterisk/modules/func_logic.so
%{_libdir}/asterisk/modules/func_math.so
%{_libdir}/asterisk/modules/func_md5.so
%{_libdir}/asterisk/modules/func_module.so
%{_libdir}/asterisk/modules/func_periodic_hook.so
%{_libdir}/asterisk/modules/func_pitchshift.so
%{_libdir}/asterisk/modules/func_presencestate.so
%{_libdir}/asterisk/modules/func_rand.so
%{_libdir}/asterisk/modules/func_realtime.so
%{_libdir}/asterisk/modules/func_sha1.so
%{_libdir}/asterisk/modules/func_shell.so
%{_libdir}/asterisk/modules/func_sorcery.so
%{_libdir}/asterisk/modules/func_speex.so
%{_libdir}/asterisk/modules/func_sprintf.so
%{_libdir}/asterisk/modules/func_srv.so
%{_libdir}/asterisk/modules/func_strings.so
%{_libdir}/asterisk/modules/func_sysinfo.so
%{_libdir}/asterisk/modules/func_talkdetect.so
%{_libdir}/asterisk/modules/func_timeout.so
%{_libdir}/asterisk/modules/func_uri.so
%{_libdir}/asterisk/modules/func_version.so
%{_libdir}/asterisk/modules/func_volume.so
%{_libdir}/asterisk/modules/pbx_config.so
%{_libdir}/asterisk/modules/pbx_dundi.so
%{_libdir}/asterisk/modules/pbx_loopback.so
%{_libdir}/asterisk/modules/pbx_realtime.so
%{_libdir}/asterisk/modules/pbx_spool.so
%{_libdir}/asterisk/modules/res_adsi.so
%{_libdir}/asterisk/modules/res_agi.so
%{_libdir}/asterisk/modules/res_ari.so
%{_libdir}/asterisk/modules/res_ari_applications.so
%{_libdir}/asterisk/modules/res_ari_asterisk.so
%{_libdir}/asterisk/modules/res_ari_bridges.so
%{_libdir}/asterisk/modules/res_ari_channels.so
%{_libdir}/asterisk/modules/res_ari_device_states.so
%{_libdir}/asterisk/modules/res_ari_endpoints.so
%{_libdir}/asterisk/modules/res_ari_events.so
#%{_libdir}/asterisk/modules/res_ari_mailboxes.so
%{_libdir}/asterisk/modules/res_ari_model.so
%{_libdir}/asterisk/modules/res_ari_playbacks.so
%{_libdir}/asterisk/modules/res_ari_recordings.so
%{_libdir}/asterisk/modules/res_ari_sounds.so
%{_libdir}/asterisk/modules/res_audiosocket.so
%{_libdir}/asterisk/modules/res_chan_stats.so
%{_libdir}/asterisk/modules/res_clialiases.so
%{_libdir}/asterisk/modules/res_clioriginate.so
%{_libdir}/asterisk/modules/res_convert.so
%{_libdir}/asterisk/modules/res_crypto.so
%{_libdir}/asterisk/modules/res_endpoint_stats.so
%{_libdir}/asterisk/modules/res_format_attr_celt.so
%{_libdir}/asterisk/modules/res_format_attr_g729.so
%{_libdir}/asterisk/modules/res_format_attr_h263.so
%{_libdir}/asterisk/modules/res_format_attr_h264.so
%{_libdir}/asterisk/modules/res_format_attr_ilbc.so
%{_libdir}/asterisk/modules/res_format_attr_opus.so
%{_libdir}/asterisk/modules/res_format_attr_silk.so
%{_libdir}/asterisk/modules/res_format_attr_vp8.so
%{_libdir}/asterisk/modules/res_format_attr_siren14.so
%{_libdir}/asterisk/modules/res_format_attr_siren7.so
%if (0%{?fedora} > 0 || 0%{?rhel} >= 7) && 0%{?gmime}
%{_libdir}/asterisk/modules/res_http_post.so
%endif
%{_libdir}/asterisk/modules/res_http_media_cache.so
%{_libdir}/asterisk/modules/res_http_websocket.so
%{_libdir}/asterisk/modules/res_limit.so
%{_libdir}/asterisk/modules/res_manager_devicestate.so
%{_libdir}/asterisk/modules/res_manager_presencestate.so
%{_libdir}/asterisk/modules/res_monitor.so
%{_libdir}/asterisk/modules/res_musiconhold.so
%{_libdir}/asterisk/modules/res_mutestream.so
%{_libdir}/asterisk/modules/res_mwi_devstate.so
%{_libdir}/asterisk/modules/res_parking.so
%{_libdir}/asterisk/modules/res_phoneprov.so
%{_libdir}/asterisk/modules/res_realtime.so
# Now needed by res_rtp_asterisk otherwise there's a missing symbol
%{_libdir}/asterisk/modules/res_pjproject.so
%{_libdir}/asterisk/modules/res_prometheus.so
%{_libdir}/asterisk/modules/res_remb_modifier.so
%{_libdir}/asterisk/modules/res_rtp_asterisk.so
%{_libdir}/asterisk/modules/res_rtp_multicast.so
%{_libdir}/asterisk/modules/res_security_log.so
%{_libdir}/asterisk/modules/res_smdi.so
%{_libdir}/asterisk/modules/res_sorcery_astdb.so
%{_libdir}/asterisk/modules/res_sorcery_config.so
%{_libdir}/asterisk/modules/res_sorcery_memory.so
%{_libdir}/asterisk/modules/res_sorcery_memory_cache.so
%{_libdir}/asterisk/modules/res_sorcery_realtime.so
%{_libdir}/asterisk/modules/res_speech.so
%{_libdir}/asterisk/modules/res_srtp.so
%{_libdir}/asterisk/modules/res_stasis.so
%{_libdir}/asterisk/modules/res_stasis_answer.so
%{_libdir}/asterisk/modules/res_stasis_device_state.so
%{_libdir}/asterisk/modules/res_stasis_playback.so
%{_libdir}/asterisk/modules/res_stasis_recording.so
%{_libdir}/asterisk/modules/res_stasis_snoop.so
%{_libdir}/asterisk/modules/res_statsd.so
%{_libdir}/asterisk/modules/res_stun_monitor.so
%{_libdir}/asterisk/modules/res_timing_pthread.so
%if 0%{?fedora} > 0 || 0%{?rhel} >= 6
%{_libdir}/asterisk/modules/res_timing_timerfd.so
%endif

%{_sbindir}/astcanary
%{_sbindir}/astdb2sqlite3
%{_sbindir}/asterisk
%{_sbindir}/astgenkey
%{_sbindir}/astman
%{_sbindir}/astversion
%{_sbindir}/autosupport
%{_sbindir}/check_expr
%{_sbindir}/check_expr2
%{_sbindir}/muted
%{_sbindir}/rasterisk
#%{_sbindir}/refcounter
%if ! %{systemd}
%{_sbindir}/safe_asterisk
%endif
%{_sbindir}/smsq
%{_sbindir}/stereorize
%{_sbindir}/streamplayer

%{_mandir}/man8/astdb2bdb.8*
%{_mandir}/man8/astdb2sqlite3.8*
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*
%{_mandir}/man8/safe_asterisk.8*

%attr(0750,asterisk,asterisk) %dir %{_sysconfdir}/asterisk
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/acl.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/adsi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/agents.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/alarmreceiver.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/amd.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ari.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/asterisk.adsi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/asterisk.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ast_debug_tools.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ccss.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_manager.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_syslog.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cli.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cli_aliases.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cli_permissions.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/codecs.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/confbridge.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dnsmgr.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dsp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dundi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/enum.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extconfig.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/features.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/followme.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/http.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/indications.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/logger.conf
%attr(0600,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/manager.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/modules.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/musiconhold.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/muted.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/osp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/phoneprov.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/prometheus.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/queuerules.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/queues.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_parking.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_stun_monitor.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/resolver_unbound.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/rtp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/say.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sla.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/smdi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sorcery.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/stasis.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/statsd.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/telcordia-1.adsi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/udptl.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/users.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/vpb.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk

%dir %{_datadir}/asterisk
%dir %{_datadir}/asterisk/agi-bin
%{_datadir}/asterisk/documentation
%{_datadir}/asterisk/images
%attr(0750,asterisk,asterisk) %{_datadir}/asterisk/keys
%{_datadir}/asterisk/phoneprov
%{_datadir}/asterisk/static-http
%{_datadir}/asterisk/scripts
%{_datadir}/asterisk/rest-api
%dir %{_datadir}/asterisk/moh
%dir %{_datadir}/asterisk/sounds

%attr(0755,asterisk,asterisk) %dir %{_localstatedir}/lib/asterisk

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-csv
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-custom

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk
%attr(0770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/monitor
%attr(0770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/outgoing
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/tmp
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/uploads
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/voicemail

%if %{tmpfilesd}
%attr(0644,root,root) /usr/lib/tmpfiles.d/asterisk.conf
%endif
%attr(0755,asterisk,asterisk) %dir %{astvarrundir}

%files ael
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions.ael
%{_sbindir}/aelparse
%{_sbindir}/conf2ael
%{_libdir}/asterisk/modules/pbx_ael.so
%{_libdir}/asterisk/modules/res_ael_share.so

%files alsa
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/alsa.conf
%{_libdir}/asterisk/modules/chan_alsa.so

%if %{?apidoc}
%files apidoc
%defattr(-,root,root,-)
%doc doc/api/html/*
%endif

%files calendar
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/calendar.conf
%{_libdir}/asterisk/modules/res_calendar.so
%{_libdir}/asterisk/modules/res_calendar_caldav.so
%{_libdir}/asterisk/modules/res_calendar_ews.so
%if 0%{?rhel} < 8
%{_libdir}/asterisk/modules/res_calendar_exchange.so
%endif
%{_libdir}/asterisk/modules/res_calendar_icalendar.so

%if 0%{?corosync}
%files corosync
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_corosync.conf
%{_libdir}/asterisk/modules/res_corosync.so
%endif

%files curl
%defattr(-,root,root,-)
%doc contrib/scripts/dbsep.cgi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dbsep.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_curl.conf
%{_libdir}/asterisk/modules/func_curl.so
%{_libdir}/asterisk/modules/res_config_curl.so
%{_libdir}/asterisk/modules/res_curl.so

%files dahdi
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/meetme.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/chan_dahdi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ss7.timers
%{_libdir}/asterisk/modules/app_flash.so
%{_libdir}/asterisk/modules/app_meetme.so
%{_libdir}/asterisk/modules/app_page.so
%{_libdir}/asterisk/modules/app_dahdiras.so
%{_libdir}/asterisk/modules/chan_dahdi.so
%{_libdir}/asterisk/modules/codec_dahdi.so
%{_libdir}/asterisk/modules/res_timing_dahdi.so
%{_datadir}/dahdi/span_config.d/40-asterisk

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/asterisk
%dir %{_includedir}/asterisk/doxygen
%{_includedir}/asterisk.h
%{_includedir}/asterisk/*.h
%{_includedir}/asterisk/doxygen/*.h


%files fax
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_fax.conf
%{_libdir}/asterisk/modules/res_fax.so
%{_libdir}/asterisk/modules/res_fax_spandsp.so

%files festival
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/festival.conf
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/festival
%{_libdir}/asterisk/modules/app_festival.so

%files iax2
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/iax.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/iaxprov.conf
%dir %{_datadir}/asterisk/firmware
%dir %{_datadir}/asterisk/firmware/iax
%{_libdir}/asterisk/modules/chan_iax2.so

%files hep
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/hep.conf
%{_libdir}/asterisk/modules/res_hep.so
%{_libdir}/asterisk/modules/res_hep_rtcp.so
%{_libdir}/asterisk/modules/res_hep_pjsip.so

%if 0%{?fedora} || 0%{?rhel} >= 7
%files ices
%defattr(-,root,root,-)
%doc contrib/asterisk-ices.xml
%{_libdir}/asterisk/modules/app_ices.so
%endif

%if 0%{?jack}
%files jack
%defattr(-,root,root,-)
%{_libdir}/asterisk/modules/app_jack.so
%endif

%files lua
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions.lua
%{_libdir}/asterisk/modules/pbx_lua.so

%if 0%{?ldap}
%files ldap
%defattr(-,root,root,-)
#doc doc/ldap.txt
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_ldap.conf
%{_libdir}/asterisk/modules/res_config_ldap.so
%endif

%files minivm
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions_minivm.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/minivm.conf
%{_libdir}/asterisk/modules/app_minivm.so

%if %{misdn}
%files misdn
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/misdn.conf
%{_libdir}/asterisk/modules/chan_misdn.so
%endif

%files mgcp
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/mgcp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_pktccops.conf
%{_libdir}/asterisk/modules/chan_mgcp.so
%{_libdir}/asterisk/modules/res_pktccops.so

%files mobile
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/chan_mobile.conf
%{_libdir}/asterisk/modules/chan_mobile.so

%files mp3
%defattr(-,root,root,-)
%{_libdir}/asterisk/modules/format_mp3.so

%if %{mysql}
%files mysql
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/app_mysql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_mysql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_config_mysql.conf
%doc contrib/realtime/mysql/*.sql
%{_libdir}/asterisk/modules/app_mysql.so
%{_libdir}/asterisk/modules/cdr_mysql.so
%{_libdir}/asterisk/modules/res_config_mysql.so
%endif

%files mwi-external
%defattr(-,root,root,-)
%{_libdir}/asterisk/modules/res_mwi_external.so
%{_libdir}/asterisk/modules/res_mwi_external_ami.so
%{_libdir}/asterisk/modules/res_stasis_mailbox.so

%if %{odbc}
%files odbc
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_adaptive_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/func_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_odbc.conf
%{_libdir}/asterisk/modules/cdr_adaptive_odbc.so
%{_libdir}/asterisk/modules/cdr_odbc.so
%{_libdir}/asterisk/modules/cel_odbc.so
%{_libdir}/asterisk/modules/func_odbc.so
%{_libdir}/asterisk/modules/res_config_odbc.so
%{_libdir}/asterisk/modules/res_odbc.so
%{_libdir}/asterisk/modules/res_odbc_transaction.so
%endif

%files ooh323
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ooh323.conf
%{_libdir}/asterisk/modules/chan_ooh323.so

%files oss
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/oss.conf
%{_libdir}/asterisk/modules/chan_oss.so

%if 0%{?rhel} < 8
%files phone
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/phone.conf
%{_libdir}/asterisk/modules/chan_phone.so
%endif

%files pjsip
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjproject.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjsip.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjsip_notify.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjsip_wizard.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/stir_shaken.conf
%{_libdir}/asterisk/modules/chan_pjsip.so
%{_libdir}/asterisk/modules/func_pjsip_aor.so
%{_libdir}/asterisk/modules/func_pjsip_contact.so
%{_libdir}/asterisk/modules/func_pjsip_endpoint.so
%{_libdir}/asterisk/modules/res_pjsip.so
%{_libdir}/asterisk/modules/res_pjsip_acl.so
%{_libdir}/asterisk/modules/res_pjsip_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_caller_id.so
%{_libdir}/asterisk/modules/res_pjsip_config_wizard.so
%{_libdir}/asterisk/modules/res_pjsip_dialog_info_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_diversion.so
%{_libdir}/asterisk/modules/res_pjsip_dlg_options.so
%{_libdir}/asterisk/modules/res_pjsip_dtmf_info.so
%{_libdir}/asterisk/modules/res_pjsip_empty_info.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_anonymous.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_ip.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_user.so
%{_libdir}/asterisk/modules/res_pjsip_exten_state.so
%{_libdir}/asterisk/modules/res_pjsip_header_funcs.so
%{_libdir}/asterisk/modules/res_pjsip_history.so
#%{_libdir}/asterisk/modules/res_pjsip_keepalive.so
%{_libdir}/asterisk/modules/res_pjsip_logger.so
%{_libdir}/asterisk/modules/res_pjsip_messaging.so
#%{_libdir}/asterisk/modules/res_pjsip_multihomed.so
%{_libdir}/asterisk/modules/res_pjsip_mwi.so
%{_libdir}/asterisk/modules/res_pjsip_mwi_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_nat.so
%{_libdir}/asterisk/modules/res_pjsip_notify.so
%{_libdir}/asterisk/modules/res_pjsip_one_touch_record_info.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_publish.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_registration.so
%{_libdir}/asterisk/modules/res_pjsip_path.so
%{_libdir}/asterisk/modules/res_pjsip_phoneprov_provider.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_digium_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_eyebeam_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_publish_asterisk.so
%{_libdir}/asterisk/modules/res_pjsip_pubsub.so
%{_libdir}/asterisk/modules/res_pjsip_refer.so
%{_libdir}/asterisk/modules/res_pjsip_registrar.so
#%{_libdir}/asterisk/modules/res_pjsip_registrar_expire.so
%{_libdir}/asterisk/modules/res_pjsip_rfc3326.so
%{_libdir}/asterisk/modules/res_pjsip_sdp_rtp.so
%{_libdir}/asterisk/modules/res_pjsip_send_to_voicemail.so
%{_libdir}/asterisk/modules/res_pjsip_session.so
%{_libdir}/asterisk/modules/res_pjsip_sips_contact.so
%{_libdir}/asterisk/modules/res_pjsip_stir_shaken.so
%{_libdir}/asterisk/modules/res_pjsip_t38.so
#%{_libdir}/asterisk/modules/res_pjsip_transport_management.so
%{_libdir}/asterisk/modules/res_pjsip_transport_websocket.so
%{_libdir}/asterisk/modules/res_pjsip_xpidf_body_generator.so
#%{_libdir}/asterisk/modules/res_sdp_translator_pjmedia.so
%{_libdir}/asterisk/modules/res_stir_shaken.so

%files portaudio
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/console.conf
%{_libdir}/asterisk/modules/chan_console.so

%if %{postgresql}
%files postgresql
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_pgsql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_pgsql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_pgsql.conf
%doc contrib/realtime/postgresql/*.sql
%{_libdir}/asterisk/modules/cdr_pgsql.so
%{_libdir}/asterisk/modules/cel_pgsql.so
%{_libdir}/asterisk/modules/res_config_pgsql.so
%endif

%if %{radius}
%files radius
%defattr(-,root,root,-)
%{_libdir}/asterisk/modules/cdr_radius.so
%{_libdir}/asterisk/modules/cel_radius.so
%endif

%files sip
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sip.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sip_notify.conf
%{_libdir}/asterisk/modules/chan_sip.so

%files skinny
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/skinny.conf
%{_libdir}/asterisk/modules/chan_skinny.so

%if %{snmp}
%files snmp
%defattr(-,root,root,-)
#doc doc/asterisk-mib.txt
#doc doc/digium-mib.txt
#doc doc/snmp.txt
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_snmp.conf
#%{_datadir}/snmp/mibs/ASTERISK-MIB.txt
#%{_datadir}/snmp/mibs/DIGIUM-MIB.txt
%{_libdir}/asterisk/modules/res_snmp.so
%endif

%files sqlite
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_sqlite3_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_sqlite3_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_config_sqlite.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_config_sqlite3.conf
%{_libdir}/asterisk/modules/cdr_sqlite3_custom.so
%{_libdir}/asterisk/modules/cel_sqlite3_custom.so
%{_libdir}/asterisk/modules/res_config_sqlite3.so

%files tds
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_tds.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_tds.conf
%{_libdir}/asterisk/modules/cdr_tds.so
%{_libdir}/asterisk/modules/cel_tds.so

%files unistim
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/unistim.conf
%{_libdir}/asterisk/modules/chan_unistim.so

%files voicemail
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/voicemail.conf
%{_libdir}/asterisk/modules/func_vmcount.so
%{_libdir}/asterisk/modules/app_directory.so
%{_libdir}/asterisk/modules/app_voicemail.so

%if 0%{?fedora} > 0 || 0%{?rhel} >= 7
%files voicemail-imap
%defattr(-,root,root,)
#%{_libdir}/asterisk/modules/app_directory_imap.so
%{_libdir}/asterisk/modules/app_voicemail_imap.so
%endif

%files voicemail-odbc
%defattr(-,root,root,-)
#doc doc/voicemail_odbc_postgresql.txt
#%{_libdir}/asterisk/modules/app_directory_odbc.so
%{_libdir}/asterisk/modules/app_voicemail_odbc.so

%if 0%{?rhel} < 8
%files xmpp
%defattr(-,root,root,-)
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/motif.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/xmpp.conf
%{_libdir}/asterisk/modules/chan_motif.so
%{_libdir}/asterisk/modules/res_xmpp.so
%endif

%changelog
* Fri Mar 26 2021 D Tucny <d@tucny.com> - 18.3.0-1
- New version

* Thu Mar 11 2021 D Tucny <d@tucny.com> - 18.2.2-2
- Adding Opus, Silk and Siren to 16, 17 and 18 after already tested with 13

* Fri Mar 05 2021 D Tucny <d@tucny.com> - 18.2.2-1
- New version

* Fri Feb 19 2021 D Tucny <d@tucny.com> - 18.2.1-1
- New version

* Fri Jan 22 2021 D Tucny <d@tucny.com> - 18.2.0-1
- New version

* Wed Dec 23 2020 D Tucny <d@tucny.com> - 18.1.1-1
- New version

* Fri Nov 20 2020 D Tucny <d@tucny.com> - 18.1.0-1
- New version

* Sat Nov 07 2020 D Tucny <d@tucny.com> - 18.0.1-1
- New version

* Fri Oct 23 2020 D Tucny <d@tucny.com> - 18.0.0-1
- New release - 18

