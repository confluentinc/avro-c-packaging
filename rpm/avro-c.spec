Name:    avro-c
Version: %{__version}
Release: %{__release}%{?dist}

Summary: Apache Avro data serialization C library
Group:   Development/Libraries/C and C++
License: ASL 2.0
URL:     http://avro.apache.org
Source:	 avro-c-%{version}.tar.gz

Patch0: 0001-Use-GNUInstallDirs-for-proper-install-locations.patch

BuildRequires: cmake zlib-devel snappy-devel jansson-devel
# lzma-devel not available on fc20
#BuildRequires: lzma-devel
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Something odd happens with AutoReq.
# snappy-devel provides 'pkgconfig(snappy)', but for some reason
# AutoReq picks up 'pkgconfig(libsnappy)' so we insert a hack here
# to change it to the right Req
%filter_from_requires s/pkgconfig(libsnappy)/pkgconfig(snappy)/g
# After defining the filter, we need to call this to set it up
%filter_setup

%description
Apache Avro™ is a data serialization system.
Avro provides:
 * Rich data structures.
 * A compact, fast, binary data format.
 * A container file, to store persistent data.
 * Remote procedure call (RPC).
 * Simple integration with dynamic languages.

%package devel
Summary: Apache Avro data serialization C library (Development Environment)
Group:   Development/Libraries/C and C++
Requires: %{name} = %{version}

%description devel
Apache Avro™ is a data serialization system.
Avro provides:
 * Rich data structures.
 * A compact, fast, binary data format.
 * A container file, to store persistent data.
 * Remote procedure call (RPC).
 * Simple integration with dynamic languages.

This package contains headers and libraries required to build applications
using avro-c.


%package tools
Summary: Apache Avro data serialization C library (Tools)
Group:   Development/Libraries/C and C++
Requires: %{name} = %{version}

%description tools
Apache Avro™ is a data serialization system.
Avro provides:
 * Rich data structures.
 * A compact, fast, binary data format.
 * A container file, to store persistent data.
 * Remote procedure call (RPC).
 * Simple integration with dynamic languages.

This package contains Avro tools using avro-c.



%prep
%setup -q -n %{name}-%{version}

%patch0 -p1

%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} make install
rm -f %{buildroot}/usr/share/doc/AvroC/index.html

%clean
rm -rf %{buildroot}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(444,root,root)
%{_libdir}/libavro.so.*
%defattr(-,root,root)
%doc LICENSE


%files devel
%defattr(-,root,root)
%{_includedir}/avro.h
%{_includedir}/avro
%defattr(444,root,root)
%{_libdir}/libavro.a
%{_libdir}/libavro.so
%{_libdir}/pkgconfig/avro-c.pc
%doc LICENSE docs/index.txt


%files tools
%defattr(755,root,root)
%{_bindir}/avroappend
%{_bindir}/avrocat
%{_bindir}/avromod
%{_bindir}/avropipe
%doc LICENSE

%changelog
* Mon May 16 2016 Magnus Edenhill <magnus@confluent.io> 1.8.0-0
- Initial RPM
