from PyQt5 import QtWidgets, QtCore
from ui_py.nhat_ky_an_uong_ui import Ui_Dialog 
from utils.nhatkyanuong_utils import NhatKyAnUongUtils
from data.database import get_connection
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView
from styles.nhatkyanuong_style import NHATKYANUONG_STYLE


class NhatKyAnUongScreen(QtWidgets.QWidget, NhatKyAnUongUtils):
    def __init__(self, username="", role="user"):
        super().__init__()
        self.current_user = username
        self.current_role = role
        
        # 1. Setup UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 2. Thiết lập giao diện màu sắc
        self.setStyleSheet(NHATKYANUONG_STYLE)

        # 3. Cấu hình bảng dữ liệu
        if self.layout() is None:
            self.main_layout = QtWidgets.QVBoxLayout(self)
        else:
            self.main_layout = self.layout()
        
        self.main_layout.setContentsMargins(15, 40, 15, 15)
        self.main_layout.setSpacing(10)

        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 1)
       
        self.ui.tableWidget_nhatkyanuong.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_nhatkyanuong.setHorizontalHeaderLabels([
            "Họ và tên",
            "Ngày",
            "Bữa ăn",
            "Tên món",
            "Số lượng",
            "Calo(1 phần)",
            "Ghi chú",
        ])
        self.ui.tableWidget_nhatkyanuong.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.ui.tableWidget_nhatkyanuong.verticalHeader().setVisible(False)
        self.ui.tableWidget_nhatkyanuong.resizeRowsToContents()        
        self.id_dang_chon = None

        # 4. Kết nối sự kiện
        self.ui.btn_them.clicked.connect(self.ThemNhatKy)
        self.ui.btn_sua.clicked.connect(self.SuaNhatKy)
        self.ui.btn_xoa.clicked.connect(self.XoaNhatKy)
        self.ui.btn_reset.clicked.connect(self.ResetForm)
        self.ui.tableWidget_nhatkyanuong.cellClicked.connect(self.ChonDong)

        self.LayDuLieuAnUong()
        self.LoadHoSo()

    def LoadHoSo(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.current_role == "admin":
                cursor.execute("SELECT id, ho_ten FROM ho_so")
            else:
                cursor.execute("""
                    SELECT h.id, h.ho_ten
                    FROM ho_so h
                    JOIN users u ON h.user_id = u.id
                    WHERE u.username=?
                """, (self.current_user,))
            rows = cursor.fetchall()
            self.ui.comboBox_hoso.clear()
            for r in rows:
                self.ui.comboBox_hoso.addItem(r[1], r[0]) # Gán tên làm hiển thị, ID làm dữ liệu đến
            conn.close()
        except Exception as e:
            print(f"Lỗi tải danh sách hồ sơ: {e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cap_nhat_kich_thuoc_giao_dien()

    def cap_nhat_kich_thuoc_giao_dien(self):
        margin = 20
        group_top = 20
        group_height = 295
        width = max(self.width() - margin * 2, 980)
        table_top = group_top + group_height + 15
        table_height = max(self.height() - table_top - margin, 240)

        self.ui.groupBox_2.setGeometry(margin, group_top, width, group_height)
        self.ui.tableWidget_nhatkyanuong.setGeometry(
            margin,
            table_top,
            width,
            table_height
        )

        # Cum thong ke nam ben phai va tu bam theo do rong groupBox.
        stats_label_x = max(560, width - 430)
        stats_value_x = stats_label_x + 170
        stats_width = max(width - stats_value_x - 35, 160)

        self.ui.label_14.move(stats_label_x, 145)
        self.ui.label_16.move(stats_label_x, 185)
        self.ui.label_17.move(stats_label_x, 225)
        self.ui.lineEdit_tongcalo.setGeometry(stats_value_x, 145, stats_width, 31)
        self.ui.lineEdit_TDEE.setGeometry(stats_value_x, 185, stats_width, 31)
        self.ui.lineEdit_trangthai.setGeometry(stats_value_x, 225, stats_width, 31)

        note_width = max(stats_label_x - 110, 380)
        self.ui.lineEdit_ghichu.setGeometry(90, 190, note_width, 31)

    def LayDuLieuAnUong(self):
        try:
            rows = self.LayDuLieuAnUongDB() # GĂ¡Â»Â�i phĂ†Â°Ă†Â¡ng thĂ¡Â»Â©c kĂ¡ÂºÂ¿t nĂ¡Â»â€˜i JOIN tĂ¡Â»Â« lĂ¡Â»â€ºp tiĂ¡Â»â€¡n ĂƒÂ­ch
            self.ui.tableWidget_nhatkyanuong.setRowCount(0)
            for row_idx, row_data in enumerate(rows):
                self.ui.tableWidget_nhatkyanuong.insertRow(row_idx)
                self.ui.tableWidget_nhatkyanuong.setVerticalHeaderItem(row_idx, QtWidgets.QTableWidgetItem(str(row_data[0])))
                for col_idx, data in enumerate(row_data[1:]):
                    val = f"{data} kcal" if col_idx == 5 else str("" if data is None else data)
                    item = QtWidgets.QTableWidgetItem(val)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.ui.tableWidget_nhatkyanuong.setItem(row_idx, col_idx, item)
        except Exception as e:
            print(f"Lỗi tải nhật ký ăn uống: {e}")

    def ChonDong(self, row, col):
        header = self.ui.tableWidget_nhatkyanuong.verticalHeaderItem(row)
        if not header: return
        self.id_dang_chon = header.text()
        
        # --- BƯỚC KHÓA TÍN HIỆU: Ngăn ComboBox kích hoạt các sự kiện ngầm gây lỗi ---
        self.ui.comboBox_hoso.blockSignals(True)

        try:
            # Tìm và chọn đúng tên hiển thị trong combobox hồ sơ
            ten_ho_so = self.ui.tableWidget_nhatkyanuong.item(row, 0).text()
            index = self.ui.comboBox_hoso.findText(ten_ho_so)
            if index >= 0:
                self.ui.comboBox_hoso.setCurrentIndex(index)
            else:
                self.ui.comboBox_hoso.setCurrentText(ten_ho_so)

            self.ui.dateEdit_ngay.setDate(QDate.fromString(self.ui.tableWidget_nhatkyanuong.item(row, 1).text(), "yyyy-MM-dd"))
            self.ui.comboBox_buaan.setCurrentText(self.ui.tableWidget_nhatkyanuong.item(row, 2).text())
            self.ui.lineEdit_mon.setText(self.ui.tableWidget_nhatkyanuong.item(row, 3).text())
            self.ui.spinBox_soluong.setValue(int(float(self.ui.tableWidget_nhatkyanuong.item(row, 4).text() or 1)))
            self.ui.lineEdit_calo.setText(self.ui.tableWidget_nhatkyanuong.item(row, 5).text().replace(" kcal", ""))
            self.ui.lineEdit_ghichu.setText(self.ui.tableWidget_nhatkyanuong.item(row, 6).text())
            
        finally:
            # --- MỞ LẠI TÍN HIỆU: Cho phép ComboBox hoạt động bình thường sau khi gán xong ---
            self.ui.comboBox_hoso.blockSignals(False)

        # Chủ động gọi cập nhật thống kê sau khi dữ liệu form đã được điền hoàn toàn chuẩn xác
        self.CapNhatThongKe()


    def ThemNhatKy(self):
        try:
            ho_so_id = self.ui.comboBox_hoso.currentData()
            ngay = self.ui.dateEdit_ngay.date().toString("yyyy-MM-dd")
            bua_an = self.ui.comboBox_buaan.currentText()
            ten_mon = self.ui.lineEdit_mon.text().strip()
            if not ten_mon:
                QtWidgets.QMessageBox.warning(self, "Thông Báo", "Vui lòng điền tên món ăn!")
                return
            so_luong = self.ui.spinBox_soluong.value()
            calo = float(self.ui.lineEdit_calo.text() or 0)
            ghi_chu = self.ui.lineEdit_ghichu.text().strip() 
            
            # 
            self.ThemNhatKyDB(ho_so_id, ngay, bua_an, ten_mon, so_luong, calo, ghi_chu)
            
            self.LayDuLieuAnUong()
            self.CapNhatThongKe()
            self.ResetForm()
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã lưu bữa ăn vào nhật ký!")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Dữ liệu không hợp lệ hoặc thiếu thuộc tính: {e}")

    def SuaNhatKy(self):
        if not self.id_dang_chon:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng chọn bản ghi cần sửa!")
            return
        try:
            ngay = self.ui.dateEdit_ngay.date().toString("yyyy-MM-dd")
            bua_an = self.ui.comboBox_buaan.currentText()
            ten_mon = self.ui.lineEdit_mon.text().strip()
            so_luong = self.ui.spinBox_soluong.value()
            calo = float(self.ui.lineEdit_calo.text() or 0)
            ghi_chu = self.ui.lineEdit_ghichu.text().strip()

            
            self.SuaNhatKyDB(int(self.id_dang_chon), ngay, bua_an, ten_mon, so_luong, calo, ghi_chu)
            self.CapNhatThongKe()
            self.LayDuLieuAnUong()
            QtWidgets.QMessageBox.information(self, "Xong", "Đã cập nhật thay đổi thành công!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể chỉnh sửa: {e}")

    def XoaNhatKy(self):
        if not self.id_dang_chon: return
        msg = QtWidgets.QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa nhật ký ăn uống này?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            try:
                self.XoaNhatKyDB(int(self.id_dang_chon))
                self.LayDuLieuAnUong()
                self.CapNhatThongKe()
                self.ResetForm()
            except Exception as e:
                print(f"Lỗi xóa bản ghi ăn uống: {e}")

    def ResetForm(self):
        self.id_dang_chon = None
        self.ui.lineEdit_mon.clear()
        self.ui.lineEdit_calo.clear()
        self.ui.lineEdit_ghichu.clear()
        self.ui.spinBox_soluong.setValue(1)
        self.ui.dateEdit_ngay.setDate(QDate.currentDate())
        self.ui.tableWidget_nhatkyanuong.clearSelection()

    def CapNhatThongKe(self):
        try:
            # 1. Lấy ngày từ widget
            ngay = self.ui.dateEdit_ngay.date().toString("yyyy-MM-dd")
            
            # 2. Lấy ho_so_id từ comboBox
            ho_so_id = self.ui.comboBox_hoso.currentData()

            # --- GIẢI PHÁP SỬA LỖI KHÔNG HIỆN SỐ ---
            # Nếu comboBox không trả về ID (do bị lệch text), ta tự tìm ID từ database dựa vào chữ đang hiển thị
            if ho_so_id is None or ho_so_id == "":
                ten_hien_tai = self.ui.comboBox_hoso.currentText().strip()
                if ten_hien_tai:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM ho_so WHERE ho_ten = ? LIMIT 1", (ten_hien_tai,))
                        row = cursor.fetchone()
                        if row:
                            ho_so_id = row[0]
                        conn.close()
                    except Exception as db_err:
                        print("Lỗi truy vấn tìm ID hồ sơ dự phòng:", db_err)

            # Nếu sau khi tìm dự phòng vẫn không có ID thì mới dừng
            if ho_so_id is None or ho_so_id == "":
                self.ui.lineEdit_tongcalo.setText("0")
                self.ui.lineEdit_TDEE.setText("0")
                self.ui.lineEdit_trangthai.setText("Chưa chọn hồ sơ")
                return

            # Chắc chắn ép kiểu số nguyên để truyền xuống SQLite
            ho_so_id_int = int(ho_so_id)

            # 3. Tính toán dữ liệu bữa ăn từ Utils của bạn
            tong_calo = self.TongCaloHomNay(ho_so_id_int, ngay)
            suc_khoe = self.TinhSucKhoe(ho_so_id_int)
            tdee = suc_khoe["tdee"] if (suc_khoe and "tdee" in suc_khoe) else 0

            # 4. Hiển thị kết quả lên giao diện
            self.ui.lineEdit_tongcalo.setText(str(round(tong_calo, 1)))
            self.ui.lineEdit_TDEE.setText(str(round(tdee, 1)))

            # 5. Phân tích trạng thái năng lượng
            if tdee <= 0:
                trang_thai = "Chưa có chỉ số TDEE"
            elif tong_calo < tdee - 50:
                trang_thai = "Thiếu calo"
            elif tong_calo > tdee + 50:
                trang_thai = "Dư calo"
            else:
                trang_thai = "Đủ calo"

            self.ui.lineEdit_trangthai.setText(trang_thai)

        except Exception as e:
            print("Lỗi tính toán thống kê nhật ký ăn uống:", e)
