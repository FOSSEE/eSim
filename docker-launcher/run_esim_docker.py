"""
eSim Docker Launcher
FOSSEE IIT Bombay Internship Project

Simple launcher to run eSim in Docker with VNC or X11 display.
"""

import os
import sys
import platform
import subprocess
import shutil
import socket
import webbrowser
import time
import tempfile
import urllib.request
from pathlib import Path

# Docker image (GitHub Container Registry)
DOCKER_IMAGE = "ghcr.io/barun-2005/esim-docker:latest"
LOCAL_IMAGE = "esim:latest"
CONTAINER_NAME = "esim-container"
DOCKERFILE_DIR = Path(__file__).parent.resolve()
WORKSPACE_DIR_NAME = "eSim_Workspace"

# VcXsrv config for Windows X11 mode
VCXSRV_CONFIG = """<?xml version="1.0" encoding="UTF-8"?>
<XLaunch WindowMode="MultiWindow" ClientMode="NoClient" LocalClient="False" Display="-1" LocalProgram="xcalc" RemoteProgram="xterm" RemotePassword="" PrivateKey="" RemoteHost="" RemoteUser="" XDMCPHost="" XDMCPBroadcast="False" XDMCPIndirect="False" Clipboard="True" ClipboardPrimary="True" ExtraParams="" Wgl="True" DisableAC="True" XDMCPTerminate="False"/>
"""


def run_cmd(cmd, capture=False, check=True, shell=False):
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True, check=check, shell=shell)
    return subprocess.run(cmd, check=check, shell=shell)


def cmd_exists(cmd):
    return shutil.which(cmd) is not None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    clear()
    print("""
    ╔══════════════════════════════════════════╗
    ║          eSim Docker Launcher            ║
    ║        FOSSEE, IIT Bombay                ║
    ╚══════════════════════════════════════════╝
    """)


def info(msg):
    print(f"  [i] {msg}")

def ok(msg):
    print(f"  [+] {msg}")

def warn(msg):
    print(f"  [!] {msg}")

def err(msg):
    print(f"  [-] {msg}", file=sys.stderr)


