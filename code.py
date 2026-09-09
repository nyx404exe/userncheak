#!/usr/bin/env python3
"""
====================================================================
 ⚡ CYBER PARK - ADVANCED OSINT & RECON SUITE
 Multi-Purpose Intelligence Gathering & OSINT Reconnaissance Framework
====================================================================
"""

import sys
import os
import shutil
import subprocess
import datetime
import json
import socket
import urllib.request
import urllib.error
from pathlib import Path

# Force UTF-8 stdout encoding for Windows terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# --- Cyber Park ANSI Color Palette ---
COLOR_RESET   = "\033[0m"
COLOR_BOLD    = "\033[1m"
COLOR_CYAN    = "\033[96m"
COLOR_GREEN   = "\033[92m"
COLOR_YELLOW  = "\033[93m"
COLOR_RED     = "\033[91m"
COLOR_BLUE    = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_WHITE   = "\033[97m"

def print_banner():
    banner = f"""
{COLOR_CYAN}{COLOR_BOLD}
   ▄████▄ ▓█████ ▄▄▄█████▓ ▒█████  ███▄    █  
  ▒██▀ ▀█ ▓█   ▀ ▓  ██▒ ▓▒▒██▒  ██▒██ ▀█   █  
  ▒▓█    ▄▒███   ▒ ▓██░ ▒░▒██░  ██▒██  ▀█ ██▒ 
  ▒▓▓▄ ▄██▒▓█  ▄ ░ ▓██▓ ░ ▒██   ██░██▒  ▐▌██▒ 
  ▒ ▓███▀ ░▒████▒  ▒██▒ ░ ░ ████▓▒░██░   ▓██░ 
  ░ ░▒ ▒  ░░ ▒░ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
{COLOR_RESET}{COLOR_MAGENTA}{COLOR_BOLD}
   ██████╗  █████╗ ██████╗ ██╗  ██╗
  ██╔═══██╗██╔══██╗██╔══██╗██║ ██╔╝
  ██║   ██║███████║██████╔╝█████═╝ 
  ██║   ██║██╔══██║██╔══██╗██  ██╗ 
  ╚██████╔╝██║  ██║██║  ██║██║ ██╗ 
   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
{COLOR_RESET}
{COLOR_YELLOW}{COLOR_BOLD}       ⚡ CYBER PARK - ALL-IN-ONE OSINT & RECON FRAMEWORK ⚡{COLOR_RESET}
{COLOR_CYAN}       [ Holehe | Maigret | PhoneInfoga | IP/Domain GeoIP | DNS Recon ]{COLOR_RESET}
{COLOR_MAGENTA}       ------------------------------------------------------------------{COLOR_RESET}
"""
    print(banner)

def log_info(msg):
    print(f"{COLOR_CYAN}[i]{COLOR_RESET} {msg}")

def log_status(msg):
    print(f"{COLOR_BLUE}[*]{COLOR_RESET} {msg}")

def log_success(msg):
    print(f"{COLOR_GREEN}[✓]{COLOR_RESET} {COLOR_BOLD}{msg}{COLOR_RESET}")

def log_warning(msg):
    print(f"{COLOR_YELLOW}[!]{COLOR_RESET} {msg}")

def log_error(msg):
    print(f"{COLOR_RED}[✗]{COLOR_RESET} {msg}")

def check_tool_installed(tool_name):
    """Check if binary tool is available on system PATH."""
    return shutil.which(tool_name) is not None

def verify_dependencies():
    """Check all required OSINT binaries."""
    tools = {
        "holehe": "Email registration checker (pipx install holehe)",
        "maigret": "Username search tool (pipx install maigret)",
        "phoneinfoga": "Phone OSINT scanner (Binary/Go)"
    }
    log_status("Checking Cyber Park tool dependencies...")
    all_ok = True
    for tool, desc in tools.items():
        if check_tool_installed(tool):
            log_success(f"{tool:<12} -> Installed & Ready")
        else:
            log_warning(f"{tool:<12} -> Not Found ({desc})")
            all_ok = False
            
    if not all_ok:
        log_warning("\nMissing external tools. To install on Kali Linux / Debian:")
        print(f"  {COLOR_YELLOW}sudo apt update && sudo apt install -y holehe maigret pipx{COLOR_RESET}")
        print(f"  {COLOR_YELLOW}curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash{COLOR_RESET}")
        print(f"  {COLOR_YELLOW}sudo mv ./phoneinfoga /usr/local/bin/{COLOR_RESET}\n")
    return all_ok

