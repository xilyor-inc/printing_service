import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .print_lib import Printer


class ePosPrintService(toga.App):
    printer = Printer()

    def startup(self):
        main_box = toga.Box()

        # Create buttons
        btn_connect = toga.Button('Connect to Network Printer', on_press=self.connect)
        btn_print = toga.Button('Print Test Text', on_press=self.print_test_text)

        # Add the buttons to the main box
        main_box.add(btn_connect)
        main_box.add(btn_print)

        # Add the main box to the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def show_alert(self, widget):
        # Display an alert when the button is clicked
        self.main_window.info_dialog('Alert', 'Button clicked! hoho')

    def connect(self, widget):
        print("Connect to Network Printer")
        # Get IP and port from input fields
        ip = '192.168.1.33'  # self.ip_input.value
        port = 9100  # self.port_input.value

        # Connect to the network printer
        self.printer.connect_printer(ip, port)
        if self.printer.is_connected:
            self.main_window.info_dialog('Info', 'Successfully connected to printer!')
        else:
            self.main_window.error_dialog('Error', 'Failed to connect to printer!')

    def print_test_text(self, widget):
        self.printer.print_text('Hello, World!')
        self.printer.cut_paper()
        self.printer.close_printer()


def main():
    return ePosPrintService()
