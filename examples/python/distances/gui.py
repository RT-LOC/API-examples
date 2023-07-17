
import asyncio
import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTableWidgetItem,
                               QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QComboBox, QStackedWidget, QTableWidget)
from PySide6.QtGui import QIcon, QTextCursor
from qasync import QEventLoop

# Constants
NEW_PATH = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(1, str(NEW_PATH))
import parsers.socket.Python.decoder
import parsers.socket.Python.udp_client


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.init_ui()
        self.init_connection_state()

    def init_ui(self):
        """Initializes all UI components and configures UI layout."""
        self.configure_window()
        self.create_display_stack()
        self.create_control_buttons()
        self.create_config_widgets()
        self.configure_layouts()

    def init_connection_state(self):
        """Initializes state variables for connection and script running status."""
        self.running = False
        self.connected = False
        self.tags = set()
        self.anchors = set()

    def configure_window(self):
        """Configures the main window properties."""
        self.setWindowTitle("RTLOC API Tools - Distance Example")
        self.setWindowIcon(QIcon("RTLOCpng.png"))
        self.resize(800, 600)

    def create_display_stack(self):
        """Creates the display stack for switching between text and table display."""
        self.display_stack = QStackedWidget()
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.table_display = QTableWidget()
        self.display_stack.addWidget(self.text_display)
        self.display_stack.addWidget(self.table_display)
        self.display_stack.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
    def add_anchor(self, anchor_id):
        if anchor_id not in self.anchors:
            self.anchors.add(anchor_id)
            row_position = self.table_display.rowCount()
            self.table_display.insertRow(row_position)
            self.table_display.setVerticalHeaderItem(row_position, QTableWidgetItem(str(anchor_id)))
            for i in range(self.table_display.columnCount()):
                self.table_display.setItem(row_position, i, QTableWidgetItem("-"))
    
    def add_tag(self, tag_id):
        if tag_id not in self.tags:
            self.tags.add(tag_id)              
            colum_position = self.table_display.columnCount()
            self.table_display.insertColumn(colum_position)
            self.table_display.setHorizontalHeaderItem(colum_position, QTableWidgetItem(str(tag_id)))
            for i in range(self.table_display.rowCount()):
                self.table_display.setItem(i, colum_position, QTableWidgetItem("-"))

    def create_control_buttons(self):
        """Creates buttons for controlling the script."""
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.start)

        self.button_pause = QPushButton("Pause")
        self.button_pause.clicked.connect(self.pause)

        self.button_stop = QPushButton("Stop")
        self.button_stop.clicked.connect(self.stop)
        

    def create_config_widgets(self):
        """Creates widgets for configuring the script."""
        self.ip_edit = QLineEdit()
        self.ip_edit.setPlaceholderText("Enter IP address")

        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("Enter port number")

        self.config_dropdown = QComboBox()
        self.config_dropdown.setPlaceholderText("Select config")
        self.config_dropdown.addItems(["main.py", "cross.py"])
        self.config_dropdown.currentIndexChanged.connect(self.config_dropdown_changed)

    def configure_layouts(self):
        """Configures the layouts for the UI."""
        configuration_layout = self.create_configuration_layout()
        control_buttons_layout = self.create_control_buttons_layout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display_stack)
        main_layout.addLayout(configuration_layout)
        main_layout.addLayout(control_buttons_layout)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_configuration_layout(self):
        """Creates the layout for the configuration widgets."""
        configuration_layout = QHBoxLayout()
        configuration_layout.addWidget(QLabel("IP address:"))
        configuration_layout.addWidget(self.ip_edit)
        configuration_layout.addWidget(QLabel("Port:"))
        configuration_layout.addWidget(self.port_edit)
        configuration_layout.addWidget(QLabel("Config:"))
        configuration_layout.addWidget(self.config_dropdown)
        return configuration_layout

    def create_control_buttons_layout(self):
        """Creates the layout for the control buttons."""
        control_buttons_layout = QHBoxLayout()
        control_buttons_layout.addWidget(self.button_start)
        control_buttons_layout.addWidget(self.button_pause)       
        control_buttons_layout.addWidget(self.button_stop)
        return control_buttons_layout

    def config_dropdown_changed(self):
        if self.config_dropdown.currentText() == "main.py":
            self.display_stack.setCurrentWidget(self.text_display)
            self.current_config = "main.py"
        elif self.config_dropdown.currentText() == "cross.py":
            self.display_stack.setCurrentWidget(self.table_display)
            self.current_config = "cross.py"
        
    def start(self):
        # Check if all fields are filled in
        if self.port_edit.text() == "" or self.ip_edit.text() == "" or hasattr(self, "current_config") == False:
            self.log_and_print("Please fill in all fields configuration fields")
            return
        
        # If already connected, resume logging
        if self.connected:
            self.running = True
            
        # Not yet connected, start script up
        else:
            self.connected = True
            self.running = True
            self.start_script(self.current_config)
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
    
    def start_script(self, config):
        asyncio.ensure_future(self.main_script())

        
    async def main_script(self):
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
            self.log_and_print(f"fr = {frame_nr}")
            for x in range(len(data)):
                self.log_and_print(f"> T {data[x][0]}: [", end="")
                tag_id = data[x][0]
                self.add_tag(tag_id)
                anchors = data[x][3]
                for idx, anchor in enumerate(anchors):
                    if idx != 0:
                        self.log_and_print(", ", end="")
                    anchor_id = anchors[idx][0]
                    distance = anchors[idx][1]
                    self.add_anchor(anchor_id)
                    self.table_display.setItem(list(self.anchors).index(anchor_id), list(self.tags).index(tag_id), QTableWidgetItem(str(distance)))
                    self.log_and_print(f"{anchor_id}:{anchors[idx][1]}", end="")
                self.log_and_print("]")
                


    def log_and_print(self, message, end='\n'):
        """Log the message and print it to the console."""
        print(message, end=end)
        self.display_stack.widget(0).insertPlainText(message + end)
        if self.running:
            self.display_stack.widget(0).moveCursor(QTextCursor.End)
                    
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        sys.exit(loop.run_forever())
