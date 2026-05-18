from PyQt5 import QtCore
from PyQt5 import QtWidgets
from styles.hososuckhoe_style import HOSOSUCKHOE_STYLE
from ui_py.ho_so_suc_khoe_ui import Ui_Dialog
from utils.hososuckhoe_utils import HoSoSucKhoeUtils
from data.database import get_connection
from PyQt5.QtWidgets import QHeaderView

class HoSoSucKhoeScreen(QtWidgets.QWidget, HoSoSucKhoeUtils):
    def __init__(self, username="", user_id=None, role="user"):
        super().__init__()
        self.username = username
        self.current_role = role
        self.user_id = user_id if user_id is not None else self.lay_user_id(username)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self) 
        
        if self.layout() is None:
            self.main_layout = QtWidgets.QVBoxLayout(self)
        else:
            self.main_layout = self.layout()

        self.main_layout.setContentsMargins(15, 25, 15, 15)
        self.main_layout.setSpacing(10)
        
        if self.main_layout.count() > 2:
            self.main_layout.setStretch(2, 1)

        self.setStyleSheet(HOSOSUCKHOE_STYLE)
        self.id_dang_chon = None
        self.ui.tableWidget_hososuckhoe.verticalHeader().setVisible(False)
        
        header = self.ui.tableWidget_hososuckhoe.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # THAY ĐỔI: Chỉ số cột cuối cùng (Ngày) giờ là 7 thay vì 8
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        for i in range(1, self.ui.tableWidget_hososuckhoe.columnCount()):
            if i == 7:
                continue
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        

        self.ui.btn_sua.clicked.connect(self.SuaHoSo)
        self.ui.btn_reset.clicked.connect(self.ResetForm)
        
        self.ui.tableWidget_hososuckhoe.itemSelectionChanged.connect(self.ChonDong)
        self.HienThiDuLieuLenBang()

    def lay_user_id(self, username):
        if not username:
            return None
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cap_nhat_kich_thuoc_giao_dien()

    def cap_nhat_kich_thuoc_giao_dien(self):
        margin = 20
        group_top = 20
        group_height = 250
        width = max(self.width() - margin * 2, 880)
        table_top = group_top + group_height + 15
        table_height = max(self.height() - table_top - margin, 260)

        self.ui.groupBox.setGeometry(margin, group_top, width, group_height)
        self.ui.tableWidget_hososuckhoe.setGeometry(margin, table_top, width, table_height)

        button_x = max(630, width - 250)
        for button, y in [
         
            (self.ui.btn_sua, 70),
            (self.ui.btn_reset, 170),
        ]:
            button.setGeometry(button_x, y, 120, 51)

    # --- THAY ĐỔI: XOÁ BỎ HOÀN TOÀN HÀM TinhBMI ---

    def HienThiDuLieuLenBang(self):
        try:
            self.ui.tableWidget_hososuckhoe.blockSignals(True)
            rows = self.LayDuLieuHoSo() 
            self.ui.tableWidget_hososuckhoe.setRowCount(0)
            
            for row_index, row_data in enumerate(rows):
                self.ui.tableWidget_hososuckhoe.insertRow(row_index)
                self.ui.tableWidget_hososuckhoe.setVerticalHeaderItem(row_index, QtWidgets.QTableWidgetItem(str(row_data[0])))
                
                # Cấu trúc row_data từ DB (bỏ ID đầu): [ho_ten, tuoi, gioi_tinh, chieu_cao, can_nang, huyet_ap, nhip_tim, ngay_tao, muc_do]
                # THAY ĐỔI: Đổ thẳng cấu trúc gốc tuần tự vào 8 cột hiển thị sạch sẽ không chen BMI tính toán vào nữa
                for col_index, data in enumerate(row_data[1:9]):
                    val = "" if data is None else str(data)
                    item = QtWidgets.QTableWidgetItem(val)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.ui.tableWidget_hososuckhoe.setItem(row_index, col_index, item)
        except Exception as e:
            print(f"Lỗi hiển thị dữ liệu lên giao diện hồ sơ: {e}")
        finally:
            self.ui.tableWidget_hososuckhoe.blockSignals(False)

    def ChonDong(self):
        selected_ranges = self.ui.tableWidget_hososuckhoe.selectedRanges()
        if not selected_ranges:
            return
            
        row = selected_ranges[0].topRow()
        header = self.ui.tableWidget_hososuckhoe.verticalHeaderItem(row)
        
        if header:
            self.id_dang_chon = header.text()
            
            def get_safe_text(r, c):
                item = self.ui.tableWidget_hososuckhoe.item(r, c)
                return item.text().strip() if item else ""

            self.ui.lineEdit_hoten.setText(get_safe_text(row, 0))
            
            tuoi_str = get_safe_text(row, 1) or "0"
            try:
                self.ui.spinBox_tuoi.setValue(int(float(tuoi_str)))
            except ValueError:
                self.ui.spinBox_tuoi.setValue(0)
                
            self.ui.comboBox_gioitinh.setCurrentText(get_safe_text(row, 2))
            self.ui.lineEdit_chieucao.setText(get_safe_text(row, 3))
            self.ui.lineEdit_cannang.setText(get_safe_text(row, 4))
            
            # THAY ĐỔI: Sắp xếp lại chỉ số cột index do loại bỏ BMI (Huyết áp cột 5, Nhịp tim cột 6)
            self.ui.lineEdit_huyetap.setText(get_safe_text(row, 5))
            self.ui.lineEdit_nhiptim.setText(get_safe_text(row, 6))
            
    # def ThemHoSo(self):
    #     ho_ten = self.ui.lineEdit_hoten.text().strip()
    #     tuoi = self.ui.spinBox_tuoi.value()
    #     gioi_tinh = self.ui.comboBox_gioitinh.currentText()
        
    #     try:
    #         chieu_cao = float(self.ui.lineEdit_chieucao.text().strip())
    #         can_nang = float(self.ui.lineEdit_cannang.text().strip())
    #     except ValueError:
    #         QtWidgets.QMessageBox.warning(self, "Thông báo", "Chiều cao và Cân nặng phải là số!")
    #         return

    #     huyet_ap = self.ui.lineEdit_huyetap.text().strip()
    #     nhip_tim = self.ui.lineEdit_nhiptim.text().strip()

    #     if not ho_ten:
    #         QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng nhập họ tên!")
    #         return

    #     # KIỂM TRA & ÉP KIỂU USER_ID AN TOÀN
    #     if self.user_id is None:
    #         self.user_id = self.lay_user_id(self.username)
        
    #     if self.user_id is None:
    #         QtWidgets.QMessageBox.critical(self, "Lỗi", "Không tìm thấy User ID hợp lệ trong hệ thống!")
    #         return

    #     try:
    #         # Gọi hàm Utils (Đã loại bỏ tham số bmi)
    #         self.ThemHoSoDB(
    #             int(self.user_id), # Ép kiểu số nguyên chắc chắn cho SQLite
    #             ho_ten,
    #             int(tuoi),
    #             gioi_tinh,
    #             chieu_cao,
    #             can_nang,
    #             huyet_ap,
    #             nhip_tim
    #         )
    #         QtWidgets.QMessageBox.information(self, "Thành công", "Đã thêm hồ sơ thành công!")
    #         self.HienThiDuLieuLenBang()
    #         self.ResetForm()
    #     except Exception as e:
    #         QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi thực hiện thêm dữ liệu: {e}")

    def SuaHoSo(self):
        if not self.id_dang_chon:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một dòng hồ sơ để sửa!")
            return

        ho_ten = self.ui.lineEdit_hoten.text().strip()
        tuoi = self.ui.spinBox_tuoi.value()
        gioi_tinh = self.ui.comboBox_gioitinh.currentText()

        try:
            chieu_cao = float(self.ui.lineEdit_chieucao.text().strip())
            can_nang = float(self.ui.lineEdit_cannang.text().strip())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Chiều cao và Cân nặng phải là số!")
            return

        huyet_ap = self.ui.lineEdit_huyetap.text().strip()
        nhip_tim = self.ui.lineEdit_nhiptim.text().strip()

        try:
            # Gọi hàm Utils (Đã loại bỏ tham số bmi và ép kiểu id ẩn chắc chắn)
            self.SuaHoSoDB(
                int(self.id_dang_chon),
                ho_ten,
                int(tuoi),
                gioi_tinh,
                chieu_cao,
                can_nang,
                huyet_ap,
                nhip_tim
            )
            QtWidgets.QMessageBox.information(self, "Thành công", "Cập nhật dữ liệu thành công!")
            self.HienThiDuLieuLenBang()
            self.ResetForm()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi thực hiện sửa dữ liệu: {e}")

    # def XoaHoSo(self):
    #     if not self.id_dang_chon: 
    #         QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng chọn dòng cần xóa!")
    #         return
            
    #     msg = QtWidgets.QMessageBox.question(self, "Xác nhận xóa", "Bạn có chắc muốn xóa vĩnh viễn hồ sơ này?", 
    #                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    #     if msg == QtWidgets.QMessageBox.Yes:
    #         try:
    #             # Sửa lại hàm gọi: Chỉ truyền duy nhất tham số id theo đúng cấu trúc XoaHoSoDB(self, id)
    #             self.XoaHoSoDB(int(self.id_dang_chon))
    #             self.HienThiDuLieuLenBang()
    #             self.ResetForm()
    #             QtWidgets.QMessageBox.information(self, "Thành công", "Đã xóa hồ sơ thành công!")
    #         except Exception as e:
    #             QtWidgets.QMessageBox.critical(self, "Lỗi", f"Gặp lỗi khi xóa bản ghi: {e}")
    
    def ResetForm(self):
        self.id_dang_chon = None
        self.ui.lineEdit_hoten.clear()
        self.ui.spinBox_tuoi.setValue(0)
        self.ui.lineEdit_chieucao.clear()
        self.ui.lineEdit_cannang.clear()
        # THAY ĐỔI: Đã xóa dòng clear lineEdit_BMI thừa ở đây
        self.ui.lineEdit_huyetap.clear()
        self.ui.lineEdit_nhiptim.clear()
        self.ui.comboBox_gioitinh.setCurrentIndex(0)
        self.ui.tableWidget_hososuckhoe.clearSelection()