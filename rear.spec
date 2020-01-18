
Summary:    Relax-and-Recover is a Linux disaster recovery and system migration tool
Name:       rear
Version:    2.4
Release:    10%{?dist}
License:    GPLv3
Group:      Applications/File
URL:        http://relax-and-recover.org/

Source0:    https://github.com/rear/rear/archive/%{version}.tar.gz#/rear-%{version}.tar.gz
Patch4:  rear-bz1492177-warning.patch
Patch6:  rear-rhbz1610638.patch
Patch7:  rear-rhbz1610647.patch
Patch8:  rear-bz1652828-bz1652853.patch
Patch9:  rear-bz1631183.patch
Patch10: rear-bz1639705.patch
Patch11: rear-bz1653214.patch
Patch12: rear-bz1659137.patch
Patch14: rear-bz1672938.patch
Patch15: rear-bz1685166.patch
Patch16: rear-bz1655956.patch
Patch17: rear-bz1732328.patch
Patch18: rear-bz1726982.patch
Patch20: rear-bz1700807.patch

ExcludeArch: s390x
ExcludeArch: s390

### Dependencies on all distributions
BuildRequires:   asciidoc
Requires:   binutils
Requires:   ethtool
Requires:   gzip
Requires:   iputils
Requires:   parted
Requires:   tar
Requires:   openssl
Requires:   gawk
Requires:   attr
Requires:   bc

### If you require NFS, you may need the below packages
#Requires:  nfsclient portmap rpcbind

### We drop LSB requirements because it pulls in too many dependencies
### The OS is hardcoded in /etc/rear/os.conf instead
#Requires:  redhat-lsb

### Required for Bacula/MySQL support
#Requires:  bacula-mysql

### Required for OBDR
#Requires:  lsscsi sg3_utils

### Optional requirement
#Requires:  cfg2html

%ifarch x86_64 i686
Requires:   syslinux
%endif
%ifarch ppc ppc64
Requires:   yaboot
%endif

Requires:   crontabs
Requires:   iproute
Requires:   xorriso

# mingetty is not available anymore with RHEL 7 (use agetty instead via systemd)
# Note that CentOS also has %rhel defined so there is no need to use %centos
%if 0%{?rhel} && 0%{?rhel} > 6
Requires:   util-linux
%else
Requires:   mingetty
Requires:   util-linux
%endif

### The rear-snapshot package is no more
#Obsoletes: rear-snapshot

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
Bacula, Bareos, BORG, Duplicity, rsync).

Relax-and-Recover was designed to be easy to set up, requires no maintenance
and is there to assist when disaster strikes. Its setup-and-forget nature
removes any excuse for not having a disaster recovery solution implemented.

Professional services and support are available.

%pre
if [ $1 -gt 1 ] ; then
# during upgrade remove obsolete directories
%{__rm} -rf %{_datadir}/rear/output/NETFS
fi

%prep
%setup 
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1

echo "30 1 * * * root /usr/sbin/rear checklayout || /usr/sbin/rear mkrescue" >rear.cron

### Add a specific os.conf so we do not depend on LSB dependencies
%{?fedora:echo -e "OS_VENDOR=Fedora\nOS_VERSION=%{?fedora}" >etc/rear/os.conf}
%{?rhel:echo -e "OS_VENDOR=RedHatEnterpriseServer\nOS_VERSION=%{?rhel}" >etc/rear/os.conf}

%build
# asciidoc writes a timestamp to files it produces, based on the last
# modified date of the source file, but is sensible to the timezone.
# This makes the results differ according to the timezone of the build machine
# and spurious changes will be seen.
# Set the timezone to UTC as a workaround.
# https://wiki.debian.org/ReproducibleBuilds/TimestampsInDocumentationGeneratedByAsciidoc
TZ=UTC %{__make} -C doc

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__install} -Dp -m0644 rear.cron %{buildroot}%{_sysconfdir}/cron.d/rear
#%{__install} -Dp -m0644 etc/udev/rules.d/62-rear-usb.rules %{buildroot}%{_sysconfdir}/udev/rules.d/62-rear-usb.rules

