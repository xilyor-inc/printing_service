import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT
import threading
from .print_lib import Printer
from .server import PrintServer


class ePosPrintService(toga.App):
    main_window = None
    printer = Printer()
    input_ip = None
    input_port = None
    server_indicator = None

    def startup(self):

        address_box = toga.Box()
        port_box = toga.Box()
        buttons_box = toga.Box()
        log_view_box = toga.Box()
        main_box = toga.Box()

        # IP address input field
        ip_label = toga.Label('IP Address:')
        self.input_ip = toga.TextInput(value='192.168.1.37', placeholder='Enter The Printer IP')
        # Port input field
        port_label = toga.Label('Port:')
        self.input_port = toga.TextInput(value='9100', placeholder='Enter The Printer Port')

        # Buttons
        btn_connect = toga.Button('Connect to Printer', on_press=self.connect_printer)
        btn_disconnect = toga.Button('Disconnect', on_press=self.disconnect_printer)
        btn_test_printer = toga.Button('Test Printer', on_press=self.print_test_text)
        btn_start_server = toga.Button('Start Server', on_press=self.start_server)
        self.server_indicator = toga.Label("OFF", style=Pack(text_align=RIGHT))

        # Add widgets to the main box
        address_box.add(ip_label)
        address_box.add(self.input_ip)
        port_box.add(port_label)
        port_box.add(self.input_port)
        buttons_box.add(btn_connect)
        buttons_box.add(btn_disconnect)

        main_box.add(address_box)
        main_box.add(port_box)
        main_box.add(buttons_box)
        main_box.add(btn_test_printer)
        main_box.add(btn_start_server)
        main_box.add(self.server_indicator)

        main_box.style.update(direction=COLUMN, padding=10)
        address_box.style.update(direction=ROW, padding=5)
        port_box.style.update(direction=ROW, padding=5)
        buttons_box.style.update(direction=ROW, padding=5)

        self.input_ip.style.update(width=220, padding=5)
        self.input_port.style.update(width=100, padding=5)
        ip_label.style.update(width=100, padding=5, alignment=CENTER)
        port_label.style.update(width=100, padding=5, alignment=CENTER)

        # Add the main box to the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def connect_printer(self, widget, debug=True):
        print("Connect to Network Printer")
        # Get IP and port from input fields
        ip = self.input_ip.value
        port = int(self.input_port.value)

        # Connect to the network printer
        self.printer.connect_printer(ip, port)
        if debug:
            if self.printer.is_connected:
                self.main_window.info_dialog('Info', 'Successfully connected to printer!')
            else:
                self.main_window.error_dialog('Error', 'Failed to connect to printer!')

    def print_test_text(self, widget):
        self.connect_printer(widget, debug=False)
        self.printer.print_test_text()
        self.disconnect_printer(widget)

    def disconnect_printer(self, widget):
        self.printer.close_printer()

    def start_server(self, widget):
        PrintServer.set_printer(self.printer)
        # Create a new thread to run the server
        server_thread = threading.Thread(target=PrintServer.run_server)
        # Start the thread
        server_thread.start()
        self.server_indicator.label = "ON"


def main():
    return ePosPrintService()
