# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1087, 703)
        
        # --- GroupBox thông số ---
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 471, 311))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        
        # BMI
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(20, 50, 121, 41))
        font_lbl = QtGui.QFont()
        font_lbl.setPointSize(10)
        self.label_13.setFont(font_lbl)
        self.label_13.setObjectName("label_13")
        
        self.lineEdit_BMI = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_BMI.setGeometry(QtCore.QRect(200, 60, 231, 31))
        self.lineEdit_BMI.setFont(font_lbl)
        self.lineEdit_BMI.setReadOnly(True)
        self.lineEdit_BMI.setObjectName("lineEdit_BMI")

        # TDEE
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(20, 110, 111, 41))
        self.label_15.setFont(font_lbl)
        self.label_15.setObjectName("label_15")
        
        self.lineEdit_TDEE = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_TDEE.setGeometry(QtCore.QRect(200, 120, 231, 31))
        self.lineEdit_TDEE.setFont(font_lbl)
        self.lineEdit_TDEE.setReadOnly(True)
        self.lineEdit_TDEE.setObjectName("lineEdit_TDEE")
        
        # Lượng nước (ĐÂY LÀ BIẾN BỊ THIẾU KHIẾN APP BỊ LỖI)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(20, 170, 151, 41))
        self.label_14.setFont(font_lbl)
        self.label_14.setObjectName("label_14")
        
        self.lineEdit_Luongnuoc = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_Luongnuoc.setGeometry(QtCore.QRect(200, 180, 231, 31))
        self.lineEdit_Luongnuoc.setFont(font_lbl)
        self.lineEdit_Luongnuoc.setReadOnly(True)
        self.lineEdit_Luongnuoc.setObjectName("lineEdit_Luongnuoc")

        # Calo nạp hôm nay
        self.label_calo_hom_nay = QtWidgets.QLabel(self.groupBox)
        self.label_calo_hom_nay.setGeometry(QtCore.QRect(20, 230, 181, 41))
        self.label_calo_hom_nay.setFont(font_lbl)
        self.label_calo_hom_nay.setObjectName("label_calo_hom_nay")
        
        self.lineEdit_CaloHomNay = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_CaloHomNay.setGeometry(QtCore.QRect(200, 240, 231, 31))
        self.lineEdit_CaloHomNay.setFont(font_lbl)
        self.lineEdit_CaloHomNay.setReadOnly(True)
        self.lineEdit_CaloHomNay.setObjectName("lineEdit_CaloHomNay")

        # --- Khung Canvas chứa Biểu đồ ---
        # 1. Biểu đồ Cân nặng
        self.figure_weight = Figure(facecolor='#ffffff')
        self.chart_widget_cannang = FigureCanvas(self.figure_weight)
        self.chart_widget_cannang.setParent(Dialog)
        self.chart_widget_cannang.setGeometry(QtCore.QRect(500, 20, 551, 311))
        self.chart_widget_cannang.setObjectName("chart_widget_cannang")
        
        # 2. Biểu đồ Calo
        self.figure_calo = Figure(facecolor='#ffffff')
        self.chart_widget_calo = FigureCanvas(self.figure_calo)
        self.chart_widget_calo.setParent(Dialog)
        self.chart_widget_calo.setGeometry(QtCore.QRect(10, 350, 1041, 311))
        self.chart_widget_calo.setObjectName("chart_widget_calo")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Thống kê sức khỏe"))
        self.groupBox.setTitle(_translate("Dialog", "Thống kê sức khỏe "))
        self.label_13.setText(_translate("Dialog", "BMI hiện tại: "))
        self.label_15.setText(_translate("Dialog", "TDEE khuyến nghị: "))
        self.label_14.setText(_translate("Dialog", "Lượng nước cần uống: "))
        self.label_calo_hom_nay.setText(_translate("Dialog", "Calo đã nạp hôm nay: "))