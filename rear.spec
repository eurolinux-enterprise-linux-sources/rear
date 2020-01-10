Summary:     Relax-and-Recover is a Linux disaster recovery and system migration tool
Name:        rear
Version:     1.17.2
Release:     7%{?dist}
License:     GPLv2+
Group:       Applications/File
URL:         http://relax-and-recover.org/

# as GitHub stopped with download section we need to go back to Sourceforge for downloads
Source0:     https://sourceforge.net/projects/rear/files/rear/1.17/%{version}/rear-%{version}.tar.gz
Patch0:      pr-1383.diff

BuildRoot:   %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:        git
Requires:    binutils
Requires:    ethtool
Requires:    gzip
Requires:    iputils
Requires:    parted
Requires:    tar
Requires:    openssl
Requires:    gawk
Requires:    attr

%ifarch %ix86 x86_64
Requires:    syslinux
%endif
%ifarch ppc ppc64 ppc64le
Requires: yaboot
%endif

Requires:    crontabs
Requires:    iproute
Requires:    genisoimage

%if 0%{?rhel} && 0%{?rhel} > 6
Requires:    util-linux
%else
Requires:    mingetty
Requires:    util-linux
%endif

%description
Relax-and-Recover is the leading Open Source disaster recovery and system
migration solution. It comprises of a modular
frame-work and ready-to-go workflows for many common situations to produce
a bootable image and restore from backup using this image. As a benefit,
it allows to restore to different hardware and can therefore be used as
a migration tool as well.

Currently Relax-and-Recover supports various boot media (incl. ISO, PXE,
OBDR tape, USB or eSATA storage), a variety of network protocols (incl.
sftp, ftp, http, nfs, cifs) as well as a multitude of backup strategies
(incl.  IBM TSM, HP DataProtector, Symantec NetBackup, EMC NetWorker,
Bacula, Bareos, rsync).

Relax-and-Recover was designed to be easy to set up, requires no maintenance
and is there to assist when disaster strikes. Its setup-and-forget nature
removes any excuse for not having a disaster recovery solution implemented.

%pre
if [ $1 -gt 1 ] ; then
# during upgrade remove obsolete directories
%{__rm} -rf %{_datadir}/rear/output/NETFS
fi

%prep
%setup -q 
git init
git config user.email "rpm-build"
git config user.name "rpm-build"
git add .
git commit -a -q -m "%{version} baseline."
# Apply all the patches on top.
git apply %{patches}
rm -rf .git

echo "30 1 * * * root /usr/sbin/rear checklayout || /usr/sbin/rear mkrescue" >rear.cron

### Add a specific os.conf so we do not depend on LSB dependencies
%{?fedora:echo -e "OS_VENDOR=Fedora\nOS_VERSION=%{?fedora}" >etc/rear/os.conf}
%{?rhel:echo -e "OS_VENDOR=RedHatEnterpriseServer\nOS_VERSION=%{?rhel}" >etc/rear/os.conf}

%build

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__install} -Dp -m0644 rear.cron %{buildroot}%{_sysconfdir}/cron.d/rear
#%{__install} -Dp -m0644 etc/udev/rules.d/62-rear-usb.rules %{buildroot}%{_sysconfdir}/udev/rules.d/62-rear-usb.rules

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING README.adoc doc/*.txt
%doc %{_mandir}/man8/rear.8*
%config(noreplace) %{_sysconfdir}/cron.d/rear
%config(noreplace) %{_sysconfdir}/rear/
%{_datadir}/rear/
%{_localstatedir}/lib/rear/
%{_sbindir}/rear

%changelog
* Thu Apr 19 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.17.2-7
- Backport upstream PR1383: Allow backup to be stored in ISO for ppc64/ppc64le
- Resolves: #1478584

* Tue Dec 15 2015 Petr Hracek <phracek@redhat.com> - 1.17.2-4
- Upstream license 1.17.2 is GPLv2+. Changing license to proper one.
- Resolves: #981637

* Mon Dec 14 2015 Petr Hracek <phracek@redhat.com> - 1.17.2-3
- Change license to GPLv3 suggested by upstream
- Resolves: #981637

* Mon Dec 14 2015 Petr Hracek <phracek@redhat.com> - 1.17.2-2
- Update description
- Remove other distros from SPEC
- Changed license
- Change Source0 to Sourceforge
- Resolves: #981637

* Mon Dec 07 2015 Petr Hracek <phracek@redhat.com> - 1.17.2-1
- Initial package for RHEL 6
Resolves: #981637

* Fri Oct 17 2014 Gratien D'haese <gratien.dhaese@gmail.com>
- added the suse_version lines to identify the corresponding OS_VERSION

* Fri Jun 20 2014 Gratien D'haese <gratien.dhaese@gmail.com>
- add %%pre section

* Thu Apr 11 2013 Gratien D'haese <gratien.dhaese@gmail.com>
- changes Source

* Thu Jun 03 2010 Dag Wieers <dag@wieers.com>
- Initial package. (using DAR)
