from PyQt5 import QtCore, QtWidgets
from data.database import get_connection
from styles.quanlytaikhoan_style import QUANLYTAIKHOAN_STYLE
from utils.quanlytaikhoan_utils import QuanLyTaiKhoanUtils
from ui_py.quanlytaikhoan_ui import Ui_QuanLyTaiKhoan

class QuanLyTaiKhoanScreen(QtWidgets.QWidget, QuanLyTaiKhoanUtils):
    def __init__(self, current_user=""):
        super().__init__()
        self.current_user = current_user
        self.quanlytaikhoan_utils = QuanLyTaiKhoanUtils()
        self.selected_user_id = None
        self.ui = Ui_QuanLyTaiKhoan()
        self.ui.setupUi(self)
        self.setStyleSheet(QUANLYTAIKHOAN_STYLE)

        # Kết nối sự kiện các nút bấm và chọn dòng trên bảng
        self.ui.btnAdd.clicked.connect(self.add_account)
        self.ui.btnUpdate.clicked.connect(self.update_account)
        self.ui.btnDelete.clicked.connect(self.delete_account)
        self.ui.btnReset.clicked.connect(self.reset_form)
        self.ui.table.itemSelectionChanged.connect(self.select_account)

        self.load_accounts()

    def load_accounts(self):
        rows = self.load_accounts_db()
        self.ui.table.setRowCount(0)
        for row_index, row_data in enumerate(rows):
            self.ui.table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.table.setItem(row_index, col_index, item)

    def select_account(self):
        selected = self.ui.table.selectedItems()
        if not selected:
            return

        row = selected[0].row()
        self.selected_user_id = int(self.ui.table.item(row, 0).text())
        self.ui.txtUsername.setText(self.ui.table.item(row, 1).text())
        self.ui.txtPassword.clear()
        self.ui.cboRole.setCurrentText(self.ui.table.item(row, 2).text())
        self.ui.cboStatus.setCurrentText(self.ui.table.item(row, 3).text())

    def account_data(self):
        username = self.ui.txtUsername.text().strip()
        password = self.ui.txtPassword.text().strip()
        role = self.ui.cboRole.currentText()
        status = self.ui.cboStatus.currentText().strip().lower()

        if not username:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập tên đăng nhập.")
            return None

        return username, password, role, status

    def add_account(self):
        data = self.account_data()
        if not data:
            return

        username, password, role, status = data
        if not password:
            QtWidgets.QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập mật khẩu khi thêm tài khoản.")
            return

        try:
            self.add_account_db(
                username,
                password,
                role,
                status
            )

            self.reset_form()
            self.load_accounts()

            QtWidgets.QMessageBox.information(
                self,
                "Thành công",
                "Đã thêm tài khoản."
            )

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể thêm tài khoản: {e}")

    def update_account(self):
        if not self.selected_user_id:
            QtWidgets.QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn tài khoản cần sửa.")
            return

        data = self.account_data()
        if not data:
            return

        username, password, role, status = data
        if username == self.current_user and role != "admin":
            QtWidgets.QMessageBox.warning(self, "Không hợp lệ", "Không thể tự hạ quyền admin của tài khoản đang đăng nhập.")
            return

        try:
            self.update_account_db(
                self.selected_user_id,
                username,
                password,
                role,
                status
            )

            self.reset_form()
            self.load_accounts()

            QtWidgets.QMessageBox.information(
                self,
                "Thành công",
                "Đã cập nhật tài khoản."
            )

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể cập nhật tài khoản: {e}")

    def delete_account(self):
        if not self.selected_user_id:
            QtWidgets.QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn tài khoản cần xóa.")
            return

        username = self.ui.txtUsername.text().strip()
        if username == self.current_user:
            QtWidgets.QMessageBox.warning(self, "Không hợp lệ", "Không thể xóa tài khoản đang đăng nhập.")
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn xóa tài khoản này không?"
        )
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        try:
            self.delete_account_db(self.selected_user_id)

            self.reset_form()
            self.load_accounts()

            QtWidgets.QMessageBox.information(
                self,
                "Thành công",
                "Đã xóa tài khoản."
            )

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể xóa tài khoản: {e}")

    def reset_form(self):
        self.selected_user_id = None
        self.ui.txtUsername.clear()
        self.ui.txtPassword.clear()
        self.ui.cboRole.setCurrentText("user")
        self.ui.cboStatus.setCurrentText("active")
        self.ui.table.clearSelection()