%files
%defattr(-, root, root, 0755)
%doc MAINTAINERS COPYING README.adoc doc/*.txt doc/user-guide/relax-and-recover-user-guide.html
%doc %{_mandir}/man8/rear.8*
%config(noreplace) %{_sysconfdir}/cron.d/rear
%config(noreplace) %{_sysconfdir}/rear/
#%config(noreplace) %{_sysconfdir}/udev/rules.d/62-rear-usb.rules
%{_datadir}/rear/
%{_localstatedir}/lib/rear/
%{_sbindir}/rear

%changelog
* Tue Aug 27 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-10
- Apply upstream PR2122: add additional NBU library path to fix support for
  NetBackup 8.
  Resolves: rhbz1700807

* Wed Jul 31 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-9
- Apply upstream PR2173 - Cannot restore using Bacula method
  due to "bconsole" not showing its prompt
  Resolves: rhbz1726982

* Tue Jul 30 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-8
- Backport fix for upstream issue 2187 (disklayout.conf file contains
  duplicate lines, breaking recovery in migration mode or when
  thin pools are used). PR2194, 2196.
  Resolves: rhbz1732328

* Tue Mar 26 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-7
- Backport fix for upstream bug 1913 (backup succeeds in case of tar error)
  Resolves: rhbz1631183
- Apply upstream patch PR1885
  Partition information recorded is unexpected when disk has 4K block size
  Resolves: rhbz1610638
- Apply upstream patch PR1887
  LPAR/PPC64 bootlist is incorrectly set when having multiple 'prep' partitions
  Resolves: rhbz1610647
- Apply upstream patch PR1993
  Automatically exclude $BUILD_DIR from the backup
  Resolves: rhbz1655956
- Require xorriso instead of genisoimage, it is now the preferred method
  and supports files over 4GB in size.
  Resolves: rhbz1462189

* Wed Mar 13 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-5
- Apply upstream PR2065 (record permanent MAC address for team members)
  Resolves: rhbz1685166

* Tue Feb 26 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-4
- Apply upstream PR2034 (multipath optimizations for lots of devices)

* Thu Jan 03 2019 Pavel Cahyna <pcahyna@redhat.com> - 2.4-3
- Backport fixes for upstream bugs 1974 and 1975
- Apply upstream PR1954 (record permanent MAC address for bond members)
- Apply upstream PR2004 (support for custom network interface naming)
- Backport fix for upstream bug 1926 (support for LACP bonding and teaming)

* Wed Jul 18 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.4-2
- Build and install the HTML user guide. #1418459

* Wed Jun 27 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.4-1
- Rebase to version 2.4, drop patches integrated upstream
  Resolves #1534646 #1484051 #1498828 #1571266 #1496518

* Wed Feb 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.00-6
- Ensure that NetBackup is started automatically upon recovery (PR#1544)
  Also do not kill daemons spawned by sysinit.service at the service's end
  (PR#1610, applies to NetBackup and also to dhclient)
  Resolves #1506231
- Print a warning if grub2-mkimage is about to fail and suggest what to do.
  bz#1492177
- Update the patch for #1388653 to the one actually merged upstream (PR1418)

* Fri Jan 12 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.00-5
- cd to the correct directory before md5sum to fix BACKUP_INTEGRITY_CHECK.
  Upstream PR#1685, bz1532676

* Mon Oct 23 2017 Pavel Cahyna <pcahyna@redhat.com> - 2.00-4
- Retry get_disk_size to fix upstream #1370, bz1388653

* Wed Sep 13 2017 Pavel Cahyna <pcahyna@redhat.com> - 2.00-3
- Fix rear mkrescue on systems w/o UEFI. Upstream PR#1481 issue#1478
- Resolves: #1479002

* Wed May 17 2017 Jakub Mazanek <jmazanek@redhat.com> - 2.00-2
- Excluding Archs s390 and s390x
- Related #1355667

* Mon Feb 20 2017 Jakub Mazanek <jmazanek@redhat.com> - 2.00-1
- Rebase to version 2.00 
- Resolves #1355667

* Tue Jul 19 2016 Petr Hracek <phracek@redhat.com> - 1.17.2-6
- Replace experimental grep -P with grep -E
Resolves: #1290205

* Wed Mar 23 2016 Petr Hracek <phracek@redhat.com> - 1.17.2-5
- Remove backuped patched files
Related: #1283930

* Wed Mar 23 2016 Petr Hracek <phracek@redhat.com> - 1.17.2-4
- Rear recovery over teaming interface will not work
Resolves: #1283930

* Tue Mar 08 2016 Petr Hracek <phracek@redhat.com> - 1.17.2-3
- Replace experimental grep -P with grep -E
Resolves: #1290205

* Tue Feb 23 2016 Petr Hracek <phracek@redhat.com> - 1.17.2-2
- rear does not require syslinux
- changing to arch package so that syslinux is installed
- Resolves: #1283927

* Mon Sep 14 2015 Petr Hracek <phracek@redhat.com> - 1.17.2-1
- New upstream release 1.17.2
Related: #1059196

* Wed May 13 2015 Petr Hracek <phracek@redhat.com> 1.17.0-2
- Fix Source tag
Related: #1059196

* Mon May 04 2015 Petr Hracek <phracek@redhat.com> 1.17.0-1
- Initial package for RHEL 7
Resolves: #1059196

* Fri Oct 17 2014 Gratien D'haese <gratien.dhaese@gmail.com>
- added the suse_version lines to identify the corresponding OS_VERSION

* Fri Jun 20 2014 Gratien D'haese <gratien.dhaese@gmail.com>
- add %%pre section

* Thu Apr 11 2013 Gratien D'haese <gratien.dhaese@gmail.com>
- changes Source

* Thu Jun 03 2010 Dag Wieers <dag@wieers.com>
- Initial package. (using DAR)
