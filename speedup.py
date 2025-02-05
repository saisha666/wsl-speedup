import os
import subprocess
import re
import urllib.request
import urllib.error
import shutil

# Function to find the fastest Ubuntu mirror
def find_fastest_mirror():
    print("🔍 Finding the fastest Ubuntu mirror...")
    mirror_list_url = "https://launchpad.net/ubuntu/+archivemirrors"

    try:
        response = urllib.request.urlopen(mirror_list_url, timeout=10)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e}. Using default mirror.")
        return "http://archive.ubuntu.com/ubuntu/"
    except Exception as e:
        print(f"❌ Unexpected error: {e}. Using default mirror.")
        return "http://archive.ubuntu.com/ubuntu/"

    mirrors = set(re.findall(r'https?://[a-zA-Z0-9./?=_-]+', html))

    fastest_mirror = None
    fastest_time = float('inf')

    for mirror in mirrors:
        try:
            cmd = ["curl", "-o", "/dev/null", "-s", "-w", "%{time_total}\n", f"{mirror}/ubuntu/"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print(f"⚠️ Curl failed for {mirror}. Skipping...")
                continue
            time_taken = float(result.stdout.strip())
            if time_taken < fastest_time:
                fastest_time = time_taken
                fastest_mirror = mirror
        except Exception as e:
            print(f"⚠️ Error checking mirror {mirror}: {e}")
            continue

    if fastest_mirror:
        print(f"🚀 Fastest Mirror Found: {fastest_mirror}")
    else:
        print("❌ Failed to find a valid fastest mirror. Using default.")
        fastest_mirror = "http://archive.ubuntu.com/ubuntu/"

    return fastest_mirror

# Function to update sources list
def update_sources_list(fastest_mirror):
    print("✅ Updating sources.list with the fastest mirror...")
    if not os.path.exists("/etc/apt/sources.list.backup"):
        os.system("sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup")

    os.system(f"sudo sed -i 's|http://archive.ubuntu.com/ubuntu/|{fastest_mirror}|g' /etc/apt/sources.list")
    os.system(f"sudo sed -i 's|http://security.ubuntu.com/ubuntu/|{fastest_mirror}|g' /etc/apt/sources.list")

    result = subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Package update failed. Error: {result.stderr}")

# Function to install necessary tools
def install_tools():
    print("🚀 Installing essential tools...")
    os.system("sudo apt install -y apt-fast aria2 speedtest-cli ca-certificates")
    os.system("sudo update-ca-certificates")

# Function to test aria2 download
def test_aria2():
    test_url = "https://speed.hetzner.de/100MB.bin"
    print(f"📅 Testing aria2 download from {test_url}")
    result = subprocess.run(["aria2c", "-x", "16", "-s", "16", test_url], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ aria2c download test failed. Error: {result.stderr}")

# Function to run speedtest
def run_speedtest():
    print("🚀 Running speedtest...")
    result = os.system("speedtest")
    if result != 0:
        print("❌ Speedtest failed. Please check your network connection and try again.")

if __name__ == "__main__":
    fastest_mirror = find_fastest_mirror()
    update_sources_list(fastest_mirror)
    install_tools()
    test_aria2()
    run_speedtest()
    print("🎉 Optimization Complete! Use 'apt-fast' for faster APT downloads and 'aria2c' for multi-threaded downloads.")
