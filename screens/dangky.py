import json
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget

from data.database import get_connection
from styles.dangky_style import REGITER_STYLE


# Hàm load_users và save_users để quản lý tài khoản trong file JSON
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

# Hàm lưu người dùng mới vào file JSON
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Màn hình đăng ký
class RegisterScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
        self.setMinimumSize(620, 650)
        #thiết kế hình nền cho toàn bộ cửa sổ Đăng ký 
        self.setStyleSheet(REGITER_STYLE)
        #thiết lập giao diện cho các thành phần
        self.label.setText("Đăng ký")
        self.txtUsername.setPlaceholderText("Nhập tên đăng nhập")
        self.txtPassword.setPlaceholderText("Nhập mật khẩu")
        self.txtConfirmPassword.setPlaceholderText("Nhập lại mật khẩu")
        self.btnRegister.setText("Đăng ký")
        self.btnBackLogin.setText("Quay lại đăng nhập")
        self.btnTogglePassword.setText("👁")
        self.btnToggleConfirm.setText("👁")
        self.verticalLayout.setContentsMargins(70, 60, 70, 60)
        self.verticalLayout.setSpacing(16)

        self.btnRegister.clicked.connect(self.register)

        self.btnBackLogin.clicked.connect(self.back_login)
        self.btnTogglePassword.clicked.connect(self.toggle_password)
        self.btnToggleConfirm.clicked.connect(self.toggle_confirm)

        self.is_password_visible = False
        self.is_confirm_visible = False

# Hàm toggle_password và toggle_confirm để ẩn/hiện mật khẩu và xác nhận mật khẩu
    def toggle_password(self):
        if self.is_password_visible:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.btnTogglePassword.setText("👁")
            self.is_password_visible = False
        else:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btnTogglePassword.setText("🙈")
            self.is_password_visible = True
# Hàm toggle_confirm để ẩn/hiện mật khẩu xác nhận
    def toggle_confirm(self):
        if self.is_confirm_visible:
            self.txtConfirmPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.btnToggleConfirm.setText("👁")
            self.is_confirm_visible = False
        else:
            self.txtConfirmPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btnToggleConfirm.setText("🙈")
            self.is_confirm_visible = True
# Hàm register để xử lý logic đăng ký tài khoản mới
    def register(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text().strip()
        confirm = self.txtConfirmPassword.text().strip()

        if username == "" or password == "":
            self.lblError.setText("Không được để trống!")
            return

        if len(password) < 6:
            self.lblError.setText("Mật khẩu >= 6 ký tự!")
            return

        if password != confirm:
            self.lblError.setText("Mật khẩu không khớp!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE username=?",
                (username,)
            )

            if cursor.fetchone():
                self.lblError.setText("Tài khoản đã tồn tại!")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO users(username,password,role)
                VALUES(?,?,?)
            """, (username, password, "user"))

            conn.commit()
            conn.close()

            self.lblError.setText("Đăng ký thành công!")

        except Exception as e:
            self.lblError.setText(f"Lỗi: {e}")
            return

        self.lblError.setText("Đăng ký thành công!")

    def back_login(self):
        from screens.dangnhap import LoginScreen
        self.login = LoginScreen()
        self.login.show()
        self.close()
