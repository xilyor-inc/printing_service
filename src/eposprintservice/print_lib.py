from escpos.printer import Network
from PIL import Image
import io


class Printer:
    def __init__(self):
        self.printer = None
        self.is_connected = False
        self.__align = 'left'
        self.__font = 'a'
        self.__bold = False
        self.__underline = 0
        self.__width = 1
        self.__height = 1
        self.__density = 9
        self.__invert = False
        self.__smooth = False
        self.__flip = False
        self.__double_width = False
        self.__double_height = False
        self.__custom_size = False

    def connect_printer(self, ip, port):
        # Connect to the network printer
        self.printer = Network(ip, port=port)

        print(self.printer, ip, port)

        # Display an alert when the button is clicked
        if self.printer is None:
            self.is_connected = False
        else:
            self.is_connected = True

        return self.is_connected

    def print_text(self, text):
        if self.is_connected:
            self.printer.text(text)
            return True
        return False

    def cut_paper(self):
        self.printer.cut()

    def apply_style(self):
        """ Set text properties by sending them to the printer
        :param align: horizontal position for text, possible values are:

            * 'center'
            * 'left'
            * 'right'

            *default*: 'left'

        :param font: font given as an index, a name, or one of the
            special values 'a' or 'b', referring to fonts 0 and 1.
        :param bold: text in bold, *default*: False
        :param underline: underline mode for text, decimal range 0-2,  *default*: 0
        :param double_height: doubles the height of the text
        :param double_width: doubles the width of the text
        :param custom_size: uses custom size specified by width and height
            parameters. Cannot be used with double_width or double_height.
        :param width: text width multiplier when custom_size is used, decimal range 1-8,  *default*: 1
        :param height: text height multiplier when custom_size is used, decimal range 1-8, *default*: 1
        :param density: print density, value from 0-8, if something else is supplied the density remains unchanged
        :param invert: True enables white on black printing, *default*: False
        :param smooth: True enables text smoothing. Effective on 4x4 size text and larger, *default*: False
        :param flip: True enables upside-down printing, *default*: False

        :type font: str
        :type invert: bool
        :type bold: bool
        :type underline: bool
        :type smooth: bool
        :type flip: bool
        :type custom_size: bool
        :type double_width: bool
        :type double_height: bool
        :type align: str
        :type width: int
        :type height: int
        :type density: int
        """
        align = self.__align
        font = self.__font
        bold = self.__bold
        underline = self.__underline
        width = self.__width
        height = self.__height
        density = self.__density
        invert = self.__invert
        smooth = self.__smooth
        flip = self.__flip
        double_width = self.__double_width
        double_height = self.__double_height
        custom_size = self.__custom_size
        self.printer.set(align, font, bold, underline, width, height, density, invert, smooth,
                         flip, double_width, double_height, custom_size)

    def close_printer(self):
        self.printer.close()

    def get_paper_status(self):
        return self.printer.paper_status()

    def set_font(self, font):
        """
        Set the font style for the text.
        Possible values for font: 'a', 'b', 'c'.
        """
        self.__font = font
        self.apply_style()

    def set_size(self, width, height):
        """
        Set the font size for the text.
        Parameters:
        - width: Width of the font (1 to 8).
        - height: Height of the font (1 to 8).
        """
        self.__width = width
        self.__height = height
        self.apply_style()

    def set_align(self, align):
        """
        Set the alignment of the text.
        Possible values for align: 'left', 'center', 'right'.
        """
        self.__align = align
        self.apply_style()

    def set_bold(self, bold=True):
        """
        Set the bold style for the text.
        Parameters:
        - bold: Boolean value indicating whether to enable bold style (default: True).
        """
        self.__bold = bold
        self.apply_style()

    def set_underline(self, underline=True):
        """
        Set the underline style for the text.
        Parameters:
        - underline: Boolean value indicating whether to enable underline style (default: True).
        """
        self.__underline = underline
        self.apply_style()

    def set_inverted(self, inverted=True):
        """
        Set the reverse color style for the text.
        Parameters:
        - reverse: Boolean value indicating whether to enable reverse color style (default: True).
        """
        self.__invert = inverted
        self.apply_style()

    def set_width(self, width):
        """
        Set the reverse color style for the text.
        Parameters:
        - reverse: Boolean value indicating whether to enable reverse color style (default: True).
        """
        self.__invert = width
        self.apply_style()

    def set_height(self, height):
        """
        Set the reverse color style for the text.
        Parameters:
        - reverse: Boolean value indicating whether to enable reverse color style (default: True).
        """
        self.__invert = height
        self.apply_style()

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

    def print_table(self, table_data, col_widths):

        # Print the table
        for row in table_data:
            for col, width in zip(row, col_widths):
                self.printer.text(col.ljust(width))
            self.printer.text("\n")

    def print_test_text(self):
        text = "Hello World!\n"
        self.set_bold(True)
        self.print_text("Bold: "+text)
        self.set_bold(False)
        self.print_text("Normal: "+text)
        self.set_font('a')
        self.print_text("Font A: "+text)
        self.set_font('b')
        self.print_text("Font B: "+text)
        self.set_size(8, 8)
        self.print_text("Size 8x8: "+text)
        self.set_size(7, 7)
        self.print_text("Size 7x7: "+text)
        self.set_size(6, 6)
        self.print_text("Size 6x6: "+text)
        self.set_size(5, 5)
        self.print_text("Size 5x5: "+text)
        self.set_size(4, 4)
        self.print_text("Size 4x4: "+text)
        self.set_size(3, 3)
        self.print_text("Size 3x3: "+text)
        self.set_size(2, 2)
        self.print_text("Size 2x2: "+text)
        self.set_size(1, 1)
        self.print_text("Size 1x1: "+text)
        self.set_align('left')
        self.print_text("Left: "+text)
        self.set_align('center')
        self.print_text("Center: "+text)
        self.set_align('right')
        self.print_text("Right: "+text)
        self.cut_paper()

    def print_test_table(self):
        table = [
            ["Wide Col 1", "Col 2", "Col 3"],
            ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
            ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"],
            ["Row 3 Col 1", "Row 3 Col 2", "Row 3 Col 3"],
            ["Row 4 Col 1", "Row 4 Col 2", "Row 4 Col 3"],
        ]
        col_widths = [32, 8, 8]
        self.print_table(table, col_widths)


