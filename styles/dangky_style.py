# styles/dangky_style.py

REGITER_STYLE = """
/* Hình nền */
QMainWindow {
    border-image: url("images/hinhdangky.png") 0 0 0 0 stretch stretch;
}

/* Widget trung tâm */
#centralwidget {
    background: transparent;
}

/* Frame */
QFrame {
    background-color: rgba(0, 0, 0, 130);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 30);
}

/* Ô nhập */
QLineEdit {
    background-color: rgba(255, 255, 255, 20);
    color: white;
    border: 1px solid rgba(255, 255, 255, 50);
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 18px;
    min-height: 34px;
}

QLineEdit:focus {
    border: 2px solid #74b9ff;
}

/* Label */
QLabel {
    color: white;
    background: transparent;
    font-weight: bold;
    font-size: 16px;
    border: none;
}

/* Title */
#label {
    color: white;
    background: transparent;
    font-size: 34px;
    font-weight: bold;
    padding: 18px 0;
}

/* Error */
#lblError {
    color: #ff4d4d;
    font-size: 15px;
    min-height: 28px;
    font-weight: normal;
}

/* Button register */
QPushButton#btnRegister {
    background-color: #1a73e8;
    color: white;
    border-radius: 10px;
    padding: 12px;
    font-weight: bold;
    font-size: 17px;
    min-height: 34px;
}

QPushButton#btnRegister:hover {
    background-color: #1557b0;
}

/* Các button khác */
QPushButton {
    background-color: rgba(255, 255, 255, 30);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px;
    font-size: 16px;
    min-height: 32px;
}

/* Nút mắt */
#btnTogglePassword,
#btnToggleConfirm {
    min-width: 48px;
    max-width: 56px;
    padding: 8px;
    font-size: 18px;
}
"""