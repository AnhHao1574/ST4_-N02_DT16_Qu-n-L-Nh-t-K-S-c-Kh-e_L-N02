QUANLYTAIKHOAN_STYLE = """
            QWidget { background-color: #f5f6fa; }
            QGroupBox {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 12px;
                margin-top: 14px;
                padding: 16px;
                font-weight: bold;
                color: #2f3640;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px;
            }
            QLabel {
                background: transparent;
                color: #2f3640;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                border: 1px solid #dcdde1;
                border-radius: 8px;
                padding: 8px;
                background: white;
                min-height: 28px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0984e3;
                color: white;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #74b9ff; }
            QPushButton#btnDelete {
                background-color: #d63031;
            }
            QPushButton#btnDelete:hover {
                background-color: #ff7675;
            }
            QTableWidget {
                background: white;
                border: 1px solid #dcdde1;
                gridline-color: #dfe6e9;
                border-radius: 8px;
                color: black;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #0984e3;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #dfe6e9;
                color: black;
            }
        """