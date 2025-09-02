#!/bin/bash

# HackerOne Link Scraper Installation Script

echo "Installing HackerOne Link Scraper dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if Chrome is installed
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo "Warning: Chrome or Chromium browser not found."
    echo "The script requires Chrome/Chromium to be installed."
    
    # Ask if user wants to install Chrome
    read -p "Do you want to install Chrome/Chromium? (y/n): " install_chrome
    
    if [[ $install_chrome == "y" || $install_chrome == "Y" ]]; then
        # Detect OS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt-get &> /dev/null; then
                # Debian/Ubuntu
                echo "Installing Chromium on Debian/Ubuntu..."
                sudo apt-get update
                sudo apt-get install -y chromium-browser
            elif command -v dnf &> /dev/null; then
                # Fedora
                echo "Installing Chromium on Fedora..."
                sudo dnf install -y chromium
            elif command -v yum &> /dev/null; then
                # CentOS/RHEL
                echo "Installing Chromium on CentOS/RHEL..."
                sudo yum install -y chromium
            else
                echo "Could not detect package manager. Please install Chrome/Chromium manually."
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                echo "Installing Chrome on macOS using Homebrew..."
                brew install --cask google-chrome
            else
                echo "Homebrew not found. Please install Chrome manually."
            fi
        else
            echo "Unsupported OS. Please install Chrome/Chromium manually."
        fi
    else
        echo "Skipping Chrome installation. Please install Chrome/Chromium manually."
    fi
fi

# Create output directory
mkdir -p output

# Make main script executable
chmod +x main.py

echo "Installation completed!"
echo "You can now run the scraper using: ./main.py"