Summary:	Basic FHS 2.3 filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du système de fichiers
Summary(pl):	Podstawowy uk³ad katalogów systemu Linux zgodny z FHS 2.3
Summary(tr):	Temel dosya sistemi yapýsý
Name:		FHS
Version:	2.3
Release:	11
License:	GPL
Group:		Base
URL:		http://www.pathname.com/fhs/
BuildRequires:	rpmbuild(macros) >= 1.213
PreReq:		setup >= 2.4.6-4
Provides:	filesystem
Obsoletes:	filesystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_locmandir	/usr/local/man
%define		_xmandir	/usr/X11R6/man
# directory for "privilege separation" chroot
%define		_privsepdir	/usr/share/empty
# directory for *.idl files (for CORBA implementations)
%define		_idldir		/usr/share/idl

%description
This package contains the basic directory layout for a Linux system,
including the proper permissions for the directories. This layout
conforms to the Filesystem Hierarchy Standard (FHS) 2.3.

%description -l de
Dieses Paket enthält die grundlegende Verzeichnisstruktur eines
Linux-Systems, einschließlich der entsprechenden Zugriffsrechte. Diese
Struktur entspricht dem Filesystem Hierarchy Standard (FHS) 2.3.

%description -l fr
Ce package contient l'arborescence type pour système Linux y compris
les permissions adéquates pour les répertoires. Cette arborescence est
conforme au standard "Filesystem Hierarchy Standard" (FHS) 2.3.

%description -l pl
Pakiet ten zawiera informacje o podstawowej strukturze katalogów
systemu i praw dostêpu do nich. Struktura katalogów jest zgodna z FHS
2.3.

