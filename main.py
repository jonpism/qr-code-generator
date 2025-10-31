from PyQt6.QtWidgets    import QWidget, QLabel, QTextEdit, QMessageBox, QFileDialog, QApplication
from PyQt6.QtGui        import QPixmap, QFont
from DefaultStyles      import *
from pathlib            import Path
from io                 import BytesIO
import sys, qrcode, os, numpy as np

class QRcodeGeneratorWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generate QR Code")
        self.setFixedSize(700, 800)

        # Data input
        data_label = QLabel("Enter data:", parent=self)
        data_label.setGeometry(300, 10, 100, 50)
        self.data_input = DefaultQLineEditStyle(parent=self)
        self.data_input.setGeometry(10, 60, 680, 50)

        # version input (integer from 1 to 40 that controls the size of the QR code image
        # 1 is small, 21x21 matrix, 40 is 185x185 matrix
        version_input_label = QLabel("Enter version number:", parent=self)
        version_input_label.setGeometry(10, 130, 150, 50)
        self.version_input = DefaultQLineEditStyle(
            parent=self, int_validator=True, placeholder_text="1 to 40")
        self.version_input.setGeometry(170, 130, 70, 50)

        # box_size input (pixels each box of the QR code is)
        box_size_input_label = QLabel("Enter box size number:", parent=self)
        box_size_input_label.setGeometry(10, 200, 160, 50)
        self.box_size_input = DefaultQLineEditStyle(
            parent=self, int_validator=True)
        self.box_size_input.setGeometry(170, 200, 70, 50)

        # border controls how many boxes thick the border should be.
        border_size_input_label = QLabel("Enter border size:", parent=self)
        border_size_input_label.setGeometry(300, 130, 160, 50)
        self.border_size_input = DefaultQLineEditStyle(
            parent=self, int_validator=True)
        self.border_size_input.setGeometry(430, 130, 70, 50)

        # background color: back_color
        back_color_label = QLabel("Select background color:", parent=self)
        back_color_label.setGeometry(300, 200, 180, 50)
        self.back_color_options = DefaultQComboBoxStyle(
            parent=self,
            items=["white", "black"])
        self.back_color_options.setGeometry(480, 200, 130, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.generate)
        submit_button.setGeometry(300, 280, 100, 50)

        # show the shape of the image
        self.print_shape_label = QTextEdit(parent=self)
        self.print_shape_label.setGeometry(200, 350, 280, 50)
        self.print_shape_label.setReadOnly(True)
        self.print_shape_label.hide()

        # show qr image
        self.show_qr_image_label = QLabel(parent=self)
        self.show_qr_image_label.setGeometry(160, 450, 380, 300)
        self.show_qr_image_label.setScaledContents(True)  # Scale image to fit QLabel size
        self.show_qr_image_label.hide()

    def generate(self):
        try:
            data = self.data_input.text()
            if data:
                version = int(self.version_input.text()) if self.version_input.text() else 1
                box_size = int(self.box_size_input.text()) if self.box_size_input.text() else 8
                border_size = int(self.border_size_input.text()) if self.border_size_input.text() else 2
                back_color = self.back_color_options.currentText()

                qr = qrcode.QRCode(version=version, box_size=box_size, border=border_size)
                qr.add_data(data)
                qr.make()

                # print the shape of the image
                self.print_shape_label.clear()
                self.print_shape_label.setHtml(f"<b>The shape of the QR image is:</b><br>{str(np.array(qr.get_matrix()).shape)}")
                self.print_shape_label.show()

                # transfer the array into an actual image
                if back_color == "white":
                    img = qr.make_image(fill_color="black", back_color="white")
                else:
                    img = qr.make_image(fill_color="white", back_color="black")

                # show qr image in QLabel
                image_data = self.plot_qr_image(img)
                pixmap = QPixmap()
                pixmap.loadFromData(image_data.getvalue())
                self.show_qr_image_label.setPixmap(pixmap)
                self.show_qr_image_label.show()

                # Save the image to the Downloads folder
                downloads_path = str(Path.home() / "Downloads")  # Get the user's Downloads folder
                file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", os.path.join(downloads_path, "qrcode.png"), "PNG Files (*.png)")

                if file_path:
                    img.save(file_path, "PNG")
                    QMessageBox.information(self, "Saved", f"QR code saved successfully at:\n{file_path}")
            else:
                raise ValueError('No data entered.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def plot_qr_image(self, img):
        byte_array = BytesIO()
        img.save(byte_array, format='PNG')  # Save image to BytesIO as PNG
        return byte_array

try:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.setFont(QFont("Ubuntu"))
        app.setStyleSheet("QWidget { background-color: #3B3B3B; color: white; }")
        window = QRcodeGeneratorWindow()
        window.show()
        sys.exit(app.exec())
except Exception as e:
    print(f"An error occured: {e}")
