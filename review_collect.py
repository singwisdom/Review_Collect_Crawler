from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt
from get_smartstore_review import get_review
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
        check_return = get_review(url)
        if check_return==2:
            self.info.setText("다른 URL을 입력해주세요")
            self.info.setFont(QtGui.QFont("나눔스퀘어OTF Bold",13)) # 폰트,크기 조절 
            self.info.setAlignment(Qt.AlignCenter) # 가운데 정렬
            self.info.setStyleSheet("Color : red") # 글자색 변환
        else :
            self.info.setText("리뷰 분석이 완료되었습니다.")
            self.info.setFont(QtGui.QFont("나눔스퀘어OTF Bold",14)) # 폰트,크기 조절 
            self.info.setAlignment(Qt.AlignCenter) # 가운데 정렬
            self.info.setStyleSheet("Color : green") # 글자색 변환

if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    sys.exit(app.exec_())