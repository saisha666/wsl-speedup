#!/bin/bash

echo "🔍 Finding the fastest Ubuntu mirror..."
FASTEST_MIRROR=$(curl -s "https://launchpad.net/ubuntu/+archivemirrors" | grep -Eo 'http[s]?://[a-zA-Z0-9./?=_-]+' | head -n 1)

if [[ -z "$FASTEST_MIRROR" ]]; then
    echo "❌ No fast mirror found. Using default."
    FASTEST_MIRROR="http://archive.ubuntu.com/ubuntu/"
else
    echo "🚀 Fastest Mirror Found: $FASTEST_MIRROR"
fi

echo "✅ Updating sources.list..."
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
sudo sed -i "s|http://archive.ubuntu.com/ubuntu/|$FASTEST_MIRROR|g" /etc/apt/sources.list
sudo sed -i "s|http://security.ubuntu.com/ubuntu/|$FASTEST_MIRROR|g" /etc/apt/sources.list

echo "🚀 Running package updates..."
sudo apt update -y && sudo apt upgrade -y

echo "🚀 Installing essential tools..."
sudo apt install -y apt-fast aria2 speedtest-cli ca-certificates
sudo update-ca-certificates

echo "📅 Testing aria2 download..."
aria2c -x 16 -s 16 "https://speed.hetzner.de/100MB.bin"

echo "🚀 Running speedtest..."
speedtest

echo "🎉 Optimization Complete! Use 'apt-fast' for faster APT downloads and 'aria2c' for multi-threaded downloads."
