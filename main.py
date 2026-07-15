import sys
from PyQt6.QtWidgets import QApplication
from src.interfaz import ShimejiVentana

def main():
    app = QApplication(sys.argv)
    shimeji = ShimejiVentana()
    shimeji.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()