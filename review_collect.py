from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from get_smartstore_review import get_review
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("리뷰 분석 프로그램")
        Dialog.resize(414, 246)
        Dialog.setStyleSheet("")
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(170, 190, 91, 31))
        self.ok.setStyleSheet("font: 12pt \"12롯데마트드림Medium\";")
        self.ok.setObjectName("ok")
        self.edit = QtWidgets.QTextEdit(Dialog)
        self.edit.setGeometry(QtCore.QRect(20, 110, 371, 51))
        self.edit.setObjectName("edit")
        self.info = QtWidgets.QLabel(Dialog)
        self.info.setGeometry(QtCore.QRect(80, 40, 271, 41))
        self.info.setStyleSheet("font: 9pt \"12롯데마트행복Bold\";")
        self.info.setScaledContents(False)
        self.info.setIndent(-1)
        self.info.setObjectName("info")
        self.ok.clicked.connect(self.btnClick)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def btnClick(self):
        url = self.edit.toPlainText() # 에디트 박스에서 URL를 받아옴
        print("\n>>>>>>> 리뷰 분석을 시작합니다. <<<<<<<\n")
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

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ok.setText(_translate("Dialog", "확인"))
        self.info.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">URL를 입력하세요!</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
