#!/usr/bin/env bash
set -euo pipefail

PACKAGE_NAME="esim"
VERSION="${1:-1.0.0}"
ARCH="${2:-amd64}"
SOURCE_DIR="${3:-}"

if [[ -z "${SOURCE_DIR}" ]]; then
  echo "Usage: $0 <version> <arch> <source-dir>" >&2
  echo "Example: $0 1.0.0 amd64 /path/to/esim/app" >&2
  exit 1
fi

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Source directory not found: ${SOURCE_DIR}" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE_DIR="${ROOT_DIR}/build/${PACKAGE_NAME}_${VERSION}_${ARCH}"

rm -rf "${STAGE_DIR}"
mkdir -p "${STAGE_DIR}/DEBIAN"
mkdir -p "${STAGE_DIR}/opt/esim"
mkdir -p "${STAGE_DIR}/usr/bin"
mkdir -p "${STAGE_DIR}/usr/share/applications"
mkdir -p "${STAGE_DIR}/usr/share/doc/${PACKAGE_NAME}"

# Copy application payload
cp -a "${SOURCE_DIR}/." "${STAGE_DIR}/opt/esim/"

# Install helper launcher and desktop entry from this repository
install -m 0755 "${ROOT_DIR}/usr/bin/esim" "${STAGE_DIR}/usr/bin/esim"
install -m 0644 "${ROOT_DIR}/usr/share/applications/esim.desktop" "${STAGE_DIR}/usr/share/applications/esim.desktop"

# Copy Debian metadata
install -m 0644 "${ROOT_DIR}/DEBIAN/control" "${STAGE_DIR}/DEBIAN/control"
install -m 0755 "${ROOT_DIR}/DEBIAN/postinst" "${STAGE_DIR}/DEBIAN/postinst"
install -m 0755 "${ROOT_DIR}/DEBIAN/prerm" "${STAGE_DIR}/DEBIAN/prerm"

# Best-effort docs
if [[ -f "${ROOT_DIR}/README.md" ]]; then
  install -m 0644 "${ROOT_DIR}/README.md" "${STAGE_DIR}/usr/share/doc/${PACKAGE_NAME}/README.md"
fi

# If there is an executable called esim or start.sh, keep it executable
chmod 0755 "${STAGE_DIR}/opt/esim"/* 2>/dev/null || true

dpkg-deb --build "${STAGE_DIR}"
mv "${STAGE_DIR}.deb" "${ROOT_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo "Created ${ROOT_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
