from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui
from smartstore_review import get_review
import sys

# UI 파일을 불러옴
form_class = uic.loadUiType("get_store.ui")[0]

class MyWindow(QMainWindow, form_class):
    
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.ok.clicked.connect(self.btnClick)

    def btnClick(self):
        
        url = self.edit.toPlainText() # 에디트 박스에서 URL를 받아옴
        get_review(url)
        self.info.setText("작업 완료")
        self.info.setFont(QtGui.QFont("12롯데마트행복Bold",17)) #폰트,크기 조절 
        self.info.setStyleSheet("Color : green") #글자색 변환

if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    sys.exit(app.exec_())




