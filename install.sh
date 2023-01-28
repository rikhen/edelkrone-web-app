#!/bin/bash

# Default PATH
HOME_SDK_PATH="$HOME/edelkrone SDK"

# Error Enums
ROOT_PERMISSION_ERR=20
WRONG_CPU_ARCH=30
NOT_HAVE_DESKTOP_ENV=40
RUN_WITH_SUDO=50
EULA_NOT_ACCEPTED=60
CPU_ARCH=x86_64

# CPU architecture
GUI_MODE=true

# Application Mode


function err_report {
  echo "errexit on line $(caller)" >&2
}

trap err_report ERR

function exitScript {
  exit ${1}
}

function printBanner {

  cat << "EOF"
           _      _ _                         
   ___  __| | ___| | | ___ __ ___  _ __   ___ 
  / _ \/ _` |/ _ \ | |/ / '__/ _ \| '_ \ / _ \
 |  __/ (_| |  __/ |   <| | | (_) | | | |  __/
  \___|\__,_|\___|_|_|\_\_|  \___/|_| |_|\___|
                                               
EOF

}

function welcomeMessage {
  echo "Welcome to edelkrone SDK installer"
  echo "This script is going to be installed the edelkrone SDK and its components."
}

function finishMessage {
  echo "Installation is finished."
  echo "Removing remaining files."
  echo "TO UNINSTALL edelkrone SDK, YOU CAN DO IT WITH UNINSTALL SCRIPT."  
}

function printLicence {
  less --quit-at-eof license.txt

  echo -n "Accept? (yes/no):"
  read choice

  if [ "$choice" ==  "yes" ] ; then
    echo "Confirmed!"
  else
    echo "EULA is not confirmed!"
	  exitScript ${EULA_NOT_ACCEPTED}
  fi
}

function checkCPUArch {
  arch=$(uname -m)
  if [[ $arch != $CPU_ARCH ]]; then
    echo "This installer for the $CPU_ARCH arch."
    exitScript ${WRONG_CPU_ARCH}
  fi
}

function checkDesktopEnv {

  if [ -z "$XDG_CURRENT_DESKTOP" ]
  then
    echo "The os does not have any desktop environment."
    exitScript ${NOT_HAVE_DESKTOP_ENV}
  fi
}

function checkLibGTK {

  local var=` ldconfig -p | grep libgtk-3.so`

  if [ -z "$var" ]
  then
    echo "The libgtk-3 not found. Please install it."
    exitScript ${NOT_HAVE_DESKTOP_ENV}
  fi
}

function checkSudoPermission {

  if [ `id -u` != 0 ]
  then
    echo "Script does not have a root permission, please run with sudo."
    exitScript ${ROOT_PERMISSION_ERR}
  fi
}

function checkPrerequisites {
  checkCPUArch

  if [ ! -z $GUI_MODE ] 
  then
    # checkDesktopEnv
    checkLibGTK
  fi
}

function installNotificationTool {

  if [[ $CPU_ARCH == "armv7l" ]] && [[ ! -z $GUI_MODE ]]
  then
    sudo mv notification-tool/notify-osd /usr/lib/arm-linux-gnueabihf/
    sudo mv notification-tool/org.freedesktop.mate.Notifications.service /usr/share/dbus-1/services/
    sudo mv notification-tool/com.canonical.NotifyOSD.gschema.xml /usr/share/glib-2.0/schemas/

    sudo /usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
  fi

}

function installComponent {

  mkdir "$HOME_SDK_PATH"

  mv bin "$HOME_SDK_PATH"
  mv www "$HOME_SDK_PATH"
  mv firmware "$HOME_SDK_PATH"
  mv examples "$HOME_SDK_PATH"
  mv cfg "$HOME_SDK_PATH"
  mv uninstall.sh "$HOME_SDK_PATH"

  installNotificationTool

  chmod +x "$HOME_SDK_PATH/uninstall.sh"
}

function installLibraries {

  sudo cp lib/*.so* /usr/local/lib/

  if [[ $CPU_ARCH == "armv7l" ]] && [[ ! -z $GUI_MODE ]]
  then 
    sudo cp lib/gui/*.so* /lib/arm-linux-gnueabihf/
  fi

  sudo ldconfig
}

function installationResourceFiles {
  sudo cp res/* /usr/share/pixmaps/
}

function createDesktopEntry {
  echo "[Desktop Entry]">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Name=edelkrone SDK">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Type=Application">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Comment=edelkrone">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Exec=$HOME/\"edelkrone SDK\"/bin/edelkrone_sdk">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Path=$HOME/edelkrone SDK/bin/">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Icon=app_icon">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Terminal=false">> "$HOME_SDK_PATH/edelkronesdk.desktop"
  echo "Categories=Development">> "$HOME_SDK_PATH/edelkronesdk.desktop"

  cp "$HOME_SDK_PATH/edelkronesdk.desktop" ~/.local/share/applications/
  sudo cp "$HOME_SDK_PATH/edelkronesdk.desktop" /usr/share/applications/

  rm "$HOME_SDK_PATH/edelkronesdk.desktop"

  update-desktop-database ~/.local/share/applications
}

function createUDEVRule {
  
  sudo mv  "$HOME_SDK_PATH/firmware/60-dfu-util.rules" /lib/udev/rules.d/
  sudo udevadm control --reload-rules && sudo udevadm trigger

}

function giveCapabilities {
  
  sudo usermod -a -G dialout $USER  
  sudo adduser $USER plugdev

}

function removeRemainingFiles {
  cd ..
  rm -rf edelkrone_sdk
}

function checkSudo {
  if [[ ! -z $SUDO_USER ]]
  then
    echo "Run script \"without sudo\" " 
    exitScript ${RUN_WITH_SUDO}
  fi
}

function main {
  
  checkSudo

  printBanner
  welcomeMessage

  checkPrerequisites

  sleep 2

  printLicence

  installComponent
  installLibraries

  if [[ ! -z $GUI_MODE ]]
  then
    installationResourceFiles
    createDesktopEntry
  fi
  
  createUDEVRule
  giveCapabilities
  finishMessage

  removeRemainingFiles
}

main
