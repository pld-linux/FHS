Summary:	Basic FHS 2.1 filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du syst�me de fichiers
Summary(pl):	Podstawowy uk�ad katalog�w systemu Linux zgodny z FHS 2.1
Summary(tr):	Temel dosya sistemi yap�s�
Name:		FHS
Version:	2.1
Release:	16
License:	GPL
Group:		Base
Group(cs):	Z�klad
Group(da):	Basal
Group(de):	Basis
Group(es):	Base
Group(fr):	Base
Group(is):	Grunnforrit
Group(it):	Base
Group(ja):	�١���
Group(no):	Basis
Group(pl):	Podstawowe
Group(pt):	Base
Group(pt_BR):	Base
Group(ru):	������� �����
Group(sl):	Osnova
Group(sv):	Bas
URL:		http://www.pathname.com/fhs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	grep
BuildRequires:	textutils
PreReq:		setup
BuildArch:	noarch
Provides:	filesystem
Obsoletes:	filesystem

%define		_locmandir	/usr/local/share/man
%define		_xmandir	/usr/X11R6/man

%description
This package contains the basic directory layout for a Linux system,
including the proper permissions for the directories. This layout
conforms to the Filesystem Hierarchy Standard (FHS) 2.1.

%description -l de
Dieses Paket enth�lt die grundlegende Verzeichnisstruktur eines
Linux-Systems, einschlie�lich der entsprechenden Zugriffsrechte. Diese
Struktur entspricht dem Filesystem Hierarchy Standard (FHS) 2.1.

%description -l fr
Ce package contient l'arborescence type pour syst�me Linux y compris
les permissions ad�quates pour les r�pertoires. Cette arborescence est
conforme au standard \"Filesystem Hierarchy Standard\" (FHS) 2.1.

%description -l pl
Pakiet ten zawiera informacje o podstawowej strukturze katalog�w
systemu i praw dost�pu do nich. Struktura katalog�w jest zgodna z FHS
2.1.

%description -l tr
Bu paket GNU makro i�leme dilini i�erir. Mant�ksal olarak
ayr��t�r�labilen metin dosyalar� yaz�m� i�in yararl�d�r.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,dev,etc,home/{users,services},opt} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{X11,opt,security} \
	$RPM_BUILD_ROOT/lib/{modules,security} \
	$RPM_BUILD_ROOT/{mnt/{cdrom,floppy},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT%{_prefix}/{bin,games,include,lib,sbin,share,src/examples} \
	$RPM_BUILD_ROOT%{_datadir}/{dict,doc,games,info,misc,tmac} \
	$RPM_BUILD_ROOT%{_libdir}/games \
	$RPM_BUILD_ROOT%{_prefix}/local/{bin,games,lib,sbin,share/{doc,info},src} \
	$RPM_BUILD_ROOT/var/{lock/subsys,log,mail,run,spool} \
	$RPM_BUILD_ROOT/var/{cache,crash,db,games,lib/misc,opt,tmp} \
	$RPM_BUILD_ROOT/usr/X11R6/share/idl \
	$RPM_BUILD_ROOT%{_fontsdir}/Type1/{afm,pfm} \
	$RPM_BUILD_ROOT%{_applnkdir}

for manp in man{1,2,3,4,5,6,7,8} ; do
	install -d $RPM_BUILD_ROOT%{_mandir}/${manp}
	install -d $RPM_BUILD_ROOT%{_locmandir}/${manp}
	install -d $RPM_BUILD_ROOT%{_xmandir}/${manp}
	for mloc in bg cs da de es fi fr hr hu id it ja ko nl pl pt pt_BR ru sl sk sv ; do
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
	echo -e "\nNot so good, some directories are not included in package\n"
	exit 1;
fi

%files
%defattr(644,root,root,755)
%dir /
/bin
/boot
/dev
%dir /etc
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/opt
%attr(751,root,root) %dir /etc/security
%dir /home
/home/users
%attr(751,root,root) /home/services
/lib
/mnt
/opt
%attr(555,root,proc) %verify(not group) /proc
%attr(700,root,root) /root
%dir /sbin
%attr(1777,root,root) /tmp
%dir %{_prefix}
%{_prefix}/bin
%{_prefix}/games
%{_prefix}/include
%{_prefix}/lib
%{_prefix}/sbin
%dir %{_prefix}/share
%{_datadir}/dict
%{_datadir}/doc
%{_fontsdir}
%{_datadir}/games
%{_datadir}/info
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
%lang(id) %{_mandir}/id
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
%{_datadir}/misc
%{_datadir}/tmac
%{_prefix}/src
%dir %{_prefix}/local
%{_prefix}/local/bin
%{_prefix}/local/games
%{_prefix}/local/lib
%{_prefix}/local/sbin
%dir %{_prefix}/local/share
%{_prefix}/local/share/doc
%{_prefix}/local/share/info
%{_locmandir}
%{_prefix}/local/src
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
%dir /var/run
%dir /var/spool
%attr(1777,root,root) %dir /var/tmp
