import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QToolBar, QPushButton, QLineEdit, QLabel, QTabWidget)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
from urllib.request import urlopen
from io import BytesIO

class BrowserTab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.macbines.com/macbines"))

class MacBinesExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MacBines Explorer")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Toolbar
        self.toolbar = QToolBar("Navigation")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Navigation Buttons
        self.add_nav_button("Home", "https://upload.wikimedia.org/wikipedia/commons/6/64/Home_icon_2012.png", self.navigate_home)
        self.add_nav_button("Refresh", "https://upload.wikimedia.org/wikipedia/commons/3/3a/Refresh_icon_2012.png", self.refresh_page)
        self.add_nav_button("Back", "https://upload.wikimedia.org/wikipedia/commons/9/90/Back_icon_2012.png", self.navigate_back)
        self.add_nav_button("Forward", "https://upload.wikimedia.org/wikipedia/commons/2/2f/Forward_icon_2012.png", self.navigate_forward)
        self.add_nav_button("Gmail", "https://icon-library.com/images/gmail-icon-svg/gmail-icon-svg-28.jpg", self.navigate_gmail)
        self.add_nav_button("YouTube", "https://upload.wikimedia.org/wikipedia/commons/2/21/YouTube_icon_%282011-2013%29.svg", self.navigate_youtube)
        self.add_nav_button("Bing", "https://static.wikia.nocookie.net/logopedia/images/0/03/Bing_2009_favicon.svg/revision/latest?cb=20160514134627", self.navigate_bing)
        self.add_nav_button("MSN", "https://static.wikia.nocookie.net/logopedia/images/9/92/MSN_logo.svg/revision/latest?cb=20220608144358", self.navigate_msn)
        self.add_nav_button("Amazon", "https://i.pinimg.com/originals/01/ca/da/01cada77a0a7d326d85b7969fe26a728.jpg", self.navigate_amazon)
        self.add_nav_button("Facebook", "https://static.wikia.nocookie.net/logopedia/images/0/0f/Facebook_%282005-2012%29.svg/revision/latest/scale-to-width-down/1000?cb=20161012152350", self.navigate_facebook)
        self.add_nav_button("Twitter", "https://upload.wikimedia.org/wikipedia/sco/9/9f/Twitter_bird_logo_2012.svg", self.navigate_twitter)

        # New Tab Button
        self.add_nav_button("New Tab", "https://upload.wikimedia.org/wikipedia/commons/6/64/Home_icon_2012.png", self.new_tab)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        self.toolbar.addWidget(self.url_bar)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        main_layout.addWidget(self.tabs)
        
        # Add first tab
        self.add_new_tab(QUrl("https://www.macbines.com/macbines"), "New Tab")

    def add_nav_button(self, text, icon_url, function):
        button = QPushButton()
        button.setIcon(self.load_icon_from_url(icon_url))
        button.setText(text)
        button.setStyleSheet("background-color: #1a73e8; color: white; padding: 10px; border: none; display: flex; flex-direction: column; align-items: center;")
        button.setToolTip(text)
        button.clicked.connect(function)
        self.toolbar.addWidget(button)

    def load_icon_from_url(self, url):
        try:
            data = urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            return QIcon(pixmap)
        except:
            return QIcon()

    def add_new_tab(self, qurl, label):
        browser = BrowserTab()
        browser.setUrl(qurl)
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        browser.urlChanged.connect(lambda url, br=browser: self.update_tab_title(url, br))

    def new_tab(self):
        self.add_new_tab(QUrl("https://www.newtab.macbines.com/newtab"), "New Tab")

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_tab_title(self, url, browser):
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, url.host() or "New Tab")

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://www.macbines.com/macbines"))

    def refresh_page(self):
        self.current_browser().reload()

    def navigate_gmail(self):
        self.current_browser().setUrl(QUrl("https://mail.google.com"))

    def navigate_youtube(self):
        self.current_browser().setUrl(QUrl("https://www.youtube.com"))

    def navigate_bing(self):
        self.current_browser().setUrl(QUrl("https://www.bing.com"))
    
    def navigate_msn(self):
        self.current_browser().setUrl(QUrl("https://www.msn.com"))
    
    def navigate_amazon(self):
        self.current_browser().setUrl(QUrl("https://www.amazon.com"))
    
    def navigate_facebook(self):
        self.current_browser().setUrl(QUrl("https://www.facebook.com"))
    
    def navigate_twitter(self):
        self.current_browser().setUrl(QUrl("https://www.twitter.com"))

    def navigate_back(self):
        if self.current_browser().history().canGoBack():
            self.current_browser().back()

    def navigate_forward(self):
        if self.current_browser().history().canGoForward():
            self.current_browser().forward()

    def navigate_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self, index):
        if index >= 0:
            url = self.current_browser().url().toString()
            self.url_bar.setText(url)

    def current_browser(self):
        return self.tabs.currentWidget()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MacBinesExplorer()
    window.show()
    sys.exit(app.exec_())
