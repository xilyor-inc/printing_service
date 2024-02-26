from escpos.printer import Network
from PIL import Image
import io


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

    def set_font(self, font):
        """
        Set the font style for the text.
        Possible values for font: 'a', 'b', 'c'.
        """
        self.printer.set(font=font)

    def set_size(self, width, height):
        """
        Set the font size for the text.
        Parameters:
        - width: Width of the font (1 to 8).
        - height: Height of the font (1 to 8).
        """
        self.printer.set(width=width, height=height)

    def set_align(self, align):
        """
        Set the alignment of the text.
        Possible values for align: 'left', 'center', 'right'.
        """
        self.printer.set(align=align)

    def set_bold(self, bold=True):
        """
        Set the bold style for the text.
        Parameters:
        - bold: Boolean value indicating whether to enable bold style (default: True).
        """
        self.printer.set(bold=bold)

    def set_underline(self, underline=True):
        """
        Set the underline style for the text.
        Parameters:
        - underline: Boolean value indicating whether to enable underline style (default: True).
        """
        self.printer.set(underline=underline)

    def set_reverse(self, reverse=True):
        """
        Set the reverse color style for the text.
        Parameters:
        - reverse: Boolean value indicating whether to enable reverse color style (default: True).
        """
        self.printer.set(reverse=reverse)

    def print_image(self, image_data):
        if not self.is_connected:
            return False

        try:
            # Load image from binary data
            image = Image.open(io.BytesIO(image_data))

            # Convert image to monochrome bitmap
            width, height = image.size
            image = image.convert('1')  # Convert to 1-bit monochrome bitmap

            # Send image data to the printer
            self.printer.image(image, width, height)
            return True
        except Exception as e:
            print(f"Error printing image: {e}")
            return False
