# utils/quanlytaikhoan_utils.py

from data.database import get_connection


class QuanLyTaiKhoanUtils:

    def load_accounts_db(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                u.id,
                u.username,
                u.role,
                COALESCE(u.status, 'active'),
                COUNT(h.id)
            FROM users u
            LEFT JOIN ho_so h ON h.user_id = u.id
            GROUP BY u.id, u.username, u.role, u.status
            ORDER BY u.id
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    def add_account_db(self, username, password, role, status):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(username, password, role, status)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, status))

        conn.commit()
        conn.close()

    def update_account_db(
        self,
        user_id,
        username,
        password,
        role,
        status
    ):
        conn = get_connection()
        cursor = conn.cursor()

        if password:
            cursor.execute("""
                UPDATE users
                SET username=?, password=?, role=?, status=?
                WHERE id=?
            """, (username, password, role, status, user_id))

        else:
            cursor.execute("""
                UPDATE users
                SET username=?, role=?, status=?
                WHERE id=?
            """, (username, role, status, user_id))

        conn.commit()
        conn.close()

    def delete_account_db(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM users
            WHERE id=?
        """, (user_id,))

        conn.commit()
        conn.close()