def find_free_port(start=6080, tries=20):
    for port in range(start, start + tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No free port found between {start}-{start+tries}")


def wait_for_port(port, timeout=30):
    """Wait until noVNC HTTP server is responding."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.urlopen(f"http://localhost:{port}/", timeout=2)
            req.close()
            return True
        except:
            time.sleep(1)
    return False


def get_os():
    system = platform.system().lower()
    if system == "linux":
        try:
            with open("/proc/version") as f:
                if "microsoft" in f.read().lower():
                    return "wsl2"
        except:
            pass
        return "linux"
    if system == "windows":
        return "windows"
    if system == "darwin":
        return "macos"
    return system


def is_wslg():
    return (get_os() == "wsl2" and 
            os.environ.get("WAYLAND_DISPLAY") and 
            Path("/mnt/wslg").exists())


# Docker installation helpers

def open_url(url):
    """Open URL in browser."""
    try:
        webbrowser.open(url)
        return True
    except:
        return False


def install_docker_windows():
    """Check Docker on Windows - try to start it, or install if needed."""
    # First check if Docker Desktop is installed but not running
    docker_paths = [
        Path(os.environ.get("PROGRAMFILES", "")) / "Docker" / "Docker" / "Docker Desktop.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Docker" / "Docker Desktop.exe",
    ]
    
    docker_exe = None
    for p in docker_paths:
        if p.exists():
            docker_exe = p
            break
    
    if docker_exe:
        info("Docker Desktop is installed but not running.")
        resp = input("  Start Docker Desktop now? (y/n): ").strip().lower()
        if resp == 'y':
            try:
                info("Starting Docker Desktop...")
                subprocess.Popen([str(docker_exe)], creationflags=subprocess.DETACHED_PROCESS)
                info("Docker Desktop is starting. Please wait 30-60 seconds...")
                info("Then run this launcher again.")
                input("\n  Press Enter to exit...")
                return True
            except Exception as e:
                err(f"Failed to start: {e}")
        return False
    
    # Docker not installed - offer to install
    info("Docker Desktop is not installed.")
    print()
    print("  Docker Desktop is required to run eSim.")
    print()
    resp = input("  Install Docker Desktop now? (y/n): ").strip().lower()
    if resp != 'y':
        print()
        info("You can install Docker manually from:")
        info("https://www.docker.com/products/docker-desktop")
        return False
    
    if not cmd_exists("winget"):
        info("Opening Docker download page...")
        open_url("https://www.docker.com/products/docker-desktop")
        info("Please install Docker Desktop and restart this launcher.")
        return False
    
    try:
        info("Installing Docker Desktop (this takes a few minutes)...")
        subprocess.run(["winget", "install", "-e", "--id", "Docker.DockerDesktop", 
                       "--accept-source-agreements"], check=True)
        print()
        ok("Docker Desktop installed!")
        warn("Please RESTART your computer, then run this launcher again.")
        input("\n  Press Enter to exit...")
        return True
    except Exception as e:
        err(f"Install failed: {e}")
        info("Opening Docker download page...")
        open_url("https://www.docker.com/products/docker-desktop")
        return False


def guide_docker_linux():
    """Guide user to install Docker on Linux."""
    info("Docker is not running or not installed.")
    print()
    print("  To install Docker on Linux, run these commands:")
    print()
    print("    curl -fsSL https://get.docker.com | sudo sh")
    print("    sudo usermod -aG docker $USER")
    print("    # Then log out and log back in")
    print()
    print("  After installation, start Docker:")
    print("    sudo systemctl start docker")
    print()
    resp = input("  Open Docker installation guide? (y/n): ").strip().lower()
    if resp == 'y':
        open_url("https://docs.docker.com/engine/install/")


def guide_docker_macos():
    """Guide user to install Docker on macOS."""
    info("Docker Desktop is not running or not installed.")
    print()
    print("  Docker Desktop is required to run eSim.")
    print()
    resp = input("  Open Docker download page? (y/n): ").strip().lower()
    if resp == 'y':
        open_url("https://www.docker.com/products/docker-desktop")
    print()
    info("After installing, open Docker Desktop and wait for it to start.")


def install_vcxsrv_windows():
    """Install VcXsrv on Windows."""
    info("VcXsrv is needed for native window mode on Windows.")
    resp = input("  Install VcXsrv now? (y/n): ").strip().lower()
    if resp != 'y':
        return False
    
    if not cmd_exists("winget"):
        info("Opening VcXsrv download page...")
        open_url("https://sourceforge.net/projects/vcxsrv/")
        return False
    
    try:
        info("Installing VcXsrv...")
        subprocess.run(["winget", "install", "-e", "--id", "marha.VcXsrv",
                       "--accept-source-agreements"], check=True)
        ok("VcXsrv installed!")
        return True
    except:
        err("Install failed")
        open_url("https://sourceforge.net/projects/vcxsrv/")
        return False


def start_vcxsrv():
    """Start VcXsrv X server on Windows."""
    paths = [
        Path(os.environ.get("PROGRAMFILES", "")) / "VcXsrv" / "vcxsrv.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "VcXsrv" / "vcxsrv.exe",
    ]
    
    vcxsrv = None
    for p in paths:
        if p.exists():
            vcxsrv = p
            break
    
    if not vcxsrv:
        if not install_vcxsrv_windows():
            return False
        for p in paths:
            if p.exists():
                vcxsrv = p
                break
        if not vcxsrv:
            err("VcXsrv not found")
            return False
    
    # Check if already running
    try:
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq vcxsrv.exe"], 
                               capture_output=True, text=True)
        if "vcxsrv.exe" in result.stdout.lower():
            ok("VcXsrv already running")
            return True
    except:
        pass
    
    # Write config and launch
    config = Path(tempfile.gettempdir()) / "esim_xserver.xlaunch"
    config.write_text(VCXSRV_CONFIG)
    
    info("Starting VcXsrv...")
    try:
        xlaunch = vcxsrv.parent / "xlaunch.exe"
        if xlaunch.exists():
            subprocess.Popen([str(xlaunch), "-run", str(config)],
                           creationflags=subprocess.DETACHED_PROCESS)
        else:
            subprocess.Popen([str(vcxsrv), ":0", "-multiwindow", "-clipboard", "-wgl", "-ac"],
                           creationflags=subprocess.DETACHED_PROCESS)
        time.sleep(2)
        ok("VcXsrv started")
        return True
    except Exception as e:
        err(f"Failed: {e}")
        return False


def get_display_args(os_type):
    """Get Docker display environment for X11 mode."""
    if os_type == "linux":
        display = os.environ.get("DISPLAY", ":0")
        try:
            subprocess.run(["xhost", "+local:docker"], capture_output=True)
        except:
            pass
        return display, ["-e", f"DISPLAY={display}", "-v", "/tmp/.X11-unix:/tmp/.X11-unix:rw"]
    
    if os_type == "wsl2":
        if is_wslg():
            display = os.environ.get("DISPLAY", ":0")
            return display, ["-e", f"DISPLAY={display}", "-e", "QT_QPA_PLATFORM=xcb",
                           "-v", "/tmp/.X11-unix:/tmp/.X11-unix:rw"]
        try:
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        host_ip = line.split()[1]
                        break
                else:
                    host_ip = "localhost"
        except:
            host_ip = "localhost"
        return f"{host_ip}:0.0", ["-e", f"DISPLAY={host_ip}:0.0", "-e", "LIBGL_ALWAYS_INDIRECT=1"]
    
    if os_type == "windows":
        return "host.docker.internal:0.0", [
            "-e", "DISPLAY=host.docker.internal:0.0",
            "-e", "QT_X11_NO_MITSHM=1", "-e", "NO_AT_BRIDGE=1", "-e", "GTK_A11Y=none"
        ]
    
    if os_type == "macos":
        return "host.docker.internal:0", [
            "-e", "DISPLAY=host.docker.internal:0", "-e", "LIBGL_ALWAYS_INDIRECT=1"
        ]
    
    return ":0", ["-e", "DISPLAY=:0"]


# Docker operations

def docker_ok():
    if not cmd_exists("docker"):
        return False
    try:
        run_cmd(["docker", "info"], capture=True)
        return True
    except:
        return False


def image_exists(image):
    try:
        result = run_cmd(["docker", "images", "-q", image], capture=True)
        return bool(result.stdout.strip())
    except:
        return False


def pull_image(image=DOCKER_IMAGE):
    info(f"Pulling {image}...")
    info("This may take a few minutes on first run...")
    print()
    try:
        subprocess.run(["docker", "pull", image], check=True)
        print()
        ok("Image downloaded!")
        return True
    except:
        err("Pull failed")
        return False


def build_image():
    dockerfile = DOCKERFILE_DIR / "Dockerfile"
    if not dockerfile.exists():
        err(f"Dockerfile not found: {dockerfile}")
        return False
    
    info("Building from Dockerfile (10-15 min)...")
    print()
    try:
        subprocess.run(["docker", "build", "-t", LOCAL_IMAGE, str(DOCKERFILE_DIR)], check=True)
        print()
        ok("Build complete!")
        return True
    except:
        err("Build failed")
        return False


def stop_container():
    run_cmd(["docker", "rm", "-f", CONTAINER_NAME], capture=True, check=False)


def get_workspace():
    ws = Path.home() / WORKSPACE_DIR_NAME
    ws.mkdir(exist_ok=True)
    return ws


def get_image(build_local=False):
    if build_local:
        return LOCAL_IMAGE if build_image() else None
    
    if image_exists(DOCKER_IMAGE):
        return DOCKER_IMAGE
    
    print()
    if pull_image(DOCKER_IMAGE):
        return DOCKER_IMAGE
    
    if image_exists(LOCAL_IMAGE):
        warn(f"Using local image: {LOCAL_IMAGE}")
        return LOCAL_IMAGE
    
    warn("Remote unavailable, trying local build...")
    return LOCAL_IMAGE if build_image() else None


# Launch modes

def launch_vnc(image, workspace):
    """Run eSim in VNC mode (browser)."""
    stop_container()
    
    try:
        vnc_port = find_free_port(6080)
        server_port = find_free_port(5901)
    except RuntimeError as e:
        err(str(e))
        return 1
    
    cmd = [
        "docker", "run", "--rm", "-it", "--name", CONTAINER_NAME,
        "--shm-size=256m", "--ipc=host",
        "-v", f"{workspace}:/home/esim-user/eSim-Workspace:rw",
        "-p", f"{vnc_port}:6080", "-p", f"{server_port}:5901",
        "-e", "USE_VNC=1", image, "--vnc"
    ]
    
    url = f"http://localhost:{vnc_port}/vnc.html"
    
    print()
    print("  " + "=" * 50)
    ok("Starting VNC Mode...")
    print()
    print(f"     Browser URL: {url}")
    print(f"     VNC Server:  localhost:{server_port}")
    print()
    print("     Waiting for container to start...")
    print("  " + "=" * 50)
    print()
    
    # Start container in background thread and wait for port
    import threading
    container_started = threading.Event()
    
    def run_container():
        subprocess.run(cmd)
        container_started.set()
    
    thread = threading.Thread(target=run_container, daemon=True)
    thread.start()
    
    # Wait for VNC port to be ready, then open browser
    info("Waiting for eSim to start...")
    if wait_for_port(vnc_port, timeout=45):
        time.sleep(5)  # Wait for noVNC and eSim to fully initialize
        ok("Opening browser...")
        webbrowser.open(url)
    else:
        warn("Container is starting slowly. Please open manually:")
        print(f"     {url}")
    
    # Wait for container to finish
    thread.join()
    return 0


def launch_x11(image, workspace, os_type):
    """Run eSim in X11 mode (native window)."""
    if os_type == "windows":
        if not start_vcxsrv():
            err("X11 server not available. Try VNC mode instead.")
            return 1
    
    if os_type == "macos":
        info("Make sure XQuartz is running (download from xquartz.org)")
        info("Run 'xhost +localhost' in terminal if needed")
        print()
    
    display, display_args = get_display_args(os_type)
    stop_container()
    
    cmd = [
        "docker", "run", "--rm", "-it", "--name", CONTAINER_NAME,
        "--shm-size=256m", "--ipc=host",
        "-v", f"{workspace}:/home/esim-user/eSim-Workspace:rw",
    ] + display_args + [image]
    
    print()
    print("  " + "=" * 50)
    ok("Starting X11 Mode")
    print(f"     Display: {display}")
    if os_type in ["windows", "macos"]:
        print("     Note: KiCad schematic editor may lag slightly")
    print("  " + "=" * 50)
    print()
    
    return subprocess.run(cmd).returncode


# Menu system

def show_menu(os_type):
    """Display interactive menu based on OS."""
    show_banner()
    print(f"  OS: {os_type.upper()}")
    print()
    
    if os_type == "linux":
        # Linux: X11 first (recommended)
        print("  1. Launch X11 Mode (Recommended)")
        print("  2. Launch VNC Mode (Browser)")
    else:
        # Windows/Mac: VNC first (recommended)
        print("  1. Launch VNC Mode (Recommended - Browser)")
        print("  2. Launch X11 Mode (Native Window)")
        if os_type == "windows":
            print("     [KiCad may lag, auto-installs VcXsrv if needed]")
        elif os_type == "macos":
            print("     [Requires XQuartz, KiCad may lag]")
    
    print("  3. Update Image")
    print("  4. Build from Source")
    print("  0. Exit")
    print()
    return input("  Choice: ").strip()


def handle_docker_missing(os_type):
    """Handle case when Docker is not available."""
    if os_type == "windows":
        install_docker_windows()
    elif os_type == "linux":
        guide_docker_linux()
    elif os_type == "macos":
        guide_docker_macos()
    else:
        err("Docker is required. Please install Docker Desktop.")
    input("\n  Press Enter to continue...")


def run_menu():
    """Interactive menu loop."""
    while True:
        os_type = get_os()
        choice = show_menu(os_type)
        
        if choice == "0":
            print()
            info("Bye!")
            return 0
        
        if choice not in ["1", "2", "3", "4"]:
            err("Invalid choice")
            input("\n  Press Enter...")
            continue
        
        # Check Docker
        print()
        if not docker_ok():
            handle_docker_missing(os_type)
            continue
        
        ok("Docker ready")
        workspace = get_workspace()
        ok(f"Workspace: {workspace}")
        
        if choice == "3":
            print()
            pull_image(DOCKER_IMAGE)
            input("\n  Press Enter...")
            continue
        
        if choice == "4":
            print()
            build_image()
            input("\n  Press Enter...")
            continue
        
        image = get_image()
        if not image:
            err("No image available")
            input("\n  Press Enter...")
            continue
        
        # Launch based on OS and choice
        if os_type == "linux":
            # Linux: 1=X11, 2=VNC
            if choice == "1":
                return launch_x11(image, workspace, os_type)
            else:
                return launch_vnc(image, workspace)
        else:
            # Windows/Mac: 1=VNC, 2=X11
            if choice == "1":
                return launch_vnc(image, workspace)
            else:
                return launch_x11(image, workspace, os_type)
    
    return 0


# CLI mode

def run_cli(args):
    import argparse
    
    parser = argparse.ArgumentParser(description="eSim Docker Launcher")
    parser.add_argument("--vnc", "-v", action="store_true", help="VNC mode (browser)")
    parser.add_argument("--x11", "-x", action="store_true", help="X11 mode (native)")
    parser.add_argument("--build", "-b", action="store_true", help="Build from Dockerfile")
    parser.add_argument("--pull", "-p", action="store_true", help="Force pull image")
    parser.add_argument("--shell", "-s", action="store_true", help="Open shell only")
    
    opts = parser.parse_args(args)
    os_type = get_os()
    
    if not docker_ok():
        handle_docker_missing(os_type)
        return 1
    
    workspace = get_workspace()
    
    if opts.pull:
        if not pull_image():
            return 1
    
    image = get_image(build_local=opts.build)
    if not image:
        err("No image available")
        return 1
    
    if opts.shell:
        stop_container()
        cmd = ["docker", "run", "--rm", "-it", "--name", CONTAINER_NAME,
               "-v", f"{workspace}:/home/esim-user/eSim-Workspace:rw",
               image, "/bin/bash"]
        return subprocess.run(cmd).returncode
    
    if opts.x11:
        return launch_x11(image, workspace, os_type)
    
    # Default: VNC for Windows/Mac, X11 for Linux
    if os_type == "linux" and not opts.vnc:
        return launch_x11(image, workspace, os_type)
    
    return launch_vnc(image, workspace)


# Entry point

def main():
    if len(sys.argv) == 1:
        try:
            return run_menu()
        except KeyboardInterrupt:
            print("\n")
            info("Cancelled")
            return 0
    else:
        show_banner()
        try:
            return run_cli(sys.argv[1:])
        except KeyboardInterrupt:
            print("\n")
            info("Cancelled")
            return 0


if __name__ == "__main__":
    sys.exit(main())
