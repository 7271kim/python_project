## Ex 3-5. 상태바 만들기.

import sys
import time

from io import BytesIO

from PIL import Image
import urllib.request
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QLineEdit, QPushButton, QMainWindow

from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.labelNaver = QLabel('네이버', self)
        self.labelNaver.setAlignment(Qt.AlignCenter)
        self.labelNaver.move(10, 30)

        self.inputNaver = QLineEdit(self)
        self.inputNaver.resize(500, 40)
        self.inputNaver.move(100, 20)

        self.btnNaver = QPushButton(self)
        self.btnNaver.setText('이미지 가져오기')
        self.btnNaver.resize(150, 40)
        self.btnNaver.move(630, 20)
        self.btnNaver.clicked.connect(self.clickNaver)

        self.labelCupang = QLabel('쿠팡', self)
        self.labelCupang.setAlignment(Qt.AlignCenter)
        self.labelCupang.move(10, 110)

        self.inputCupang = QLineEdit(self)
        self. inputCupang.resize(500, 40)
        self.inputCupang.move(100, 100)

        self.btnCupang = QPushButton(self)
        self.btnCupang.setText('이미지 가져오기')
        self.btnCupang.resize(150, 40)
        self.btnCupang.move(630, 100)
        self.btnCupang.clicked.connect(self.clickCupang)

        self.setWindowTitle('이미지 다 가져오기')
        self.resize(800, 200)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_concat_v(self, ori, past):
        full_width = max(ori.width, past.width)
        dst = Image.new('RGB', (full_width, ori.height + past.height))
        dst.paste(ori, (0, 0))
        dst.paste(past, (0, ori.height))
        return dst

    def clickCupang(self):
        self.statusBar().showMessage('progressing')

        print(self.inputCupang.text())
        driver = webdriver.Chrome(service=Service('./chromedriver_116.0.5845.96.exe'))
        driver.implicitly_wait(3)
        driver.get(self.inputCupang.text())
        driver.find_elements(By.CSS_SELECTOR, ".product-detail-seemore-btn")[0].click()

        images = driver.find_elements(By.CSS_SELECTOR,".product-detail-content-inside .vendor-item .subType-IMAGE img")
        titles = driver.find_elements(By.CSS_SELECTOR, ".prod-buy-header__title")
        fileName = titles[0].text

        img_url = []
        new_image = Image.new('RGB', (10, 10))

        for image in images:
            url = image.get_attribute('src')
            tmpImg = urllib.request.urlopen(url).read()
            time.sleep(0.1)
            image1 = Image.open(BytesIO(tmpImg)).convert('RGB')
            new_image = self.get_concat_v(new_image, image1)
            img_url.append(url)
            print(url)

        driver.quit()
        new_image.show()
        new_image.save("./(Cupang)"+fileName+".png", 'png')

        self.statusBar().showMessage('완료')
        self.inputCupang.setText('')

    def clickNaver(self):
        self.statusBar().showMessage('progressing')
        driver = webdriver.Chrome(service=Service('./chromedriver_116.0.5845.96.exe'))
        driver.implicitly_wait(3)
        driver.get(self.inputNaver.text())

        images = driver.find_elements(By.CSS_SELECTOR, ".se-main-container .se-image .se-module-image-link img")
        h3s = driver.find_elements(By.CSS_SELECTOR, "h3")
        fileName = h3s[0].text
        img_url = []
        new_image = Image.new('RGB', (10, 10))
        for image in images:
            url = image.get_attribute('data-src')
            tmpImg = urllib.request.urlopen(url).read()
            time.sleep(0.1)
            image1 = Image.open(BytesIO(tmpImg)).convert('RGB')
            new_image = self.get_concat_v(new_image, image1)
            img_url.append(url)
            print(url)

        driver.quit()
        new_image.show()
        new_image.save("./(Naver)"+fileName+".png", 'png')

        self.statusBar().showMessage('완료')
        self.inputNaver.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())