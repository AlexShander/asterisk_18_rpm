# Note that this is NOT a relocatable package
%define ver      3.2.3
%define prefix   /usr
%define enable_gtk_doc 1
%define libdir lib64

%if %{enable_gtk_doc}
%define gtkdoc_configure_flags --enable-gtk-doc
%else
%define gtkdoc_configure_flags --disable-gtk-doc
%endif

Summary: MIME library
Name: gmime
Version: %ver
Release: 1
License: LGPL
Group: Development/Libraries
URL: https://github.com/jstedfast/gmime

Source: ftp://ftp.gnome.org/pub/GNOME/sources/gmime/3.0/gmime-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

Requires: glib2 >= 2.26.0
BuildRequires: glib2-devel >= 2.26.0
BuildRequires: gtk-doc
BuildRequires: zlib-devel 

%description
GMime is a C/C++ library for parsing and creating messages using
the Multipurpose Internet Mail Extension (MIME).

%package devel
Summary:        MIME Parser and Utility Library -- Development Files
Group:          Development/Libraries/C and C++
Requires:       gmime = %{version}

%description devel
GMime is a C/C++ library for parsing and creating messages using
the Multipurpose Internet Mail Extension (MIME).

%prep
%setup

%build
if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh $ARCHFLAG
fi
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix %gtkdoc_configure_flags --libdir=%{prefix}/%{libdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT}

# rename to prevent conflict with uu* utils from sharutils

#mv $RPM_BUILD_ROOT%{prefix}/bin/uuencode $RPM_BUILD_ROOT%{prefix}/bin/gmime-uuencode
#mv $RPM_BUILD_ROOT%{prefix}/bin/uudecode $RPM_BUILD_ROOT%{prefix}/bin/gmime-uudecode

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%doc AUTHORS ChangeLog NEWS README.md LICENSE COPYING TODO
%{prefix}/%{libdir}/libgmime-*.a
%{prefix}/%{libdir}/libgmime-*.la
%{prefix}/%{libdir}/*.so.*
%if %{enable_gtk_doc}
%{prefix}/share/gtk-doc/html/gmime-3.2*
%endif

%files devel
%defattr (-, root, root)
%doc PORTING
%{prefix}/include/gmime-3.0/gmime/*.h
%{prefix}/%{libdir}/pkgconfig/*
%{prefix}/%{libdir}/*.so
%doc %{prefix}/share/gtk-doc/html/gmime-3.2*

%changelog
* Mon Nov 29 2004 Ryan Skadberg <skadz@stigmata.org>
- Added in sharp package for .NET bindings

* Wed Dec  9 2002 Benjamin Lee <benjamin.lee@aspectdata.com>
- fixed sharutils conflict with uudecode and uuencode.
- removed duplicate libgmime inclusion in %files.

* Wed Dec  4 2002 Benjamin Lee <benjamin.lee@aspectdata.com>
- fixed files for gtk-doc, pkconfig, and includes.

* Sat Mar 24 2001 Leland Elie <lelie@airmail.net>
- created spec file.