def execute_command(cmd, title, log_file=None):
    """Executes external tool command safely with output logging."""
    tool_binary = cmd[0]
    if not check_tool_installed(tool_binary):
        log_error(f"Cannot execute '{title}': '{tool_binary}' is not installed or not on PATH.")
        return False

    print(f"\n{COLOR_CYAN}{COLOR_BOLD}==================================================")
    print(f"▶ RUNNING: {title}")
    print(f"▶ COMMAND: {' '.join(cmd)}")
    print(f"=================================================={COLOR_RESET}\n")

    try:
        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- {title} [{datetime.datetime.now()}] ---\n")
                f.flush()
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                print(process.stdout)
                f.write(process.stdout)
        else:
            subprocess.run(cmd)
        log_success(f"Finished: {title}\n")
        return True
    except Exception as e:
        log_error(f"Error executing {title}: {e}")
        return False

# --- Built-in Native OSINT Modules (No External Dependencies Needed) ---

def scan_ip_domain_geoip(target, log_file=None):
    """Fetch Geolocation & Network info for IP or Domain."""
    log_status(f"Cyber Park GeoIP Lookup for: {COLOR_BOLD}{target}{COLOR_RESET}")
    
    try:
        # Resolve domain to IP if domain name is passed
        ip_addr = target
        try:
            ip_addr = socket.gethostbyname(target)
            log_info(f"Resolved {target} to IP: {COLOR_BOLD}{ip_addr}{COLOR_RESET}")
        except Exception:
            pass

        url = f"http://ip-api.com/json/{ip_addr}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        req = urllib.request.Request(url, headers={'User-Agent': 'CyberPark-OSINT/1.0'})
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            
        if data.get("status") == "success":
            print(f"\n{COLOR_GREEN}{COLOR_BOLD}=== GEOLOCATION & NETWORK RECON ==={COLOR_RESET}")
            res = (
                f"IP Address  : {data.get('query')}\n"
                f"Country     : {data.get('country')} ({data.get('countryCode')})\n"
                f"Region/City : {data.get('regionName')}, {data.get('city')}\n"
                f"Coordinates : Lat {data.get('lat')}, Lon {data.get('lon')}\n"
                f"ISP         : {data.get('isp')}\n"
                f"Organization: {data.get('org')}\n"
                f"ASN         : {data.get('as')}\n"
                f"Timezone    : {data.get('timezone')}"
            )
            print(f"{COLOR_CYAN}{res}{COLOR_RESET}\n")
            
            if log_file:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"\n--- GeoIP & Network Recon ---\n{res}\n")
            log_success("GeoIP & Network Recon Completed.")
        else:
            log_error(f"GeoIP Lookup Failed: {data.get('message', 'Unknown error')}")

    except Exception as e:
        log_error(f"GeoIP scan failed: {e}")

def scan_dns_records(domain, log_file=None):
    """Retrieve DNS Host Info for a domain."""
    log_status(f"Cyber Park DNS Recon for: {COLOR_BOLD}{domain}{COLOR_RESET}")
    records = []
    
    try:
        ip = socket.gethostbyname(domain)
        records.append(f"A Record (IPv4): {ip}")
    except Exception as e:
        records.append(f"A Record: Failed ({e})")

    try:
        host = socket.gethostbyaddr(domain)
        records.append(f"PTR / Hostname : {host[0]}")
    except Exception:
        pass

    print(f"\n{COLOR_GREEN}{COLOR_BOLD}=== DNS RECON RESULTS ==={COLOR_RESET}")
    for r in records:
        print(f" {COLOR_CYAN}[+] {r}{COLOR_RESET}")
    print()

    if log_file and records:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- DNS Recon ---\n" + "\n".join(records) + "\n")

# --- External Tool Workflows ---

def scan_email(target, log_file=None):
    """Scan Email target using Holehe & Maigret."""
    log_status(f"Cyber Park Email Recon for: {COLOR_BOLD}{target}{COLOR_RESET}")
    username = target.split("@")[0]
    
    execute_command(["holehe", target], f"Holehe Email Platform Check ({target})", log_file)
    execute_command(["maigret", username, "--site", "all"], f"Maigret Username Search ({username})", log_file)

