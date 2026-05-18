import json
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit

from data.database import get_connection
from styles.dangnhap_style import LOGIN_STYLE


# Hàm load_users và save_users để quản lý tài khoản trong file JSON
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}


class LoginScreen(QMainWindow):
    # Tín hiệu trả về (True/False, Username, Role)
    login_success = QtCore.pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.setMinimumSize(620, 620)

        # 1. Thiết lập hình nền cho toàn bộ cửa sổ Đăng nhập
        self.setStyleSheet(LOGIN_STYLE)
        # 2. Thiết lập giao diện cho các thành phần
        self.label.setText("Đăng nhập")
        self.txtUsername.setPlaceholderText("Nhập tên đăng nhập")
        self.txtPassword.setPlaceholderText("Nhập mật khẩu")
        self.btnLogin.setText("Đăng nhập")
        self.btnGoRegister.setText("Tạo tài khoản mới")
        self.btnTogglePassword.setText("👁")
        self.verticalLayout.setContentsMargins(70, 70, 70, 70)
        self.verticalLayout.setSpacing(18)

        self.btnLogin.clicked.connect(self.login)
        self.btnGoRegister.clicked.connect(self.open_register)
        self.btnTogglePassword.clicked.connect(self.toggle_password)

        self.is_password_visible = False

    def toggle_password(self):
        if self.is_password_visible:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.btnTogglePassword.setText("👁")
            self.is_password_visible = False
        else:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btnTogglePassword.setText("🙈")
            self.is_password_visible = True

    login_success = QtCore.pyqtSignal(str, str)

    def login(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text().strip()

        if username == "" or password == "":
            self.lblError.setText("Vui lòng nhập đầy đủ!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT username, role, COALESCE(status, 'active')
                FROM users
                WHERE username=? AND password=?
            """, (username, password))

            user = cursor.fetchone()
            conn.close()

            if user:

                # chuẩn hóa trạng thái
                status = str(user[2]).strip().lower()

                if status != "active":
                    self.lblError.setText("Tài khoản đã bị khóa!")
                    return

                self.login_success.emit(user[0], user[1])
                self.close()

            else:
                self.lblError.setText("Sai tài khoản hoặc mật khẩu!")

        except Exception as e:
            self.lblError.setText(f"Lỗi: {e}")
       
    def open_register(self):
        from screens.dangky import RegisterScreen
        self.reg = RegisterScreen()
        self.reg.show()
        self.close()
