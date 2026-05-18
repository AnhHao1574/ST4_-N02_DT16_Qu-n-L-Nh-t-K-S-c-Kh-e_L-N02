# Khi tải về mấy ông chạy thử luôn khỏi cần phải lấy link tìm sqlite , tui có hàm tự tìm kiếm link và chạy code luôn 
# chạy chương trình dùng lệnh :        python -m main 
dưới đây là giao diện và vị trí hàm sử dụng 

#Chú ý câu trúc file 
<img width="398" height="627" alt="image" src="https://github.com/user-attachments/assets/4adac156-fa9c-497b-b490-23bf764bbe9a" />
# file screens là thiết giao diện và có một số hàm 
# file styles điều chỉnh font chữ màu sắc giao diện
# file ui giao diện đc thiết kế từ Qt desginer lưu vào 
# file ui_py chứa các câu lệnh giao diện từ ui một câu lệnh dưới 


python -m PyQt5.uic.pyuic -x ui/Thongkesuckhoe.ui -o ui_py/thong_ke_suc_khoe_ui.py

python -m PyQt5.uic.pyuic -x ui/Hososuckhoe.ui -o ui_py/ho_so_suc_khoe_ui.py

python -m PyQt5.uic.pyuic -x ui/Nhatkyanuong.ui -o ui_py/nhat_ky_an_uong_ui.py
# file utils chứa các câu lệnh sql và hàm (là mấy ông làm bổ sung chức năng còn lại ), hàm tách ra làm cho gọn lại thui cho mấy ông sẽ hiểu 

# Giao diện đăng nhập và đăng ký 
<img width="635" height="663" alt="Screenshot 2026-05-18 142255" src="https://github.com/user-attachments/assets/6c25f437-2983-4cd4-93ae-87d62d52b2c7" />

<img width="630" height="695" alt="Screenshot 2026-05-18 142301" src="https://github.com/user-attachments/assets/a1f03a94-6341-40fe-bd23-cc9265840dc3" />

# Giao diện hồ sơ sức khỏe và nhật ký ăn uống 
<img width="1421" height="751" alt="Screenshot 2026-05-18 142212" src="https://github.com/user-attachments/assets/9f6a2924-47bf-4c69-b401-ba42cca295fb" />

<img width="1435" height="740" alt="Screenshot 2026-05-18 142224" src="https://github.com/user-attachments/assets/239005a4-0c08-47b4-a1d9-31ea5ca2c011" />

Chú ý hai giao diện này 
# Ông Phi Long là ông đảm nhiệm phần thêm , xóa , sửa, làm mới  . Riêng giao diện hồ sơ sức khỏe nó sẽ dữ liệu có sẵn nên khỏi phải thêm và xóa , nhưng sửa vẫn để chỉ sửa chỉ số thôi 

# Ông Đức chú ý cái giao diện nhật ký ăn uống nó một số hàm tính toán ông copy phần code trong screens > nhatkyanuong.py hỏi thử 
# ví dụ một người ăn uống sáng , trưa , chiều trong ngày 16/05/2026 khi ông trỏ chuột vào bảng là nó sẽ tự tính toán đúng một ngày xong ông trỏ ngày tiếp theo tương tự 
# Tổng calo trong một ngày (công thức thì mở trên mạng xem nha )


#Giao diện thống kê sức khỏe 
<img width="1431" height="754" alt="Screenshot 2026-05-18 142236" src="https://github.com/user-attachments/assets/ddeb0219-90b5-498e-b012-b141a7186fc9" />

# Ông Phi Long ông cần chú ý thêm phần sqlite 
# nên hiểu khóa chính , khóa ngoại nha , có gì ko biết hỏi á
# Bảng users

# CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE
                     NOT NULL,
    password TEXT    NOT NULL,
    role     TEXT    DEFAULT ('user') 
                     CHECK (role IN ('admin', 'user') ), (cái này nhận diện người dùng và admin)
    status   TEXT    DEFAULT ('active') );

#Bảng ho_so

# CREATE TABLE ho_so (
    id              INTEGER PRIMARY KEY AUTOINCREMENT 
                            NOT NULL,
    user_id         INTEGER REFERENCES users (id) (do sử dụng UNIQUE nên một người dùng chỉ có một hồ sơ thôi mà database có 3 hồ sơ của mỗi người có gì sửa sau nên là tui bỏ thêm và xóa á )
                            UNIQUE,
    ho_ten          TEXT,
    tuoi            INTEGER,
    gioi_tinh       TEXT,
    chieu_cao       REAL,
    muc_do_van_dong TEXT );

#Bảng chi_so

# CREATE TABLE chi_so (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ho_so_id INTEGER REFERENCES ho_so (id),
    can_nang REAL,
    huyet_ap TEXT,
    nhip_tim INTEGER,
    ngay     DATE );

#Bảng an_uong

# CREATE TABLE an_uong (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ho_so_id INTEGER REFERENCES ho_so (id),
    ngay     DATE,
    bua_an   TEXT,
    calo     REAL,
    ten_mon  TEXT,
    so_luong INTEGER,
    ghi_chu  TEXT);

# mấy câu lệnh dùng khi ông xóa hết dữ liệu bảng và cập nhật số id tự động về 1 


# PRAGMA foreign_keys = OFF;

# DELETE FROM an_uong;
# DELETE FROM chi_so;
# DELETE FROM ho_so;
# DELETE FROM users;

# DELETE FROM sqlite_sequence WHERE name='users';
# DELETE FROM sqlite_sequence WHERE name='ho_so';
# DELETE FROM sqlite_sequence WHERE name='chi_so';
# DELETE FROM sqlite_sequence WHERE name='an_uong';

# PRAGMA foreign_keys = ON;

DELETE FROM sqlite_sequence;



