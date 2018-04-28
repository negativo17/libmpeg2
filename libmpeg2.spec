Name:           libmpeg2
Version:        0.5.1
Release:        13%{?dist}
Summary:        MPEG-2 decoder libraries
License:        GPLv2+
URL:            http://libmpeg2.sourceforge.net/

Source0:        http://libmpeg2.sourceforge.net/files/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  SDL-devel
BuildRequires:  libtool
BuildRequires:  libXt-devel
BuildRequires:  libXv-devel

%description
libmpeg2 is a free library for decoding MPEG-2 and MPEG-1 video streams.

%package -n     mpeg2dec
Summary:        MPEG-2 decoder program

%description -n mpeg2dec
mpeg2dec is a test program for %{name}. It decodes MPEG-1 and MPEG-2 video
streams, and also includes a demultiplexer for MPEG-1 and MPEG-2 program
streams. It is purposely kept simple: it does not include features like reading
files from a DVD, CSS, full screen output, navigation, etc.
The main purpose of mpeg2dec is to have a simple test bed for %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q
iconv -f ISO-8859-1 -t UTF-8 AUTHORS > AUTHORS.tmp
touch -r AUTHORS AUTHORS.tmp 
cp -p -f AUTHORS.tmp AUTHORS
rm AUTHORS.tmp

# Disable ppc altivec case
sed -i -e 's/ppc-/noppc64-/' configure.ac configure
sed -i -e 's/powerpc-/nopowerpc64-/' configure.ac configure

%build
autoreconf -vif
%configure \
    --disable-static \
%ifarch ppc
    --disable-accel-detect \
%endif

make %{?_smp_mflags} \
%ifarch %{ix86}
  OPT_CFLAGS="-fPIC -DPIC" \
%else
  OPT_CFLAGS="" \
%endif

%install
%make_install
find %{buildroot} -name '*.la' -delete

# Fix datatype internal definitions
install -pm 0644 libmpeg2/mpeg2_internal.h %{buildroot}%{_includedir}/mpeg2dec/

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README TODO
%{_libdir}/*.so.*

%files -n mpeg2dec
%{_bindir}/corrupt_mpeg2
%{_bindir}/extract_mpeg2
%{_bindir}/mpeg2dec
%{_mandir}/man1/*.1*

%files devel
%doc CodingStyle doc/libmpeg2.txt doc/sample*.c
%{_includedir}/mpeg2dec/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/libmpeg2convert.pc

%changelog
* Sat Apr 28 2018 Simone Caronni <negativo17@gmail.com> - 0.5.1-13
- SPEC file cleanup.

* Wed May 25 2016 Simone Caronni <negativo17@gmail.com> - 0.5.1-12
- SPEC file cleanup.
- Add license macro.
- Use autotools to remove RPATH macro.

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
