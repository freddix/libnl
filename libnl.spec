Summary:	Netlink sockets library
Name:		libnl
Version:	3.2.21
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://www.infradead.org/~tgr/libnl/files/%{name}-%{version}.tar.gz
# Source0-md5:	6fe7136558a9071e70673dcda38545b3
Patch0:		%{name}-link.patch
URL:		http://www.infradead.org/~tgr/libnl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	python-devel
BuildRequires:	swig-python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	bfifo.so.0.0.0 blackhole.so.0.0.0 htb.so.0.0.0 pfifo.so.0.0.0 basic.so.0.0.0 cgroup.so.0.0.0

%description
libnl is a library for applications dealing with netlink socket. It
provides an easy to use interface for raw netlink message but also
netlink family specific APIs.

%package devel
Summary:	Header files for libnl library
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for libnl library.

%package -n python-netlink
Summary:	Python wrapper for netlink protocols
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-netlink
Python wrapper for netlink protocols.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static
%{__make}

cd python
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags} -L$(pwd)/../lib/.libs" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd python
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnl/cli/*/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%dir %{_sysconfdir}/libnl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libnl/classid
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libnl/pktloc
%attr(755,root,root) %{_sbindir}/genl-ctrl-list
%attr(755,root,root) %{_sbindir}/nl-class-*
%attr(755,root,root) %{_sbindir}/nl-classid-lookup
%attr(755,root,root) %{_sbindir}/nl-cls-*
%attr(755,root,root) %{_sbindir}/nl-link-list
%attr(755,root,root) %{_sbindir}/nl-pktloc-lookup
%attr(755,root,root) %{_sbindir}/nl-qdisc-*

%attr(755,root,root) %ghost %{_libdir}/libnl-3.so.200
%attr(755,root,root) %ghost %{_libdir}/libnl-cli-3.so.200
%attr(755,root,root) %ghost %{_libdir}/libnl-genl-3.so.200
%attr(755,root,root) %ghost %{_libdir}/libnl-nf-3.so.200
%attr(755,root,root) %ghost %{_libdir}/libnl-route-3.so.200
%attr(755,root,root) %{_libdir}/libnl-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libnl-cli-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libnl-genl-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libnl-nf-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libnl-route-3.so.*.*.*

%dir %{_libdir}/libnl
%dir %{_libdir}/libnl/cli
%dir %{_libdir}/libnl/cli/cls
%dir %{_libdir}/libnl/cli/qdisc
%attr(755,root,root) %{_libdir}/libnl/cli/cls/*.so*
%attr(755,root,root) %{_libdir}/libnl/cli/qdisc/*.so*

%{_mandir}/man8/genl-ctrl-list.8.gz
%{_mandir}/man8/nl-classid-lookup.8*
%{_mandir}/man8/nl-pktloc-lookup.8*
%{_mandir}/man8/nl-qdisc-*.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnl-3.so
%attr(755,root,root) %{_libdir}/libnl-cli-3.so
%attr(755,root,root) %{_libdir}/libnl-genl-3.so
%attr(755,root,root) %{_libdir}/libnl-nf-3.so
%attr(755,root,root) %{_libdir}/libnl-route-3.so
%{_libdir}/libnl-3.la
%{_libdir}/libnl-cli-3.la
%{_libdir}/libnl-genl-3.la
%{_libdir}/libnl-nf-3.la
%{_libdir}/libnl-route-3.la
%{_includedir}/libnl3
%{_pkgconfigdir}/libnl-3.0.pc
%{_pkgconfigdir}/libnl-cli-3.0.pc
%{_pkgconfigdir}/libnl-genl-3.0.pc
%{_pkgconfigdir}/libnl-nf-3.0.pc
%{_pkgconfigdir}/libnl-route-3.0.pc

%files -n python-netlink
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/netlink/_capi.so
%attr(755,root,root) %{py_sitedir}/netlink/route/_capi.so
%dir %{py_sitedir}/netlink
%dir %{py_sitedir}/netlink/route
%dir %{py_sitedir}/netlink/route/links
%dir %{py_sitedir}/netlink/route/qdisc
%{py_sitedir}/netlink/*.py[co]
%{py_sitedir}/netlink/route/*.py[co]
%{py_sitedir}/netlink/route/links/*.py[co]
%{py_sitedir}/netlink/route/qdisc/*.py[co]

