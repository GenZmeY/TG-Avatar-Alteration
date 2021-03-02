%global debug_package %{nil}
%global __python %{__python3}
%global user tg-aa-user

Name:      tg-avatar-alteration
Version:   1.0.1
Release:   1%{dist}
Summary:   telegram avatar alteration
Group:     Applications/Communications
License:   GNU GPLv3
Url:       https://github.com/GenZmeY/TG-Avatar-Alternation
BuildArch: noarch

Source0:  %{name}
Source1:  main.py
Source2:  %{name}.service
Source3:  %{name}.timer
Source4:  config.py
Source5:  requirements.txt
Source6:  COPYING

Requires: systemd >= 219
Requires: python3 >= 3.6
Requires: python3-pip
Requires: coreutils

Provides: %{name}

%description
telegram avatar alteration

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_unitdir}
install -d %{buildroot}/%{_datadir}/%{name}
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -d %{buildroot}/%{_localstatedir}/cache/%{name}
install -d %{buildroot}/%{_datadir}/licenses/%{name}/*

install -m 644 %{SOURCE0} %{buildroot}/%{_bindir}
install -m 644 %{SOURCE1} %{buildroot}/%{_datadir}/%{name}
install -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}
install -m 644 %{SOURCE5} %{buildroot}/%{_datadir}/%{name}
install -m 644 %{SOURCE5} %{buildroot}/%{_datadir}/licenses/%{name}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(775,root,root)    %dir %{_datadir}/%{name}
%attr(775,root,root)    %dir %{_sysconfdir}/%{name}
%attr(770,root,%{user}) %dir %{_localstatedir}/cache/%{name}
%attr(640,root,%{user}) %config(noreplace) %{_sysconfdir}/%{name}/config.py
%attr(0644,root,root)   %doc %{_datadir}/licenses/%{name}/*
%attr(644,root,root)    %{_datadir}/%{name}/*
%attr(644,root,root)    %{_unitdir}/*
%attr(755,root,root)    %{_bindir}/*

%pre
#!/bin/bash
if [[ $1 -eq 1 ]]; then # First pre installation
	if ! getent passwd %{user} >/dev/null ; then
		useradd -s '/sbin/nologin' %{user}
	fi
fi

%post
#!/bin/bash
if [[ "$1" -eq 1 ]]; then # First install
	sudo -u %{user} -s -- %{_bindir}/pip3 install --user -r %{_datadir}/%{name}/requirements.txt --no-cache-dir
fi

systemctl daemon-reload

%preun
#!/bin/bash
if [[ "$1" -eq 0 ]]; then # Uninstall
	systemctl stop %{name}.service
	systemctl disable %{name}.service
fi

%postun
#!/bin/bash
systemctl daemon-reload
if [[ "$1" -ge 1 ]]; then # Upgrade
	systemctl try-restart %{name}.service
fi

if [[ "$1" -eq 0 ]]; then # Uninstall
	userdel -r %{user}
fi

%changelog
* Tue Mar 02 2021 GenZmeY <genzmey@gmail.com> - 1.0.1-1
- Removed the gap when changing the avatar.

* Mon Mar 01 2021 GenZmeY <genzmey@gmail.com> - 1.0.0-1
- first version.
