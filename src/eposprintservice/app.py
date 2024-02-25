import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from escpos.printer import Network


class ePosPrintService(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        # Create buttons for printing text and barcode
        print_text_button = toga.Button('Print Text', on_press=self.print_text)
        print_text_button2 = toga.Button('Print Text2', on_press=self.print_text2)
        print_barcode_button = toga.Button('Print Barcode', on_press=self.show_alert)

        # Add the buttons to the main box
        main_box.add(print_text_button)
        main_box.add(print_text_button2)
        main_box.add(print_barcode_button)

        # Add the main box to the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def show_alert(self, widget):
        # Display an alert when the button is clicked
        self.main_window.info_dialog('Alert', 'Button clicked! hoho')

    def print_text(self, widget):
        # Display an alert when the button is clicked
        self.main_window.info_dialog('Alert', 'goodle hoho')
        print("goodle hoho")



    def print_text2(self, widget):
        # Connect to the network printer
        printer = Network('192.168.1.33', port=9100)
        random_text = "Hello World!!!" # self.generate_random_text()
        printer.text("Random Text: {}\n".format(random_text))
        printer.cut()
        printer.close()


def main():
    return ePosPrintService()
