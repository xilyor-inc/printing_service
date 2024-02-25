from escpos.printer import Network


class Printer:
    printer = None
    is_connected = False

    def connect_printer(self, ip, port):
        # Connect to the network printer
        self.printer = Network(ip, port=port)

        print(self.printer)

        # Display an alert when the button is clicked
        if self.printer is None:
            self.is_connected = False
        else:
            self.is_connected = True

    def print_text(self, text):
        if self.is_connected:
            self.printer.text(text)
            return True
        return False

    def cut_paper(self):
        self.printer.cut()

    def close_printer(self):
        self.printer.close()
