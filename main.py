from __future__ import annotations

import sys
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets


class TextEditor(QtWidgets.QMainWindow):
    def __init__(self, initial_path: Path | None = None) -> None:
        super().__init__()
        self._path: Path | None = None
        self._encoding = "utf-8"

        self._editor = QtWidgets.QPlainTextEdit()
        self._editor_font = QtGui.QFontDatabase.systemFont(
            QtGui.QFontDatabase.FixedFont
        )
        self._font_size_default = 18
        self._font_size_min = self._font_size_default
        self._font_size_max = 120
        self._editor_font.setPointSize(self._font_size_default)
        self._apply_editor_font()
        self.setCentralWidget(self._editor)

        self._status = self.statusBar()
        self._path_label = QtWidgets.QLabel()
        self._path_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self._path_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self._status.addWidget(self._path_label, 1)
        self._cursor_label = QtWidgets.QLabel()
        self._status.addPermanentWidget(self._cursor_label)

        self._build_actions()
        self._build_menus()
        # self._build_toolbar()
        self._connect_signals()

        self.resize(900, 650)
        self._update_title()

        if initial_path is not None:
            self.open_path(initial_path)

    def _build_actions(self) -> None:
        style = self.style()

        self._new_action = QtGui.QAction("&New", self)
        self._new_action.setShortcut(QtGui.QKeySequence.StandardKey.New)
        # self._new_action.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileIcon))

        self._open_action = QtGui.QAction("&Open…", self)
        self._open_action.setShortcut(QtGui.QKeySequence.StandardKey.Open)
        # self._open_action.setIcon(
        #     style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton)
        # )

        self._save_action = QtGui.QAction("&Save", self)
        self._save_action.setShortcut(QtGui.QKeySequence.StandardKey.Save)
        # self._save_action.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton))

        self._save_as_action = QtGui.QAction("Save &As…", self)
        self._save_as_action.setShortcut(QtGui.QKeySequence.SaveAs)

        self._quit_action = QtGui.QAction("&Quit", self)
        self._quit_action.setShortcut(QtGui.QKeySequence.StandardKey.Quit)

        self._undo_action = QtGui.QAction("&Undo", self)
        self._undo_action.setShortcut(QtGui.QKeySequence.StandardKey.Undo)

        self._redo_action = QtGui.QAction("&Redo", self)
        self._redo_action.setShortcut(QtGui.QKeySequence.StandardKey.Redo)

        self._cut_action = QtGui.QAction("Cu&t", self)
        self._cut_action.setShortcut(QtGui.QKeySequence.StandardKey.Cut)

        self._copy_action = QtGui.QAction("&Copy", self)
        self._copy_action.setShortcut(QtGui.QKeySequence.StandardKey.Copy)

        self._paste_action = QtGui.QAction("&Paste", self)
        self._paste_action.setShortcut(QtGui.QKeySequence.StandardKey.Paste)

        self._select_all_action = QtGui.QAction("Select &All", self)
        self._select_all_action.setShortcut(QtGui.QKeySequence.StandardKey.SelectAll)

        self._word_wrap_action = QtGui.QAction("&Word Wrap", self)
        self._word_wrap_action.setCheckable(True)
        self._word_wrap_action.setChecked(True)

        self._zoom_in_action = QtGui.QAction("Zoom &In", self)
        self._zoom_in_action.setShortcut(QtGui.QKeySequence.StandardKey.ZoomIn)

        self._zoom_out_action = QtGui.QAction("Zoom &Out", self)
        self._zoom_out_action.setShortcut(QtGui.QKeySequence.StandardKey.ZoomOut)

        self._reset_font_action = QtGui.QAction("&Reset Font Size", self)
        self._reset_font_action.setShortcut(QtGui.QKeySequence("Ctrl+0"))

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._open_action)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self._quit_action)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(self._undo_action)
        edit_menu.addAction(self._redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self._cut_action)
        edit_menu.addAction(self._copy_action)
        edit_menu.addAction(self._paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self._select_all_action)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self._word_wrap_action)
        view_menu.addSeparator()
        view_menu.addAction(self._zoom_in_action)
        view_menu.addAction(self._zoom_out_action)
        view_menu.addAction(self._reset_font_action)

    def _build_toolbar(self) -> None:
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        toolbar.addAction(self._new_action)
        toolbar.addAction(self._open_action)
        toolbar.addAction(self._save_action)
        toolbar.addSeparator()
        toolbar.addAction(self._cut_action)
        toolbar.addAction(self._copy_action)
        toolbar.addAction(self._paste_action)

    def _connect_signals(self) -> None:
        self._new_action.triggered.connect(self.new_file)
        self._open_action.triggered.connect(self.open_file)
        self._save_action.triggered.connect(self.save_file)
        self._save_as_action.triggered.connect(self.save_file_as)
        self._quit_action.triggered.connect(self.close)

        self._undo_action.triggered.connect(self._editor.undo)
        self._redo_action.triggered.connect(self._editor.redo)
        self._cut_action.triggered.connect(self._editor.cut)
        self._copy_action.triggered.connect(self._editor.copy)
        self._paste_action.triggered.connect(self._editor.paste)
        self._select_all_action.triggered.connect(self._editor.selectAll)

        self._word_wrap_action.toggled.connect(self._set_word_wrap)
        self._zoom_in_action.triggered.connect(self._zoom_in)
        self._zoom_out_action.triggered.connect(self._zoom_out)
        self._reset_font_action.triggered.connect(self._reset_font_size)

        self._editor.document().modificationChanged.connect(self._update_title)
        self._editor.document().modificationChanged.connect(self._save_action.setEnabled)
        self._editor.cursorPositionChanged.connect(self._update_cursor_status)
        self._editor.textChanged.connect(self._update_cursor_status)

        self._save_action.setEnabled(False)
        self._update_cursor_status()

    def _set_word_wrap(self, enabled: bool) -> None:
        if enabled:
            self._editor.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth)
        else:
            self._editor.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

    def _apply_editor_font(self) -> None:
        self._editor.setFont(self._editor_font)
        metrics = QtGui.QFontMetrics(self._editor_font)
        self._editor.setTabStopDistance(metrics.horizontalAdvance(" ") * 4)

    def _set_font_point_size(self, size: int) -> None:
        size = max(self._font_size_min, min(self._font_size_max, size))
        if self._editor_font.pointSize() == size:
            return
        self._editor_font.setPointSize(size)
        self._apply_editor_font()

    def _zoom_in(self) -> None:
        self._set_font_point_size(self._editor_font.pointSize() + 1)

    def _zoom_out(self) -> None:
        self._set_font_point_size(self._editor_font.pointSize() - 1)

    def _reset_font_size(self) -> None:
        self._set_font_point_size(self._font_size_default)

    def _update_title(self) -> None:
        name = self._path.name if self._path else "Untitled"
        modified = " •" if self._editor.document().isModified() else ""
        self.setWindowTitle(f"{name}{modified} — Waynotes")
        if self._path is not None:
            self._path_label.setText(str(self._path.resolve()))
        else:
            self._path_label.setText("scratch file")

    def _update_cursor_status(self) -> None:
        cursor = self._editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.positionInBlock() + 1
        self._cursor_label.setText(f"Ln {line}, Col {col}")

    def new_file(self) -> None:
        if not self._maybe_save():
            return
        self._editor.clear()
        self._path = None
        self._editor.document().setModified(False)
        self._update_title()

    def open_file(self) -> None:
        if not self._maybe_save():
            return
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open File",
            str(self._path.parent if self._path else Path.home()),
            "All Files (*);;Text Files (*.txt *.md *.py *.json *.xml *.html *.css *.js)",
        )
        if path:
            self.open_path(Path(path))

    def open_path(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding=self._encoding)
        except OSError as exc:
            QtWidgets.QMessageBox.warning(
                self,
                "Waynotes",
                f"Could not open file:\n{path}\n\n{exc}",
            )
            return False

        self._editor.setPlainText(text)
        self._path = path
        self._editor.document().setModified(False)
        self._update_title()
        return True

    def save_file(self) -> bool:
        if self._path is None:
            return self.save_file_as()
        return self._write_to_path(self._path)

    def save_file_as(self) -> bool:
        start = str(self._path.parent if self._path else Path.home())
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File As", start)
        if not path:
            return False
        return self._write_to_path(Path(path))

    def _write_to_path(self, path: Path) -> bool:
        try:
            path.write_text(self._editor.toPlainText(), encoding=self._encoding)
        except OSError as exc:
            QtWidgets.QMessageBox.warning(
                self,
                "Waynotes",
                f"Could not save file:\n{path}\n\n{exc}",
            )
            return False

        self._path = path
        self._editor.document().setModified(False)
        self._update_title()
        return True

    def _maybe_save(self) -> bool:
        if not self._editor.document().isModified():
            return True

        name = self._path.name if self._path else "Untitled"
        answer = QtWidgets.QMessageBox.question(
            self,
            "Waynotes",
            f"Save changes to “{name}” before closing?",
            QtWidgets.QMessageBox.StandardButton.Save
            | QtWidgets.QMessageBox.StandardButton.Discard
            | QtWidgets.QMessageBox.StandardButton.Cancel,
        )
        if answer == QtWidgets.QMessageBox.StandardButton.Cancel:
            return False
        if answer == QtWidgets.QMessageBox.StandardButton.Save:
            return self.save_file()
        return True

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self._maybe_save():
            event.accept()
        else:
            event.ignore()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Waynotes")
    app.setOrganizationName("Waynotes")

    initial: Path | None = None
    if len(sys.argv) > 1:
        candidate = Path(sys.argv[1])
        if candidate.is_file():
            initial = candidate

    window = TextEditor(initial)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
