import types
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
import xdot.ui
from precice.configvisualizer.common import configFileToDotCode
import cairo
from math import ceil

def makeVisibilityCombobox(callback, withMerged = True):
        cb = Gtk.ComboBoxText()
        cb.append_text("Show")
        if withMerged:
            cb.append_text("Merge")
        cb.append_text("Hide")
        cb.set_active(0)
        cb.connect("changed", callback)
        return cb

class ConfigVisualizerWindow(Gtk.Window):

    def __init__(self, filename=None):
        self._filename = filename;
        super().__init__(title="preCICE config visualizer")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        self.top = Gtk.Toolbar()
        self.box.pack_start(self.top, False, False, 0)
        self.tool_open=Gtk.ToolButton(stock_id=Gtk.STOCK_OPEN)
        self.tool_open.connect("clicked", self.on_open)
        self.tool_save=Gtk.ToolButton(stock_id=Gtk.STOCK_SAVE_AS)
        self.tool_save.connect("clicked", self.on_export)
        self.tool_copy=Gtk.ToolButton(stock_id=Gtk.STOCK_COPY)
        self.tool_copy.connect("clicked", self.on_copy)
        self.tool_refresh=Gtk.ToggleToolButton(stock_id=Gtk.STOCK_REFRESH, active=True)
        self.tool_refresh.connect("clicked", self.on_toogle_refresh)

        self.top.insert(self.tool_open, -1)
        self.top.insert(Gtk.SeparatorToolItem(), -1)
        self.top.insert(self.tool_save, -1)
        self.top.insert(self.tool_copy, -1)
        self.top.insert(Gtk.SeparatorToolItem(), -1)
        self.top.insert(self.tool_refresh, -1)

        self.dotwidget = xdot.ui.DotWidget()
        self.dotwidget.connect("error", lambda e, m: self.error_dialog(m))
        self.box.pack_start(self.dotwidget, True, True, 0)

        self.bottom = Gtk.Box(spacing=4)
        self.box.pack_start(self.bottom, False, False, 0)

        self.data_access = makeVisibilityCombobox(self.on_option_change);
        self.data_exchange = makeVisibilityCombobox(self.on_option_change);
        self.communicators = makeVisibilityCombobox(self.on_option_change);
        self.cplschemes = makeVisibilityCombobox(self.on_option_change);
        # TODO add toogles
        #self.watchpoints = makeVisibilityCombobox(self.on_option_change,False);
        #self.exporters = makeVisibilityCombobox(self.on_option_change,False);

        optionsRow = [
            Gtk.Label(label="Data access"),
            self.data_access,
            Gtk.Separator(),
            Gtk.Label(label="Data exchange"),
            self.data_exchange,
            Gtk.Separator(),
            Gtk.Label(label="Communicators"),
            self.communicators,
            Gtk.Separator(),
            Gtk.Label(label="Couplig schemes"),
            self.cplschemes,
            #Gtk.Separator(),
            #Gtk.Label(label="Watchpoints"),
            #self.watchpoints,
            #Gtk.Separator(),
            #Gtk.Label(label="Exporters"),
            #self.exporters,
        ]
        for x in optionsRow:
            self.bottom.pack_start(x, False, False, 0)
        self.show_all()
        self.reload()
        self.monitor()

    def on_file_change(self, m, f, o, event):
        if self.tool_refresh.get_active() and event == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.reload()

    def monitor(self):
        # No filename given?
        if self._filename is None:
            self._monitor = None
            return

        file = Gio.File.new_for_path(self._filename)
        self._monitor = file.monitor_file(Gio.FileMonitorFlags.NONE, None)
        self._monitor.connect("changed", self.on_file_change)


    def reload(self):
        if self._filename is None:
            self.dotwidget.set_dotcode("")
            return

        def getVisibilty(cb):
            return {
                "Show" : 'full',
                "Merge": 'merged',
                "Hide": 'hide',
            }[cb.get_active_text()]

        args = types.SimpleNamespace(
            data_access=getVisibilty(self.data_access),
            data_exchange=getVisibilty(self.data_exchange),
            communicators=getVisibilty(self.communicators),
            cplschemes=getVisibilty(self.cplschemes),
            no_watchpoints=False,
            no_colors=False,
        )

        dot = configFileToDotCode(self._filename, args)
        self.dotwidget.set_dotcode(dot.encode())

    def on_open(self, caller):
        dialog = Gtk.FileChooserDialog(
            title="Choose preCICE configuration",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK)

        filter = Gtk.FileFilter()
        filter.set_name("XML files")
        filter.add_mime_type("text/xml")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._filename = dialog.get_filename()
            self.reload()
            self.monitor()
        dialog.destroy()

    def on_copy(self, caller):
        width, height = map(ceil, self.dotwidget.graph.get_size())
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        self.dotwidget.graph.draw(ctx)
        pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(pixbuf)
        clipboard.store()

    def on_export(self, caller):
        dialog = Gtk.FileChooserDialog(
            "Save As Image",
            None,
            Gtk.FileChooserAction.SAVE,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE, Gtk.ResponseType.OK
            )
        )

        filter_image = Gtk.FileFilter()
        filter_image.set_name("PNG images")
        filter_image.add_mime_type("image/png")
        dialog.add_filter(filter_image)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            width, height = map(ceil, self.dotwidget.graph.get_size())
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            ctx = cairo.Context(surface)
            self.dotwidget.graph.draw(ctx)
            surface.write_to_png(filename)

        dialog.destroy()

    def on_toogle_refresh(self, caller):
        if self.tool_refresh.get_active():
            self.reload()

    def on_option_change(self, caller):
        self.reload()
