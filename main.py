import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream

# Import UI từ file sidebar
from screens.dangnhap import LoginScreen
from utils.sidebar_ui import Ui_MainWindow

# Import màn hình Nhật ký ăn uống của bạn
from screens.nhatkyanuong import NhatKyAnUongScreen
from screens.hososuckhoe import HoSoSucKhoeScreen
from screens.thongkesuckhoe import ThongKeSucKhoeScreen
from screens.quanlytaikhoan import QuanLyTaiKhoanScreen
from data.database import get_connection
from screens.users import UsersScreen

def open_main(username, role):
    global window

    window = MainWindow(username, role)
    window.show()

class MainWindow(QMainWindow):
    def __init__(self, username, role):
        super(MainWindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_user = username
        self.current_role = role
        self.configure_responsive_main_window()

        self.ho_so_id = self.lay_ho_so_id()

        if self.ho_so_id is None and self.current_role != "admin":

            self.ui.ThongKe_btn_1.hide()
            self.ui.ThongKe_btn_2.hide()

            self.ui.NhatKy_btn_1.hide()
            self.ui.NhatKy_btn_2.hide()

            self.ui.HoSo_btn_1.hide()
            self.ui.HoSo_btn_2.hide()

        self.ui.user_btn.setText(self.current_user)
        self.ui.user_btn.setMinimumWidth(180)
        # --- KHỞI TẠO VÀ NHÚNG CÁC MÀN HÌNH ---
        
        # 1. Nhật ký ăn uống
        self.screen_nhatky_anuong = NhatKyAnUongScreen(self.current_user, self.current_role)
        # Kiểm tra và thêm vào layout của page
        if self.ui.page.layout() is None:
            # Nếu trong Designer chưa có layout, ta tạo mới
            layout = QVBoxLayout(self.ui.page)
            layout.setContentsMargins(0, 0, 0, 0)
            self.ui.page.setLayout(layout)

        self.ui.page.layout().addWidget(self.screen_nhatky_anuong)
        self.screen_nhatky_anuong.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.setMinimumSize(1200, 700)
        # 2. Hồ sơ sức khỏe
        self.screen_hoso = HoSoSucKhoeScreen(self.current_user, role=self.current_role)
        if self.ui.page_2.layout() is None:
            layout_page2 = QtWidgets.QVBoxLayout(self.ui.page_2)
            layout_page2.setContentsMargins(0, 0, 0, 0)
            self.ui.page_2.setLayout(layout_page2)

        self.ui.page_2.layout().addWidget(self.screen_hoso)
        self.setMinimumSize(1200, 700)

        # 3. Thống kê sức khỏe
        self.screen_thongke = ThongKeSucKhoeScreen(None)
        if self.ui.page_3.layout() is None:
            layout_page3 = QtWidgets.QVBoxLayout(self.ui.page_3)
            layout_page3.setContentsMargins(0, 0, 0, 0)
            self.ui.page_3.setLayout(layout_page3)
        self.ui.page_3.layout().addWidget(self.screen_thongke)

        # 4. Quan ly tai khoan: chi admin duoc thay menu nay.
        self.screen_quanly_taikhoan = QuanLyTaiKhoanScreen(self.current_user)
        if self.ui.page_4.layout() is None:
            layout_page4 = QtWidgets.QVBoxLayout(self.ui.page_4)
            layout_page4.setContentsMargins(0, 0, 0, 0)
            self.ui.page_4.setLayout(layout_page4)
        self.ui.page_4.layout().addWidget(self.screen_quanly_taikhoan)

        # 5. Trang thông tin người dùng (Đã tách riêng thành class)
        self.screen_thongtin_user = UsersScreen(self.current_user, self.current_role)
        if self.ui.page_7.layout() is None:
            layout_page7 = QtWidgets.QVBoxLayout(self.ui.page_7)
            layout_page7.setContentsMargins(0, 0, 0, 0)
            self.ui.page_7.setLayout(layout_page7)

        self.ui.page_7.layout().addWidget(self.screen_thongtin_user)

        # --- CẤU HÌNH BAN ĐẦU ---
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0) # Mở trang Nhật ký đầu tiên
        self.ui.NhatKy_btn_1.setChecked(True)
        self.phan_quyen()

        # Ngắt kết nối mặc định (chỉ đóng ứng dụng) từ file UI
        try:
            self.ui.exit_btn_1.clicked.disconnect()
            self.ui.exit_btn_2.clicked.disconnect()
        except TypeError:
            pass # Phòng trường hợp chưa được kết nối

        # Kết nối tới hàm xử lý đăng xuất
        self.ui.exit_btn_1.clicked.connect(self.on_exit_clicked)
        self.ui.exit_btn_2.clicked.connect(self.on_exit_clicked)

    def configure_responsive_main_window(self):
        self.setMinimumSize(1200, 700)
        self.ui.gridLayout.setColumnStretch(0, 0)
        self.ui.gridLayout.setColumnStretch(1, 0)
        self.ui.gridLayout.setColumnStretch(2, 1)
        self.ui.verticalLayout_5.setStretch(0, 0)
        self.ui.verticalLayout_5.setStretch(1, 1)
        self.ui.stackedWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.ui.search_input.setMinimumWidth(260)
        self.ui.search_input.setMaximumWidth(520)
        self.ui.user_btn.setMinimumWidth(160)

        for page in [
            self.ui.page,
            self.ui.page_2,
            self.ui.page_3,
            self.ui.page_4,
            self.ui.page_5,
            self.ui.page_6,
            self.ui.page_7,
        ]:
            page.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding
            )
            
    ## Function for searching
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        if hasattr(self, 'screen_thongtin_user'):
            self.screen_thongtin_user.load_user_info()
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## ĐIỀU HƯỚNG MENU
    def on_NhatKy_btn_1_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(0)
            # Cập nhật lại dữ liệu mỗi khi nhấn vào nút
            if hasattr(self.screen_nhatky_anuong, 'LayDuLieuAnUong'):
                self.screen_nhatky_anuong.LayDuLieuAnUong()
    
    def on_NhatKy_btn_2_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(0)
            if hasattr(self.screen_nhatky_anuong, 'LayDuLieuAnUong'):
                self.screen_nhatky_anuong.LayDuLieuAnUong()

    def on_HoSo_btn_1_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(1)
            if hasattr(self.screen_hoso, 'LayDuLieuHoSo'):
                self.screen_hoso.LayDuLieuHoSo()

    def on_HoSo_btn_2_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(1)
            if hasattr(self.screen_hoso, 'LayDuLieuHoSo'):
                self.screen_hoso.LayDuLieuHoSo()

    def on_ThongKe_btn_1_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(2)
            self.ho_so_id = self.lay_ho_so_id()

            self.screen_thongke.set_ho_so_id(self.ho_so_id)
    def on_ThongKe_btn_2_toggled(self, checked):
        if checked: self.ui.stackedWidget.setCurrentIndex(2)

    def on_QuanLyTaiKhoan_btn_1_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(3)
            if hasattr(self.screen_quanly_taikhoan, "load_accounts"):
                self.screen_quanly_taikhoan.load_accounts()

    def on_QuanLyTaiKhoan_btn_2_toggled(self, checked):
        if checked:
            self.ui.stackedWidget.setCurrentIndex(3)
            if hasattr(self.screen_quanly_taikhoan, "load_accounts"):
                self.screen_quanly_taikhoan.load_accounts()

    # Phân quyền hiển thị menu dựa trên vai trò người dùng
    def phan_quyen(self):
        if self.current_role == "user":
            # ẩn menu quản lý tài khoản
            self.ui.QuanLyTaiKhoan_btn_1.hide()
            self.ui.QuanLyTaiKhoan_btn_2.hide()

        elif self.current_role == "admin":
            self.ui.QuanLyTaiKhoan_btn_1.show()
            self.ui.QuanLyTaiKhoan_btn_2.show()
            self.ui.ThongKe_btn_1.hide()

    def on_exit_clicked(self):
        # Mở lại màn hình đăng nhập
        self.login_window = LoginScreen()

        # Khi đăng nhập thành công -> mở MainWindow mới
        self.login_window.login_success.connect(open_main)
        self.login_window.show()

        # Đóng cửa sổ hiện tại
        self.close()

    def lay_ho_so_id(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id
            FROM ho_so
            WHERE user_id = (
                SELECT id
                FROM users
                WHERE username=?
            )
        """, (self.current_user,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0]

        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load QSS
    style_file = QFile("style.qss")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        style_stream = QTextStream(style_file)
        app.setStyleSheet(style_stream.readAll())

    # Mở Login trước
    from screens.dangnhap import LoginScreen
    login = LoginScreen()

    # Đăng nhập thành công mới mở Main
    login.login_success.connect(open_main)
    login.show()

    sys.exit(app.exec())