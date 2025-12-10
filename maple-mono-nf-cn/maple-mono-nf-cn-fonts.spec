## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec
# SPDX-License-Identifier: MIT

%global forgeurl      https://github.com/subframe7536/maple-font
%global commitdate    20251205
%global version0      7.9
%global bumpver       1
%global fontlicense   OFL-1.1
%global fontlicenses  LICENSE.txt
#%%global fontdocs      *.md
#%%global fontdocsex    %%{fontlicenses}

%global common_description  %{expand:
Maple Mono is an open source monospace font focused on smoothing your coding flow. }

%global fontfamily       Maple Mono NF CN
%global fontsummary      Maple Mono Ligature Nerd CN Fonts
%global fonts            MapleMono-*
%global fontconfs        config.json
%global fontdescription  %{expand:
%{common_description}
font. }

Version: %{version0}
Release: %autorelease -b1
URL: %{forgeurl}
VCS: git:%{url}.git

Source0:  %{forgeurl}/releases/download/v%{version}/MapleMono-NF-CN-unhinted.zip

%fontpkg

%prep
%autosetup -c

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
%autochangelog

