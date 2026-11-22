// ==========================================================================
// eSim.exe - native Windows entry point for eSim.
//
// A .bat launcher cannot carry an icon or version info and flashes a console.
// This tiny executable mirrors esim.bat's environment setup and launches
// the bundled CPython interpreter with Application.py.
//
// Source companion to esim_launcher.c for environments without MinGW gcc.
// Built reproducibly via Windows system csc.exe.
// ==========================================================================

using System;
using System.Diagnostics;
using System.IO;

namespace eSimLauncher {
    static class Program {
        [STAThread]
        static void Main(string[] args) {
            string root = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\');
            string python = Path.Combine(root, "python", "python.exe");
            string app = Path.Combine(root, "src", "frontEnd", "Application.py");

            if (!File.Exists(python)) {
                python = "python.exe";
            }

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = python;
            string argStr = "\"" + app + "\"";
            if (args != null && args.Length > 0) {
                argStr += " " + string.Join(" ", args);
            }
            psi.Arguments = argStr;
            psi.WorkingDirectory = root;
            psi.UseShellExecute = false;

            string existingPath = Environment.GetEnvironmentVariable("PATH") ?? "";
            string kicadBin = Path.Combine(root, "tools", "kicad", "bin");
            string ngspiceBin = Path.Combine(root, "tools", "ngspice", "bin");
            string nghdlBin = Path.Combine(root, "tools", "nghdl", "install_dir", "bin");
            string nghdlLib = Path.Combine(root, "tools", "nghdl", "install_dir", "lib", "ngspice");

            string newPath = "";
            if (Directory.Exists(kicadBin)) newPath += kicadBin + ";";
            if (Directory.Exists(nghdlBin)) newPath += nghdlBin + ";" + nghdlLib + ";";
            if (Directory.Exists(ngspiceBin)) newPath += ngspiceBin + ";";
            newPath += existingPath;

            psi.EnvironmentVariables["PATH"] = newPath;
            psi.EnvironmentVariables["ESIM_ENV_READY"] = "1";
            psi.EnvironmentVariables["ESIM_HOME"] = root;

            if (Directory.Exists(Path.Combine(root, "tools", "nghdl", "install_dir", "share", "ngspice"))) {
                psi.EnvironmentVariables["SPICE_LIB_DIR"] = Path.Combine(root, "tools", "nghdl", "install_dir", "share", "ngspice");
            }

            try {
                Process proc = Process.Start(psi);
            } catch (Exception ex) {
                System.Windows.Forms.MessageBox.Show("Failed to launch eSim:\n" + ex.Message, "eSim Launcher Error");
            }
        }
    }
}
