Name:           umurmur
Version:        0.2.17
Release:        1%{?dist}
Summary:        Minimalistic Murmur server

License:        BSD
URL:            http://umurmur.net
Source0:        https://github.com/umurmur/umurmur/archive/%{version}.tar.gz
Source1:        umurmurd.service

BuildRequires:  openssl-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  libconfig-devel
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  systemd
Requires:       openssl
Requires:       protobuf-c


%description
Minimalistic Murmur server


%prep
%setup -n %{name}-%{version}
sed -i 's|/var/log/umurmurd.log|/var/log/umurmurd/umurmurd.log|' umurmur.conf.example
sed -i 's|/etc/umurmur/|/var/lib/umurmurd/|' umurmur.conf.example


%build
./autogen.sh
%configure --with-ssl=openssl
make
strip src/umurmurd


%install
install -p -D -m 0755 src/umurmurd %{buildroot}%{_bindir}/umurmurd
install -p -D -m 0640 umurmur.conf.example %{buildroot}%{_sysconfdir}/umurmurd/umurmurd.conf
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/umurmurd.service
install -d -m 750 %{buildroot}%{_localstatedir}/log/umurmurd
install -d -m 755 %{buildroot}%{_sharedstatedir}/umurmurd


%pre
getent group umurmurd >/dev/null || groupadd -r umurmurd
if ! getent passwd umurmurd >/dev/null; then
  useradd -r -g umurmurd -G umurmurd -d %{_sharedstatedir}/umurmurd -s /sbin/nologin -c "Umurmur daemon" umurmurd
fi
exit 0


%post
%systemd_post umurmurd.service


%preun
%systemd_preun umurmurd.service


%postun
%systemd_postun_with_restart umurmurd.service


%files
%{_bindir}/umurmurd
%{_unitdir}/umurmurd.service
%dir %attr(0750, umurmurd, umurmurd) %{_sysconfdir}/umurmurd
%attr(0750, root, umurmurd) %{_sysconfdir}/umurmurd/umurmurd.conf
%dir %attr(0750, umurmurd, root) %{_localstatedir}/log/umurmurd
%dir %attr(0750, umurmurd, umurmurd) %{_sharedstatedir}/umurmurd


%changelog
* Tue Aug 01 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 0.2.17-1
- Bump to 0.2.17

* Fri Feb 17 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 0.2.16-1
- Initial packaging
