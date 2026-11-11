from PyQt6 import QtCore, QtGui, QtWidgets
from configuration import Dialogs
import os
import re
from configuration.Appconfig import Appconfig
from frontEnd.SnapshotStore import SnapshotStore
from projManagement.Validation import Validation
from projManagement.projectPaths import resolve_stem, canonical_path, \
    same_project, find_anchors, save_project_explorer
from codeEditor import EditorWindow


class _ProjectTree(QtWidgets.QTreeWidget):
    """Project tree that expands/collapses a project on a *single* click
    anywhere on its row -- not only on the small branch arrow.

    Toggles via ``setExpanded`` directly -- the exact call QTreeView's own
    arrow hit-test makes internally -- instead of retargeting the click onto
    the arrow and replaying it through QTreeView. That retargeting used to
    hit QTreeView's itemDecorationAt() branch, which handles the arrow click
    and returns *without* calling QAbstractItemView's mousePressEvent, so
    Qt's internal pressedIndex bookkeeping never updated, and a later real
    double-click on the row got silently downgraded back into a plain press
    -- no project switch, even though the row could still look selected.

    The toggle itself is deferred rather than run inline: with animation on
    (setAnimated(True)), calling setExpanded() synchronously *inside*
    mousePressEvent also corrupts that same pressedIndex bookkeeping for the
    row just pressed, breaking doubleClicked on it -- even with the unmodified
    event passed straight to QTreeView. Deferring lets the whole press/release
    sequence for this event finish first, so the expand animation can never
    land inside the same window Qt uses to validate a double-click.

    That deferral is also why the row click used to expand with a snap while
    the arrow expanded smoothly. QTreeView drives the drop-down off the view's
    State: expand() puts the view in AnimatingState and paintEvent only
    composites the before/after pixmaps while it stays there. The deferred
    toggle runs between the press and the release, so the animation is already
    under way when QAbstractItemView::mouseReleaseEvent fires -- and that
    unconditionally calls setState(NoState), dropping the view out of
    AnimatingState one frame in. The native arrow click never hits it, because
    QTreeView::mouseReleaseEvent sees the click on the decoration and skips the
    base-class release entirely.

    So the release restores the state the base class clobbered, instead of the
    toggle being moved after the release. Moving it there does keep the
    animation, but it lands the expand inside the window Qt uses to validate a
    double-click, and project switching (doubleClicked -> openProject) stops
    working. Re-arming AnimatingState touches nothing else: pressedIndex and
    the rest of the double-click bookkeeping are left exactly as the
    unmodified base class left them, and the animation's own completion
    handler still returns the view to NoState when it finishes.

    Re-arming it does mean the view is now in AnimatingState for the ~250ms
    the drop-down takes -- and the second click of a double-click lands inside
    that window. QTreeView::mouseDoubleClickEvent begins with a bare
    ``if (state() != NoState) return;``, so it would swallow the click and no
    project would open. mouseDoubleClickEvent below steps over that guard: an
    animation still in flight is not a reason to ignore a double-click, and
    the animation settles on its own either way (it did before this class
    existed, since the release used to end it every time)."""

    def mousePressEvent(self, event):
        # Any fresh input ends the re-armed animation state first -- see
        # _settleAnimation. A press that arrives while the view still reads as
        # AnimatingState is reported as already-handled by QTreeView's
        # expandOrCollapseItemAtPos, which then skips QAbstractItemView's
        # press entirely: clicking a second project during the first one's
        # drop-down would never move the selection.
        self._settleAnimation()
        index = self.indexAt(event.position().toPoint())
        item = self.itemFromIndex(index) if index.isValid() else None
        # Only toggle on left-clicks on an expandable top-level project row.
        # File rows (children) fall through untouched -- they open via
        # double-click.
        if (event.button() == QtCore.Qt.MouseButton.LeftButton
                and item is not None
                and item.parent() is None
                and item.childCount() > 0):
            content_left = self.visualRect(index).left()
            # Only toggle when the click missed the arrow; on the arrow
            # itself the native hit-test already handles it.
            if event.position().toPoint().x() >= content_left:
                persistent = QtCore.QPersistentModelIndex(index)
                QtCore.QTimer.singleShot(
                    0, lambda: self._deferredToggle(persistent))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Only ever re-arms a drop-down this same click started: NoState is
        # read back after super(), so a release that was not animating to
        # begin with cannot be turned into one.
        animating = QtWidgets.QAbstractItemView.State.AnimatingState
        was_animating = self.state() == animating
        super().mouseReleaseEvent(event)
        if was_animating and \
                self.state() == QtWidgets.QAbstractItemView.State.NoState:
            self.setState(animating)

    def mouseDoubleClickEvent(self, event):
        # QTreeView::mouseDoubleClickEvent early-returns on `state() !=
        # NoState`, so the re-armed state has to go before the click can open
        # a project.
        self._settleAnimation()
        super().mouseDoubleClickEvent(event)

    def _settleAnimation(self):
        """Give up the re-armed AnimatingState ahead of handling new input.

        Only the *painting* of the drop-down needs that state, and only while
        the tree is idle; every QTreeView input path treats a non-NoState view
        as busy and drops the event. The animation itself is unaffected -- it
        keeps running and its own completion handler repaints and returns the
        view to NoState -- so the branch simply finishes opening without the
        remaining frames being composited.
        """
        if self.state() == QtWidgets.QAbstractItemView.State.AnimatingState:
            self.setState(QtWidgets.QAbstractItemView.State.NoState)

    def _deferredToggle(self, persistent):
        if persistent.isValid():
            idx = QtCore.QModelIndex(persistent)
            self.setExpanded(idx, not self.isExpanded(idx))


