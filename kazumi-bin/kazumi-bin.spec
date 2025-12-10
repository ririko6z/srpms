Name: Kazumi
Version: 1.9.2
Release:        %autorelease
Summary: 基于自定义规则的番剧采集APP，支持流媒体在线观看，支持弹幕，支持实时超分辨率。

License: GPL-2.0-or-later
URL: https://github.com/Predidit/Kazumi
Source0: %{url}/releases/download/%{version}/Kazumi_linux_%{version}_amd64.tar.gz

ExclusiveArch: x86_64

# 禁用调试包（关键添加）
%global debug_package %{nil}
# the last build right now is xx
%global obs_ver 1.8.7

Requires:       xdg-user-dirs
Requires:       webkit2gtk4.1
Requires:       libayatana-appindicator-gtk3

BuildRequires:  patchelf

# 提供虚拟包
Provides:       Kazumi = %{version}-%{release}
Obsoletes:      Kazumi <= %{obs_ver}

%description
Kazumi is a feature-rich cross-platform application built with Flutter.
It integrates advanced media playback (via media_kit), web browsing capabilities
(on Linux via a custom webview_windows fork), and various utility functions.
This package provides the Linux desktop version of Kazumi.

%prep
# -c: 创建 %{name}-%{version} 目录（符合 rpmbuild 预期）
# -T: 禁用默认 tar 解压逻辑，避免目录查找错误
# -q: 静默模式
%setup -qcT
# 手动解压源文件到当前目录（直接提取文件，无外层目录）
tar -xf %{SOURCE0}

%build
:

%install
# 创建安装目录
#mkdir -p %{buildroot}/opt/%{name}
# mkdir -p %{buildroot}%{_bindir}
#mkdir -p %{buildroot}%{_datadir}/applications
#mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -d "%{buildroot}/opt/Kazumi" "%{buildroot}%{_bindir}" "%{buildroot}%{_datadir}/applications" "%{buildroot}%{_iconsdir}/hicolor/512x512/apps"
cp -r ./kazumi ./lib ./data %{buildroot}/opt/Kazumi/
install -Dm644 data/flutter_assets/assets/images/logo/logo_linux.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/Kazumi.png
ln -s ../../opt/Kazumi/kazumi %{buildroot}%{_bindir}/kazumi

# 安装桌面文件（.desktop）
cat > %{buildroot}%{_datadir}/applications/Kazumi.desktop << EOF
[Desktop Entry]
Name=Kazumi
Comment=Watch Animes online with danmaku support.
Comment[zh_CN]=一款好用的追番软件
Exec=/opt/Kazumi/kazumi
StartupWMClass=kazumi
Icon=%{_datadir}/icons/hicolor/512x512/apps/Kazumi.png
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Video;Player;Browser;
EOF

# 关键：清理插件库的无效 RUNPATH，仅保留 $ORIGIN（当前目录）
PLUGIN_LIBS="%{buildroot}/opt/Kazumi/lib/*.so"
for lib in $PLUGIN_LIBS; do
  # 移除无效的临时路径，设置 RUNPATH 为 $ORIGIN（让库从自身目录查找依赖）
  patchelf --set-rpath '$ORIGIN' "$lib"
done

# # 可选：验证修复结果（可注释，用于调试）
# for lib in $PLUGIN_LIBS; do
#   echo "修复后的 RUNPATH for $lib:"
#   patchelf --print-rpath "$lib"
# done

%files
%{_bindir}/kazumi
%{_datadir}/applications/Kazumi.desktop
%{_iconsdir}/hicolor/512x512/apps/Kazumi.png
/opt/Kazumi/

%changelog
%autochangelog