# --- Phone OSINT Registered Location Databases ---
LK_LANDLINE_LOCATIONS = {
    "+9411": ("Colombo District", "Western Province", "Asia/Colombo"),
    "+9421": ("Jaffna District", "Northern Province", "Asia/Colombo"),
    "+9423": ("Mannar District", "Northern Province", "Asia/Colombo"),
    "+9424": ("Vavuniya District", "Northern Province", "Asia/Colombo"),
    "+9425": ("Anuradhapura District", "North Central Province", "Asia/Colombo"),
    "+9426": ("Trincomalee District", "Eastern Province", "Asia/Colombo"),
    "+9427": ("Polonnaruwa District", "North Central Province", "Asia/Colombo"),
    "+9431": ("Negombo / Gampaha District", "Western Province", "Asia/Colombo"),
    "+9432": ("Chilaw / Puttalam District", "North Western Province", "Asia/Colombo"),
    "+9433": ("Gampaha District", "Western Province", "Asia/Colombo"),
    "+9434": ("Kalutara District", "Western Province", "Asia/Colombo"),
    "+9435": ("Kegalle District", "Sabaragamuwa Province", "Asia/Colombo"),
    "+9436": ("Avissawella / Ratnapura District", "Sabaragamuwa/Western Province", "Asia/Colombo"),
    "+9437": ("Kurunegala District", "North Western Province", "Asia/Colombo"),
    "+9438": ("Panadura / Kalutara District", "Western Province", "Asia/Colombo"),
    "+9441": ("Matara District", "Southern Province", "Asia/Colombo"),
    "+9445": ("Ratnapura District", "Sabaragamuwa Province", "Asia/Colombo"),
    "+9447": ("Hambantota District", "Southern Province", "Asia/Colombo"),
    "+9451": ("Hatton / Nuwara Eliya District", "Central Province", "Asia/Colombo"),
    "+9452": ("Nuwara Eliya District", "Central Province", "Asia/Colombo"),
    "+9454": ("Nawalapitiya / Kandy District", "Central Province", "Asia/Colombo"),
    "+9455": ("Badulla District", "Uva Province", "Asia/Colombo"),
    "+9457": ("Bandarawela / Badulla District", "Uva Province", "Asia/Colombo"),
    "+9463": ("Ampara District", "Eastern Province", "Asia/Colombo"),
    "+9465": ("Batticaloa District", "Eastern Province", "Asia/Colombo"),
    "+9466": ("Matale District", "Central Province", "Asia/Colombo"),
    "+9467": ("Kalmunai / Ampara District", "Eastern Province", "Asia/Colombo"),
    "+9481": ("Kandy District", "Central Province", "Asia/Colombo"),
    "+9491": ("Galle District", "Southern Province", "Asia/Colombo")
}

GLOBAL_COUNTRY_LOCATIONS = {
    "+94": ("Sri Lanka 🇱🇰", "South Asia", "Colombo", "Asia/Colombo"),
    "+1": ("USA / Canada 🇺🇸 🇨🇦", "North America", "Washington D.C. / Ottawa", "America/New_York"),
    "+44": ("United Kingdom 🇬🇧", "Europe", "London", "Europe/London"),
    "+91": ("India 🇮🇳", "South Asia", "New Delhi", "Asia/Kolkata"),
    "+61": ("Australia 🇦🇺", "Oceania", "Canberra", "Australia/Sydney"),
    "+971": ("United Arab Emirates 🇦🇪", "Middle East", "Abu Dhabi / Dubai", "Asia/Dubai"),
    "+966": ("Saudi Arabia 🇸🇦", "Middle East", "Riyadh", "Asia/Riyadh"),
    "+974": ("Qatar 🇶🇦", "Middle East", "Doha", "Asia/Qatar"),
    "+965": ("Kuwait 🇰🇼", "Middle East", "Kuwait City", "Asia/Kuwait"),
    "+968": ("Oman 🇴🇲", "Middle East", "Muscat", "Asia/Muscat"),
    "+60": ("Malaysia 🇲🇾", "Southeast Asia", "Kuala Lumpur", "Asia/Kuala_Lumpur"),
    "+65": ("Singapore 🇸🇬", "Southeast Asia", "Singapore", "Asia/Singapore"),
    "+81": ("Japan 🇯🇵", "East Asia", "Tokyo", "Asia/Tokyo"),
    "+86": ("China 🇨🇳", "East Asia", "Beijing", "Asia/Shanghai"),
    "+49": ("Germany 🇩🇪", "Europe", "Berlin", "Europe/Berlin"),
    "+33": ("France 🇫🇷", "Europe", "Paris", "Europe/Paris"),
    "+39": ("Italy 🇮🇹", "Europe", "Rome", "Europe/Rome"),
    "+7": ("Russia / Kazakhstan", "Eurasia", "Moscow / Astana", "Europe/Moscow"),
    "+880": ("Bangladesh 🇧🇩", "South Asia", "Dhaka", "Asia/Dhaka"),
    "+92": ("Pakistan 🇵🇰", "South Asia", "Islamabad", "Asia/Karachi"),
    "+977": ("Nepal 🇳🇵", "South Asia", "Kathmandu", "Asia/Kathmandu"),
    "+960": ("Maldives 🇲🇻", "South Asia", "Malé", "Indian/Maldives")
}

