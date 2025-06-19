from PyQt5.QtWidgets import QFileDialog

def browse_path(self, text_box):
    file_dialog = QFileDialog()  # a dialog that allows the user to select files or directories
    file_dialog.setFileMode(QFileDialog.AnyFile)
    file_dialog.setNameFilter("Supported Files (*.sch *.asc *.slb *.asy);;ASY Files (*.asy)")  # Include all supported extensions
    file_dialog.exec_()  # Execute the dialog

    selected_files = file_dialog.selectedFiles()  # Get the selected file(s)
    if selected_files:
        text_box.setText(selected_files[0])
