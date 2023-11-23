# hedaer = {
#     "Referer":"https://djsfenxiang.com/",
#     "Sec-Ch-Ua":'''"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"''',
#     "Sec-Ch-Ua-Mobile":"?1",
#     "Sec-Ch-Ua-Platform":'''"Android"''',
#     "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0"
# }
# datas = requests.get("https://djsfenxiang.com/api.txt",headers=hedaer)
# print(datas.content)



# 安装
# pip install pyqt5 -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
# pip install PyQtWebEngine -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
'''
:describate  Ganro的私人网络嗅探器
:date  2023/11/23 11:52
'''

#baseUrl = "https://djsfenxiang.com/"
baseUrl = "https://baidu.com"  # 请将此处替换为您的基础 URL
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import pyqtSignal, QObject
import threading
def QULRUNCODE(CODE):
    return str(CODE).replace("PyQt5.QtCore.QUrl('","")[:-2]

'''
ganro的私人使用网络请求拦截器
:param None
:return:Noen
'''
class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self,parent=None):
        self.List = []
        self.RequestAllInformation  = [] #保留了所有的数据的请求信息
        super().__init__(parent)
    def interceptRequest(self, info):
        #pass
        self.List.append(QULRUNCODE(info.requestUrl()))
        self.RequestAllInformation.append(info)
        #print("请求数据----->"+QULRUNCODE(info.requestUrl()))
    def ClearData(self):
        self.RequestAllInformation.clear()
        self.List.clear()


'''
用于JavaScript通讯
:param None
:return:Noen
'''

class JavaScriptRunner(QObject):
    # 创建一个信号
    runJavaScriptSignal = pyqtSignal(str)

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.JavaScriptReslut = []
        # 连接信号到槽函数
        self.runJavaScriptSignal.connect(self.runJavaScript)

    def runJavaScript(self, code):
        self.page.runJavaScript(code, self.handleJavaScriptResult)

    def handleJavaScriptResult(self, result):
        self.JavaScriptReslut.append(result)
        #print("JavaScript 返回值：", result)



'''
:param None
:return:Noen
'''
class HTML_WebRequest:
    def __init__(self) -> None:
        self.app = None
        self.view = None
        self.page = None
        self.Html = "" #当前页面HTML
        self.thread =None
        self.JavaScriptResult=[]
        self.javaScriptRunner = None
        self.StateReBuildListenClass = None
    '''
    主要用于判断状态，并绑定HTML代码记录函数
    :param ok: 请求状态
    :return:Noen
    '''
    def handleLoadFinished(self,ok):
        if ok:
            self.page.toHtml(self.handleHtml)
        else:
            print("Error")
    '''
    主要用于处理HTML数据，并进行记录
    :param html: HTML代码
    :return:Noen
    '''
    def handleHtml(self,html):
        #TODO HTML的处理函数，顺便
        #print(html)  # 这里将打印 HTML 内容
        #self.view.close()#获取完成结束
        #return html
        self.Html = html
    '''
    运行浏览器（阻塞）
    :param Url: 请求的URL
    :param hidden: 是否隐藏窗口（可选 默认False）
    :return:Noen
    '''
    def RunWebPropety(self,Url,hidden=False): #阻塞运行
            self.app = QApplication(sys.argv)
            self.view = QWebEngineView()
            self.page = QWebEnginePage()
            self.javaScriptRunner = JavaScriptRunner(self.page) 
            self.page.setUrl(QUrl(
        Url))
            self.StateReBuildListenClass = WebEngineUrlRequestInterceptor()
            self.page.profile().setRequestInterceptor(self.StateReBuildListenClass) #设置请求拦截器  获取请求信息
            self.page.loadFinished.connect(self.handleLoadFinished) #绑定渲染页面完成后的操作
            self.view.setPage(self.page)
            if(hidden):
                self.view.resize(0, 0)
            else:
                self.view.resize(600, 400)
            #now_url = self.page.url()
            #print(QULRUNCODE(now_url))
            self.view.show()
            sys.exit(self.app.exec_())
    '''
    运行浏览器（非阻塞）
    :param Url: 请求的URL
    :param hidden: 是否隐藏窗口（可选 默认False）
    :return:Noen
    '''
    def RunWeb(self,Url,hidden=False):#建立线程单独运行
        self.thread = threading.Thread(target=self.RunWebPropety,args=(Url,hidden))
        self.thread.start()
    '''
    运行当前浏览器地址
    :return:str 浏览器地址
    '''
    def GetNowWebUrl(self):#获取当前的Url:
        return self.page.url()
    '''
    重新设置浏览器地址
    :param Url: 请求的URL
    :return:None
    '''
    def ReSetUrl(self,Url): #重新定位网址
        self.page.setUrl(QUrl(
        Url))
    '''
    获取网页HTML代码
    :return:str HTML代码
    '''
    def GetHTML(self):#获取HTML
        return self.Html
    '''
    清理HTML代码
    :return:None
    '''
    def ClearHTML(self):#清除HTML
        self.Html = ""
    '''
    获取网页网络请求URL
    :return:list  Url列表
    '''
    def GetWebRequestUrl(self): #网页的网络请求Url
        return self.StateReBuildListenClass.List
    '''
    获取网页网络请求完整全部信息
    :return:list  网络请求完整全部信息
    '''
    def GetWebRequestFullInformation(self):
        return self.StateReBuildListenClass.RequestAllInformation
    '''
    清理网页网络请求记录
    :return:None
    '''
    def ClearWebRequest(self):
        self.StateReBuildListenClass.ClearData()
    '''
    关闭浏览器
    :return:None
    '''
    def CloseServer(self):
        self.view.close()
    '''
    获取JavaScript执行列表返回值
    :return:list  js返回值
    '''
    def GetJavaSctiptReslut(self):
        return self.javaScriptRunner.JavaScriptReslut
    '''
    清理JavaScript返回值列表
    :return:none
    '''
    def ClearJavaScriptReslut(self):
        self.javaScriptRunner.JavaScriptReslut = []
    '''
    执行JavaScript代码
    :param code: 执行的JavaScript代码
    :return:None
    '''
    def JavaScriptCode(self,code):
        self.javaScriptRunner.runJavaScriptSignal.emit(code)



def Example():
    TEST = HTML_WebRequest()
    TEST.RunWeb(baseUrl)
    # print(TEST.Html)
    import time
    #这边必须等待页面完全加载成功
    while(TEST.GetHTML()==""):
        time.sleep(0.5)
    print(TEST.GetHTML())
    print(TEST.GetWebRequestUrl())
    time.sleep(2)
    print("--------1--------")
    TEST.JavaScriptCode("document.title;")
    time.sleep(2)
    print("--------2--------")
    res = TEST.GetJavaSctiptReslut()
    print(res)
    print("----------------")
    print(type(res))
    TEST.CloseServer()
Example()
