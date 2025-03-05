import sys
import json
import random
import numpy as np
from PIL import Image

try:
    from PIL.ImageQt import ImageQt


    def pil_to_pixmap(image):
        from PyQt5.QtGui import QPixmap
        return QPixmap.fromImage(ImageQt(image))
except ImportError:
    from PyQt5.QtGui import QImage, QPixmap


    def pil_to_pixmap(image):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QImage(data, image.size[0], image.size[1], QImage.Format_RGBA8888)
        return QPixmap.fromImage(qimage)

from sklearn.cluster import KMeans
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsItem)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QBrush, QFont


class SwatchItem(QGraphicsItem):
    def __init__(self, rect, color_hex, callback, parent=None):
        super().__init__(parent)
        self.rect = rect
        self.color_hex = color_hex
        self.callback = callback
        # Enable movement and selection
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.start_pos = None

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(QColor(self.color_hex)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        self.start_pos = event.scenePos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.start_pos is not None:
            end_pos = event.scenePos()
            if (end_pos - self.start_pos).manhattanLength() < 5:
                if self.callback:
                    self.callback(self.color_hex)
        super().mouseReleaseEvent(event)


class ColorPaletteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Color Palette Extractor")
        self.setGeometry(100, 100, 850, 750)

        # Define two application themes as style sheets.
        self.themes = {
            "Gradient Galaxy": """
                QMainWindow { 
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #000428, stop:1 #004e92); 
                }
                QPushButton { 
                    background-color: #8e44ad; 
                    color: white; 
                    border: none; 
                    padding: 10px 20px; 
                    border-radius: 8px; 
                    font-size: 14px; 
                }
                QPushButton:hover { 
                    background-color: #9b59b6; 
                }
                QLabel { 
                    color: white; 
                    font-size: 12px; 
                }
            """,
            "Nature Green": """
                QMainWindow { 
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #3b5323, stop:1 #d4c59e); 
                }
                QPushButton { 
                    background-color: #556B2F; 
                    color: white; 
                    border: none; 
                    padding: 10px 20px; 
                    border-radius: 8px; 
                    font-size: 14px; 
                }
                QPushButton:hover { 
                    background-color: #6b8e23; 
                }
                QLabel { 
                    color: white; 
                    font-size: 12px; 
                }
            """
        }
        self.theme_names = list(self.themes.keys())
        self.current_theme_index = 0  # Start with Gradient Galaxy

        # Apply initial theme
        self.setStyleSheet(self.themes[self.theme_names[self.current_theme_index]])

        self.colors = []  # Colors extracted from image or generated randomly
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Top button layout
        button_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload Image", self)
        self.upload_btn.clicked.connect(self.upload_image)
        button_layout.addWidget(self.upload_btn)

        self.random_btn = QPushButton("Random Colors", self)
        self.random_btn.clicked.connect(self.generate_random_colors)
        button_layout.addWidget(self.random_btn)

        self.switch_theme_btn = QPushButton("Switch Theme", self)
        self.switch_theme_btn.clicked.connect(self.switch_theme)
        button_layout.addWidget(self.switch_theme_btn)

        self.export_btn = QPushButton("Export Palette", self)
        self.export_btn.clicked.connect(self.export_palette)
        button_layout.addWidget(self.export_btn)

        layout.addLayout(button_layout)

        # Label to display the uploaded image
        self.image_display = QLabel("No image loaded", self)
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setFixedHeight(250)
        self.image_display.setStyleSheet("background-color: #ffffff; border: 2px solid #ccc;")
        layout.addWidget(self.image_display)

        # Color display area
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedHeight(300)
        self.view.setFrameStyle(0)
        layout.addWidget(self.view)

        # Info label
        self.info_label = QLabel("Click any color to copy HEX code", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        main_widget.setLayout(layout)

        # Display an initial placeholder palette
        self.display_colors(["#ffffff"] * 5)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)"
        )
        if file_path:
            self.process_image(file_path)

    def process_image(self, file_path):
        try:
            image = Image.open(file_path)
            # Update the image display
            image_for_display = image.copy()
            image_for_display.thumbnail((400, 250))
            pixmap = pil_to_pixmap(image_for_display)
            self.image_display.setPixmap(pixmap)
            self.image_display.setText("")

            # Process image for color extraction
            image = image.resize((150, 150))
            img_array = np.array(image)
            if img_array.ndim == 2:
                img_array = np.stack((img_array,) * 3, axis=-1)
            elif img_array.shape[2] == 4:
                img_array = img_array[:, :, :3]
            img_array = img_array.reshape((-1, 3))

            kmeans = KMeans(n_clusters=5, random_state=0)
            kmeans.fit(img_array)
            dominant_colors = kmeans.cluster_centers_.astype(int)

            self.colors = [self.rgb_to_hex(color) for color in dominant_colors]
            self.display_colors(self.colors)
        except Exception as e:
            self.info_label.setText(f"Error: {str(e)}")

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    def display_colors(self, colors):
        self.scene.clear()
        swatch_size = 100
        spacing = 20
        scene_width = 50 + len(colors) * (swatch_size + spacing)
        self.scene.setSceneRect(0, 0, scene_width, 300)

        for i, color in enumerate(colors):
            x = 50 + i * (swatch_size + spacing)
            y = 50
            rect = QRectF(0, 0, swatch_size, swatch_size)
            swatch = SwatchItem(rect, color, self.copy_to_clipboard)
            swatch.setPos(x, y)
            self.scene.addItem(swatch)

            # Add HEX text as a child of the swatch so it doesn’t intercept clicks
            text_item = QGraphicsTextItem(color, swatch)
            text_color = Qt.white if self.is_dark(color) else Qt.black
            text_item.setDefaultTextColor(text_color)
            text_item.setFont(QFont("Arial", 8))
            text_rect = text_item.boundingRect()
            text_item.setPos((swatch_size - text_rect.width()) / 2, (swatch_size - text_rect.height()) / 2)

    def is_dark(self, color_hex):
        rgb = tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5))
        luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        return luminance < 128

    def copy_to_clipboard(self, hex_code):
        clipboard = QApplication.clipboard()
        clipboard.setText(hex_code)
        self.info_label.setText(f"Copied: {hex_code}")

    def generate_random_colors(self):
        random_scheme = []
        for _ in range(5):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            random_scheme.append('#{:02x}{:02x}{:02x}'.format(r, g, b))
        self.colors = random_scheme  # Update current palette
        self.display_colors(random_scheme)
        self.info_label.setText("Random colors generated")

    def switch_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_names)
        theme_name = self.theme_names[self.current_theme_index]
        self.setStyleSheet(self.themes[theme_name])
        self.info_label.setText(f"Theme switched to: {theme_name}")

    def export_palette(self):
        # Export the current palette (self.colors) to a JSON or TXT file.
        if not self.colors:
            self.info_label.setText("No palette to export!")
            return
        # Open a save dialog; allow JSON and TXT files
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Palette", "", "JSON Files (*.json);;Text Files (*.txt)"
        )
        if not file_path:
            return
        try:
            if file_path.endswith(".json") or "JSON" in selected_filter:
                with open(file_path, "w") as f:
                    json.dump({"palette": self.colors}, f, indent=4)
            else:
                with open(file_path, "w") as f:
                    for color in self.colors:
                        f.write(color + "\n")
            self.info_label.setText(f"Palette exported to: {file_path}")
        except Exception as e:
            self.info_label.setText(f"Export error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorPaletteApp()
    window.show()
    sys.exit(app.exec_())