def parse_phone_number_details(target):
    """Native OSINT Phone parser: auto-formats numbers & resolves country, region, district, carrier, line type."""
    clean = target.strip().replace(" ", "").replace("-", "")
    
    # Auto-format Sri Lankan local numbers (07XXXXXXXX or 0XXXXXXXX -> +94XXXXXXXXX)
    formatted = clean
    if clean.startswith("0") and len(clean) == 10:
        formatted = "+94" + clean[1:]
    elif not clean.startswith("+"):
        formatted = "+" + clean

    country = "Global / Unknown"
    region_location = "Unknown Region"
    capital_city = "N/A"
    timezone = "UTC"
    carrier = "Unknown Operator"
    line_type = "Unknown Line"

    # Match Global Country location first
    for cc, info in sorted(GLOBAL_COUNTRY_LOCATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        if formatted.startswith(cc):
            country = info[0]
            region_location = info[1]
            capital_city = info[2]
            timezone = info[3]
            break

    # If Sri Lanka (+94)
    if formatted.startswith("+94"):
        prefix5 = formatted[:5]
        
        # Mobile Operators
        if prefix5 in ["+9477", "+9476"]:
            carrier = "Dialog Axiata"
            line_type = "Mobile Network (GSM/LTE/5G)"
            region_location = "Nationwide Mobile (HQ: Colombo, Western Province)"
        elif prefix5 in ["+9471", "+9470"]:
            carrier = "SLT-Mobitel"
            line_type = "Mobile Network (GSM/LTE/5G)"
            region_location = "Nationwide Mobile (HQ: Colombo, Western Province)"
        elif prefix5 in ["+9475"]:
            carrier = "Airtel Sri Lanka"
            line_type = "Mobile Network (GSM/LTE/5G)"
            region_location = "Nationwide Mobile (HQ: Colombo, Western Province)"
        elif prefix5 in ["+9478", "+9472"]:
            carrier = "Hutchison Lanka"
            line_type = "Mobile Network (GSM/LTE/5G)"
            region_location = "Nationwide Mobile (HQ: Colombo, Western Province)"
        else:
            # Fixed Regional Landline Area Codes
            prefix4 = formatted[:5]
            if prefix4 in LK_LANDLINE_LOCATIONS:
                dist, prov, tz = LK_LANDLINE_LOCATIONS[prefix4]
                carrier = "SLT-Mobitel Landline / Fixed Wireless"
                line_type = "Fixed Landline (Regional Area)"
                region_location = f"{dist}, {prov}"
                timezone = tz
            else:
                line_type = "Fixed / Mobile Line"
                region_location = "Sri Lanka Registered Region"

    return {
        "formatted": formatted,
        "country": country,
        "region_location": region_location,
        "capital_city": capital_city,
        "carrier": carrier,
        "line_type": line_type,
        "timezone": timezone
    }

def scan_phone(target, log_file=None):
    """Scan Phone Number using Native Recon + PhoneInfoga & Maigret."""
    phone_data = parse_phone_number_details(target)
    formatted_number = phone_data["formatted"]
    
    log_status(f"Cyber Park Phone Recon for: {COLOR_BOLD}{formatted_number}{COLOR_RESET}")
    if formatted_number != target:
        log_info(f"Auto-formatted local number: {target} -> {COLOR_BOLD}{formatted_number}{COLOR_RESET}")
        
    print(f"\n{COLOR_GREEN}{COLOR_BOLD}=== PHONE NUMBER & REGISTERED LOCATION OSINT ==={COLOR_RESET}")
    res = (
        f"Input Target          : {target}\n"
        f"Formatted Number      : {formatted_number}\n"
        f"Registered Country    : {phone_data['country']}\n"
        f"Registered Location   : {phone_data['region_location']}\n"
        f"Primary City / Capital: {phone_data['capital_city']}\n"
        f"Network Operator      : {phone_data['carrier']}\n"
        f"Line Type             : {phone_data['line_type']}\n"
        f"Timezone              : {phone_data['timezone']}"
    )
    print(f"{COLOR_CYAN}{res}{COLOR_RESET}\n")

    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- Phone Number & Registered Location Recon ---\n{res}\n")

    # 1. PhoneInfoga scan with international format (+94...)
    execute_command(["phoneinfoga", "scan", "-n", formatted_number], f"PhoneInfoga OSINT Scan ({formatted_number})", log_file)
    
    # 2. Maigret scan for social links tied to number
    execute_command(["maigret", formatted_number], f"Maigret Phone/Username Search ({formatted_number})", log_file)

def scan_username(target, log_file=None):
    """Scan Username target using Maigret & Holehe."""
    log_status(f"Cyber Park Username Recon for: {COLOR_BOLD}{target}{COLOR_RESET}")
    
    execute_command(["maigret", target], f"Maigret Username Footprint Scan ({target})", log_file)
    execute_command(["holehe", target], f"Holehe Username Email Check ({target})", log_file)

def auto_detect_scan(target, log_file=None):
    """Automatically detect target type and route to appropriate scan module."""
    log_info(f"Target received: {COLOR_BOLD}{target}{COLOR_RESET}")
    
    clean_target = target.strip()
    clean_phone = clean_target.replace("+", "").replace("-", "").replace(" ", "")

    if "@" in clean_target:
        log_info("Target Classification: EMAIL ADDRESS ✉️")
        scan_email(clean_target, log_file)
    elif clean_target.startswith("+") or (clean_phone.isdigit() and len(clean_phone) >= 7):
        log_info("Target Classification: PHONE NUMBER 📞")
        scan_phone(clean_target, log_file)
    elif "." in clean_target and not clean_target.endswith("."):
        log_info("Target Classification: DOMAIN / IP ADDRESS 🌐")
        scan_ip_domain_geoip(clean_target, log_file)
        scan_dns_records(clean_target, log_file)
    else:
        log_info("Target Classification: USERNAME 👤")
        scan_username(clean_target, log_file)

def setup_report_file(target):
    """Creates a report log file path in reports/ directory."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    safe_name = "".join(c if c.isalnum() else "_" for c in target)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"cyberpark_recon_{safe_name}_{timestamp}.log"
    log_info(f"Report Log File: {COLOR_BOLD}{report_path}{COLOR_RESET}")
    return report_path

def interactive_menu():
    """Interactive Cyber Park CLI menu."""
    while True:
        print(f"\n{COLOR_CYAN}{COLOR_BOLD}==================================================")
        print(f" ⚡ CYBER PARK OSINT RECON MENU")
        print(f"=================================================={COLOR_RESET}")
        print("1. 🎯 Auto-Detect Target & Run Full Cyber Recon")
        print("2. ✉️ Email Recon (Holehe + Maigret)")
        print("3. 📞 Phone Number Recon (PhoneInfoga + Maigret)")
        print("4. 👤 Username Search (Maigret + Holehe)")
        print("5. 🌐 IP Address / Domain GeoIP & DNS Recon")
        print("6. 🔍 Check Installed Dependencies")
        print("7. 🚪 Exit")
        
        choice = input(f"\n{COLOR_YELLOW}Select Cyber Park Option (1-7): {COLOR_RESET}").strip()
        
        if choice == "1":
            target = input(f"{COLOR_CYAN}Enter Target (Email / Phone / Domain / Username): {COLOR_RESET}").strip()
            if target:
                log_file = setup_report_file(target)
                auto_detect_scan(target, log_file)
        elif choice == "2":
            target = input(f"{COLOR_CYAN}Enter Email address (e.g. target@gmail.com): {COLOR_RESET}").strip()
            if target:
                log_file = setup_report_file(target)
                scan_email(target, log_file)
        elif choice == "3":
            target = input(f"{COLOR_CYAN}Enter Phone number (e.g. +94771234567): {COLOR_RESET}").strip()
            if target:
                log_file = setup_report_file(target)
                scan_phone(target, log_file)
        elif choice == "4":
            target = input(f"{COLOR_CYAN}Enter Username (e.g. cyber_user): {COLOR_RESET}").strip()
            if target:
                log_file = setup_report_file(target)
                scan_username(target, log_file)
        elif choice == "5":
            target = input(f"{COLOR_CYAN}Enter IP address or Domain (e.g. 8.8.8.8 or example.com): {COLOR_RESET}").strip()
            if target:
                log_file = setup_report_file(target)
                scan_ip_domain_geoip(target, log_file)
                scan_dns_records(target, log_file)
        elif choice == "6":
            verify_dependencies()
        elif choice == "7":
            log_info("Exiting Cyber Park OSINT Suite. Happy Hunting!")
            break
        else:
            log_error("Invalid choice. Please select options 1 to 7.")

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
        log_file = setup_report_file(target)
        verify_dependencies()
        auto_detect_scan(target, log_file)
    else:
        verify_dependencies()
        interactive_menu()

if __name__ == "__main__":
    main()
