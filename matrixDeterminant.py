import sys
import copy
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QWidget, QPushButton, QLineEdit, QLabel, QSpinBox, QMessageBox,
                               QFrame, QSizePolicy, QGroupBox)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QGradient
from determinant import MatrixDeterminantCalculator


class StyledLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 5px;
                background-color: #F8F8F8;
                color: #333333;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
        """)
        self.setMinimumHeight(40)


class StyledButton(QPushButton):
    def __init__(self, text, color_scheme="blue", parent=None):
        super().__init__(text, parent)
        
        if color_scheme == "blue":
            primary_color = "#3498db"
            hover_color = "#2980b9"
        elif color_scheme == "green":
            primary_color = "#2ecc71"
            hover_color = "#27ae60"
        elif color_scheme == "red":
            primary_color = "#e74c3c"
            hover_color = "#c0392b"
        else:
            primary_color = "#95a5a6"
            hover_color = "#7f8c8d"
            
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                padding-left: 13px;
                padding-top: 13px;
                background-color: {hover_color};
            }}
        """)
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)


class MatrixInputFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            MatrixInputFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class ResultDisplay(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                background-color: #F0F8FF;
                color: #2c3e50;
                min-height: 45px;
                margin: 5px;
            }
        """)


class MatrixDeterminantCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = MatrixDeterminantCalculator()
        self.matrix_inputs = []
        self.initUI()
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
                font-weight: bold;
            }
            QGroupBox {
                border: 1px solid #D0D0D0;
                border-radius: 10px;
                margin-top: 15px;
                font-weight: bold;
                background-color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #333333;
            }
            QSpinBox {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 5px;
                background-color: #F8F8F8;
                color: #333333;
                min-height: 30px;
                min-width: 80px;
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border-radius: 4px;
                background-color: #3498db;
                color: white;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #2980b9;
            }
        """)

    def initUI(self):
        self.setWindowTitle('Matrix Determinant Calculator')
        self.setGeometry(100, 100, 700, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title_label = QLabel("Matrix Determinant Calculator")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Matrix size controls in a group box
        size_group = QGroupBox("Matrix Configuration")
        size_layout = QVBoxLayout(size_group)
        
        size_control_layout = QHBoxLayout()
        size_label = QLabel("Matrix Size:")
        size_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.size_spinner = QSpinBox()
        self.size_spinner.setRange(1, 10)
        self.size_spinner.setValue(3)
        self.size_spinner.valueChanged.connect(self.update_matrix_grid)
        
        size_control_layout.addWidget(size_label)
        size_control_layout.addWidget(self.size_spinner)
        size_control_layout.addStretch()
        
        size_layout.addLayout(size_control_layout)
        main_layout.addWidget(size_group)

        # Matrix input in a group box
        matrix_group = QGroupBox("Matrix Elements")
        matrix_layout = QVBoxLayout(matrix_group)
        
        self.matrix_frame = MatrixInputFrame()
        matrix_container_layout = QVBoxLayout(self.matrix_frame)
        matrix_container_layout.setContentsMargins(15, 15, 15, 15)
        
        self.matrix_grid_widget = QWidget()
        self.matrix_grid_layout = QGridLayout(self.matrix_grid_widget)
        self.matrix_grid_layout.setSpacing(10)
        
        matrix_container_layout.addWidget(self.matrix_grid_widget)
        matrix_layout.addWidget(self.matrix_frame)
        
        main_layout.addWidget(matrix_group)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        calculate_btn = StyledButton("Calculate Determinant", "blue")
        calculate_btn.clicked.connect(self.calculate_determinant)
        button_layout.addWidget(calculate_btn)

        clear_btn = StyledButton("Clear All", "red")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)

        main_layout.addLayout(button_layout)

        # Result display in a group box
        result_group = QGroupBox("Result")
        result_layout = QVBoxLayout(result_group)
        
        self.result_display = ResultDisplay()
        result_layout.addWidget(self.result_display)
        
        main_layout.addWidget(result_group)

        # Create initial matrix grid
        self.update_matrix_grid()

    def update_matrix_grid(self):
        # Clear existing inputs from layout
        while self.matrix_grid_layout.count():
            item = self.matrix_grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear the stored input references
        self.matrix_inputs = []

        # Get size from spinner
        size = self.size_spinner.value()

        # Create matrix input grid
        for row in range(size):
            row_inputs = []
            for col in range(size):
                input_field = StyledLineEdit()
                input_field.setFixedWidth(60)
                input_field.setAlignment(Qt.AlignCenter)
                self.matrix_grid_layout.addWidget(input_field, row, col)
                row_inputs.append(input_field)
            self.matrix_inputs.append(row_inputs)

        # Center the grid
        self.matrix_grid_layout.setAlignment(Qt.AlignCenter)

    def get_matrix_values(self):
        size = self.size_spinner.value()
        matrix = []

        for row in range(size):
            matrix_row = []
            for col in range(size):
                try:
                    value = float(
                        self.matrix_inputs[row][col].text().strip() or "0")
                    matrix_row.append(value)
                except ValueError:
                    QMessageBox.warning(
                        self, 
                        "Invalid Input",
                        f"Invalid value at row {row+1}, column {col+1}. Using 0 instead.",
                        QMessageBox.Ok
                    )
                    matrix_row.append(0)
            matrix.append(matrix_row)

        return matrix

    def calculate_determinant(self):
        try:
            matrix = self.get_matrix_values()
            determinant = self.calculator.calculateMatrixDeterminant(matrix)
            
            # Animate the result display
            self.result_display.setText("")
            QApplication.processEvents()
            
            # Format the result
            if determinant == int(determinant):
                formatted_result = str(int(determinant))
            else:
                formatted_result = f"{determinant:.6f}"
            
            self.result_display.setText(formatted_result)
            
            # Flash effect for the result display
            original_style = self.result_display.styleSheet()
            self.result_display.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #27ae60;
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #E8F8F5;
                    color: #27ae60;
                    min-height: 45px;
                    margin: 5px;
                    font-weight: bold;
                }
            """)
            
            # Return to original style after a delay
            QApplication.processEvents()
            from PySide6.QtCore import QTimer
            QTimer.singleShot(500, lambda: self.result_display.setStyleSheet(original_style))
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"An error occurred: {str(e)}",
                QMessageBox.Ok
            )

    def clear_all(self):
        for row in self.matrix_inputs:
            for input_field in row:
                input_field.clear()
        self.result_display.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app_font = QFont("Segoe UI", 10)
    app.setFont(app_font)
    
    window = MatrixDeterminantCalculatorApp()
    window.show()
    sys.exit(app.exec())