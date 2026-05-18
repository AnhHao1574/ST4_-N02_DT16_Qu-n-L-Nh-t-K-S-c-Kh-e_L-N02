from data.database import get_connection
from datetime import datetime


class HoSoSucKhoeUtils:

    def LayDuLieuHoSo(self):
        conn = get_connection()
        cursor = conn.cursor()

        # Đã loại bỏ c.bmi khỏi câu lệnh SELECT
        query = """
        SELECT
            h.id,
            h.ho_ten,
            h.tuoi,
            h.gioi_tinh,
            h.chieu_cao,
            c.can_nang,
            c.huyet_ap,
            c.nhip_tim,
            c.ngay
        FROM ho_so h
        LEFT JOIN chi_so c
        ON h.id = c.ho_so_id
        """

        if getattr(self, "current_role", "user") == "admin":
            cursor.execute(query)
        else:
            query += " WHERE h.user_id=?"
            cursor.execute(query, (getattr(self, "user_id", None),))
        rows = cursor.fetchall()
        conn.close()

        return rows


    def ThemHoSoDB(
        self,
        user_id,
        ho_ten,
        tuoi,
        gioi_tinh,
        chieu_cao,
        can_nang,
        huyet_ap,
        nhip_tim
    ):
        # Đã xóa tham số 'bmi' ra khỏi hàm

        conn = get_connection()
        cursor = conn.cursor()

        # Thêm hồ sơ vào bảng ho_so
        cursor.execute("""
            INSERT INTO ho_so(
                user_id,
                ho_ten,
                tuoi,
                gioi_tinh,
                chieu_cao
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            ho_ten,
            tuoi,
            gioi_tinh,
            chieu_cao
        ))

        ho_so_id = cursor.lastrowid

        # Thêm chỉ số vào bảng chi_so (Đã bỏ cột bmi)
        cursor.execute("""
            INSERT INTO chi_so(
                ho_so_id,
                can_nang,
                huyet_ap,
                nhip_tim,
                ngay
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ho_so_id,
            can_nang,
            huyet_ap,
            nhip_tim,
            datetime.now().strftime("%Y-%m-%d")
        ))

        conn.commit()
        conn.close()


    def SuaHoSoDB(
        self,
        id,
        ho_ten,
        tuoi,
        gioi_tinh,
        chieu_cao,
        can_nang,
        huyet_ap,
        nhip_tim
    ):
        # Đã xóa tham số 'bmi' ra khỏi hàm

        conn = get_connection()
        cursor = conn.cursor()

        # Cập nhật thông tin bảng ho_so
        cursor.execute("""
            UPDATE ho_so
            SET
                ho_ten=?,
                tuoi=?,
                gioi_tinh=?,
                chieu_cao=?
            WHERE id=?
        """, (
            ho_ten,
            tuoi,
            gioi_tinh,
            chieu_cao,
            id
        ))

        # Cập nhật thông tin bảng chi_so (Đã bỏ cập nhật trường bmi)
        cursor.execute("""
            UPDATE chi_so
            SET
                can_nang=?,
                huyet_ap=?,
                nhip_tim=?,
                ngay=?
            WHERE ho_so_id=?
        """, (
            can_nang,
            huyet_ap,
            nhip_tim,
            datetime.now().strftime("%Y-%m-%d"),
            id
        ))

        conn.commit()
        conn.close()


    def XoaHoSoDB(self, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM chi_so
            WHERE ho_so_id=?
        """, (id,))

        cursor.execute("""
            DELETE FROM ho_so
            WHERE id=?
        """, (id,))

        conn.commit()
        conn.close()