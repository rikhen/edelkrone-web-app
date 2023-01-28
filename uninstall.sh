#!/bin/bash

# Default PATH
HOME_SDK_PATH="$HOME/edelkrone SDK"

# CPU architecture
CPU_ARCH=x86_64

# Application Mode
GUI_MODE=true


function welcomeMessage {
  echo "Welcome to edelkrone SDK uninstaller"
  echo "This script is going to be uninstalled the edelkrone SDK and its components."
}

function removeBinaries {
  rm -rf "$HOME_SDK_PATH"
}

function removeResourceFile {
  sudo rm -rf  /usr/share/pixmaps/tray_icon.png
  sudo rm -rf  /usr/share/pixmaps/app_icon.png
}

function removeNotificationTool {

  if [[ $CPU_ARCH == "armv7l" ]] && [[ ! -z $GUI_MODE ]]
  then
    sudo rm /usr/lib/arm-linux-gnueabihf/notify-osd
    sudo rm /usr/share/dbus-1/services/org.freedesktop.mate.Notifications.service
    sudo rm /usr/share/glib-2.0/schemas/com.canonical.NotifyOSD.gschema.xml

    sudo /usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
  fi

}

function removeDesktopEntry {
  sudo rm -rf ~/.local/share/applications/edelkronesdk.desktop 
  sudo rm -rf /usr/share/applications/edelkronesdk.desktop 

  update-desktop-database ~/.local/share/applications
}

function removeUdevRule {
  sudo rm -rf /lib/udev/rules.d/60-dfu-util.rules
  sudo udevadm control --reload-rules && sudo udevadm trigger
}

function main {
  welcomeMessage

  if [[ ! -z $GUI_MODE ]]
  then
    removeDesktopEntry
    removeResourceFile
  fi

  removeUdevRule
  removeBinaries  
}

main
