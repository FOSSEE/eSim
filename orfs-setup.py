#!/usr/bin/env python3
import os,sys,shutil,subprocess
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
ORFS_DIR=BASE_DIR/"OpenROAD-flow-scripts"
FLOW_DIR=ORFS_DIR/"flow"
TOOLS_DIR=ORFS_DIR/"tools/install"
OPENROAD_BIN=TOOLS_DIR/"OpenROAD/bin/openroad"
YOSYS_BIN=TOOLS_DIR/"yosys/bin/yosys"
ENV_SCRIPT=ORFS_DIR/"env.sh"
KLAYOUT_DEB=BASE_DIR/"library/klayout_0.30.7-1_amd64.deb"
KLAYOUT_BIN=Path("/usr/bin/klayout")
REPO_URL="https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git"

def run_cmd(cmd,cwd=None,shell=False):
 print("\n================================================")
 print(f"[RUNNING] {cmd if isinstance(cmd,str) else ' '.join(cmd)}")
 print("================================================")
 result=subprocess.run(cmd,cwd=cwd,shell=shell,text=True)
 if result.returncode!=0:
  print("\n[ERROR] Command failed!")
  return False
 return True

def check_exists(path,name):
 if not path.exists():
  print(f"\n[ERROR] {name} not found:")
  print(path)
  return False
 return True

def install_dependencies():
 print("\n========================================")
 print("STEP 0 : INSTALL DEPENDENCIES")
 print("========================================")

 run_cmd(["sudo","apt","update"])

 packages=[
 "build-essential","clang","cmake","git","curl","wget","python3",
 "python3-pip","python3-dev","bison","flex","swig","tcl-dev",
 "libreadline-dev","zlib1g-dev","qtbase5-dev","qtchooser",
 "qt5-qmake","qtbase5-dev-tools","libboost-all-dev",
 "libeigen3-dev","libspdlog-dev","libfmt-dev","libomp-dev",
 "libffi-dev","libtbb-dev","xdot","pkg-config","ccache",
 "gcc-11","g++-11","make","gawk"
 ]

 if not run_cmd(["sudo","apt","install","-y"]+packages):sys.exit(1)

 os.environ["CC"]="gcc-11"
 os.environ["CXX"]="g++-11"

 print("\n[OK] Dependencies Installed")

def create_swap():
 print("\n========================================")
 print("STEP 1 : ENABLE SWAP")
 print("========================================")

 swap_check=subprocess.run(
  ["swapon","--show"],
  capture_output=True,
  text=True
 )

 if swap_check.stdout.strip():
  print("\n[INFO] Swap already enabled")
  return

 run_cmd(["sudo","fallocate","-l","8G","/swapfile"])
 run_cmd(["sudo","chmod","600","/swapfile"])
 run_cmd(["sudo","mkswap","/swapfile"])
 run_cmd(["sudo","swapon","/swapfile"])
 run_cmd("echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab",shell=True)

 print("\n[OK] 8GB Swap Enabled")

def install_klayout():
 print("\n========================================")
 print("STEP 2 : INSTALL KLAYOUT")
 print("========================================")

 if KLAYOUT_BIN.exists():
  print("\n[INFO] KLayout already installed")
  print(KLAYOUT_BIN)
  return

 if not check_exists(KLAYOUT_DEB,"KLayout .deb file"):sys.exit(1)

 if not run_cmd(["sudo","dpkg","-i",str(KLAYOUT_DEB)]):
  run_cmd(["sudo","apt","install","-f","-y"])

 if not KLAYOUT_BIN.exists():
  print("\n[ERROR] KLayout installation failed")
  sys.exit(1)

 print("\n[OK] KLayout Installed")
 print(KLAYOUT_BIN)

def clone_orfs():
 print("\n========================================")
 print("STEP 3 : CLONING ORFS")
 print("========================================")

 if ORFS_DIR.exists():
  print("\n[INFO] Removing old ORFS")
  shutil.rmtree(ORFS_DIR)

 if not run_cmd(["git","clone",REPO_URL,str(ORFS_DIR)]):sys.exit(1)

