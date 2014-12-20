# NOTE
# - don't use %{_*dir} macros for paths defined by FHS
# - do not add any dependencies to this pkg, FHS should be the first package being installed
# - do not use any other user/group than "root", as then we have to depend on "setup" package.
Summary:	Basic FHS 2.3 filesystem layout
Summary(de.UTF-8):	Grundlegende Dateisystemstruktur
Summary(fr.UTF-8):	Arborescence de base du système de fichiers
Summary(pl.UTF-8):	Podstawowy układ katalogów systemu Linux zgodny z FHS 2.3
Summary(tr.UTF-8):	Temel dosya sistemi yapısı
Name:		FHS
Version:	2.3
Release:	36
License:	GPL
Group:		Base
URL:		http://www.pathname.com/fhs/
Source0:	locale-dirs
BuildRequires:	mktemp
BuildRequires:	rpmbuild(macros) >= 1.213
Conflicts:	setup < 2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to put there
%define		_enable_debug_packages	0

# avoid rpm 4.4.9 adding rm -rf buildroot, we need the dirs to check consistency
%define		__spec_clean_body	%{nil}

%define		_locmandir	/usr/local/man

# doesn't contain any files, but we're not noarch package
%define 	no_install_post_strip	1
%define 	no_install_post_chrpath	1
%define 	no_install_post_compress_modules	1

# we have to use numeric uids/groups. see comment above

%define		gid_uucp	14
%define		gid_mail	12

%description
This package contains the basic directory layout for a Linux system,
including the proper permissions for the directories. This layout
conforms to the Filesystem Hierarchy Standard (FHS) 2.3.

%description -l de.UTF-8
Dieses Paket enthält die grundlegende Verzeichnisstruktur eines
Linux-Systems, einschließlich der entsprechenden Zugriffsrechte. Diese
Struktur entspricht dem Filesystem Hierarchy Standard (FHS) 2.3.

%description -l fr.UTF-8
Ce package contient l'arborescence type pour système Linux y compris
les permissions adéquates pour les répertoires. Cette arborescence est
conforme au standard "Filesystem Hierarchy Standard" (FHS) 2.3.

%description -l pl.UTF-8
Pakiet ten zawiera informacje o podstawowej strukturze katalogów
systemu i praw dostępu do nich. Struktura katalogów jest zgodna z FHS
2.3.

%description -l tr.UTF-8
Bu paket GNU makro işleme dilini içerir. Mantıksal olarak
ayrıştırılabilen metin dosyaları yazımı için yararlıdır.

%prep
%setup -qcT
cp -a %{SOURCE0} .

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{bin,boot,dev,etc,home,opt,srv} \
	$RPM_BUILD_ROOT/etc/{X11,opt} \
	$RPM_BUILD_ROOT/lib/modules \
	$RPM_BUILD_ROOT/{mnt,media,proc,root/tmp,sbin,tmp} \
	$RPM_BUILD_ROOT/usr/{bin,games,include,lib,sbin,share,src} \
	$RPM_BUILD_ROOT/usr/share/{dict,doc,games,info,misc,tmac,xml} \
	$RPM_BUILD_ROOT/usr/lib/games \
	$RPM_BUILD_ROOT/usr/local/{bin,etc,games,include,lib,sbin,share/{doc,info},src} \
	$RPM_BUILD_ROOT/var/{cache,crash,db,games,lib/misc,local,lock,log,mail,opt,run,spool,tmp,yp}

%if "%{_lib}" == "lib64"
install -d $RPM_BUILD_ROOT{/lib64,/usr/lib64/games,/usr/local/lib64}
%ifarch %{x8664}
install -d $RPM_BUILD_ROOT{/libx32,/usr/libx32/games,/usr/local/libx32}
%endif
%endif

%if "%{_lib}" == "libx32"
install -d $RPM_BUILD_ROOT{/libx32,/usr/libx32/games,/usr/local/libx32}
%endif

install -d $RPM_BUILD_ROOT/usr/share/man/man{1,2,3,4,5,6,7,8}
install -d $RPM_BUILD_ROOT%{_locmandir}/man{1,2,3,4,5,6,7,8}

