import sys
import copy
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QWidget, QPushButton, QLineEdit, QLabel, QSpinBox, QMessageBox)
from PySide6.QtCore import Qt
from determinant import MatrixDeterminantCalculator


class MatrixDeterminantCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = MatrixDeterminantCalculator()
        self.matrix_inputs = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Matrix Determinant Calculator')
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Matrix size controls
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Matrix Size:"))

        self.size_spinner = QSpinBox()
        self.size_spinner.setRange(1, 10)
        self.size_spinner.setValue(3)
        self.size_spinner.valueChanged.connect(self.update_matrix_grid)
        size_layout.addWidget(self.size_spinner)

        main_layout.addLayout(size_layout)

        # Matrix input grid
        self.matrix_grid_widget = QWidget()
        self.matrix_grid_layout = QGridLayout(self.matrix_grid_widget)
        main_layout.addWidget(self.matrix_grid_widget)

        # Buttons
        button_layout = QHBoxLayout()

        calculate_btn = QPushButton("Calculate Determinant")
        calculate_btn.clicked.connect(self.calculate_determinant)
        button_layout.addWidget(calculate_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)

        main_layout.addLayout(button_layout)

        # Result display
        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel("Determinant:"))

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        result_layout.addWidget(self.result_display)

        main_layout.addLayout(result_layout)

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
                input_field = QLineEdit()
                input_field.setFixedWidth(60)
                input_field.setAlignment(Qt.AlignCenter)
                self.matrix_grid_layout.addWidget(input_field, row, col)
                row_inputs.append(input_field)
            self.matrix_inputs.append(row_inputs)

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
                    QMessageBox.warning(self, "Invalid Input",
                                        f"Invalid value at row {row+1}, column {col+1}. Using 0 instead.")
                    matrix_row.append(0)
            matrix.append(matrix_row)

        return matrix

    def calculate_determinant(self):
        # try:
        matrix = self.get_matrix_values()
        determinant = self.calculator.calculateMatrixDeterminant(matrix)
        self.result_display.setText(str(determinant))
        # except Exception as e:
        #     QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_all(self):
        for row in self.matrix_inputs:
            for input_field in row:
                input_field.clear()
        self.result_display.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixDeterminantCalculatorApp()
    window.show()
    sys.exit(app.exec())
