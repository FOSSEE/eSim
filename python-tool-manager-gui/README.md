<h1>eSim Tool Manager GUI</h1>

<p>
This project provides a GUI-based tool manager for eSim.
It helps install, update, and manage different tools easily.
</p>

<h2>Features</h2>
<ul>
  <li>Load tools dynamically from YAML</li>
  <li>Install, update, and uninstall tools</li>
  <li>Supports tools like KiCad, Ngspice, GHDL, LLVM, Verilator, Python</li>
  <li>Runs tasks in background (UI does not freeze)</li>
  <li>Shows logs in real time</li>
  <li>Checks installed tools and versions</li>
  <li>Basic error handling</li>
</ul>

<h2>How to run</h2>
<pre>
pip install -r requirements.txt
python gui.py
</pre>

<h2>Project files</h2>
<ul>
  <li>gui.py → main GUI</li>
  <li>installer.py → installation logic</li>
  <li>kicad.py, ngspice.py, etc. → tool modules</li>
  <li>tools.yml → configuration</li>
  <li>install_details.yml → install info</li>
</ul>

<h2>Notes</h2>
<ul>
  <li>Works on Linux, macOS, and Windows</li>
  <li>Uses system package managers</li>
  <li>.gitignore excludes unnecessary files</li>
</ul>

<h2>Contribution</h2>
<p>
You can fork the repo and create a pull request.
</p>