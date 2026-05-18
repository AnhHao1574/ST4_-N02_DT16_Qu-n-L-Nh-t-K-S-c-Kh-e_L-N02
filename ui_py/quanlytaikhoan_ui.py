from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView


class Ui_QuanLyTaiKhoan(object):

    def setupUi(self, Form):

        Form.setWindowTitle("Quản lý tài khoản")

        self.main_layout = QtWidgets.QVBoxLayout(Form)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(12)

        # ================= GROUP BOX =================
        self.form_box = QtWidgets.QGroupBox("Quản lý tài khoản")

        self.form_layout = QtWidgets.QGridLayout(self.form_box)
        self.form_layout.setContentsMargins(18, 28, 18, 18)
        self.form_layout.setHorizontalSpacing(14)
        self.form_layout.setVerticalSpacing(12)

        # ================= INPUT =================
        self.txtUsername = QtWidgets.QLineEdit()
        self.txtUsername.setPlaceholderText("Tên đăng nhập")

        self.txtPassword = QtWidgets.QLineEdit()
        self.txtPassword.setPlaceholderText("Mật khẩu")
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        self.cboRole = QtWidgets.QComboBox()
        self.cboRole.addItems(["user", "admin"])

        self.cboStatus = QtWidgets.QComboBox()
        self.cboStatus.addItems(["active", "locked"])

        # ================= LABEL =================
        self.form_layout.addWidget(QtWidgets.QLabel("Tên đăng nhập:"), 0, 0)
        self.form_layout.addWidget(self.txtUsername, 0, 1)

        self.form_layout.addWidget(QtWidgets.QLabel("Mật khẩu:"), 0, 2)
        self.form_layout.addWidget(self.txtPassword, 0, 3)

        self.form_layout.addWidget(QtWidgets.QLabel("Vai trò:"), 1, 0)
        self.form_layout.addWidget(self.cboRole, 1, 1)

        self.form_layout.addWidget(QtWidgets.QLabel("Trạng thái:"), 1, 2)
        self.form_layout.addWidget(self.cboStatus, 1, 3)

        # ================= BUTTON =================
        self.btnAdd = QtWidgets.QPushButton("Thêm")

        self.btnUpdate = QtWidgets.QPushButton("Sửa")

        self.btnDelete = QtWidgets.QPushButton("Xóa")
        self.btnDelete.setObjectName("btnDelete")

        self.btnReset = QtWidgets.QPushButton("Làm mới")

        self.button_layout = QtWidgets.QHBoxLayout()

        self.button_layout.addWidget(self.btnAdd)
        self.button_layout.addWidget(self.btnUpdate)
        self.button_layout.addWidget(self.btnDelete)
        self.button_layout.addWidget(self.btnReset)
        self.button_layout.addStretch()

        self.form_layout.addLayout(self.button_layout, 2, 0, 1, 4)

        # ================= TABLE =================
        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên đăng nhập",
            "Vai trò",
            "Trạng thái",
            "Số hồ sơ"
        ])

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        # ================= MAIN =================
        self.main_layout.addWidget(self.form_box, 0)
        self.main_layout.addWidget(self.table, 1)