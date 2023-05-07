#!/bin/bash

figlet -f /usr/share/figlet/banner.flf "A C L"

echo "Select"
echo "1. File access controll"
echo "2. Command access controll"
echo ">> "
read access_controll_choise
echo ""

if [ $access_controll_choise == '1' ]; then
        echo "Username: "
        read u_name
        echo "File Path: "
        read f_path
        echo "Access Permission: "
        read a_per

        setfacl --modify $u_name:$a_per $f_path
        echo "Access controll has been modified succefully!"
elif [ $access_controll_choise == '2' ]; then
        echo "Select "
        echo "1. Remove user form SUDO access"
        echo "2. Add user to SUDO access"
        echo ">> "
        read sudo_choise
        echo "Username: "
        read u_name
        if [ $sudo_choise == 1 ]; then
                gpasswd -d $u_name sudo
        else
                gpasswd -a $u_name sudo
        echo "Access controll has been modified succefully!"
        fi
else
        echo "Invalid option!"
fi
