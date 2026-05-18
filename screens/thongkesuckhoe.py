import matplotlib
from styles.thongkesuckhoe_style import THONGKE_STYLE
matplotlib.use("Qt5Agg")

from datetime import datetime
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data.database import get_connection


class ThongKeSucKhoeScreen(QDialog):

    def __init__(self, ho_so_id):
        super().__init__()

        uic.loadUi("ui/Thongkesuckhoe.ui", self)
        self.ho_so_id = ho_so_id
        self.setWindowTitle("Thống kê sức khỏe")

        # 1. Khởi tạo và liên kết khung Canvas của Matplotlib vào Widget UI
        # ===== Biểu đồ cân nặng =====
        self.figure_weight = Figure()
        self.canvas_weight = FigureCanvas(self.figure_weight)
        layout_weight = QVBoxLayout(self.chart_widget_cannang)
        layout_weight.setContentsMargins(0, 0, 0, 0)
        layout_weight.addWidget(self.canvas_weight)

        # ===== Biểu đồ calo =====
        self.figure_calo = Figure()
        self.canvas_calo = FigureCanvas(self.figure_calo)
        layout_calo = QVBoxLayout(self.chart_widget_calo)
        layout_calo.setContentsMargins(0, 0, 0, 0)
        layout_calo.addWidget(self.canvas_calo)
        
        self.setStyleSheet(THONGKE_STYLE)

        # 2. GỌI CÁC HÀM XỬ LÝ LOGIC (Đã sửa lỗi bỏ quên gọi hàm)
        self.load_thong_ke()  # Nạp các chỉ số văn bản trước
        self.setup_chart()    # Vẽ hai biểu đồ sau

    def set_ho_so_id(self, ho_so_id):
        self.ho_so_id = ho_so_id
        self.load_thong_ke()
        self.setup_chart()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cap_nhat_kich_thuoc_giao_dien()

    def cap_nhat_kich_thuoc_giao_dien(self):
        margin = 20
        gap = 20
        width = max(self.width() - margin * 2, 980)
        height = max(self.height() - margin * 2, 620)

        top_height = max(int(height * 0.45), 280)
        left_width = 470
        right_width = max(width - left_width - gap, 420)
        bottom_top = margin + top_height + gap
        bottom_height = max(height - top_height - gap, 260)

        self.groupBox.setGeometry(margin, margin, left_width, top_height)
        self.chart_widget_cannang.setGeometry(
            margin + left_width + gap,
            margin,
            right_width,
            top_height
        )
        self.chart_widget_calo.setGeometry(
            margin,
            bottom_top,
            width,
            bottom_height
        )

        self.figure_weight.tight_layout()
        self.figure_calo.tight_layout()
        self.canvas_weight.draw_idle()
        self.canvas_calo.draw_idle()

    # =====================================================
    # XỬ LÝ VÀ VẼ BIỂU ĐỒ (Đọc từ DB và hiển thị đồ thị)
    # =====================================================
    def setup_chart(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.ho_so_id is None or self.ho_so_id == "":
            conn.close()
            return
        # --- BIỂU ĐỒ CÂN NẶNG ---
        cursor.execute("""
            SELECT ngay, can_nang 
            FROM chi_so 
            WHERE ho_so_id=? 
            ORDER BY ngay ASC
        """, (self.ho_so_id,))
        rows = cursor.fetchall()

        dates = []
        weights = []
        for row in rows:
            try:
                # Chuyển chuỗi chữ sang định dạng ngày chuẩn để Matplotlib không xếp lộn xộn trục X
                d = datetime.strptime(row[0], "%Y-%m-%d")
                dates.append(d)
            except:
                dates.append(row[0])
            weights.append(row[1])

        self.figure_weight.clear() 
        ax = self.figure_weight.add_subplot(111)
        
        if dates:
            ax.plot(dates, weights, marker='o', color='#2ecc71', linewidth=2)
            ax.set_title("Biểu đồ biến động cân nặng")
            ax.set_xlabel("Ngày")
            ax.set_ylabel("Kg")
            ax.tick_params(axis="x", labelrotation=30)
            self.figure_weight.tight_layout()
        else:
            ax.text(0.5, 0.5, "Chưa có dữ liệu cân nặng", ha='center', va='center')
        
        self.canvas_weight.draw()

        # --- BIỂU ĐỒ CALO ---
        cursor.execute("""
            SELECT date(ngay), SUM(CAST(calo AS REAL) * CAST(so_luong AS REAL))
            FROM an_uong 
            WHERE ho_so_id=? 
            GROUP BY date(ngay) 
            ORDER BY date(ngay) ASC
        """, (self.ho_so_id,))
        rows_calo = cursor.fetchall()

        dates_calo = []
        calos = []
        for row in rows_calo:
            dates_calo.append(row[0])
            calos.append(row[1])

        self.figure_calo.clear()
        ax2 = self.figure_calo.add_subplot(111)

        if dates_calo:
            ax2.bar(dates_calo, calos, color='#3498db', width=0.4)
            ax2.set_title("Tổng calo tiêu thụ theo ngày")
            ax2.set_xlabel("Ngày")
            ax2.set_ylabel("Calories")
            ax2.tick_params(axis="x", labelrotation=30)
            self.figure_calo.tight_layout()
        else:
            ax2.text(0.5, 0.5, "Chưa có dữ liệu ăn uống", ha='center', va='center')

        self.canvas_calo.draw()
        conn.close()

 # =====================================================
    # Tổng calo hôm nay
    # =====================================================

    def get_tong_calo_hom_nay(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(CAST(calo AS REAL) * CAST(so_luong AS REAL))
            FROM an_uong
            WHERE ho_so_id = ?
            AND date(ngay) = date('now', 'localtime')
        """, (self.ho_so_id,))

        row = cursor.fetchone()
        conn.close()

        return round(row[0], 1) if row and row[0] else 0

    # =====================================================
    # TÍNH TOÁN & THIẾT LẬP THÔNG SỐ VĂN BẢN (BMI, TDEE, NƯỚC)
    # =====================================================
    def load_thong_ke(self):
        # CHẶN LỖI AN TOÀN: Nếu ID trống hoặc chưa có hồ sơ thì không thực hiện lệnh SQL
        if self.ho_so_id is None or self.ho_so_id == "":
            if hasattr(self, 'lineEdit_BMI'):
                self.lineEdit_BMI.setText("Chưa có hồ sơ")          

            if hasattr(self, 'lineEdit_TDEE'):
                self.lineEdit_TDEE.setText("0 kcal")

            if hasattr(self, 'lineEdit_Luongnuoc'):
                self.lineEdit_Luongnuoc.setText("0 lít")

            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Gửi tham số đã được ép kiểu int an toàn xuống SQLite
            cursor.execute("""
                SELECT can_nang 
                FROM chi_so 
                WHERE ho_so_id = ? 
                ORDER BY ngay DESC, id DESC 
                LIMIT 1
            """, (int(self.ho_so_id),))
            
            row_chi_so = cursor.fetchone()
            can_nang = row_chi_so[0] if row_chi_so else 0

            cursor.execute("""
                SELECT tuoi, gioi_tinh, chieu_cao, muc_do_van_dong
                FROM ho_so
                WHERE id = ?
            """, (int(self.ho_so_id),))
            
            profile = cursor.fetchone()

            if profile:
                tuoi, gioi_tinh, chieu_cao, muc_do = profile

                # Tính toán chỉ số BMI động từ chiều cao cân nặng
                if chieu_cao > 0 and can_nang > 0:
                    chieu_cao_m = chieu_cao / 100.0
                    bmi_tinh_toan = can_nang / (chieu_cao_m ** 2)
                    
                    if bmi_tinh_toan < 18.5: trang_thai_bmi = "Gầy"
                    elif 18.5 <= bmi_tinh_toan < 24.9: trang_thai_bmi = "Bình thường"
                    elif 24.9 <= bmi_tinh_toan < 29.9: trang_thai_bmi = "Tiền béo phì"
                    else: trang_thai_bmi = "Béo phì"
                        
                    if hasattr(self, 'lineEdit_BMI'):
                        self.lineEdit_BMI.setText(f"{round(bmi_tinh_toan, 1)} ({trang_thai_bmi})")
                else:
                    if hasattr(self, 'lineEdit_BMI'): self.lineEdit_BMI.setText("Chưa đủ dữ liệu")

                # Tính BMR & TDEE
                if gioi_tinh == "Nam":
                    bmr = 10 * can_nang + 6.25 * chieu_cao - 5 * tuoi + 5
                else:
                    bmr = 10 * can_nang + 6.25 * chieu_cao - 5 * tuoi - 161

                he_so = {"Ít vận động": 1.2, "Vận động nhẹ": 1.375, "Vận động vừa": 1.55, "Vận động nặng": 1.725}
                tdee = bmr * he_so.get(muc_do, 1.2)
                if hasattr(self, 'lineEdit_TDEE'): self.lineEdit_TDEE.setText(f"{round(tdee)} kcal")

                # Lượng nước
                nuoc = can_nang * 35
                if hasattr(self, 'lineEdit_Luongnuoc'): self.lineEdit_Luongnuoc.setText(f"{round(nuoc / 1000, 1)} lít")

        except Exception as e:
            print(f"Lỗi khi xử lý load thống kê sức khỏe: {e}")
        finally:
            conn.close()