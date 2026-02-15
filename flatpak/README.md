# eSim Flatpak

This directory contains the Flatpak manifest for building eSim as a distribution-agnostic package. The Flatpak build works on **all major Linux distributions** including Fedora, Ubuntu, Debian, openSUSE, Arch Linux, and others.

## Prerequisites

- Flatpak and flatpak-builder installed
- Flathub repository added

```bash
# On Fedora
sudo dnf install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

## Building

From the eSim project root:

```bash
flatpak-builder build flatpak/org.fossee.eSim.yml --install --user
```

Or from the flatpak directory:

```bash
flatpak-builder build org.fossee.eSim.yml --install --user
```

## Running

```bash
flatpak run org.fossee.eSim
```

## KiCad Integration

For schematic editing, install KiCad from Flathub (eSim will automatically use it when running as Flatpak):

```bash
flatpak install flathub org.kicad.KiCad
```

## Limitations

The Flatpak build focuses on core eSim functionality (schematic design with KiCad, circuit simulation with ngspice). The following are **not** included:

| Feature | Status |
|---------|--------|
| NGHDL | Not included – use Ubuntu installer for Verilog/Modelica workflows |
| Makerchip | Not included |
| SKY130 PDK | Not bundled – use Ubuntu installer for mixed-signal with SKY130 |
| xterm / gaw | Not included – external waveform viewer may need xterm on host |
| NGHDL KiCad symbol creation | Limited – sandbox restricts writing to KiCad symbol directories |

For full feature parity, use the Ubuntu native installer.

## Publishing to Flathub

To publish this package to Flathub for easy installation across all distributions:

1. Fork the [Flathub repository](https://github.com/flathub/flathub)
2. Add the eSim manifest to `flathub` repo
3. Submit a pull request per [Flathub's contribution guidelines](https://github.com/flathub/flathub/wiki/App-Requirements)
