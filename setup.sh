#!/usr/bin/env bash
# ====================================================================
# OSINT Recon Suite - Automatic Setup Script for Kali Linux / Debian
# ====================================================================

set -e

echo -e "\033[96m[+] Updating package repositories...\033[0m"
sudo apt update

echo -e "\033[96m[+] Installing system tools (pipx, curl, python3-pip)...\033[0m"
sudo apt install -y python3-pip pipx curl git

echo -e "\033[96m[+] Installing Python OSINT tools (Holehe, Maigret)...\033[0m"
pipx ensurepath
pipx install holehe || pipx upgrade holehe
pipx install maigret || pipx upgrade maigret

echo -e "\033[96m[+] Installing PhoneInfoga binary...\033[0m"
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash
sudo mv ./phoneinfoga /usr/local/bin/

echo -e "\033[92m[✓] All dependencies installed successfully!\033[0m"
echo -e "\033[93m[i] Run the tool using: python3 code.py\033[0m"
