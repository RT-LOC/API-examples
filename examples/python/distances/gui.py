
import asyncio
import sys
from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                               QTextEdit, QVBoxLayout, QWidget)
from qasync import QEventLoop

# Constants
IP_ADDRESS_SERVER = "0.0.0.0"
PORT = "13202"
NEW_PATH = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(1, str(NEW_PATH))
import parsers.socket.Python.decoder
import parsers.socket.Python.udp_client


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Setup UI elements
        self.setup_ui()

    def setup_ui(self):
        """Setup UI elements."""
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.on_button_clicked)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container) 
        
    def on_button_clicked(self):
        """Handle button click event."""
        self.text_edit.append("Button clicked!")
        asyncio.ensure_future(self.run_script())
        
    async def run_script(self):
        """Run the main script."""
        loop = asyncio.get_running_loop()
        udp_client = parsers.socket.Python.udp_client.UDPClient(loop)
        
        self.log_and_print(f"[UDP] - connecting to ({IP_ADDRESS_SERVER}) on port {PORT}")
        
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: udp_client,
            local_addr=(IP_ADDRESS_SERVER, PORT))
        
        while True:
            await self.process_data(udp_client)
            await asyncio.sleep(0.01)

    async def process_data(self, udp_client):
        """Process data received from the UDP client."""
        data, frame_nr = udp_client.read_data()

        if data != -1:
            measurements = []
            self.log_and_print(f"fr = {frame_nr}")
            for x in range(len(data)):
                self.log_and_print(f"> T {data[x][0]}: [", end="")
                anchors = data[x][3]
                for idx, anchor in enumerate(anchors):
                    if idx != 0:
                        self.log_and_print(", ", end="")
                    measurements.append(anchors[idx][1])
                    anchor_id = anchors[idx][0]
                    self.log_and_print(f"{anchor_id}:{anchors[idx][1]}", end="")
                self.log_and_print("]")

    def log_and_print(self, message, end='\n'):
        """Log the message and print it to the console."""
        print(message, end=end)
        self.text_edit.insertPlainText(message + end)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        sys.exit(loop.run_forever())
