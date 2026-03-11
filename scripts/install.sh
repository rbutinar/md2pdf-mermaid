#!/bin/bash
# md2pdf standalone installer for macOS and Linux
# Usage: curl -fsSL https://raw.githubusercontent.com/rbutinar/md2pdf-mermaid/master/scripts/install.sh | bash

set -e

REPO="rbutinar/md2pdf-mermaid"
INSTALL_DIR="/usr/local/bin"
BINARY="md2pdf"

# Detect platform
OS="$(uname -s)"
ARCH="$(uname -m)"

case "${OS}" in
    Darwin)
        case "${ARCH}" in
            arm64) ARTIFACT="md2pdf-macos-arm64" ;;
            x86_64) ARTIFACT="md2pdf-macos-x86_64" ;;
            *) echo "Error: Unsupported architecture: ${ARCH}"; exit 1 ;;
        esac
        ;;
    Linux)
        case "${ARCH}" in
            x86_64) ARTIFACT="md2pdf-linux-x86_64" ;;
            *) echo "Error: Unsupported architecture: ${ARCH}"; exit 1 ;;
        esac
        ;;
    *)
        echo "Error: Unsupported OS: ${OS}"
        echo "For Windows, download manually from:"
        echo "  https://github.com/${REPO}/releases/latest"
        exit 1
        ;;
esac

DOWNLOAD_URL="https://github.com/${REPO}/releases/latest/download/${ARTIFACT}.tar.gz"

echo "Installing md2pdf..."
echo "  Platform: ${OS} ${ARCH}"
echo "  Downloading: ${ARTIFACT}.tar.gz"
echo ""

# Download and extract to temp dir
TMPDIR_INSTALL="$(mktemp -d)"
trap 'rm -rf "${TMPDIR_INSTALL}"' EXIT

curl -fSL --progress-bar -o "${TMPDIR_INSTALL}/md2pdf.tar.gz" "${DOWNLOAD_URL}"
tar xzf "${TMPDIR_INSTALL}/md2pdf.tar.gz" -C "${TMPDIR_INSTALL}" 2>/dev/null || true

chmod +x "${TMPDIR_INSTALL}/${BINARY}"

# Remove quarantine on macOS
if [ "${OS}" = "Darwin" ]; then
    xattr -d com.apple.quarantine "${TMPDIR_INSTALL}/${BINARY}" 2>/dev/null || true
fi

# Install to PATH
if [ -w "${INSTALL_DIR}" ]; then
    mv "${TMPDIR_INSTALL}/${BINARY}" "${INSTALL_DIR}/${BINARY}"
else
    echo "Installing to ${INSTALL_DIR} (requires sudo)..."
    sudo mv "${TMPDIR_INSTALL}/${BINARY}" "${INSTALL_DIR}/${BINARY}"
fi

# Verify
VERSION="$("${INSTALL_DIR}/${BINARY}" --version 2>/dev/null || true)"
if [ -n "${VERSION}" ]; then
    echo ""
    echo "Installed successfully: ${VERSION}"
    echo "  Location: ${INSTALL_DIR}/${BINARY}"
    echo ""
    echo "Usage: md2pdf document.md"
else
    echo ""
    echo "Warning: Installation completed but version check failed."
    echo "  Try running: ${INSTALL_DIR}/${BINARY} --version"
fi
