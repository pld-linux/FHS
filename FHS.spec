Summary:	Basic FHS 2.1 filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du système de fichiers
Summary(pl):	Podstawa uk³ad katalogów systemu Linux zgodny z FHS 2.1
Summary(tr):	Temel dosya sistemi yapýsý
Name:		FHS
Version:	2.1
Release:	2
License:	GPL
Group:		Base
Group(pl):	Podstawowe
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		setup
Buildarch:	noarch
Provides:	filesystem
Obsoletes:	filesystem

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

install -d $RPM_BUILD_ROOT/{bin,boot,home/users,opt} \
	$RPM_BUILD_ROOT/etc/{X11,profile.d,security,opt} \
	$RPM_BUILD_ROOT/lib/{modules,security} \
	$RPM_BUILD_ROOT/{mnt/{floppy,cdrom},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT%{_prefix}/{bin,src,games,lib,include,sbin,share} \
	$RPM_BUILD_ROOT%{_datadir}/{dict,doc,info,man,misc,games,tmac} \
	$RPM_BUILD_ROOT%{_prefix}/local/{bin,games,share/{info,doc,man},lib,sbin,src} \
	$RPM_BUILD_ROOT/var/{lock/subsys,log,mail,run,spool} \
	$RPM_BUILD_ROOT/var/{games,lib/misc,tmp,db,opt,crash,cache} \
	$RPM_BUILD_ROOT/var/cache \
	$RPM_BUILD_ROOT%{_applnkdir}

%clean
cd $RPM_BUILD_ROOT 

# %{_rpmfilename} does not expanded, so use   
# %{name}-%{version}-%{release}.%{buildarch}.rpm
RPMFILE=%{name}-%{version}-%{release}.%{buildarch}.rpm
TMPFILE=%{name}-%{version}.tmp$$
find . | sed -e 's|^\.||g' -e 's|^$||g' | sort | grep -v $TMPFILE > $TMPFILE

# find finds also '.', so use option -B for diff
if rpm -qpl %{_rpmdir}/$RPMFILE | sort | diff -uB $TMPFILE - ; then
     rm -rf $RPM_BUILD_ROOT
else 
    echo -e "\nNot so good, some directories not included in package\n"
    exit 1;	
fi

%files
%defattr(755,root,root,755)
/bin
%attr(700,root,root) /boot
%dir %{_sysconfdir}
%attr(751,root,root) %dir /etc/security
%dir %{_sysconfdir}/profile.d
%dir %{_sysconfdir}/opt
%dir %{_sysconfdir}/X11
/home
/lib
/mnt
/opt
%attr(555,root,root) /proc
%attr(700,root,root) /root
%dir /sbin
%attr(1777,root,root) /tmp
%{_prefix}
%dir /var
/var/cache
%dir /var/crash
%dir /var/db
%dir /var/games
%dir /var/lib
%dir /var/lib/misc
%attr(751,root,root) /var/log
/var/lock
%attr(775,root,mail) /var/mail
%dir /var/opt
%dir /var/spool
%dir /var/run
%attr(1777,root,root) %dir /var/tmp
	
