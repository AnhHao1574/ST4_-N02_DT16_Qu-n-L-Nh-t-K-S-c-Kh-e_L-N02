import matplotlib
from styles.thongkesuckhoe_style import THONGKE_STYLE
matplotlib.use("Qt5Agg")

from datetime import datetime
from PyQt5.QtWidgets import QDialog
from ui_py.thong_ke_suc_khoe_ui import Ui_Dialog  # Import từ file UI đã dựng sẵn biểu đồ
from data.database import get_connection


class ThongKeSucKhoeScreen(QDialog):

    def __init__(self, ho_so_id):
        super().__init__()

        # Khởi tạo giao diện từ đối tượng UI đã nhúng sẵn Canvas
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ho_so_id = ho_so_id
        self.setStyleSheet(THONGKE_STYLE)

        # Đổ dữ liệu văn bản và vẽ đồ thị lên màn hình
        self.load_thong_ke()
        self.setup_chart()

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

        top_height = max(int(height * 0.48), 310)
        left_width = 470
        right_width = max(width - left_width - gap, 420)
        bottom_top = margin + top_height + gap
        bottom_height = max(height - top_height - gap, 260)

        # Định vị các widget tự động co giãn theo cửa sổ chính
        self.ui.groupBox.setGeometry(margin, margin, left_width, top_height)
        self.ui.chart_widget_cannang.setGeometry(margin + left_width + gap, margin, right_width, top_height)
        self.ui.chart_widget_calo.setGeometry(margin, bottom_top, width, bottom_height)

        self.ui.figure_weight.tight_layout()
        self.ui.figure_calo.tight_layout()
        self.ui.chart_widget_cannang.draw_idle()
        self.ui.chart_widget_calo.draw_idle()

    # =====================================================
    # XỬ LÝ VÀ VẼ BIỂU ĐỒ (Đã làm gọn mắt)
    # =====================================================
    def setup_chart(self):
        if not self.ho_so_id:
            return

        conn = get_connection()
        cursor = conn.cursor()
        
        # --- 1. BIỂU ĐỒ CÂN NẶNG ---
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
                d = datetime.strptime(row[0], "%Y-%m-%d")
                dates.append(d)
            except:
                dates.append(row[0])
            weights.append(row[1])

        self.ui.figure_weight.clear() 
        ax = self.ui.figure_weight.add_subplot(111)
        
        if dates:
            ax.plot(dates, weights, marker='o', color='#2ecc71', linewidth=2)
            ax.grid(True, linestyle=':', alpha=0.5)  # Lưới mờ giúp nhìn mốc chỉ số gọn gàng
            ax.set_title("Biến động cân nặng (Kg)", fontsize=10, fontweight='bold')
            ax.tick_params(axis="x", labelrotation=20, labelsize=9)
        else:
            ax.text(0.5, 0.5, "Chưa có dữ liệu cân nặng", ha='center', va='center', color='gray')
        
        self.ui.chart_widget_cannang.draw()

        # --- 2. BIỂU ĐỒ CALO ---
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
            try:
                # GỌN GÀNG: Đổi định dạng ngày thành DD/MM để cột không bị dính chữ đè lên nhau
                d_formatted = datetime.strptime(row[0], "%Y-%m-%d").strftime("%d/%m")
                dates_calo.append(d_formatted)
            except:
                dates_calo.append(row[0])
            calos.append(row[1])

        self.ui.figure_calo.clear()
        ax2 = self.ui.figure_calo.add_subplot(111)

        if dates_calo:
            ax2.bar(dates_calo, calos, color='#3498db', width=0.35)
            ax2.grid(True, axis='y', linestyle=':', alpha=0.5)
            ax2.set_title("Tổng năng lượng nạp hằng ngày (kcal)", fontsize=10, fontweight='bold')
            ax2.tick_params(axis="x", labelsize=9)
        else:
            ax2.text(0.5, 0.5, "Chưa có dữ liệu ăn uống", ha='center', va='center', color='gray')

        self.ui.chart_widget_calo.draw()
        conn.close()

    # =====================================================
    # TÍNH TOÁN & HIỂN THỊ THÔNG SỐ CHỈ SỐ SỨC KHỎE
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

    def load_thong_ke(self):
        # Nếu chưa chọn hoặc không có hồ sơ, đặt giá trị rỗng mặc định
        if self.ho_so_id is None or self.ho_so_id == "":
            self.ui.lineEdit_BMI.setText("Chưa có hồ sơ")          
            self.ui.lineEdit_TDEE.setText("0 kcal")
            self.ui.lineEdit_Luongnuoc.setText("0 lít")
            self.ui.lineEdit_CaloHomNay.setText("0 kcal")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Lấy cân nặng gần nhất
            cursor.execute("""
                SELECT can_nang FROM chi_so 
                WHERE ho_so_id = ? ORDER BY ngay DESC, id DESC LIMIT 1
            """, (int(self.ho_so_id),))
            row_chi_so = cursor.fetchone()
            can_nang = row_chi_so[0] if row_chi_so else 0

            # Lấy thông số hồ sơ
            cursor.execute("""
                SELECT tuoi, gioi_tinh, chieu_cao, muc_do_van_dong
                FROM ho_so WHERE id = ?
            """, (int(self.ho_so_id),))
            profile = cursor.fetchone()

            if profile:
                tuoi, gioi_tinh, chieu_cao, muc_do = profile

                # 1. Hiển thị thông số BMI
                if chieu_cao > 0 and can_nang > 0:
                    chieu_cao_m = chieu_cao / 100.0
                    bmi_tinh_toan = can_nang / (chieu_cao_m ** 2)
                    
                    if bmi_tinh_toan < 18.5: trang_thai_bmi = "Gầy"
                    elif 18.5 <= bmi_tinh_toan < 24.9: trang_thai_bmi = "Bình thường"
                    elif 24.9 <= bmi_tinh_toan < 29.9: trang_thai_bmi = "Tiền béo phì"
                    else: trang_thai_bmi = "Béo phì"
                        
                    self.ui.lineEdit_BMI.setText(f"{round(bmi_tinh_toan, 1)} ({trang_thai_bmi})")
                else:
                    self.ui.lineEdit_BMI.setText("Chưa đủ dữ liệu")

                # 2. Hiển thị thông số TDEE
                if gioi_tinh == "Nam":
                    bmr = 10 * can_nang + 6.25 * chieu_cao - 5 * tuoi + 5
                else:
                    bmr = 10 * can_nang + 6.25 * chieu_cao - 5 * tuoi - 161

                he_so = {"Ít vận động": 1.2, "Vận động nhẹ": 1.375, "Vận động vừa": 1.55, "Vận động nặng": 1.725}
                tdee = bmr * he_so.get(muc_do, 1.2)
                self.ui.lineEdit_TDEE.setText(f"{round(tdee)} kcal")

                # 3. Hiển thị Lượng nước
                nuoc = can_nang * 35
                self.ui.lineEdit_Luongnuoc.setText(f"{round(nuoc / 1000, 1)} lít")

            # 4. Hiển thị tổng calo ăn trong ngày hôm nay
            calo_hom_nay = self.get_tong_calo_hom_nay()
            self.ui.lineEdit_CaloHomNay.setText(f"{calo_hom_nay} kcal")

        except Exception as e:
            print(f"Lỗi hệ thống khi tải dữ liệu thống kê: {e}")
        finally:
            conn.close()