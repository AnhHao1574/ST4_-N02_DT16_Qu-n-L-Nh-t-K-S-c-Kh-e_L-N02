from data.database import get_connection

class NhatKyAnUongUtils:

    def LayDuLieuAnUongDB(self):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            a.id,
            h.ho_ten,
            a.ngay,
            a.bua_an,
            a.ten_mon,
            a.so_luong,
            a.calo,
            a.ghi_chu,
            a.ho_so_id
        FROM an_uong a
        JOIN ho_so h
        ON a.ho_so_id = h.id
        ORDER BY a.ngay DESC
        """

        if getattr(self, "current_role", "user") == "admin":
            cursor.execute(query)
        else:
            query = query.replace(
                "ORDER BY a.ngay DESC",
                """
                WHERE h.user_id = (
                    SELECT id
                    FROM users
                    WHERE username=?
                )
                ORDER BY a.ngay DESC
                """
            )
            cursor.execute(query, (getattr(self, "current_user", ""),))
        rows = cursor.fetchall()

        conn.close()
        return rows


    def ThemNhatKyDB(
        self,
        ho_so_id,
        ngay,
        bua_an,
        ten_mon,
        so_luong,
        calo,
        ghi_chu
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO an_uong(
                ho_so_id,
                ngay,
                bua_an,
                calo,
                ten_mon,
                so_luong,
                ghi_chu
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ho_so_id,
            ngay,
            bua_an,
            calo,
            ten_mon,
            so_luong,
            ghi_chu
        ))

        conn.commit()
        conn.close()


    def SuaNhatKyDB(
        self,
        id,
        ngay,
        bua_an,
        ten_mon,
        so_luong,
        calo,
        ghi_chu
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE an_uong
            SET
                ngay=?,
                bua_an=?,
                ten_mon=?,
                so_luong=?,
                calo=?,
                ghi_chu=?
            WHERE id=?
        """, (
            ngay,
            bua_an,
            ten_mon,
            so_luong,
            calo,
            ghi_chu,
            id
        ))

        conn.commit()
        conn.close()


    def XoaNhatKyDB(self, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM an_uong
            WHERE id=?
        """, (id,))

        conn.commit()
        conn.close()


    # =========================
    # TÍNH TỔNG CALO
    # =========================
    def TongCaloHomNay(self, ho_so_id, ngay):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(a.calo * a.so_luong)
            FROM an_uong a
            JOIN ho_so h ON a.ho_so_id = h.id
            WHERE h.user_id = (SELECT user_id FROM ho_so WHERE id = ?) AND a.ngay=?
        """, (ho_so_id, ngay))

        result = cursor.fetchone()[0]

        conn.close()

        return result if result else 0


    def TinhSucKhoe(self, ho_so_id):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            h.ho_ten,
            h.tuoi,
            h.gioi_tinh,
            h.chieu_cao,
            h.muc_do_van_dong,
            c.can_nang
        FROM ho_so h
        JOIN chi_so c
        ON h.id = c.ho_so_id
        WHERE h.id=?
        ORDER BY c.ngay DESC
        LIMIT 1
        """

        cursor.execute(query, (ho_so_id,))
        row = cursor.fetchone()

        conn.close()

        if not row:
            return None

        ho_ten, tuoi, gioi_tinh, chieu_cao, muc_do, can_nang = row

        # ======================
        # BMR
        # ======================

        if gioi_tinh == "Nam":
            bmr = (
                10 * can_nang
                + 6.25 * chieu_cao
                - 5 * tuoi
                + 5
            )
        else:
            bmr = (
                10 * can_nang
                + 6.25 * chieu_cao
                - 5 * tuoi
                - 161
            )

        # ======================
        # Hệ số vận động
        # ======================

        he_so = {
            "Ít vận động": 1.2,
            "Vận động nhẹ": 1.375,
            "Vận động vừa": 1.55,
            "Vận động nặng": 1.725,
            "Thap": 1.2,
            "Trung binh": 1.55,
            "Cao": 1.725
        }

        tdee = bmr * he_so.get(muc_do, 1.2)

        # ======================
        # Nước
        # ======================

        nuoc_ml = can_nang * 35

        return {
            "bmr": round(bmr, 2),
            "tdee": round(tdee, 2),
            "nuoc_ml": round(nuoc_ml, 0),
            "nuoc_lit": round(nuoc_ml / 1000, 2)
        }
