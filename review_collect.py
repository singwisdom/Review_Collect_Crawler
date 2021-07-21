from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from save_exel import save_to_excel_file
from get_smartstore_review import get_review
from send_email import send_success_mail, send_fail_mail
from tqdm import tqdm
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(531, 495)
        font = QtGui.QFont()
        font.setUnderline(False)
        Dialog.setFont(font)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("")
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(220, 430, 81, 41))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.ok.setFont(font)
        self.ok.setStyleSheet("font: 75 12pt \"나눔스퀘어 Bold\";")
        self.ok.setObjectName("ok")
        self.find = QtWidgets.QTextEdit(Dialog)
        self.find.setGeometry(QtCore.QRect(30, 80, 471, 271))
        self.find.setObjectName("find")
        self.find_info = QtWidgets.QLabel(Dialog)
        self.find_info.setGeometry(QtCore.QRect(170, 30, 231, 31))
        self.find_info.setStyleSheet("font: 75 18pt \"나눔스퀘어OTF Bold\";")
        self.find_info.setScaledContents(False)
        self.find_info.setIndent(-1)
        self.find_info.setObjectName("find_info")
        self.email_info = QtWidgets.QLabel(Dialog)
        self.email_info.setGeometry(QtCore.QRect(20, 380, 81, 31))
        self.email_info.setStyleSheet("font: 75 18pt \"나눔스퀘어OTF Bold\";")
        self.email_info.setScaledContents(False)
        self.email_info.setIndent(-1)
        self.email_info.setObjectName("email_info")
        self.email = QtWidgets.QTextEdit(Dialog)
        self.email.setGeometry(QtCore.QRect(110, 370, 391, 41))
        self.email.setObjectName("email")

        self.ok.clicked.connect(self.btnClick) # 확인 버튼 이벤트 등록
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def btnClick(self):
        url = self.find.toPlainText().split('\n') # 에디트 박스에서 URL를 받아옴
        receiver = self.email.toPlainText() # 에디트 박스에서 이메일 주소를 받아옴

        print("\n>>>>>>> 리뷰 분석을 시작합니다. <<<<<<<\n")

        for count in tqdm(range(0, len(url)), desc="리뷰 분석 진행상황"):

            print("\n\n분석중인 URL : "+ url[count])
            return_value = get_review(url[count], count) 
            is_smartstore = return_value

            if is_smartstore==False:
                send_fail_mail(receiver, url[count])
                self.find_info.setText("다른 URL을 입력해주세요")
                self.find_info.setFont(QtGui.QFont("나눔스퀘어OTF Bold",13)) # 폰트,크기 조절 
                self.find_info.setAlignment(Qt.AlignCenter) # 가운데 정렬
                self.find_info.setStyleSheet("Color : red") # 글자색 변환
                break

        if is_smartstore==True:
            print("\n>> 모든 작업이 끝났습니다. 엑셀파일로 변환됩니다. <<")    
            send_success_mail(receiver, url)
            self.find_info.setText("리뷰 분석이 완료되었습니다.")
            self.find_info.setFont(QtGui.QFont("나눔스퀘어OTF Bold",14)) # 폰트,크기 조절 
            self.find_info.setAlignment(Qt.AlignCenter) # 가운데 정렬
            self.find_info.setStyleSheet("Color : green") # 글자색 변환
                
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "리뷰 분석 프로그램"))
        self.ok.setText(_translate("Dialog", "확인"))
        self.find_info.setText(_translate("Dialog", "<html><head/><body><p>URL를 입력하세요!</p></body></html>"))
        self.email_info.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">이메일</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
