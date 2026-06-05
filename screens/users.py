# screens/users.py
from PyQt5 import QtWidgets, QtCore
from data.database import get_connection
from styles.users_style import USER_INFO_STYLE  # Import style của bạn ở đây

class UsersScreen(QtWidgets.QWidget):
    def __init__(self, username, role, parent=None):
        super(UsersScreen, self).__init__(parent)
        self.current_user = username
        self.current_role = role
        self.user_info_labels = {}
        
        # Danh sách các trường thông tin cần hiển thị
        self.user_info_fields = [
            ("username", "Tên đăng nhập:"),
            ("role", "Vai trò:"),
            ("full_name", "Họ và tên:"),
            ("age", "Tuổi:"),
            ("gender", "Giới tính:"),
            ("height", "Chiều cao:"),
            ("weight", "Cân nặng mới nhất:"),
            ("blood_pressure", "Huyết áp:"),
            ("heart_rate", "Nhịp tim:"),
            ("date", "Ngày cập nhật:"),
        ]
        
        self.init_ui()
        self.setStyleSheet(USER_INFO_STYLE)  # Áp dụng style đã tách riêng
        self.load_user_info()

    def init_ui(self):
        # Layout chính của màn hình widget
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Container chính
        self.container = QtWidgets.QWidget(self)
        self.container.setObjectName("UserInfoContainer")
        
        box = QtWidgets.QGroupBox("Thông tin người sử dụng", self.container)
        form = QtWidgets.QFormLayout(box)
        form.setContentsMargins(18, 28, 18, 18)
        form.setHorizontalSpacing(28)
        form.setVerticalSpacing(14)

        # Tạo tự động các label kết quả
        for key, label_text in self.user_info_fields:
            label = QtWidgets.QLabel(label_text)
            label.setProperty("fieldLabel", True)

            value = QtWidgets.QLabel("Chưa có dữ liệu")
            value.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

            form.addRow(label, value)
            self.user_info_labels[key] = value

        # Đóng gói bố cục bên trong container
        box_layout = QtWidgets.QVBoxLayout(self.container)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.addWidget(box)
        box_layout.addStretch()

        main_layout.addWidget(self.container)

    def get_current_user_info(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                u.username, u.role, h.ho_ten, h.tuoi, h.gioi_tinh,
                h.chieu_cao, c.can_nang, c.huyet_ap, c.nhip_tim, c.ngay
            FROM users u
            LEFT JOIN ho_so h ON h.user_id = u.id
            LEFT JOIN chi_so c ON c.id = (
                SELECT id FROM chi_so
                WHERE ho_so_id = h.id
                ORDER BY ngay DESC, id DESC LIMIT 1
            )
            WHERE u.username=? LIMIT 1
        """, (self.current_user,))
        row = cursor.fetchone()
        conn.close()
        return row

    def load_user_info(self):
        empty_text = "Chưa có dữ liệu"
        defaults = {
            "username": self.current_user,
            "role": self.current_role,
            "full_name": "Chưa có hồ sơ",
        }
        for key, _ in self.user_info_fields:
            defaults.setdefault(key, empty_text)

        try:
            row = self.get_current_user_info()
            if row:
                keys = ["username", "role", "full_name", "age", "gender",
                        "height", "weight", "blood_pressure", "heart_rate", "date"]
                for key, value in zip(keys, row):
                    if value is not None and value != "":
                        defaults[key] = str(value)

                # Thêm đơn vị đo
                if defaults["height"] != empty_text: defaults["height"] += " cm"
                if defaults["weight"] != empty_text: defaults["weight"] += " kg"
                if defaults["heart_rate"] != empty_text: defaults["heart_rate"] += " bpm"

        except Exception as e:
            defaults["full_name"] = f"Lỗi tải thông tin: {e}"

        for key, value in defaults.items():
            self.user_info_labels[key].setText(value)