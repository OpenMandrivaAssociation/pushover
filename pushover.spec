Name:		pushover
Version:	0.0.5
Release:	1
Summary:	Fun puzzle game with dominos
Group:		Games/Puzzles
License:	GPLv3
URL:		https://pushover.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop

BuildRequires:	gettext
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	pkgconfig(zlib)

%description
Rearrange the dominoes on the different platforms so that you can start a
chain reaction that makes all dominoes topple over.

%prep
%setup -q

# Fix char encoding
iconv --from=ISO-8859-1 --to=UTF-8 ChangeLog > ChangeLog.utf8
touch -r ChangeLog ChangeLog.utf8
mv ChangeLog.utf8 ChangeLog

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir}
%make

%install
%makeinstall_std

# Remove installed docs
rm -rf %{buildroot}%{_docdir}/%{name}

# Install icons (16, 32, 48, 64px)
for i in 0 1 2 3; do
    px=$(expr ${i} \* 16 + 16)
    mkdir -p %{buildroot}%{_iconsdir}/hicolor/${px}x${px}/apps
    convert %{name}.ico[${i}] \
	%{buildroot}%{_iconsdir}/hicolor/${px}x${px}/apps/%{name}.png
done

# Install desktop file
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	%{SOURCE1}

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS README
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

