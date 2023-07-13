import customtkinter as ctk 
import main
import sys
from pathlib import Path
import asyncio
import parsers.socket.Python.udp_client
import parsers.socket.Python.decoder
import os
import threading
import time

        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Distance Display")
        self.geometry("1000x600")

        self.columnconfigure("0 1 2 3 4 5", weight=1)
        self.rowconfigure(0, weight=1)
        
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
        
        self.output_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=6)
        
        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_script)
        self.start_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=3)
        
        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_script)
        self.stop_button.grid(row=1, column=3, padx=5, pady=5, sticky="nsew", columnspan=3)
        self.stop_button.configure(state="disabled")
        
        self.ip_entry = ctk.CTkEntry(self, placeholder_text="IP Address")
        self.ip_entry.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.port_dropdown = ctk.CTkOptionMenu(self, values=["13101 (live data)", "13102 (recorded data)"])
        self.port_dropdown.grid(row=2, column=2, padx=5, pady=5, sticky="nsew", columnspan=2)
        
        self.mode_dropdown = ctk.CTkOptionMenu(self, values=["text", "table"])
        self.mode_dropdown.grid(row=2, column=4, padx=5, pady=5, sticky="nsew", columnspan=2)
        
    def start_script(self):
        self.port_dropdown.configure(state="disabled")
        self.ip_entry.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        if self.mode_dropdown.get() == "text":
            self.textbox = ctk.CTkTextbox(self.output_frame)
            self.textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            
        
        self.textbox.insert('end', "Starting script... \n")
        self.textbox.insert('end', "IP: " + self.ip_entry.get() + "\n")
        
        if self.port_dropdown.get() == "13101 (live data)":
            self.port = 13101
        if self.port_dropdown.get() == "13102 (recorded data)":
            self.port = 13102
        self.textbox.insert('end',"Port: " + str(self.port) + "\n")
        
        newPath = Path(__file__).resolve().parent.parent.parent.parent
        sys.path.insert(1, str(newPath))
        
        self.thread = threading.Thread(target=self.run_script, args=(self.ip_entry.get(), self.port))
        self.thread.start()
    
    
    def stop_script(self):
        self.running = False
        
        # Create new thread to wait for the script to end
        # If we don't do this, the GUI will freeze cause the main thread is waiting for the script to end
        threading.Thread(target=self.wait_for_script_end).start()

    def wait_for_script_end(self):
        self.thread.join()
        self.port_dropdown.configure(state="normal")
        self.ip_entry.configure(state="normal")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
    def run_script(self, ip_addr_server, port):
        # Small sleep to see to what the GUI will connect
        time.sleep(2)
        self.running = True
        asyncio.run(script(ip_addr_server, port, self))

async def script(ip_addr_server, port, App):
    # Get the running loop
    loop = asyncio.get_running_loop()

    #Create the UDP client
    udpClient = parsers.socket.Python.udp_client.UDPClient(asyncio.get_running_loop())
    
    App.textbox.insert('end', "[UDP] - connecting to (" + ip_addr_server + ") on port " + str(port) + "\n")
    
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udpClient,
        local_addr=(ip_addr_server, port))
    App.textbox.insert('end', "[UDP] - connected to (" + ip_addr_server + ") on port " + str(port) + "\n")
    
    while App.running:
        # Read out the data
        data, frameNr = udpClient.read_data()
        if data != -1:
            # Generate anchor positions array and corresponding measurements array
            measurements=[]
            
            # clearConsole()
            App.textbox.insert('end', "Frame: " + str(frameNr) + "\n")
            for x in range(0,len(data)):
                App.textbox.insert('end', "> T " + str(data[x][0]) + ": [")
                # Select anchors_data   
                anchors = data[x][3]
                
                # Within anchors_data -> #anchor_id, anchor_dist, anchor_los1, anchor_rssi1, anchor_los2, anchor_rssi2, anchor_offset
                for idx in anchors:
                    if idx != 0:
                        App.textbox.insert('end', ", ")
                    measurements.append(anchors[idx][1])
                    anchor_id = anchors[idx][0]
                    App.textbox.insert('end', str(anchor_id) + ":" + str(anchors[idx][1]))
                App.textbox.insert('end', "]\n")
                App.textbox.see('end')
            # print(measurements)
        await asyncio.sleep(0.01)
  
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    

