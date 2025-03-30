from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from configparser import ConfigParser
import os

class NgspiceWidget(QtWidgets.QWidget):

    def __init__(self, command, projPath):
        """
        - Creates constructor for NgspiceWidget class.
        - Checks whether OS is Linux or Windows and
          creates Ngspice window accordingly.
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)

        self.output_file = os.path.join(projPath, "ngspice_output.txt")  # Define output file

        print("Argument to ngspice command:", command)
        if os.name == 'nt':  # Windows OS
            parser_nghdl = ConfigParser()
            parser_nghdl.read(
                os.path.join('library', 'config', '.nghdl', 'config.ini')
            )

            msys_home = parser_nghdl.get('COMPILER', 'MSYS_HOME')

            tempdir = os.getcwd()
            projPath = self.obj_appconfig.current_project["ProjectName"]
            os.chdir(projPath)
            self.command = f'cmd /c "start /min {msys_home}/usr/bin/mintty.exe ngspice -p {command} > {self.output_file} 2>&1"'

            self.process.finished.connect(self.read_output)  # Read output after process finishes
            self.process.start(self.command)
            os.chdir(tempdir)

        else:  # Linux OS
            self.command = f"cd {projPath}; ngspice -r {command.replace('.cir.out', '.raw')} {command} 2>&1 | tee {self.output_file}"

            self.args = ['-hold', '-e', 'bash', '-c', self.command]

            self.process.start('xterm', self.args)

            self.obj_appconfig.process_obj.append(self.process)
            (
                self.obj_appconfig.proc_dict
                [self.obj_appconfig.current_project['ProjectName']].append(
                    self.process.pid())
            )

            self.process = QtCore.QProcess(self)
            self.command = "gaw " + command.replace(".cir.out", ".raw")
            self.process.start('sh', ['-c', self.command])

            self.process.finished.connect(self.read_output)  # Read output after process finishes

    
    import os

    def read_output(self):
        """Reads NGSpice output, filters error-related lines, excludes empty lines, removes duplicates, and skips lines with 'no such vector'."""
        filtered_output_file = os.path.join(os.path.dirname(self.output_file), "ngspice_filtered_output.txt")
        seen_lines = set()  # Set to track already seen lines to remove duplicates
        try:
            with open(self.output_file, "r") as infile, open(filtered_output_file, "w") as outfile:
                lines = [line.strip() for line in infile if line.strip()]        
                i = 0
                while i < len(lines):
                    line = lines[i].lower()
                    
                    # Process error-related lines
                    if any(k in line for k in ["error", "fatal", "singular matrix","no such command"]) and not any(k in line for k in ["*","!", "trying"]):
                        if line not in seen_lines:  # Check if line is already seen
                            outfile.write("\n".join(lines[i:i+3]) + "\n")  # Write up to 3 lines
                            seen_lines.add(line)  # Mark this line as seen
                            i += 2  # Skip processed lines
                    i += 1
        except Exception as e:
            print(f"Error processing NGSpice output: {e}")



