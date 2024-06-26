# NOTE
# - don't use %{_*dir} macros for paths defined by FHS
# - do not add any dependencies to this pkg, FHS should be the first package being installed
# - do not use any other user/group than "root", as then we have to depend on "setup" package.
#   But: root %attr+chown in %post means integrity verification (rpm -V) error.
#   Maybe use non-root %attr+numeric chown in %post (without setup dependency)? The only disadvantage
#   seems to be a warning message on install.
Summary:	Basic FHS 3.0 filesystem layout
Summary(de.UTF-8):	Grundlegende Dateisystemstruktur
Summary(fr.UTF-8):	Arborescence de base du système de fichiers
Summary(pl.UTF-8):	Podstawowy układ katalogów systemu Linux zgodny z FHS 3.0
Summary(tr.UTF-8):	Temel dosya sistemi yapısı
Name:		FHS
Version:	3.0
Release:	8
License:	GPL
Group:		Base
URL:		http://refspecs.linuxfoundation.org/fhs.shtml
# list of languages for localized man pages directories
Source0:	locale-dirs
BuildRequires:	mktemp
BuildRequires:	rpmbuild(macros) >= 1.213
Conflicts:	setup < 2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to put there
%define		_enable_debug_packages	0

%if "%{_lib}" == "lib64"
%define		with_lib64	1
%endif
%if "%{_lib}" == "libx32"
%define		with_libx32	1
%define		with_lib64	1
%else
%ifarch %{x8664}
# x32 as additional ABI
%define		with_libx32	1
%endif
%endif

# avoid rpm 4.4.9 adding rm -rf buildroot, we need the dirs to check consistency
%define		__spec_clean_body	%{nil}

# doesn't contain any files, but we're not noarch package
%define		no_install_post_strip	1
%define		no_install_post_chrpath	1
%define		no_install_post_compress_modules	1

# we have to use numeric uids/groups. see comment above
%define		gid_uucp	14
%define		gid_mail	12

%description
This package contains the basic directory layout for a Linux system,
including the proper permissions for the directories. This layout
conforms to the Filesystem Hierarchy Standard (FHS) %{version}.

%description -l de.UTF-8
Dieses Paket enthält die grundlegende Verzeichnisstruktur eines
Linux-Systems, einschließlich der entsprechenden Zugriffsrechte. Diese
Struktur entspricht dem Filesystem Hierarchy Standard (FHS) %{version}.

%description -l fr.UTF-8
Ce package contient l'arborescence type pour système Linux y compris
les permissions adéquates pour les répertoires. Cette arborescence est
conforme au standard "Filesystem Hierarchy Standard" (FHS) %{version}.

%description -l pl.UTF-8
Pakiet ten zawiera informacje o podstawowej strukturze katalogów
systemu i praw dostępu do nich. Struktura katalogów jest zgodna z FHS
%{version}.

%package debug
Summary:	Debug information directory hierarchy
Summary(pl.UTF-8):	Hierarchia katalogów dla informacji diagnostycznych
Group:		Development/Debug

%description debug
This package provides directory hierarchy for debug information
contained in debuginfo rpm packages.

%description debug -l pl.UTF-8
Ten pakiet dostarcza hierarchię katalogów dla zawarych w pakietach
RPM debuginfo informacji pozwalających na śledzenie programów.

%prep
%setup -qcT
cp -p %{SOURCE0} .

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{bin,boot,dev,etc,home,opt,run,srv,sys} \
	$RPM_BUILD_ROOT/etc/{X11,opt} \
	$RPM_BUILD_ROOT/lib/modules \
	$RPM_BUILD_ROOT/{mnt,media,proc,root/tmp,sbin,tmp} \
	$RPM_BUILD_ROOT/usr/{bin,games,include,lib,libexec,sbin,share,src} \
	$RPM_BUILD_ROOT/usr/share/{color/icc,dict,doc,games,info,misc,ppd,tmac,xml} \
	$RPM_BUILD_ROOT/usr/lib/games \
	$RPM_BUILD_ROOT/usr/local/{bin,etc,games,include,lib,libexec,sbin,share/{color/icc,doc,info,man},src} \
	$RPM_BUILD_ROOT/var/{cache,crash,db,games,lib/{color/icc,misc},local,lock,log,mail,opt,run,spool,tmp,yp}

