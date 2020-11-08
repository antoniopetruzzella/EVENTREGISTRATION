import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, WebKit2
window = Gtk.Window()
window.maximize()
window.connect("destroy",Gtk.main_quit)
scrolled_window = Gtk.ScrolledWindow()
webview=WebKit2.WebView()
webview.load_uri("https://www.google.com")

scrolled_window.add(webview)
window.add(scrolled_window)
window.show_all()
Gtk.main()

