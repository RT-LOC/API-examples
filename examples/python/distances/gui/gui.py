
import asyncio
import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTableWidgetItem,
                               QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QComboBox, QStackedWidget, QTableWidget)
from PySide6.QtGui import QIcon, QTextCursor
from qasync import QEventLoop
from ui_widget import Ui_Widget

# Constants
NEW_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(1, str(NEW_PATH))
import parsers.socket.Python.decoder
import parsers.socket.Python.udp_client


class Widget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("RTLOC API Tools - Distance Example")
        self.init_connection_state()
        self.setup_signals()

    def init_connection_state(self):
        """Initializes state variables for connection and script running status."""
        self.running = False
        self.connected = False
        self.tags = set()
        self.anchors = set()

    def setup_signals(self):
        """Setup signals for the buttons."""
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        
    def add_anchor(self, anchor_id):
        if anchor_id not in self.anchors:
            self.anchors.add(anchor_id)
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setVerticalHeaderItem(row_position, QTableWidgetItem(str(anchor_id)))
            for i in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row_position, i, QTableWidgetItem("-"))
    
    def add_tag(self, tag_id):
        if tag_id not in self.tags:
            self.tags.add(tag_id)              
            colum_position = self.tableWidget.columnCount()
            self.tableWidget.insertColumn(colum_position)
            self.tableWidget.setHorizontalHeaderItem(colum_position, QTableWidgetItem(str(tag_id)))
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.setItem(i, colum_position, QTableWidgetItem("-"))

    def clear_anchors(self, current_anchors):
        """Clear all anchors that are not in the current frame."""
        for anchor in self.anchors:
            if anchor not in current_anchors:
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.setItem(list(self.anchors).index(anchor), i, QTableWidgetItem("-"))            
    
    def clear_tags(self, current_tags):
        """Clear all tags that are not in the current frame."""
        for tag in self.tags:
            if tag not in current_tags:
                for i in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(i, list(self.tags).index(tag), QTableWidgetItem("-"))
        
    def start(self):
        # Check if all fields are filled in
        print("Testing")
        if self.port_line_edit.text() == "" or self.ip_line_edit.text() == "":
            self.log_and_print("Please fill in all fields configuration fields")
            return
        
        # If already connected, resume logging
        if self.connected:
            self.running = True
            
        # Not yet connected, start script up
        else:
            self.connected = True
            self.running = True
            self.start_script()
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        
    # Note that this simply stops the autoscrolling but not the logging itself
    def pause(self):
        self.start_button.setText("Resume")
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.running = False
    
    
    def stop(self):
        self.running = False
        self.udp_client.connection_lost(lambda: self.udp_client.transport)
    
    def start_script(self):
        asyncio.ensure_future(self.main_script())

        
    async def main_script(self):
        """Run the main script."""
        loop = asyncio.get_running_loop()
        self.udp_client = parsers.socket.Python.udp_client.UDPClient(loop)
        
        ip_adress = self.ip_line_edit.text()
        port = int(self.port_line_edit.text())
        
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
            current_tags = set()
            current_anchors = set()
            for x in range(len(data)):
                self.log_and_print(f"> T {data[x][0]}: [", end="")
                tag_id = data[x][0]
                self.add_tag(tag_id)
                current_tags.add(tag_id)
                anchors = data[x][3]
                for idx, anchor in enumerate(anchors):
                    if idx != 0:
                        self.log_and_print(", ", end="")
                    anchor_id = anchors[idx][0]
                    current_anchors.add(anchor_id)
                    distance = anchors[idx][1]
                    self.add_anchor(anchor_id)
                    
                    # Qt has no clean built in way to acces the row and column of a QTableWidgetItem based on
                    # what item is in the header so I had to do it like this
                    if self.running:
                        for i in range(self.tableWidget.rowCount()):
                            if(self.tableWidget.verticalHeaderItem(i).text() == str(anchor_id)):
                                for j in range(self.tableWidget.columnCount()):
                                    if(self.tableWidget.horizontalHeaderItem(j).text() == str(tag_id)):
                                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(distance)))
                    self.log_and_print(f"{anchor_id}:{anchors[idx][1]}", end="")
                self.log_and_print("]")
            if self.running:
                self.clear_tags(current_tags)
                self.clear_anchors(current_anchors)
            
                


    def log_and_print(self, message, end='\n'):
        """Log the message and print it to the console."""
        self.textEdit.insertPlainText(message + end)
        if self.running:
            self.textEdit.moveCursor(QTextCursor.End)
                    
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Widget()
    window.show()
    with loop:
        sys.exit(loop.run_forever())