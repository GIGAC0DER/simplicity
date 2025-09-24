from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Persistent storage
        storage_path = os.path.join(os.getcwd(), "simplicity_data")
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        # Persistent profile
        self.profile = QWebEngineProfile("SimplicityProfile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setCachePath(storage_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Add first tab
        self.add_new_tab(QUrl("https://gigac0der.github.io/simplicity/index.html"), "Home")

        # Toolbar
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(28,28))
        self.addToolBar(navtb)

        # Styling (keep modern look)
        navtb.setStyleSheet("""
            QToolBar { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #222, stop:1 #111); border:none; padding:6px; spacing:10px; }
            QToolButton { background: rgba(255,255,255,0.07); border-radius:10px; padding:8px; color:white; }
            QToolButton:hover { background: rgba(255,255,255,0.15); }
            QLineEdit { background: rgba(30,30,30,0.8); border-radius:15px; padding:8px 14px; color:white; font-size:14px; }
            QLineEdit:focus { border:1px solid #00ffaa; }
        """)

        # Navigation buttons
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.go_back)
        navtb.addAction(back_btn)

        next_btn = QAction("➡️", self)
        next_btn.triggered.connect(self.go_forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("🔄", self)
        reload_btn.triggered.connect(self.reload_tab)
        navtb.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        new_tab_btn = QAction("➕", self)
        new_tab_btn.setStatusTip("Open new tab")
        new_tab_btn.triggered.connect(self.add_blank_tab)
        navtb.addAction(new_tab_btn)

        navtb.addSeparator()

        # URL bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("✖️", self)
        stop_btn.triggered.connect(self.stop_loading)
        navtb.addAction(stop_btn)

        # Window
        self.setWindowTitle("Simplicity ⚡ Browser")
        self.resize(1200,720)
        self.setStyleSheet("QMainWindow { background: #111; color:white; }")
        self.show()

        # Update URL bar when tab changes
        self.tabs.currentChanged.connect(self.update_urlbar_tab)

    # Add a new tab
    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://gigac0der.github.io/simplicity/index.html")
        browser = QWebEngineView()
        browser.setPage(QWebEnginePage(self.profile, browser))
        browser.setUrl(qurl)
        browser.urlChanged.connect(lambda q, b=browser: self.update_urlbar(q, b))
        browser.loadFinished.connect(lambda _, b=browser: self.update_tab_title(b))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def add_blank_tab(self):
        self.add_new_tab()

    # Close tab
    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    # Navigation functions
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://gigac0der.github.io/simplicity/index.html"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def go_back(self):
        self.tabs.currentWidget().back()

    def go_forward(self):
        self.tabs.currentWidget().forward()

    def reload_tab(self):
        self.tabs.currentWidget().reload()

    def stop_loading(self):
        self.tabs.currentWidget().stop()

    # Update URL bar
    def update_urlbar(self, q=None, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_tab_title(self, browser):
        i = self.tabs.indexOf(browser)
        if i >= 0:
            title = browser.page().title()
            self.tabs.setTabText(i, title)
            self.setWindowTitle(f"{title} - Simplicity ⚡ Browser")

    def update_urlbar_tab(self, i):
        q = self.tabs.currentWidget().url()
        self.urlbar.setText(q.toString())

# Run
app = QApplication(sys.argv)
app.setApplicationName("Simplicity ⚡ Browser")
window = MainWindow()
app.exec_()
