"""
ICELang KiCad Plugin
====================
Registers ICELang as a KiCad ActionPlugin. Opens a file dialog for
a .ilang source file, compiles it, and loads the generated .kicad_sch
into the current schematic editor session automatically.

Installation:
    Copy this directory to:
    ~/.local/share/kicad/9.0/scripting/plugins/icelang_plugin/
"""

try:
    import pcbnew
    KICAD_AVAILABLE = True
except ImportError:
    KICAD_AVAILABLE = False

if KICAD_AVAILABLE:
    import os
    import sys

    class ICELangPlugin(pcbnew.ActionPlugin):
        def defaults(self):
            self.name        = "ICELang"
            self.category    = "Schematic Generation"
            self.description = (
                "Compile a .ilang DSL source file to a KiCad schematic "
                "and SPICE netlist."
            )
            self.show_toolbar_button = True

        def Run(self):
            import wx
            from pathlib import Path

            # Add icelang compiler to path
            plugin_dir    = Path(__file__).parent
            compiler_root = os.environ.get(
                "ICELANG_ROOT",
                str(plugin_dir.parent / "icelang")
            )
            if compiler_root not in sys.path:
                sys.path.insert(0, compiler_root)

            from icelang_plugin.runner import run, RunnerError

            # File picker dialog
            with wx.FileDialog(
                None,
                "Open ICELang source file",
                wildcard="ICELang files (*.ilang)|*.ilang",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
            ) as dlg:
                if dlg.ShowModal() == wx.ID_CANCEL:
                    return
                ilang_path = dlg.GetPath()

            output_dir = str(Path(ilang_path).parent / "output")

            # Run compiler
            try:
                result = run(ilang_path, output_dir)
            except RunnerError as e:
                wx.MessageBox(
                    str(e),
                    "ICELang Error",
                    wx.OK | wx.ICON_ERROR
                )
                return

            kicad_sch = result["kicad_sch"]

            # Auto-load into active schematic editor
            loaded = False
            try:
                frame = pcbnew.GetBoard().GetParent()
                if hasattr(frame, "OpenProjectFiles"):
                    frame.OpenProjectFiles([kicad_sch])
                    loaded = True
            except Exception:
                pass

            if loaded:
                wx.MessageBox(
                    f"Compiled and loaded:\n{kicad_sch}",
                    "ICELang",
                    wx.OK | wx.ICON_INFORMATION
                )
            else:
                # Fallback: tell user where the file is
                wx.MessageBox(
                    f"Compiled successfully.\n\nOpen this file in KiCad:\n{kicad_sch}",
                    "ICELang",
                    wx.OK | wx.ICON_INFORMATION
                )

    ICELangPlugin().register()
