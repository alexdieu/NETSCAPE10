from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: green;") 
        self.pbar = QProgressBar()
        self.pbar.setMaximumWidth(120)

        self.browser=QWebEngineView(loadProgress=self.pbar.setValue, loadFinished=self.pbar.hide,loadStarted=self.pbar.show, titleChanged=self.setWindowTitle)
        self.browser.setUrl(QUrl("https://duckduckgo.com/"))
        self.setCentralWidget(self.browser)

        self.browser.page().linkHovered.connect(self.if_link_hover)
        
        self.browser.setMinimumSize(500, 500)
        self.status = self.statusBar()
        self.status.addPermanentWidget(self.pbar)

        self.show()
        self.setWindowTitle("Netscape v10 BETA !")
        self.setWindowIcon(QIcon("net.png"))

        tb2 = QToolBar("Shortcuts :")
        tb2.setIconSize(QSize(45,45))
        self.addToolBar(Qt.RightToolBarArea,tb2)

        y_btn = QAction(QIcon("yahoo.png"), "Yahoo!", self)
        y_btn.setStatusTip("Go to Yahoo")
        y_btn.triggered.connect(lambda: self.conn("https://fr.yahoo.com/"))
        tb2.addAction(y_btn)
        
        git_btn = QAction(QIcon("github.png"), "Github", self)
        git_btn.setStatusTip("Go to Github")
        git_btn.triggered.connect(lambda: self.conn("https://github.com"))
        tb2.addAction(git_btn)

        tb=QToolBar("Navigation")
        tb.setIconSize(QSize(25,25))
        self.addToolBar(tb)

        win_btn = QAction(QIcon("nouvfenetre.gif"), "Nouvelle fenetre", self)
        win_btn.setStatusTip("New window")
        win_btn.triggered.connect(self.new_win)
        tb.addAction(win_btn)

        tb.addSeparator()

        back_btn=QAction(QIcon("AV.gif"),"Retour",self)
        back_btn.setStatusTip("Get back")
        back_btn.triggered.connect(self.browser.back)
        tb.addAction(back_btn)


        fwd_btn = QAction(QIcon("AP.gif"), "Après", self)
        fwd_btn.setStatusTip("Get forward")
        fwd_btn.triggered.connect(self.browser.forward)
        tb.addAction(fwd_btn)

        home_btn = QAction(QIcon("home.gif"), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.gohome)
        tb.addAction(home_btn)

        rld_btn = QAction(QIcon("recharge.gif"), "Régénerer", self)
        rld_btn.setStatusTip("Reload page")
        rld_btn.triggered.connect(self.browser.reload)
        tb.addAction(rld_btn)
        
        self.urlbar=QLineEdit()
        tb.addSeparator()
        self.urlbar.returnPressed.connect(self.navigate_page)
        tb.addWidget(self.urlbar)

        self.browser.urlChanged.connect(self.update_url)

        stop_btn=QAction(QIcon("stop.gif"),"Stop",self)
        stop_btn.setStatusTip("Stop loading page")
        stop_btn.triggered.connect(self.browser.stop)
        tb.addAction(stop_btn)

        self.statusBar().showMessage('Netscape v10 BETA')
        self.show()

    def new_win(self):
        windo = MainWindow()
        windo.show()

    def update_url(self,q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def gohome(self):
        self.browser.setUrl(QUrl("https://duckduckgo.com/"))

    def navigate_page(self):
        q=QUrl(self.urlbar.text())
        t=self.urlbar.text()
        if "." not in t:
            t='https://duckduckgo.com/?q='+t
            self.browser.setUrl(QUrl(t))
        elif q.scheme()=="":
            q.setScheme("http")
            self.browser.setUrl(q)
        else:
            self.browser.setUrl(q)

    def conn(self,s):
        self.browser.setUrl(QUrl(s))

    def if_link_hover(self, l):
        self.status.showMessage(l)

app=QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec())
