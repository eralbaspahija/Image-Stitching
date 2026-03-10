from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import cv2

from stitching.stitcher import PanoramaStitcher
from utils.dataset_scanner import get_dataset_folders
from gui.styles import APP_STYLE

import pathlib as Path
from PySide6.QtWidgets import (
    QScrollArea, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QImage
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panorama Stitching App")
        self.setMinimumSize(1000, 600)

        self.setStyleSheet(APP_STYLE)

        self.panorama = None  # store stitched result
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()

        # Dataset selector
        self.combo = QComboBox()
        self.combo.addItems(get_dataset_folders())
        self.combo.currentTextChanged.connect(self.load_images)

        # Buttons
        self.btn_run = QPushButton("Run Stitching")
        self.btn_run.clicked.connect(self.run_stitching)

        self.btn_save = QPushButton("Save Panorama")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_panorama)

        # Image list area (input images)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.images_widget = QWidget()
        self.images_layout = QHBoxLayout()
        self.images_widget.setLayout(self.images_layout)

        self.scroll_area.setWidget(self.images_widget)

        # Panorama preview
        self.image_label = QLabel("Panorama preview")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Layout structure
        main_layout.addWidget(QLabel("Choose dataset folder:"))
        main_layout.addWidget(self.combo)
        main_layout.addWidget(QLabel("Input images:"))
        main_layout.addWidget(self.scroll_area, stretch=1)
        main_layout.addWidget(self.btn_run)
        main_layout.addWidget(self.btn_save)
        main_layout.addWidget(self.image_label, stretch=2)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Load images initially
        self.load_images(self.combo.currentText())

    # -------------------------------------------------

    def load_images(self, folder):
        """Show all images in the selected dataset folder"""
        # Clear old thumbnails
        while self.images_layout.count():
            child = self.images_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        dataset_path = f"dataset/{folder}"

        if not os.path.exists(dataset_path):
            return

        for file in sorted(os.listdir(dataset_path)):
            if file.lower().endswith((".jpg", ".png", ".jpeg", ".jfif")):
                img_path = os.path.join(dataset_path, file)
                pixmap = QPixmap(img_path)

                thumb = QLabel()
                thumb.setPixmap(pixmap.scaled(
                    150, 150,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
                thumb.setAlignment(Qt.AlignCenter)
                self.images_layout.addWidget(thumb)

    # -------------------------------------------------

    def run_stitching(self):
        folder = self.combo.currentText()
        stitcher = PanoramaStitcher(f"dataset/{folder}")
        panorama, error = stitcher.stitch()

        if error:
            self.image_label.setText(error)
            self.btn_save.setEnabled(False)
            return

        self.panorama = panorama
        self.btn_save.setEnabled(True)

        rgb = cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.image_label.setPixmap(QPixmap.fromImage(qimg).scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    # -------------------------------------------------

    def save_panorama(self):
        if self.panorama is None:
            return

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Panorama",
            f"{output_dir}/panorama.jpg",
            "Images (*.jpg *.png)"
        )

        if path:
            cv2.imwrite(path, self.panorama)

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Saved")
            msg.setText("Panorama image saved successfully.")
            msg.setStyleSheet("QLabel { color: black; }")
            msg.exec()
