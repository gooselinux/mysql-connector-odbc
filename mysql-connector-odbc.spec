Summary: ODBC driver for MySQL
Name: mysql-connector-odbc
Version: 5.1.5r1144
Release: 7%{?dist}
Group: System Environment/Libraries
URL: http://dev.mysql.com/downloads/connector/odbc/
# exceptions allow library to be linked with most open source SW,
# not only GPL code.
License: GPLv2 with exceptions

# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/connector/odbc/
Source: mysql-connector-odbc-%{version}.tar.gz

Patch1: myodbc-my-bool.patch
Patch2: myodbc-shutdown.patch
Patch3: myodbc-multilib.patch
Patch4: myodbc-null-string.patch
Patch5: myodbc-64bit.patch

Requires: unixODBC
BuildRequires: mysql-devel unixODBC-devel
BuildRequires: automake autoconf libtool libtool-ltdl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
An ODBC (rev 3) driver for MySQL, for use with unixODBC.

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"

libtoolize --copy --force
aclocal
automake -a
automake
autoconf

%configure \
	--disable-gui \
	--with-unixODBC=/usr/foo \
	--with-odbc-ini=/etc/odbc.ini \
	--with-mysql-includes=%{_includedir}/mysql \
	--with-mysql-libs=%{_libdir}/mysql

export tagname=CC
make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
%makeinstall LIBTOOL=/usr/bin/libtool

# Remove stuff not to be packaged (possibly reconsider later)
rm -f $RPM_BUILD_ROOT%{_bindir}/myodbc-installer

# we don't want static libraries, thanks
rm -f $RPM_BUILD_ROOT%{_libdir}/libmyodbc5.*a

# makefile thinks it should install docs in totally wrong place
rm -f $RPM_BUILD_ROOT/usr/share/mysql-connector-odbc/README
rm -f $RPM_BUILD_ROOT/usr/share/mysql-connector-odbc/README.debug
rm -f $RPM_BUILD_ROOT/usr/share/mysql-connector-odbc/ChangeLog
rm -f $RPM_BUILD_ROOT/usr/share/mysql-connector-odbc/INSTALL
rm -f $RPM_BUILD_ROOT/usr/share/mysql-connector-odbc/LICENSE.exceptions
rm -f $RPM_BUILD_ROOT/usr/share/mysql-connector-odbc/LICENSE.gpl

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README README.debug ChangeLog LICENSE.gpl LICENSE.exceptions
%{_libdir}/lib*so

%changelog
* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 5.1.5r1144-7
- Correct Source: tag and comment to reflect how to get the tarball

* Mon Nov 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 5.1.5r1144-6.1
- Rebuilt for RHEL 6

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.1.5r1144-6
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5r1144-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5r1144-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 5.1.5r1144-3
- Fix some 64-bitness issues with unixODBC 2.2.14.

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 5.1.5r1144-2
- Rebuild for unixODBC 2.2.14.
- Fix problem with null username/password specifications

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.5r1144-1
- Update to mysql-connector-odbc 5.1.5r1144, to go with MySQL 5.1.x.
  Note the library name has changed from libmyodbc3 to libmyodbc5.

* Tue Aug  5 2008 Tom Lane <tgl@redhat.com> 3.51.26r1127-1
- Update to mysql-connector-odbc 3.51.26r1127

* Tue Mar 25 2008 Tom Lane <tgl@redhat.com> 3.51.24r1071-1
- Update to mysql-connector-odbc 3.51.24r1071

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 3.51.23r998-1
- Update to mysql-connector-odbc 3.51.23r998

* Wed Dec  5 2007 Tom Lane <tgl@redhat.com> 3.51.14r248-3
- Rebuild for new openssl

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 3.51.14r248-2
- Update License tag to match code.

* Fri Apr 20 2007 Tom Lane <tgl@redhat.com> 3.51.14r248-1
- Update to mysql-connector-odbc 3.51.14r248
Resolves: #236473
- Fix build problem on multilib machines

* Mon Jul 17 2006 Tom Lane <tgl@redhat.com> 3.51.12-2.2
- rebuild

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 3.51.12-2
- Remove DLL-unload cleanup call from connection shutdown (bz#185343)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.51.12-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.51.12-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Tom Lane <tgl@redhat.com> 3.51.12-1
- New package replacing MyODBC.