# "/usr/local/share/man and /usr/local/man must be synonomous" per FHS 2.3
ln -sf ../man $RPM_BUILD_ROOT/usr/local/share/man

> %{name}.lang
for mloc in $(cat locale-dirs); do
	echo "%%lang($mloc) %dir /usr/share/man/${mloc}" >> %{name}.lang
	for manp in man{1,2,3,4,5,6,7,8}; do
		install -d $RPM_BUILD_ROOT/usr/share/man/${mloc}/${manp}
		echo "%%lang($mloc) %dir /usr/share/man/${mloc}/${manp}" >> %{name}.lang
	done
done

%clean
cd $RPM_BUILD_ROOT

check_filesystem_dirs() {
	RPMFILE=%{name}-%{version}-%{release}.%{_target_cpu}.rpm
	TMPFILE=$(mktemp)
	find | sed -e 's|^\.||g' -e 's|^$||g' | LC_ALL=C sort > $TMPFILE

	# find finds also '.', so use option -B for diff
	if rpm -qpl %{_rpmdir}/$RPMFILE | grep -v '^/$' | LC_ALL=C sort | diff -uB $TMPFILE - ; then
		rm -rf $RPM_BUILD_ROOT
	else
		echo -e "\nNot so good, some directories are not included in package\n"
		exit 1
	fi
	rm -f $TMPFILE
}
check_filesystem_dirs

# XXX: it is 2009, what uucp?! but we use /var/lock/subsys, so change it just to root?
%post -p <lua>
posix.chown("/var/mail", 0, %{gid_mail})
posix.chown("/var/lock", 0, %{gid_uucp})

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir /
%dir /bin
%dir /boot
%dir /dev
%dir /etc
%dir /etc/X11
%dir /etc/opt
%dir /home
%dir /lib
%dir /lib/modules
%dir /media
%dir /mnt
%dir /opt
%dir %attr(555,root,root) %verify(not group) /proc
%dir %attr(700,root,root) /root
%dir %attr(700,root,root) /root/tmp
%dir /sbin
%dir %attr(755,root,root) /srv
%dir %attr(1777,root,root) /tmp
%dir /usr
%dir /usr/bin
%dir /usr/games
%dir /usr/include
%dir /usr/lib
%dir /usr/lib/games
%dir /usr/sbin
%dir /usr/share
%dir /usr/share/dict
%dir /usr/share/doc
%dir /usr/share/games
%dir /usr/share/info
%dir /usr/share/man
%dir /usr/share/man/man[1-8]
%dir /usr/share/misc
%dir /usr/share/tmac
%dir /usr/share/xml
%dir /usr/src
%dir /usr/local
%dir /usr/local/bin
%dir /usr/local/etc
%dir /usr/local/games
%dir /usr/local/include
%dir /usr/local/lib
%dir /usr/local/sbin
%dir /usr/local/share
%dir /usr/local/share/doc
%dir /usr/local/share/info
/usr/local/share/man
%{_locmandir}
%dir /usr/local/src
%dir /var
%dir /var/cache
%dir /var/crash
%dir /var/db
%dir /var/games
%dir /var/lib
%dir /var/lib/misc
%dir /var/local
%dir %attr(1771,root,root) /var/lock
%dir %attr(751,root,root) /var/log
%dir %attr(2775,root,root) /var/mail
%dir /var/opt
%dir /var/run
%dir /var/spool
%dir /var/yp
%dir %attr(1777,root,root) /var/tmp
%if "%{_lib}" == "lib64"
%dir /lib64
%dir /usr/lib64
%dir /usr/lib64/games
%dir /usr/local/lib64
%ifarch %{x8664}
%dir /libx32
%dir /usr/libx32
%dir /usr/libx32/games
%dir /usr/local/libx32
%endif
%endif
%if "%{_lib}" == "libx32"
%dir /libx32
%dir /usr/libx32
%dir /usr/libx32/games
%dir /usr/local/libx32
%endif
