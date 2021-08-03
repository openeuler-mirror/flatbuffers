%ifarch ppc64 s390x %{arm}
%bcond_with tests
%else
%bcond_without tests
%endif
Name:                flatbuffers
Version:             1.10.0
Release:             2
Summary:             Memory efficient serialization library
License:             Apache-2.0
URL:                 https://github.com/google/flatbuffers
Source0:             https://github.com/google/flatbuffers/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:             flatc.1
Source2:             flatbuffers.7

Patch0:              0001-generate-gcc-pragmas-to-ignore-Wclass-memaccess.patch
Patch1:              Handle-git-program-or-.git-folder-absence.patch
Patch2:              fix-compilation-failed.patch

BuildRequires:       gcc-c++ cmake >= 2.8.9
Provides:            bundled(grpc)
%description
FlatBuffers is a serialization library for games and other memory constrained
apps. FlatBuffers allows you to directly access serialized data without
unpacking/parsing it first, while still having great forwards/backwards
compatibility.

%package             devel
Summary:             Development files for %{name}
Requires:            %{name}%{?_isa} = %{version}-%{release}
%description         devel
%{summary}.

%prep
%autosetup -p1
rm -rf js net php python docs go java js biicode {samples/,}android
chmod -x readme.md
%cmake -DCMAKE_BUILD_TYPE=Release \
       -DFLATBUFFERS_BUILD_SHAREDLIB=ON \
       -DFLATBUFFERS_BUILD_FLATLIB=OFF \
       -DFLATBUFFERS_BUILD_FLATC=ON \
       -DFLATBUFFERS_BUILD_TESTS=%{?with_tests:ON}%{!?with_tests:OFF}

%build
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_mandir}/man{1,7}
cp -p %SOURCE1 %{buildroot}%{_mandir}/man1/flatc.1
cp -p %SOURCE2 %{buildroot}%{_mandir}/man7/flatbuffers.7

%check
%if %{with tests}
make test
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc readme.md
%{_bindir}/flatc
%{_libdir}/libflatbuffers.so.*
%{_mandir}/man1/flatc.1*

%files devel
%{_includedir}/flatbuffers
%{_libdir}/libflatbuffers.so
%{_mandir}/man7/flatbuffers.7*
%{_libdir}/cmake/flatbuffers/*.cmake

%changelog
* Mon Aug 2 2021 Haiwei Li <lihaiwei8@huawei.com> - 1.10.0-2
- Fix complication failed due to gcc upgrade

* Mon Jan 11 2021 yanan li <liyanan32@huawei.com> - 1.10.0-1
- Package init
