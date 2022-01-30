import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
def QULRUNCODE(CODE):
    return str(CODE).replace("PyQt5.QtCore.QUrl('","")[:-2]
class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
    def interceptRequest(self, info):
        #pass
        print("请求数据----->"+QULRUNCODE(info.requestUrl()))
        #,info.requestMethod(),info.resourceType(),info.firstPartyUrl()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QWebEngineView()
    page = QWebEnginePage()
    page.setUrl(QUrl(
 "https://music.163.com/"))
    t = WebEngineUrlRequestInterceptor()
    page.profile().setRequestInterceptor(t)
    view.setPage(page)
    view.resize(600, 400)
    now_url = page.url()
    print(QULRUNCODE(now_url))
    view.show()
    sys.exit(app.exec_())