# This is main class for Project Explorer Area.
class ProjectExplorer(QtWidgets.QWidget):
    """
    This class contains function:

        - One work as a constructor(__init__).
        - For saving data.
        - for renaming project.
        - for refreshing project.
        - for removing project.
    """

    # Data roles stored on each top-level (project) item so identity and
    # display stay decoupled: STEM_ROLE keeps the un-disambiguated base label
    # (the project stem) so collisions can be re-resolved on every change;
    # STALE_ROLE flags a project whose folder no longer exists on disk.
    STEM_ROLE = QtCore.Qt.ItemDataRole.UserRole
    STALE_ROLE = QtCore.Qt.ItemDataRole.UserRole + 1

    def __init__(self):
        """
        This method is doing following tasks:
            - Working as a constructor for class ProjectExplorer.
            - view of project explorer area.
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        # One reusable editor window per project (keyed by project name).
        self.editor_windows = {}
        self.treewidget = _ProjectTree()
        # objectName scopes the Aurora project-tree QSS (outline selection +
        # rounded chevron) to this tree without restyling every other list.
        self.treewidget.setObjectName('projectTree')
        # Smooth drop-down animation when a project branch expands/collapses.
        self.treewidget.setAnimated(True)
        # Double-click is for opening files, not toggling folders (single click
        # already does that), so a folder double-click doesn't fight the
        # expand animation by rebuilding its children mid-gesture.
        self.treewidget.setExpandsOnDoubleClick(False)
        self._vbox = QtWidgets.QVBoxLayout()
        self.fs_watcher = QtCore.QFileSystemWatcher()
        header = QtWidgets.QTreeWidgetItem(["Projects", "path"])
        self.treewidget.setHeaderItem(header)
        self.treewidget.setColumnHidden(1, True)


        self.loadProjects()
        self._vbox.addWidget(self.treewidget)
        # Static elevation (e2) so the project tree reads as a raised panel.
        # Backdrop, not elevate(): a QGraphicsEffect on the tree itself would
        # render every project name through an offscreen ARGB buffer and cost
        # the whole panel its subpixel antialiasing.
        try:
            from frontEnd.elevation import elevate_backdrop
            # 14 == the QTreeWidget border-radius in both sheets. A square
            # backdrop behind a rounded tree shows its corners sticking out
            # past the curve as four hard tabs.
            elevate_backdrop(self.treewidget, "e2", radius=14)
        except Exception:
            pass
        self.fs_watcher.directoryChanged.connect(self.handleDirectoryChanged)
        # Coalesce QFileSystemWatcher storms. A cloud-sync client (OneDrive /
        # Dropbox) rewriting a watched project folder can fire directoryChanged
        # dozens of times in a burst; refreshing the branch on every event
        # rebuilds its children on the GUI thread each time, which janks the
        # whole tree. Collect the changed paths and refresh them once, a short
        # delay after the burst goes quiet -- restarting the single-shot timer
        # on each event debounces the storm into a single rebuild.
        # Built on first PaletteChange (see _scheduleIconRefresh).
        self._icon_refresh_timer = None
        self._pending_dir_changes = set()
        self._dir_refresh_timer = QtCore.QTimer(self)
        self._dir_refresh_timer.setSingleShot(True)
        self._dir_refresh_timer.timeout.connect(self._flushDirectoryChanges)
        # NOT refreshing on expand: rebuilding a branch's children mid-expand
        # destroys QTreeWidget's drop-down animation (jittery/broken). The
        # fs_watcher above already keeps the tree fresh on directory changes.
        # self.treewidget.expanded.connect(self.refreshInstant)
        self.treewidget.doubleClicked.connect(self.openProject)
        self.treewidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.openMenu)
        self.setLayout(self._vbox)

    def loadProjects(self):
        """
        Render the saved project list into the tree, collapsed.

        Single entry point for *bulk* loading (first construction, workspace
        open/switch). Idempotent: clears the tree, migrates persisted entries
        to canonical identity keys -- collapsing any that point at the same
        folder (legacy raw strings, symlink/'..'/case variants) so a project
        appears exactly once -- builds each node collapsed, then refreshes
        labels and persists once. Missing folders are kept but shown as stale
        rather than silently dropped, so the user can see and remove them.

        Distinct from addTreeNode, which is for the user *opening one*
        project: that focuses and expands the single node it touches. Bulk
        loading must never expand every project, so it does not go through
        addTreeNode -- the active project (e.g. a restored last project) is
        re-focused at the end instead.
        """
        # Rebuild project_explorer in place: it is a shared class-level dict
        # that other Appconfig instances (openProject, newProject, Workspace)
        # read and mutate. Replacing it with a new object would shadow it on
        # this instance only and desync everyone else, so clear()+update()
        # keeps the one shared dict's identity.
        migrated = {}
        for parents, children in list(
                self.obj_appconfig.project_explorer.items()):
            key = canonical_path(parents)
            if key:
                migrated[key] = children
        self.obj_appconfig.project_explorer.clear()
        self.obj_appconfig.project_explorer.update(migrated)

        self.treewidget.clear()
        for parents, children in migrated.items():
            self._buildNode(parents, children)
        self._refreshLabels()
        self._persist()
        self._focusCurrentProject()

    def _focusCurrentProject(self):
        """
        After a bulk load, expand + select the active project so a restored
        'last project' stays focused. No-op when nothing is open or the
        active project is not in the current list (e.g. a different
        workspace was opened).
        """
        proj = self.obj_appconfig.current_project.get('ProjectName')
        if not proj:
            return
        node = self._findNode(proj)
        if node is not None:
            self.treewidget.setCurrentItem(node)
            node.setExpanded(True)

    def handleDirectoryChanged(self, path):
        # Debounced: a lone event and a cloud-sync burst both collapse to a
        # single refresh once the timer fires (see __init__). Restarting the
        # timer on every event pushes the flush to ~300 ms after the last one.
        self._pending_dir_changes.add(path)
        self._dir_refresh_timer.start(300)

    def _flushDirectoryChanges(self):
        # Snapshot and clear first: refreshProject below can re-enter the
        # watcher and queue a fresh event, which must land in the next batch.
        paths = self._pending_dir_changes
        self._pending_dir_changes = set()
        for path in paths:
            for i in range(self.treewidget.topLevelItemCount()):
                item = self.treewidget.topLevelItem(i)
                if item.text(1) == path and item.isExpanded():
                    index = self.treewidget.indexFromItem(item)
                    self.refreshProject(indexItem=index)

    def refreshInstant(self):
        for i in range(self.treewidget.topLevelItemCount()):
            if self.treewidget.topLevelItem(i).isExpanded():
                index = self.treewidget.indexFromItem(
                    self.treewidget.topLevelItem(i))
                self.refreshProject(indexItem=index)

    def addTreeNode(self, parents, children):
        """
        Register a project in the explorer tree, keyed by its canonical path.

        Idempotent: opening a project already present does NOT create a second
        node -- it refreshes that project's file list and selects it. This is
        what stops the same project being added over and over (open it 100
        times, get one node), and what de-duplicates the same folder reached
        via a symlink, a '..' path, a trailing slash or a different-case
        spelling, since all collapse to the same canonical key.
        """
        key = canonical_path(parents)
        if not key:
            return

        existing = self._findNode(key)
        if existing is not None:
            # Already open: refresh children to the current on-disk list and
            # focus it instead of duplicating the node.
            self._fillChildren(existing, key, children)
        else:
            existing = self._buildNode(key, children)
        self.treewidget.setCurrentItem(existing)
        existing.setExpanded(True)

        self.obj_appconfig.project_explorer[key] = children
        self._persist()
        self._refreshLabels()

        # setdefault, not assignment: addTreeNode runs again on every refresh,
        # and clobbering these would drop the PIDs/docks already tracked for an
        # open project (orphaning its KiCad/ngspice windows on close).
        projName = self.obj_appconfig.current_project['ProjectName']
        self.obj_appconfig.proc_dict.setdefault(projName, [])
        self.obj_appconfig.dock_dict.setdefault(projName, [])

    # ---- project-node helpers (identity, display, staleness) ---------------

    @staticmethod
    def _dir_icon():
        """Folder icon for project (top-level) rows. Bundled SVG, not
        SP_DirIcon: the standard pixmap resolves to the OS shell folder
        (yellow Explorer folder on Windows) and never matched the theme."""
        from frontEnd import icon_paths
        return icon_paths.folder_icon()

    @staticmethod
    def _file_icon():
        """File icon for the file rows under a project. Bundled SVG for the
        same cross-platform reason as _dir_icon."""
        from frontEnd import icon_paths
        return icon_paths.file_icon()

    def changeEvent(self, event):
        """Rebuild the row icons when the theme flips.

        icon_paths._svg_icon bakes the theme's colour into the pixmap at build
        time, and the rows are painted once (_buildNode / _fillChildren). A
        light/dark flip therefore leaves every row holding the *previous*
        theme's glyph. Folders survive it because they use the accent role,
        which reads on either background; files use the plain text colour
        (#F8FBFF dark / #142033 light) and land near-invisible on the opposite
        one. Only a refresh or an expand rebuilt them before, which is why the
        symptom looked intermittent.
        """
        super().changeEvent(event)
        if event.type() == QtCore.QEvent.Type.PaletteChange:
            self._scheduleIconRefresh()

    def _scheduleIconRefresh(self):
        """Defer the re-render by a tick. Rasterising an icon *inside* the
        PaletteChange handler re-enters the polish that delivered the event.
        The timer is parented to self so it cannot outlive the widget."""
        if getattr(self, '_icon_refresh_timer', None) is None:
            self._icon_refresh_timer = QtCore.QTimer(self)
            self._icon_refresh_timer.setSingleShot(True)
            self._icon_refresh_timer.timeout.connect(self._refreshIcons)
        self._icon_refresh_timer.start(0)

    def _refreshIcons(self):
        """Re-render every row's icon against the palette that is live now."""
        dir_icon, file_icon = self._dir_icon(), self._file_icon()
        for i in range(self.treewidget.topLevelItemCount()):
            node = self.treewidget.topLevelItem(i)
            node.setIcon(0, dir_icon)
            for j in range(node.childCount()):
                node.child(j).setIcon(0, file_icon)

    def _projectLabel(self, path):
        """Base display label for a project: its stem, else the folder name."""
        stem, _status = resolve_stem(path, 'proj')
        return stem or os.path.basename(os.path.normpath(path)) or path

    def _buildNode(self, path, children):
        """
        Create a top-level project node for ``path`` (assumed canonical).
        Fills children from the on-disk file list; if the folder is missing,
        the node is created in the 'stale' state instead.
        """
        base = self._projectLabel(path)
        node = QtWidgets.QTreeWidgetItem(self.treewidget, [base, path])
        node.setData(0, self.STEM_ROLE, base)
        node.setIcon(0, self._dir_icon())
        self._fillChildren(node, path, children)
        return node

    def _fillChildren(self, node, path, children):
        """Repopulate a project node's file rows, or mark it stale."""
        node.takeChildren()
        if os.path.exists(path):
            node.setData(0, self.STALE_ROLE, False)
            self._clearStale(node, path)
            for files in children:
                child = QtWidgets.QTreeWidgetItem(
                    node, [files, os.path.join(path, files)]
                )
                child.setIcon(0, self._file_icon())
            if path not in self.fs_watcher.directories():
                self.fs_watcher.addPath(path)
        else:
            self._markStale(node, path)

    def _markStale(self, node, path):
        """Style a project whose folder no longer exists on disk."""
        node.setData(0, self.STALE_ROLE, True)
        node.setForeground(0, QtGui.QBrush(QtGui.QColor('gray')))
        font = node.font(0)
        font.setItalic(True)
        node.setFont(0, font)
        node.setToolTip(
            0, path + '  —  missing on disk '
            '(right-click ▸ Remove Project)')
        if path in self.fs_watcher.directories():
            self.fs_watcher.removePath(path)

    def _clearStale(self, node, path):
        """Undo stale styling once a project's folder is back/refreshed."""
        node.setForeground(0, QtGui.QBrush())
        font = node.font(0)
        font.setItalic(False)
        node.setFont(0, font)
        node.setToolTip(0, path)

    def _findNode(self, path):
        """Top-level item whose folder is the same project as ``path``."""
        key = canonical_path(path)
        for i in range(self.treewidget.topLevelItemCount()):
            item = self.treewidget.topLevelItem(i)
            if canonical_path(item.text(1)) == key:
                return item
        return None

    def _locHint(self, path):
        """Short parent-folder hint to disambiguate same-named projects."""
        parent = os.path.dirname(path)
        home = os.path.expanduser('~')
        if parent == home or parent.startswith(home + os.sep):
            parent = '~' + parent[len(home):]
        return parent or os.sep

    def _refreshLabels(self):
        """
        Resolve display labels for all projects. Projects with a unique stem
        show just the stem; projects whose stems collide are disambiguated by
        their parent folder so they are never indistinguishable. Stale projects
        are suffixed '(missing)'. Full path is always in the tooltip.
        """
        groups = {}
        for i in range(self.treewidget.topLevelItemCount()):
            item = self.treewidget.topLevelItem(i)
            base = item.data(0, self.STEM_ROLE) or item.text(0)
            groups.setdefault(base, []).append(item)

        for base, items in groups.items():
            collide = len(items) > 1
            for item in items:
                label = base
                if collide:
                    label += '  (' + self._locHint(item.text(1)) + ')'
                if item.data(0, self.STALE_ROLE):
                    label += '  (missing)'
                item.setText(0, label)

    def _persist(self):
        """Write the project list to disk; tolerate an unwritable workspace."""
        try:
            save_project_explorer(
                self.obj_appconfig.dictPath["path"],
                self.obj_appconfig.project_explorer)
        except OSError as err:
            print("Could not save project list:", err)

    def openMenu(self, position):
        indexes = self.treewidget.selectedIndexes()
        if not indexes:
            return

        level = 0
        index = indexes[0]
        while index.parent().isValid():
            index = index.parent()
            level += 1

        from frontEnd import icon_paths
        menu = QtWidgets.QMenu()
        if level == 0:
            renameProject = menu.addAction(self.tr("Rename Project"))
            renameProject.triggered.connect(self.renameProject)
            deleteproject = menu.addAction(self.tr("Remove Project"))
            deleteproject.setIcon(icon_paths.trash_icon())
            deleteproject.triggered.connect(self.removeProject)
            refreshproject = menu.addAction(self.tr("Refresh"))
            refreshproject.setIcon(icon_paths.refresh_icon())
            refreshproject.triggered.connect(self.refreshProject)
            menu.addSeparator()
            snapshotProject = menu.addAction(self.tr("Snapshot Project"))
            snapshotProject.setIcon(icon_paths.snapshot_icon())
            snapshotProject.triggered.connect(self.takeProjectSnapshot)
            openSnaps = menu.addAction(self.tr("Open Snapshots…"))
            openSnaps.triggered.connect(self.openSnapshotsPanel)
        elif level == 1:
            openfile = menu.addAction(self.tr("Open"))
            openfile.setIcon(self._file_icon())
            openfile.triggered.connect(self.openProject)
            snapshot = menu.addAction(self.tr("Snapshot"))
            snapshot.triggered.connect(self.takeSnapshot)

        path = str(index.sibling(index.row(), 1).data()) if level == 0 \
            else str(indexes[0].sibling(indexes[0].row(), 1).data())
        self._add_chatbot_actions(menu, level, path)

        menu.exec(self.treewidget.viewport().mapToGlobal(position))

    def _add_chatbot_actions(self, menu, level, path):
        """Offer AI-assistant netlist analysis when the assistant is installed."""
        if getattr(self.window(), "chatbot_dock", None) is None:
            return
        if level == 0:
            netlist = os.path.join(path, self._projectLabel(path) + ".cir.out")
            action = menu.addAction(self.tr("Analyze Project Netlist"))
        elif level == 1 and path.endswith((".cir", ".cir.out", ".net")):
            netlist = path
            action = menu.addAction(self.tr("Analyze this Netlist"))
        else:
            return
        action.triggered.connect(
            lambda: self._analyze_netlist_in_chatbot(netlist))

    def _analyze_netlist_in_chatbot(self, netlist_path):
        """Send a netlist to the AI assistant and bring its panel forward."""
        main_window = self.window()
        main_window.chatbot_dock.show()
        main_window.chatbot_dock.raise_()
        main_window.chatbot_window.analyse_netlist(netlist_path)

    def openProject(self):
        self.indexItem = self.treewidget.currentIndex()
        self.filePath = str(
            self.indexItem.sibling(self.indexItem.row(), 1).data()
        )

        if (os.path.isfile(str(self.filePath))):
            self.openInEditor(str(self.filePath))
        else:
            # refreshProject shows its own "does not exist" dialog and returns
            # False for a vanished folder (stale USB / unmounted network drive).
            # Bail out then -- setting a dead path current makes every later tool
            # click operate on a ghost project (eeschema on a missing file,
        # "netlist not found", NgspiceWidget on a nonexistent cwd).
            if not self.refreshProject(self.filePath):
                return

            self.obj_appconfig.print_info(
                'The current project is: ' + self.filePath
            )

            self.obj_appconfig.set_current_project(str(self.filePath))
            # setdefault, never clobber: re-opening an already-open project
            # must not drop the PIDs/docks it already has, or its live
            # KiCad/ngspice windows are orphaned on close (cf. addTreeNode).
            name = self.obj_appconfig.current_project['ProjectName']
            self.obj_appconfig.proc_dict.setdefault(name, [])
            self.obj_appconfig.dock_dict.setdefault(name, [])

    def openInEditor(self, filePath):
        """Open a project text file in the eSim code editor.

        Reuses one tabbed editor window per project, so a file already
        open just gets focused instead of spawning another window.
        """
        self._editorWindow().open(filePath)

    def _editorWindow(self):
        """Return the editor window for the current project."""
        project = self.obj_appconfig.current_project.get('ProjectName')
        key = project or '__noproject__'
        window = self.editor_windows.get(key)
        # closeDock() destroys the editor when its project is closed; a deleted
        # Qt wrapper raises on any access, so probe the cached window and start
        # fresh if it's gone (else re-opening the project would crash here).
        if window is not None:
            try:
                window.isVisible()
            except RuntimeError:
                window = None
        if window is None:
            window = EditorWindow.EditorWindow()
            self.editor_windows[key] = window
        # Tie its lifecycle to the project so closeDock() reaps it
        # (re-register in case the project was closed and reopened).
        if project and project in self.obj_appconfig.dock_dict:
            if window not in self.obj_appconfig.dock_dict[project]:
                self.obj_appconfig.dock_dict[project].append(window)
        return window

    def removeProject(self):
        """
        This function removes the project in explorer area by right \
        clicking on project and selecting remove option.
        """
        self.indexItem = self.treewidget.currentIndex()
        filePath = str(
            self.indexItem.sibling(self.indexItem.row(), 1).data()
        )
        self.int = self.indexItem.row()
        self.treewidget.takeTopLevelItem(self.int)

        key = canonical_path(filePath)
        if same_project(
                self.obj_appconfig.current_project["ProjectName"], key):
            self.obj_appconfig.set_current_project(None)

        if key in self.fs_watcher.directories():
            self.fs_watcher.removePath(key)

        # Drop the canonical key and any legacy alias resolving to the same
        # project, so a removed project never lingers under a stale spelling.
        for stored in [
            k for k in self.obj_appconfig.project_explorer
            if canonical_path(k) == key
        ]:
            self.obj_appconfig.project_explorer.pop(stored, None)

        self._persist()
        self._refreshLabels()

    def refreshProject(self, filePath=None, indexItem=None):
        """
        This function refresh the project in explorer area by right \
        clicking on project and selecting refresh option.
        """

        if not filePath or filePath is None:
            if indexItem is None:
                self.indexItem = self.treewidget.currentIndex()
            else:
                self.indexItem = indexItem

            filePath = str(
                self.indexItem.sibling(self.indexItem.row(), 1).data()
            )

        if os.path.exists(filePath):
            filelistnew = os.listdir(os.path.join(filePath))
            if indexItem is None:
                parentnode = self.treewidget.currentItem()
            else:
                parentnode = self.treewidget.itemFromIndex(self.indexItem)
            # openProject can call this with a filePath but no current selection,
            # so currentItem() may be None; locate the node by path first.
            if parentnode is None:
                parentnode = self._findNode(filePath)
            if parentnode is None:
                # The folder exists but has no tree node to rebuild against.
                # Record its contents and report success rather than raising
                # AttributeError on None.childCount().
                self.obj_appconfig.project_explorer[
                    canonical_path(filePath)] = filelistnew
                self._persist()
                return True
            count = parentnode.childCount()
            for i in range(count):
                parentnode.removeChild(parentnode.child(0))
            parentnode.setIcon(0, self._dir_icon())
            for files in filelistnew:
                child = QtWidgets.QTreeWidgetItem(
                    parentnode, [files, os.path.join(filePath, files)]
                )
                child.setIcon(0, self._file_icon())

            # Key by canonical identity and clear any prior stale state -- a
            # refresh that succeeds means the folder is back/valid.
            key = canonical_path(filePath)
            self.obj_appconfig.project_explorer[key] = filelistnew
            parentnode.setData(0, self.STALE_ROLE, False)
            self._clearStale(parentnode, filePath)
            self._refreshLabels()
            self._persist()
            return True

        else:
            # Folder vanished (moved/deleted/unmounted): keep the node but show
            # it as stale so the user can locate or remove it, rather than
            # silently losing the project.
            node = self._findNode(filePath)
            if node is not None:
                self._markStale(node, canonical_path(filePath))
                self._refreshLabels()
            print("Selected project not found")
            print("==================")
            Dialogs.critical(
                self, "Error Message", 'Selected project does not exist.')
            return False

    def renameProject(self):
        """
        This function renames the project present in project explorer area.
        It validates first:

            - If project names is not empty.
            - Project name does not contain spaces between them.
            - Project name is different between what it was earlier.
            - Project name should not exist.

        After project name is changed, it recreates the project explorer tree.
        """
        self.indexItem = self.treewidget.currentIndex()
        # Identity, not display text. The tree label may carry a
        # disambiguation suffix ("(~/parent)" for a stem collision, or
        # "(missing)" for a stale node) that must never leak into path math;
        # the STEM_ROLE holds the un-suffixed stem the files are named after.
        oldStem = self.indexItem.data(self.STEM_ROLE) \
            or str(self.indexItem.data())
        filePath = str(
                    self.indexItem.sibling(self.indexItem.row(), 1).data()
                )

        newBaseFileName, ok = QtWidgets.QInputDialog.getText(
            self, 'Rename Project', 'Project Name:',
            QtWidgets.QLineEdit.EchoMode.Normal, oldStem
        )

        if ok and newBaseFileName:
            newBaseFileName = str(newBaseFileName).strip()

            if not newBaseFileName:
                print("Project name cannot be empty")
                print("==================")
                Dialogs.critical(
                    self, "Error Message", 'The project name cannot be empty')

            elif re.search(r"\s", newBaseFileName):
                print("Name can not contain space between them")
                print("===========================")
                Dialogs.critical(
                    self, "Error Message",
                    'The project name should not contain space between them')

            elif oldStem == newBaseFileName:
                print("Project name has to be different")
                print("==================")
                Dialogs.critical(
                    self, "Error Message",
                    'The project name has to be different')

            elif self.refreshProject(filePath):

                projectPath = None
                projectFiles = None

                for parents, children in list(
                        self.obj_appconfig.project_explorer.items()):
                    if filePath == parents:
                        if os.path.exists(parents):
                            projectPath, projectFiles = parents, children
                        break

                if not (projectPath and projectFiles):
                    print("Selected project not found")
                    print("Project Path :", projectPath)
                    print("Project Files :", projectFiles)
                    print("==================")
                    Dialogs.critical(
                        self, "Error Message",
                        'Selected project does not exist.')
                    return

                # Rename in place: keep the project wherever it lives (it may
                # sit outside the workspace) instead of assuming a
                # workspace-relative target the way validateNewproj does.
                updatedProjectPath = os.path.join(
                    os.path.dirname(projectPath), newBaseFileName)

                if os.path.exists(updatedProjectPath):
                    print("Project name already exists.")
                    print("==========================")
                    Dialogs.critical(
                        self, "Error Message",
                        'The project "' + newBaseFileName +
                        '" already exist. Please select a different name or' +
                        ' delete existing project')
                    return

                # rename project folder
                updatedProjectFiles = []
                print("Renaming " + projectPath + " to " +
                      updatedProjectPath)

                # rename project folder
                try:
                    os.rename(projectPath, updatedProjectPath)
                except OSError as e:
                    Dialogs.critical(self, "Error Message", str(e))
                    return

                # rename files matching project stem
                try:
                    for projectFile in projectFiles:
                        if oldStem in projectFile:
                            oldFilePath = os.path.join(updatedProjectPath,
                                                       projectFile)
                            projectFile = projectFile.replace(
                                oldStem, newBaseFileName, 1)
                            newFilePath = os.path.join(
                                updatedProjectPath, projectFile)
                            print("Renaming " + oldFilePath + " to " +
                                  newFilePath)
                            os.rename(oldFilePath, newFilePath)
                            updatedProjectFiles.append(projectFile)

                except OSError as e:
                    print("==================")
                    print("Error! Revert renaming project")

                    # The revert can hit the same lock/permission that broke the
                    # forward pass (a schematic open in KiCad on Windows is the
                    # norm). Guard every os.rename here too and remember what
                    # could not be put back, instead of letting a second OSError
                    # escape to the excepthook and strand the project in a mixed
                    # old/new-stem state that resolve_stem can no longer resolve.
                    stranded = []
                    for projectFile in updatedProjectFiles:
                        newFilePath = os.path.join(
                                        updatedProjectPath, projectFile)
                        origName = projectFile.replace(
                                newBaseFileName, oldStem, 1)
                        oldFilePath = os.path.join(
                                updatedProjectPath, origName)
                        try:
                            os.rename(newFilePath, oldFilePath)
                        except OSError:
                            stranded.append(projectFile)

                    # Only fold the directory name back once its contents are
                    # consistent — a renamed-back folder still holding new-stem
                    # files is exactly the mixed state we are trying to avoid.
                    projectDir = updatedProjectPath
                    if not stranded:
                        try:
                            os.rename(updatedProjectPath, projectPath)
                            projectDir = projectPath
                        except OSError:
                            stranded.append(
                                os.path.basename(updatedProjectPath))

                    print("==================")
                    if stranded:
                        Dialogs.critical(
                            self, "Error Message",
                            "Could not rename the project, and it could not be "
                            "fully restored to '" + oldStem + "':\n\n" + str(e)
                            + "\n\nThe project is left in a mixed state under:\n"
                            + projectDir + "\n\nClose anything using these "
                            "files (e.g. an open schematic in KiCad), then "
                            "rename the remaining items back to '" + oldStem
                            + "' manually before reopening the project.")
                    else:
                        Dialogs.critical(self, "Error Message", str(e))
                    return

                # Re-point the .proj's schematicFile token at the renamed
                # schematic so resolve_stem / main_schematic don't go stale
                # (the file was renamed on disk above, but the pointer inside
                # the .proj still names the old stem).
                self._repointSchematic(
                    updatedProjectPath, oldStem, newBaseFileName)

                # update project_explorer dictionary (canonical key)
                updatedProjectPath = canonical_path(updatedProjectPath)
                del self.obj_appconfig.project_explorer[projectPath]
                self.obj_appconfig.project_explorer[updatedProjectPath] = \
                    updatedProjectFiles

                # Keep current_project pointing at the renamed folder if it
                # was the active project, so identity comparisons elsewhere
                # don't go stale against the old path.
                if same_project(
                        self.obj_appconfig.current_project["ProjectName"],
                        projectPath):
                    self.obj_appconfig.set_current_project(
                        updatedProjectPath)

                # remove the old folder from the watcher
                if projectPath in self.fs_watcher.directories():
                    self.fs_watcher.removePath(projectPath)

                # save project_explorer dictionary on disk
                self._persist()

                # recreate project explorer tree (addTreeNode is idempotent
                # and renders missing folders as stale, not dropped)
                self.treewidget.clear()
                # Snapshot: addTreeNode writes back into project_explorer.
                for parent, children in list(
                        self.obj_appconfig.project_explorer.items()):
                    self.addTreeNode(parent, children)

    def _repointSchematic(self, proj_dir, oldStem, newStem):
        """Rewrite the ``schematicFile`` line inside the project's ``.proj``
        anchor so its pointer follows a renamed schematic file. Best-effort:
        a failure here only degrades to main_schematic's convention fallback.
        """
        try:
            for proj in find_anchors(proj_dir, 'proj'):
                with open(proj, 'r') as fh:
                    lines = fh.readlines()
                with open(proj, 'w') as fh:
                    for line in lines:
                        words = line.split()
                        if len(words) >= 2 and words[0] == 'schematicFile':
                            newsch = words[1].replace(oldStem, newStem, 1)
                            fh.write('schematicFile ' + newsch + '\n')
                        else:
                            fh.write(line)
                break  # only the first/only .proj is the anchor
        except (IOError, OSError) as e:
            print("Warning: could not update .proj schematicFile pointer:", e)

    def set_time_explorer(self, time_explorer_widget):
        self.time_explorer = time_explorer_widget

    def takeSnapshot(self):
        """Snapshot a single file (right-clicked in the tree)."""
        index = self.treewidget.currentIndex()
        file_path = str(index.sibling(index.row(), 1).data())
        file_name = os.path.basename(file_path)

        if not os.path.isfile(file_path):
            Dialogs.warning(
                self, "Snapshot Failed", "Selected item is not a file.")
            return

        # Key history by the file's own project folder so the snapshot lands
        # under the right project even if it isn't the active one.
        project_path = os.path.dirname(file_path)
        project_name = os.path.basename(os.path.normpath(project_path))
        try:
            SnapshotStore().create(
                project_name, project_path, files=[file_name],
                label="File snapshot")
        except Exception as exc:
            Dialogs.warning(self, "Snapshot Failed", str(exc))
            return

        self._refresh_snapshots()
        Dialogs.information(
            self, "Snapshot", "Snapshot of “%s” saved." % file_name)

    def takeProjectSnapshot(self):
        """Snapshot every file in the right-clicked project."""
        index = self.treewidget.currentIndex()
        project_path = str(index.sibling(index.row(), 1).data())
        if not os.path.isdir(project_path):
            Dialogs.warning(
                self, "Snapshot Failed", "Selected item is not a project.")
            return
        project_name = os.path.basename(os.path.normpath(project_path))
        try:
            _sid, count = SnapshotStore().create(
                project_name, project_path, label="Full backup")
        except Exception as exc:
            Dialogs.warning(self, "Snapshot Failed", str(exc))
            return

        self._refresh_snapshots()
        Dialogs.information(
            self, "Snapshot",
            "%d file(s) snapshotted for “%s”." % (count, project_name))

    def openSnapshotsPanel(self):
        """Open the Project Snapshots panel (main window's dock)."""
        win = self.window()
        if hasattr(win, 'show_snapshots'):
            win.show_snapshots()
        elif getattr(self, 'time_explorer', None) is not None:
            self.time_explorer.reload()
            self.time_explorer.show()

    def _refresh_snapshots(self):
        if getattr(self, 'time_explorer', None) is not None:
            self.time_explorer.reload()
