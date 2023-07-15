
import asyncio
import sys
from pathlib import Path
import PySide6
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                               QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLabel, QLineEdit)
from PySide6.QtGui import QIcon
from qasync import QEventLoop

# Constants
NEW_PATH = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(1, str(NEW_PATH))
import parsers.socket.Python.decoder
import parsers.socket.Python.udp_client


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("RTLOC API Tools - Distance Example")
        self.setWindowIcon(QIcon("RTLOCpng.png"))
        self.resize(800, 600)
        # Setup UI elements
        self.setup_ui()

    def setup_ui(self): 
        """Setup UI elements."""
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Control Buttons
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.on_button_clicked)
        
        self.button_pause = QPushButton("Pause")
        self.button_pause.clicked.connect(self.pause)
        
        self.button_stop = QPushButton("Stop")
        self.button_stop.clicked.connect(self.stop)
        
        # User input fields
        self.ip_edit = QLineEdit()
        self.ip_edit.setPlaceholderText("Enter IP address")
        
        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("Enter port number")
        
        # IP and port layout
        ip_port_layout = QHBoxLayout()
        ip_port_layout.addWidget(QLabel("IP address"))
        ip_port_layout.addWidget(self.ip_edit)
        ip_port_layout.addWidget(QLabel("Port"))
        ip_port_layout.addWidget(self.port_edit)        
        
        # Control Buttons layout
        control_buttons_layout = QHBoxLayout()
        control_buttons_layout.addWidget(self.button_start)
        control_buttons_layout.addWidget(self.button_pause)
        control_buttons_layout.addWidget(self.button_stop)
        
        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addLayout(ip_port_layout)
        layout.addLayout(control_buttons_layout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container) 
        
        # On startup not yet connected
        self.connected = False
        
    def on_button_clicked(self):
        """Handle button click event."""
        # If already connected, resume logging
        if self.connected:
            self.running = True
        else:
            self.connected = True
            self.text_edit.append("Button clicked!")
            self.running = True
            asyncio.ensure_future(self.run_script())
        self.button_start.setEnabled(False)
        self.button_pause.setEnabled(True)
        
    # Note that this simply stops the autoscrolling but not the logging itself
    def pause(self):
        self.button_start.setText("Resume")
        self.button_start.setEnabled(True)
        self.button_pause.setEnabled(False)
        self.running = False
    
    
    def stop(self):
        self.running = False
        self.udp_client.connection_lost(lambda: self.udp_client.transport)
        
    async def run_script(self):
        """Run the main script."""
        loop = asyncio.get_running_loop()
        self.udp_client = parsers.socket.Python.udp_client.UDPClient(loop)
        
        ip_adress = self.ip_edit.text()
        port = int(self.port_edit.text())
        
        self.log_and_print(f"[UDP] - connecting to ({ip_adress}) on port {port}")
        
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: self.udp_client,
            local_addr=(ip_adress, port))
        
        while 1:
            await self.process_data(self.udp_client)
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
        if self.running:
                self.text_edit.moveCursor(PySide6.QtGui.QTextCursor.End)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        sys.exit(loop.run_forever())
