LOGIN_STYLE="""
    QMainWindow {
        border-image: url("images/hinhdangnhap.png") 0 0 0 0 stretch stretch;
    }
    
    #centralwidget {
        background: transparent;
    }
    
    /* Áp dụng cho Frame chứa các ô nhập liệu */
    QFrame {
        background-color: rgba(0, 0, 0, 130); /* Đen mờ 160/255 */
        border-radius: 15px;
    }

    /* Chỉnh các ô nhập liệu */
    QLineEdit {
        background-color: rgba(255, 255, 255, 40); /* Nền ô nhập trắng mờ nhẹ */
        color: white; 
        border: 1px solid rgba(255, 255, 255, 60);
        border-radius: 10px;
        padding: 10px 12px;
        font-size: 18px;
        min-height: 34px;
    }

    /* Chỉnh chữ cho các nhãn (Label) */
    QLabel {
        color: white; /* Bắt buộc là màu trắng để nổi trên nền đen */
        background: transparent;
        font-weight: bold;
        font-size: 16px;
    }

    /* Thông báo lỗi màu vàng hoặc đỏ nhẹ cho dễ thấy */
    #lblError {
        color: #ff6b6b;
        font-style: italic;
    }

    /* Nút bấm Đăng ký */
    QPushButton {
        background-color: #1a73e8;
        color: white;
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
        font-size: 17px;
        min-height: 34px;
    }
    QPushButton:hover {
        background-color: #1557b0;
    }
    
    #label {
        color: white;
        background: transparent;
        font-size: 34px;
        font-weight: bold;
        padding: 18px 0;
    }
    QLineEdit:focus {
        border: 2px solid #74b9ff;
    }
    #lblError {
        font-size: 15px;
        min-height: 28px;
    }
    #btnTogglePassword {
        min-width: 48px;
        max-width: 56px;
        padding: 8px;
        font-size: 18px;
    }
"""