%if %{with lib64}
install -d $RPM_BUILD_ROOT{/lib64,/usr/lib64/games,/usr/local/lib64}
%endif
%if %{with libx32}
install -d $RPM_BUILD_ROOT{/libx32,/usr/libx32/games,/usr/local/libx32}
%endif

install -d $RPM_BUILD_ROOT/usr/share/man/man{1,2,3,4,5,6,7,8}
install -d $RPM_BUILD_ROOT/usr/local/share/man/man{1,2,3,4,5,6,7,8}

for i in $(seq 0 255); do
	install -d "$RPM_BUILD_ROOT$(printf '/usr/lib/.build-id/%02x' $i)"
done

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
	RPMFILES="%{_rpmdir}/%{name}-%{version}-%{release}.%{_target_cpu}.rpm %{_rpmdir}/%{name}-debug-%{version}-%{release}.%{_target_cpu}.rpm"
	TMPFILE=$(mktemp)
	find | sed -e 's|^\.||g' -e '/^$/d' | LC_ALL=C sort > $TMPFILE

	if rpm -qpl $RPMFILES | grep -v '^/$' | LC_ALL=C sort | diff -u $TMPFILE - ; then
		rm -rf $RPM_BUILD_ROOT
	else
		echo -e "\nNot so good, some directories are not included in package\n"
		exit 1
	fi
	rm -f $TMPFILE
}
check_filesystem_dirs

%pretrans -p <lua>
st = posix.stat("/usr/local/share/man")
if st and st.type == "link" then
    os.remove("/usr/local/share/man")
end

%post -p <lua>
--# XXX: it is 2009, what uucp?! but we use /var/lock/subsys, so change it just to root?
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
%dir /run
%dir /sbin
%dir %attr(755,root,root) /srv
%dir %attr(555,root,root) /sys
%dir %attr(1777,root,root) /tmp
%dir /usr
%dir /usr/bin
%dir /usr/games
%dir /usr/include
%dir /usr/lib
%dir /usr/libexec
%dir /usr/lib/games
%dir /usr/sbin
%dir /usr/share
%dir /usr/share/color
%dir /usr/share/color/icc
%dir /usr/share/dict
%dir /usr/share/doc
%dir /usr/share/games
%dir /usr/share/info
%dir /usr/share/man
%dir /usr/share/man/man[1-8]
%dir /usr/share/misc
%dir /usr/share/ppd
%dir /usr/share/tmac
%dir /usr/share/xml
%dir /usr/src
%dir /usr/local
%dir /usr/local/bin
%dir /usr/local/etc
%dir /usr/local/games
%dir /usr/local/include
%dir /usr/local/lib
%dir /usr/local/libexec
%dir /usr/local/sbin
%dir /usr/local/share
%dir /usr/local/share/color
%dir /usr/local/share/color/icc
%dir /usr/local/share/doc
%dir /usr/local/share/info
%dir /usr/local/share/man
%dir /usr/local/share/man/man[1-8]
%dir /usr/local/src
%dir /var
%dir /var/cache
%dir /var/crash
%dir /var/db
%dir /var/games
%dir /var/lib
%dir /var/lib/color
%dir /var/lib/color/icc
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
%if %{with lib64}
%dir /lib64
%dir /usr/lib64
%dir /usr/lib64/games
%dir /usr/local/lib64
%endif
%if %{with libx32}
%dir /libx32
%dir /usr/libx32
%dir /usr/libx32/games
%dir /usr/local/libx32
%endif

%files debug
%defattr(644,root,root,755)
%dir /usr/lib/.build-id
%dir /usr/lib/.build-id/[0-9a-f][0-9a-f]
