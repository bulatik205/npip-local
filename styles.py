class Styles:
    # Фреймы
    FRAME = """
        QFrame {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 5px;
        }
    """
    
    # GroupBox
    GROUP = """
        QGroupBox {
            border: 1px solid #ccc;
            border-radius: 10px;
            margin-top: 20px;
            padding: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
        }
    """
    
    # Поле ввода
    INPUT = """
        QLineEdit {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 14px;
            background-color: transparent;
        }
        QLineEdit:focus {
            border-color: #d3782c;
            background-color: transparent;
        }
    """
    
    @staticmethod
    def button(bg_color="#458a7d"):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 7px 10px;
                border: 1px solid #777;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #3a7569;
            }}
            QPushButton:pressed {{
                background-color: #2f6056;
            }}
        """
    
    @staticmethod
    def terminal_button(bg_color="#444"):
        return f"""
        QPushButton {{
            background-color: {bg_color};
            color: #ccc;
            padding: 5px 10px;
            border: 1px solid #555;
            border-radius: 5px;
            font-size: 11px;
        }}
        QPushButton:hover {{
            background-color: #555;
        }}
    """