import os
import subprocess

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def remove_ngspice():
    print("Checking if ngspice is installed via apt...")
    apt_check = run_command("dpkg -l | grep ngspice")

    if "ngspice" in apt_check:
        print("Removing ngspice installed via apt...")
        run_command("sudo apt remove --purge -y ngspice libngspice-kicad")
        run_command("sudo apt autoremove -y")
    else:
        print("ngspice is not installed via apt.")

    print("Checking for manually installed ngspice in /usr/local/bin...")
    if os.path.exists("/usr/local/bin/ngspice"):
        print("Removing manually installed ngspice...")
        run_command("sudo rm -f /usr/local/bin/ngspice")
        run_command("sudo rm -rf /usr/local/lib/libngspice*")
        run_command("sudo rm -rf /usr/local/include/ngspice*")
        run_command("sudo rm -rf /usr/local/share/ngspice*")
        run_command("sudo rm -f /usr/local/share/man/man1/ngspice.1")

    print("Checking for user configuration files...")
    run_command("rm -rf ~/.ngspice")

    print("Verifying removal...")
    if not run_command("which ngspice").strip():
        print("✅ ngspice has been successfully removed.")
    else:
        print("⚠️ ngspice may still exist. Please check manually.")

def remove_kicad():
    print("Checking if KiCad is installed via apt...")
    apt_check = run_command("dpkg -l | grep kicad")

    if "kicad" in apt_check:
        print("Removing KiCad installed via apt...")
        run_command("sudo apt remove --purge -y kicad kicad-* libngspice-kicad")
        run_command("sudo apt autoremove -y")
    else:
        print("KiCad is not installed via apt.")

    print("Checking for manually installed KiCad in /usr/bin/kicad...")
    if os.path.exists("/usr/bin/kicad"):
        print("Removing manually installed KiCad...")
        run_command("sudo rm -f /usr/bin/kicad")
        run_command("sudo rm -rf /usr/share/kicad")
        run_command("sudo rm -rf /usr/lib/kicad")
        run_command("sudo rm -f /usr/share/man/man1/kicad.1")

    print("Checking for user configuration files...")
    run_command("rm -rf ~/.config/kicad")
    run_command("rm -rf ~/.local/share/kicad")

    print("Verifying removal...")
    if not run_command("which kicad").strip():
        print("✅ KiCad has been successfully removed.")
    else:
        print("⚠️ KiCad may still exist. Please check manually.")

def remove_ghdl():
    print("Checking for manually installed GHDL in /usr/local/bin...")
    if os.path.exists("/usr/local/bin/ghdl"):
        print("Removing GHDL...")
        run_command("sudo rm -f /usr/local/bin/ghdl")
        run_command("sudo rm -rf /usr/local/lib/ghdl")
        run_command("sudo rm -rf /usr/local/include/ghdl")
        run_command("sudo rm -rf /usr/local/share/ghdl")
        run_command("sudo rm -f /usr/local/share/man/man1/ghdl.1")

    print("Checking for user configuration files...")
    run_command("rm -rf ~/.ghdl")

    print("Verifying removal...")
    if not run_command("which ghdl").strip():
        print("✅ GHDL has been successfully removed.")
    else:
        print("⚠️ GHDL may still exist. Please check manually.")

if __name__ == "__main__":
    print("Choose a package to remove:")
    print("1. ngspice")
    print("2. KiCad")
    print("3. GHDL")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        remove_ngspice()
    elif choice == "2":
        remove_kicad()
    elif choice == "3":
        remove_ghdl()
    else:
        print("Invalid input. Exiting.")
