Summary:	Basic FHS 2.1 filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du système de fichiers
Summary(pl):	Podstawa uk³ad katalogów systemu Linux zgodny z FHS 2.1
Summary(tr):	Temel dosya sistemi yapýsý
Name:		FHS
Version:	2.1
Release:	14
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
URL:		http://www.pathname.com/fhs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		setup
Buildarch:	noarch
Provides:	filesystem
Obsoletes:	filesystem

%define		_locmandir	/usr/local/share/man
%define		_xmandir	/usr/X11R6/man

%description
This package contains the basic directory layout for a Linux system,
including the proper permissions for the directories. This layout
conforms to the Filesystem Hierarchy Standard (FHS) 2.1.

%description -l de
Dieses Paket enthält die grundlegende Verzeichnisstruktur eines
Linux-Systems, einschließlich der entsprechenden Zugriffsrechte. Diese
Struktur entspricht dem Filesystem Hierarchy Standard (FHS) 2.1.

%description -l fr
Ce package contient l'arborescence type pour système linux y compris
les permissions adéquates pour les répertoires. Cette arborescence est
conforme au standard \"Filesystem Hierarchy Standard\" (FHS) 2.1.

%description -l pl
Pakiet ten zawiera informacje o podstawowej strukturze katalogów
systemu i praw dostêpu do nich. Struktura katalogów jest zgodna z FHS
2.1.

%description -l tr
Bu paket GNU makro iþleme dilini içerir. Mantýksal olarak
ayrýþtýrýlabilen metin dosyalarý yazýmý için yararlýdýr.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,dev,home/users,opt} \
	$RPM_BUILD_ROOT/etc/{X11,security,opt} \
	$RPM_BUILD_ROOT/lib/{modules,security} \
	$RPM_BUILD_ROOT/{mnt/{floppy,cdrom},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT%{_prefix}/{bin,src,games,lib,include,sbin,share} \
	$RPM_BUILD_ROOT%{_datadir}/{dict,doc,info,misc,games,tmac} \
	$RPM_BUILD_ROOT%{_libdir}/games \
	$RPM_BUILD_ROOT%{_prefix}/local/{bin,games,share/{info,doc},lib,sbin,src} \
	$RPM_BUILD_ROOT/var/{lock/subsys,log,mail,run,spool} \
	$RPM_BUILD_ROOT/var/{games,lib/misc,tmp,db,opt,crash,cache} \
	$RPM_BUILD_ROOT/var/cache \
	$RPM_BUILD_ROOT%{_applnkdir} \
	$RPM_BUILD_ROOT/usr/X11R6/share/idl \
	$RPM_BUILD_ROOT%{_fontsdir}/Type1/{afm,pfm}

for manp in man{1,2,3,4,5,6,7,8} ; do
	install -d $RPM_BUILD_ROOT%{_mandir}/${manp}
	install -d $RPM_BUILD_ROOT%{_locmandir}/${manp}
	install -d $RPM_BUILD_ROOT%{_xmandir}/${manp}
	for mloc in bg cs da de es fi fr hr hu it ja ko nl pl pt pt_BR ru sl sk sv ; do
		install -d $RPM_BUILD_ROOT%{_mandir}/${mloc}/${manp}
	done
	install -d $RPM_BUILD_ROOT%{_xmandir}/fr/${manp}
done
install -d $RPM_BUILD_ROOT%{_mandir}/mann

%clean
cd $RPM_BUILD_ROOT

# %{_rpmfilename} is not expanded, so use
# %{name}-%{version}-%{release}.%{buildarch}.rpm
RPMFILE=%{name}-%{version}-%{release}.%{buildarch}.rpm
TMPFILE=%{name}-%{version}.tmp$$
find . | sed -e 's|^\.||g' -e 's|^$||g' | sort | grep -v $TMPFILE > $TMPFILE

# find finds also '.', so use option -B for diff
if rpm -qpl %{_rpmdir}/$RPMFILE | grep -v '^/$' | sort | diff -uB $TMPFILE - ; then
	rm -rf $RPM_BUILD_ROOT
else
	echo -e "\nNot so good, some directories not included in package\n"
	exit 1;
fi

%files
%defattr(644,root,root,755)
%dir /
/bin
/boot
/dev
%dir %{_sysconfdir}
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/opt
%attr(751,root,root) %dir /etc/security
/home
/lib
/mnt
/opt
%attr(555,root,proc) %verify(not group) /proc
%attr(700,root,root) /root
%dir /sbin
%attr(1777,root,root) /tmp
%dir /usr
/usr/bin
/usr/games
/usr/include
/usr/lib
/usr/sbin
%dir /usr/share
/usr/share/dict
/usr/share/doc
%{_fontsdir}
/usr/share/games
/usr/share/info
%dir %{_mandir}
%dir %{_mandir}/man*
%lang(bg) %{_mandir}/bg
%lang(cs) %{_mandir}/cs
%lang(da) %{_mandir}/da
%lang(de) %{_mandir}/de
%lang(es) %{_mandir}/es
%lang(fi) %{_mandir}/fi
%lang(fr) %{_mandir}/fr
%lang(hr) %{_mandir}/hr
%lang(hu) %{_mandir}/hu
%lang(it) %{_mandir}/it
%lang(ja) %{_mandir}/ja
%lang(ko) %{_mandir}/ko
%lang(nl) %{_mandir}/nl
%lang(pl) %{_mandir}/pl
%lang(pt) %{_mandir}/pt
%lang(pt_BR) %{_mandir}/pt_BR
%lang(ru) %{_mandir}/ru
%lang(sl) %{_mandir}/sl
%lang(sk) %{_mandir}/sk
%lang(sv) %{_mandir}/sv
/usr/share/misc
/usr/share/tmac
/usr/src
%dir /usr/local
/usr/local/bin
/usr/local/games
/usr/local/lib
/usr/local/sbin
%dir /usr/local/share
/usr/local/share/doc
/usr/local/share/info
%{_locmandir}
/usr/local/src
%dir /usr/X11R6
%dir %{_xmandir}
%{_xmandir}/man*
%lang(fr) %{_xmandir}/fr
%dir /usr/X11R6/share
%{_applnkdir}
/usr/X11R6/share/idl

%dir /var
/var/cache
%dir /var/crash
%dir /var/db
%dir /var/games
%dir /var/lib
%dir /var/lib/misc
/var/lock
%attr(751,root,root) /var/log
%attr(775,root,mail) /var/mail
%dir /var/opt
%dir /var/spool
%dir /var/run
%attr(1777,root,root) %dir /var/tmp
