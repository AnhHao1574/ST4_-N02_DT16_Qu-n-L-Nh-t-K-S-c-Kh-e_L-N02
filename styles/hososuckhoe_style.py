HOSOSUCKHOE_STYLE = """
        QWidget { background-color: #f5f6fa; }
        QGroupBox {
            background-color: white; border: 1px solid #dcdde1;
            border-radius: 15px; margin-top: 15px; font-weight: bold;
            padding: 15px; color: #2f3640;
        }
        QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px; }
        QLabel { color: #2f3640; font-size: 13px; font-weight: 500; }
        QLineEdit, QSpinBox, QComboBox {
            border: 1px solid #dcdde1; border-radius: 8px;
            padding: 6px; background: white; min-height: 28px;
        }
        QPushButton {
            background-color: #0984e3; color: white; border-radius: 10px;
            padding: 8px 16px; font-weight: bold;
        }
        QPushButton:hover { background-color: #74b9ff; }
        QTableWidget {
            background: white; border: 1px solid #dcdde1;
            gridline-color: #dfe6e9; border-radius: 10px; color: black;
        }
        QHeaderView::section { background-color: #0984e3; color: white; padding: 8px; border: none; }
        QTableWidget::item:selected { background-color: #dfe6e9; color: black; }
        """