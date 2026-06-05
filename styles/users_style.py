# styles/users_style.py

USER_INFO_STYLE = """
QWidget #UserInfoContainer { 
    background-color: #f5f6fa; 
}

QGroupBox {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 12px;
    margin-top: 14px;
    padding: 18px;
    font-size: 18px;
    font-weight: bold;
    color: #2f3640;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 6px;
}

QLabel {
    background: transparent;
    color: #2f3640;
    font-size: 14px;
}

QLabel[fieldLabel="true"] {
    font-weight: bold;
}
"""