def build_openroad():
 print("\n========================================")
 print("STEP 4 : BUILDING OPENROAD")
 print("========================================")

 build_script=ORFS_DIR/"build_openroad.sh"

 if not check_exists(build_script,"build_openroad.sh"):sys.exit(1)

 jobs=max(1,os.cpu_count()-2)

 if not run_cmd(
  ["./build_openroad.sh","--local","--threads",str(jobs)],
  cwd=ORFS_DIR
 ):
  print("\n[WARNING] Build Failed")
  print("\nREMOVE BROKEN BUILD:")
  print(f"rm -rf {ORFS_DIR}")
  print("\nRERUN:")
  print("python3 orfs.py")
  sys.exit(1)

def verify_openroad():
 print("\n========================================")
 print("STEP 5 : VERIFY OPENROAD")
 print("========================================")

 if not check_exists(OPENROAD_BIN,"OpenROAD binary"):sys.exit(1)

 print("\n[OK] OpenROAD Found")
 print(OPENROAD_BIN)

 run_cmd([str(OPENROAD_BIN),"-version"])

def verify_yosys():
 print("\n========================================")
 print("STEP 6 : VERIFY YOSYS")
 print("========================================")

 if not check_exists(YOSYS_BIN,"Yosys binary"):sys.exit(1)

 print("\n[OK] Yosys Found")
 print(YOSYS_BIN)

 run_cmd([str(YOSYS_BIN),"-V"])

def configure_path():
 print("\n========================================")
 print("STEP 7 : CONFIGURE PATH")
 print("========================================")

 os.environ["PATH"]=f"{OPENROAD_BIN.parent}:{YOSYS_BIN.parent}:"+os.environ["PATH"]

 print("\nOpenROAD:")
 print(shutil.which("openroad"))

 print("\nYosys:")
 print(shutil.which("yosys"))

def verify_env():
 print("\n========================================")
 print("STEP 8 : VERIFY ENV")
 print("========================================")

 if check_exists(ENV_SCRIPT,"env.sh"):
  print("\n[OK] env.sh Found")
 else:
  print("\n[WARNING] env.sh Missing")

def test_flow():
 print("\n========================================")
 print("STEP 9 : TEST FLOW")
 print("========================================")

 if not FLOW_DIR.exists():
  print("\n[ERROR] flow directory missing")
  sys.exit(1)

 run_cmd(["make","clean_all"],cwd=FLOW_DIR)

 if not run_cmd(["make","DESIGN=gcd"],cwd=FLOW_DIR):
  print("\n[ERROR] ORFS Flow Failed")
  print(f"\nrm -rf {ORFS_DIR}")
  print("python3 orfs.py")
  sys.exit(1)

def verify_results():
 print("\n========================================")
 print("STEP 10 : VERIFY RESULTS")
 print("========================================")

 result_dir=FLOW_DIR/"results/nangate45/gcd/base"

 if not result_dir.exists():
  print("\n[ERROR] Results Missing")
  sys.exit(1)

 print("\n[SUCCESS] ORFS FLOW COMPLETED")
 print("\nGenerated Files:")

 for f in result_dir.iterdir():
  print(f"  - {f.name}")

def main():
 print("\n================================================")
 print("ORFS AUTOMATIC INSTALLER")
 print("================================================")

 print("\nINSTALL LOCATION:")
 print(BASE_DIR)

 print("\nDISCLAIMER:")
 print("If installation stops or fails:")
 print(f"rm -rf {ORFS_DIR}")
 print("python3 orfs.py")

 install_dependencies()
 create_swap()
 install_klayout()
 clone_orfs()
 build_openroad()
 verify_openroad()
 verify_yosys()
 configure_path()
 verify_env()
 test_flow()
 verify_results()

 print("\n================================================")
 print("[SUCCESS] INSTALLATION COMPLETE")
 print("================================================")

if __name__=="__main__":
 main()