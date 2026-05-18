THONGKE_STYLE = """
QDialog {
    background-color: #f5f6fa;
}

/* =========================
   GROUP BOX
========================= */
QGroupBox {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 18px;
    margin-top: 20px;

    font-size: 18px;
    font-weight: bold;
    color: #2f3640;

    padding: 20px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 18px;
    padding: 0 10px;
    color: #0984e3;
    font-size: 20px;
    font-weight: bold;
}

/* =========================
   LABEL
========================= */
QLabel {
    color: #2f3640;
    font-size: 15px;
    font-weight: bold;
    background: transparent;
}

/* =========================
   LINE EDIT
========================= */
QLineEdit {
    background-color: #f8f9fa;

    border: 2px solid #dfe6e9;
    border-radius: 12px;

    padding: 8px 12px;

    min-height: 34px;

    color: #2d3436;
    font-size: 15px;
    font-weight: bold;
}

QLineEdit:focus {
    border: 2px solid #74b9ff;
    background: white;
}

/* =========================
   CHART CONTAINER
========================= */
#chart_widget_cannang,
#chart_widget_calo {
    background-color: white;

    border: 1px solid #dcdde1;
    border-radius: 18px;
}

/* =========================
   SCROLL BAR
========================= */
QScrollBar:vertical {
    border: none;
    background: #f1f2f6;
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #b2bec3;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #74b9ff;
}

/* =========================
   TOOLTIP
========================= */
QToolTip {
    background-color: white;
    color: #2d3436;
    border: 1px solid #dfe6e9;
    padding: 6px;
    border-radius: 8px;
    font-size: 13px;
}
"""