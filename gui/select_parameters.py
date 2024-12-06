from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
)
import sys


class Window_Select_Parameters:
    def initialize(self) -> tuple[str, str]:
        """Get parameters through PyQt GUI"""
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("Image thresholding")
        self.window.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["RGB", "HSV"])
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Picture", "WebCam"])

        layout.addWidget(QLabel("Mode:"))
        layout.addWidget(self.mode_combo)
        layout.addWidget(QLabel("Source:"))
        layout.addWidget(self.source_combo)

        button = QPushButton("Select")
        button.clicked.connect(self.window.close)
        layout.addWidget(button)

        self.window.show()
        self.app.exec_()

        mode: str = self.mode_combo.currentText()
        source: str = self.source_combo.currentText()

        return mode, source