%description -l tr
Bu paket GNU makro iþleme dilini içerir. Mantýksal olarak
ayrýþtýrýlabilen metin dosyalarý yazýmý için yararlýdýr.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,initrd,dev,etc,home/{users,services},opt,selinux,srv,sys} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{X11,certs,opt,security} \
	$RPM_BUILD_ROOT{/lib/{firmware,modules},/%{_lib}/security} \
	$RPM_BUILD_ROOT/{mnt,media/{cdrom,floppy},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT%{_prefix}/{bin,games,include/security,lib,sbin,share,src/examples} \
	$RPM_BUILD_ROOT%{_datadir}/{applications,dict,doc,games,info,misc,tmac} \
	$RPM_BUILD_ROOT%{_libdir}/games \
	$RPM_BUILD_ROOT%{_libdir}/cgi-bin \
	$RPM_BUILD_ROOT%{_prefix}/local/{bin,etc,games,include,lib,sbin,share/{doc,info},src} \
	$RPM_BUILD_ROOT/var/{lock/subsys,log,mail,run,spool} \
	$RPM_BUILD_ROOT/var/{cache,crash,db,games,lib/misc,local,opt,tmp} \
	$RPM_BUILD_ROOT%{_idldir} \
	$RPM_BUILD_ROOT%{_fontsdir}/Type1/{afm,pfm} \
	$RPM_BUILD_ROOT%{_fontsdir}/TTF \
	$RPM_BUILD_ROOT%{_fontsdir}/misc \
	$RPM_BUILD_ROOT%{_privsepdir} \
	$RPM_BUILD_ROOT/usr/X11R6/share

%ifarch %{x8664} ppc64 s390x sparc64
install -d $RPM_BUILD_ROOT{/lib64,%{_prefix}/lib64,%{_prefix}/local/lib64}
%endif

for manp in man{1,2,3,4,5,6,7,8} ; do
	install -d $RPM_BUILD_ROOT%{_mandir}/${manp}
	install -d $RPM_BUILD_ROOT%{_locmandir}/${manp}
	install -d $RPM_BUILD_ROOT%{_xmandir}/${manp}
	for mloc in bg cs da de el es fi fr gl hr hu id it ja ko nl pl pt \
		    pt_BR ro ru sl sk sr sv uk zh_CN zh_TW ; do
		install -d $RPM_BUILD_ROOT%{_mandir}/${mloc}/${manp}
	done
	for mloc in it ko pl ; do
		install -d $RPM_BUILD_ROOT%{_xmandir}/${mloc}/${manp}
	done
done
install -d $RPM_BUILD_ROOT%{_mandir}/man{n,l}
install -d $RPM_BUILD_ROOT%{_mandir}/pl/mann

ln -sf ../man $RPM_BUILD_ROOT/usr/local/share/man

%clean
cd $RPM_BUILD_ROOT

# %{_rpmfilename} is not expanded, so use
# %{name}-%{version}-%{release}.%{buildarch}.rpm
RPMFILE=%{name}-%{version}-%{release}.%{_target_cpu}.rpm
TMPFILE=%{name}-%{version}.tmp$$
find . | sed -e 's|^\.||g' -e 's|^$||g' | sort | grep -v $TMPFILE > $TMPFILE

# find finds also '.', so use option -B for diff
if rpm -qpl %{_rpmdir}/$RPMFILE | grep -v '^/$' | sort | diff -uB $TMPFILE - ; then
	rm -rf $RPM_BUILD_ROOT
else
	echo -e "\nNot so good, some directories are not included in package\n"
	exit 1;
fi

%files
%defattr(644,root,root,755)
%dir /
/bin
/boot
/initrd
/dev
%dir /etc
%dir %{_sysconfdir}/X11
%attr(751,root,root) %dir /etc/certs
%dir %{_sysconfdir}/opt
%attr(751,root,root) %dir /etc/security
%dir /home
/home/users
%attr(751,root,adm) /home/services
/lib
%attr(775,root,disk) %dir /media
%attr(775,root,disk) /media/floppy
%attr(775,root,disk) /media/cdrom
/mnt
/opt
%attr(555,root,proc) %verify(not group) /proc
%attr(700,root,root) /root
%dir /sbin
%dir /sys
%dir /selinux
%attr(751,root,root) /srv
%attr(1777,root,root) /tmp
%dir %{_prefix}
%{_prefix}/bin
%{_prefix}/games
%{_prefix}/include
%{_prefix}/lib
%{_prefix}/sbin
%dir %{_prefix}/share
%{_datadir}/applications
%{_datadir}/dict
%{_datadir}/doc
%{_privsepdir}
%{_fontsdir}
%{_idldir}
%{_datadir}/games
%{_datadir}/info
%dir %{_mandir}
%dir %{_mandir}/man*
%lang(bg) %{_mandir}/bg
%lang(cs) %{_mandir}/cs
%lang(da) %{_mandir}/da
%lang(de) %{_mandir}/de
%lang(el) %{_mandir}/el
%lang(es) %{_mandir}/es
%lang(fi) %{_mandir}/fi
%lang(fr) %{_mandir}/fr
%lang(gl) %{_mandir}/gl
%lang(hr) %{_mandir}/hr
%lang(hu) %{_mandir}/hu
%lang(id) %{_mandir}/id
%lang(it) %{_mandir}/it
%lang(ja) %{_mandir}/ja
%lang(ko) %{_mandir}/ko
%lang(nl) %{_mandir}/nl
%lang(pl) %{_mandir}/pl
%lang(pt) %{_mandir}/pt
%lang(pt_BR) %{_mandir}/pt_BR
%lang(ro) %{_mandir}/ro
%lang(ru) %{_mandir}/ru
%lang(sl) %{_mandir}/sl
%lang(sk) %{_mandir}/sk
%lang(sr) %{_mandir}/sr
%lang(sv) %{_mandir}/sv
%lang(uk) %{_mandir}/uk
%lang(zh_CN) %{_mandir}/zh_CN
%lang(zh_TW) %{_mandir}/zh_TW
%{_datadir}/misc
%{_datadir}/tmac
%dir %{_libdir}/cgi-bin
%{_prefix}/src
%dir %{_prefix}/local
%{_prefix}/local/bin
%{_prefix}/local/etc
%{_prefix}/local/games
%{_prefix}/local/include
%{_prefix}/local/lib
%{_prefix}/local/sbin
%dir %{_prefix}/local/share
%{_prefix}/local/share/doc
%{_prefix}/local/share/man
%{_prefix}/local/share/info
%{_locmandir}
%{_prefix}/local/src
%dir /usr/X11R6
%dir %{_xmandir}
%{_xmandir}/man*
%lang(it) %{_xmandir}/it
%lang(ko) %{_xmandir}/ko
%lang(pl) %{_xmandir}/pl
%dir /usr/X11R6/share

%dir /var
/var/cache
%dir /var/crash
%dir /var/db
%dir /var/games
%dir /var/lib
%dir /var/lib/misc
%dir /var/local
%attr(1771,root,uucp) %dir /var/lock
%attr(700,root,root) %dir /var/lock/subsys
%attr(751,root,root) /var/log
%attr(2775,root,mail) /var/mail
%dir /var/opt
%dir /var/run
%dir /var/spool
%attr(1777,root,root) %dir /var/tmp

%ifarch ppc64 sparc64 x86_64
/lib64
%{_prefix}/lib64
%{_prefix}/local/lib64
%endif
