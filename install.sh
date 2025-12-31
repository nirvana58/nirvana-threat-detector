#!/bin/bash
# Network Threat Detector - Client Installation Script
# Usage: curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main/install.sh | bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_URL="https://raw.githubusercontent.com/YOUR-USERNAME/ntd-client/main"

echo -e "${CYAN}"
echo "  ███████████████"
echo "███████████████████"
echo "████  👁️  ████"
echo "███████████████████"
echo "  ███████████████"
echo -e "${NC}"
echo -e "${CYAN}Network Threat Detector - Client${NC}"
echo -e "${CYAN}Installation Script${NC}"
echo ""

# Check Python
echo -e "${BLUE}Checking prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3.9 or higher"
    echo ""
    echo "Install Python:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Windows: Download from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# Determine installation directory
if [ "$EUID" -eq 0 ]; then
    INSTALL_DIR="/usr/local/bin"
    echo -e "${GREEN}✓ Installing system-wide to $INSTALL_DIR${NC}"
else
    INSTALL_DIR="$HOME/bin"
    mkdir -p "$INSTALL_DIR"
    echo -e "${YELLOW}⚠ Installing to user directory: $INSTALL_DIR${NC}"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo -e "${YELLOW}⚠ Adding $INSTALL_DIR to PATH${NC}"
        
        # Detect shell
        if [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        else
            SHELL_RC="$HOME/.profile"
        fi
        
        echo "export PATH=\"\$HOME/bin:\$PATH\"" >> "$SHELL_RC"
        export PATH="$HOME/bin:$PATH"
        echo -e "${GREEN}✓ Added to $SHELL_RC${NC}"
    fi
fi

echo ""

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install --user --quiet requests pandas 2>&1 | grep -v "Requirement already satisfied" || true
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""

# Download client
echo -e "${BLUE}Downloading Network Threat Detector client...${NC}"

if command -v curl &> /dev/null; then
    curl -fsSL "$REPO_URL/ntd-client.py" -o "$INSTALL_DIR/ntd-client"
elif command -v wget &> /dev/null; then
    wget -q "$REPO_URL/ntd-client.py" -O "$INSTALL_DIR/ntd-client"
else
    echo -e "${RED}✗ Neither curl nor wget found${NC}"
    echo "Please install curl or wget"
    exit 1
fi

chmod +x "$INSTALL_DIR/ntd-client"

if [ -f "$INSTALL_DIR/ntd-client" ]; then
    echo -e "${GREEN}✓ Client installed to $INSTALL_DIR/ntd-client${NC}"
else
    echo -e "${RED}✗ Installation failed${NC}"
    exit 1
fi

echo ""

# Configure
echo -e "${CYAN}════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}Configuration${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════${NC}"
echo ""
echo "To use the client, you need:"
echo "  1. API URL (from your admin)"
echo "  2. API Key (from your admin)"
echo ""
read -p "Configure now? (y/n): " configure_now

if [ "$configure_now" = "y" ] || [ "$configure_now" = "Y" ]; then
    echo ""
    python3 "$INSTALL_DIR/ntd-client" --configure
else
    echo ""
    echo -e "${YELLOW}You can configure later by running:${NC}"
    echo -e "${CYAN}  ntd-client --configure${NC}"
fi

echo ""

# Success
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Installation Complete! 🎉                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}Quick Start:${NC}"
echo ""
echo "1. Launch interactive mode:"
echo -e "   ${WHITE}ntd-client${NC}"
echo ""
echo "2. Test connection:"
echo -e "   ${WHITE}ntd-client check${NC}"
echo ""
echo "3. Analyze network traffic:"
echo -e "   ${WHITE}ntd-client analyze traffic.csv${NC}"
echo ""
echo "4. Get help:"
echo -e "   ${WHITE}ntd-client --help${NC}"
echo ""

if [ "$EUID" -ne 0 ] && [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}⚠ Important: Restart your terminal or run:${NC}"
    echo -e "   ${CYAN}source $SHELL_RC${NC}"
    echo ""
fi

echo -e "${CYAN}Documentation:${NC}"
echo "  https://github.com/YOUR-USERNAME/ntd-client"
echo ""
echo -e "${GREEN}Happy threat hunting! 🛡️${NC}"
echo ""
