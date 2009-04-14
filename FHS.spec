# NOTE
# - don't use %{_*dir} macros for paths defined by FHS

Summary:	Basic FHS 2.3 filesystem layout
Summary(de.UTF-8):	Grundlegende Dateisystemstruktur
Summary(fr.UTF-8):	Arborescence de base du système de fichiers
Summary(pl.UTF-8):	Podstawowy układ katalogów systemu Linux zgodny z FHS 2.3
Summary(tr.UTF-8):	Temel dosya sistemi yapısı
Name:		FHS
Version:	2.3
Release:	24
License:	GPL
Group:		Base
URL:		http://www.pathname.com/fhs/
BuildRequires:	mktemp
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	setup >= 2.4.6-4
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

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{bin,boot,dev,etc,home,opt,srv} \
	$RPM_BUILD_ROOT/etc/{X11,opt} \
	$RPM_BUILD_ROOT/lib/modules \
	$RPM_BUILD_ROOT/{mnt,media/{cdrom,floppy},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT/usr/{bin,games,include,lib,sbin,share,src} \
	$RPM_BUILD_ROOT/usr/share/{dict,doc,games,info,misc,tmac,xml} \
	$RPM_BUILD_ROOT/usr/lib/games \
	$RPM_BUILD_ROOT/usr/local/{bin,etc,games,include,lib,sbin,share/{doc,info},src} \
	$RPM_BUILD_ROOT/var/{cache,crash,db,games,lib/misc,local,lock,log,mail,opt,run,spool,tmp,yp}

%if "%{_lib}" == "lib64"
install -d $RPM_BUILD_ROOT{/lib64,/usr/lib64/games,/usr/local/lib64}
%endif

for manp in man{1,2,3,4,5,6,7,8} ; do
	install -d $RPM_BUILD_ROOT/usr/share/man/${manp}
	install -d $RPM_BUILD_ROOT%{_locmandir}/${manp}
	for mloc in bg ca cs da de el eo es fi fr gl hr hu id it ja ko lt nl \
			pl pt pt_BR ro ru sk sl sr sv tr uk zh_CN zh_TW ; do
		install -d $RPM_BUILD_ROOT/usr/share/man/${mloc}/${manp}
	done
done

# "/usr/local/share/man and /usr/local/man must be synonomous" per FHS 2.3
ln -sf ../man $RPM_BUILD_ROOT/usr/local/share/man

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

%files
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
%attr(775,root,disk) %dir /media
%attr(775,root,disk) /media/floppy
%attr(775,root,disk) /media/cdrom
%dir /mnt
%dir /opt
%attr(555,root,proc) %verify(not group) /proc
%attr(700,root,root) /root
%dir /sbin
%attr(755,root,root) /srv
%attr(1777,root,root) /tmp
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
%lang(bg) /usr/share/man/bg
%lang(ca) /usr/share/man/ca
%lang(cs) /usr/share/man/cs
%lang(da) /usr/share/man/da
%lang(de) /usr/share/man/de
%lang(el) /usr/share/man/el
%lang(eo) /usr/share/man/eo
%lang(es) /usr/share/man/es
%lang(fi) /usr/share/man/fi
%lang(fr) /usr/share/man/fr
%lang(gl) /usr/share/man/gl
%lang(hr) /usr/share/man/hr
%lang(hu) /usr/share/man/hu
%lang(id) /usr/share/man/id
%lang(it) /usr/share/man/it
%lang(ja) /usr/share/man/ja
%lang(ko) /usr/share/man/ko
%lang(lt) /usr/share/man/lt
%lang(nl) /usr/share/man/nl
%lang(pl) /usr/share/man/pl
%lang(pt) /usr/share/man/pt
%lang(pt_BR) /usr/share/man/pt_BR
%lang(ro) /usr/share/man/ro
%lang(ru) /usr/share/man/ru
%lang(sl) /usr/share/man/sl
%lang(sk) /usr/share/man/sk
%lang(sr) /usr/share/man/sr
%lang(sv) /usr/share/man/sv
%lang(tr) /usr/share/man/tr
%lang(uk) /usr/share/man/uk
%lang(zh_CN) /usr/share/man/zh_CN
%lang(zh_TW) /usr/share/man/zh_TW
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
%attr(1771,root,uucp) %dir /var/lock
%attr(751,root,root) /var/log
%attr(2775,root,mail) /var/mail
%dir /var/opt
%dir /var/run
%dir /var/spool
%dir /var/yp
%attr(1777,root,root) %dir /var/tmp
%if "%{_lib}" == "lib64"
%dir /lib64
%dir /usr/lib64
%dir /usr/lib64/games
%dir /usr/local/lib64
%endif
