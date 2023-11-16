%global lead {{{ get_version_lead }}}
%global follow {{{ get_version_follow }}}


Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=%{lead} follow=%{follow} }}}
Release:        1%{?dist}
Summary:        libcamera based apps that copy raspicam apps

License:        BSD
URL:            https://www.raspberrypi.com/documentation/accessories/camera.html
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  %{arm} aarch64

Source:         {{{ git_dir_pack }}}

Patch0:         rpicam-apps-handle-connection-drop.patch

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  boost-program-options
BuildRequires:  libepoxy-devel
BuildRequires:  libdrm-devel
BuildRequires:  libexif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libcamera-devel
BuildRequires:  opencv-devel

# Dependencies to build the libav codec
BuildRequires:  libavcodec-devel
BuildRequires:  libavdevice-devel
BuildRequires:  libavformat-devel
BuildRequires:  libswresample-devel

Requires:       libcamera
Requires:       libcamera-ipa

%description
This is a small suite of libcamera-based apps that aim to copy the functionality of the existing "raspicam" apps.

%package libs
Summary:        Libraries needed by libcamera-apps

%description libs
Libraries for a small suite of libcamera-based apps that aim to copy the functionality of the existing "raspicam" apps.

%package devel
Summary:        Development files for libcamera-apps-libs
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for a small suite of libcamera-based apps that aim to copy the functionality of the existing "raspicam" apps.

%prep
{{{ git_dir_setup_macro }}}
%autopatch -p1

%build
# Remove meson version requirement
sed -i '/meson_version/d' meson.build

%meson --buildtype=release \
             -Denable_libav=true \
             -Denable_drm=true \
             -Denable_egl=true \
             -Denable_qt=false \
             -Denable_opencv=true \
             -Denable_tflite=false \
%ifarch %{arm}
             -Dneon_flags=armv8-neon
%endif
%ifarch aarch64
             -Dneon_flags=arm64
%endif

%meson_build

%install
%meson_install

%files
%license license.txt
%{_bindir}/libcamera-*
%{_bindir}/camera-bug-report

%files libs
%{_libdir}/libcamera_app.so.*

%files devel
%{_libdir}/libcamera_app.so
%{_includedir}/%{name}

%changelog
{{{ git_dir_changelog }}}
