from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from .print_lib import Printer


class PrintServer(BaseHTTPRequestHandler):
    port = 8000
    printer = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def set_printer(cls, printer: Printer):
        cls.printer = printer

    def do_POST(self):
        print("---------------------------" + self.path + "--------------------------------")
        if self.path == '/connect_printer':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = json.loads(post_data.decode('utf-8'))
            ip = json_data['ip']
            port = int(json_data['port'])

            code = 445
            msg = b'Failed to connect to printer'
            # Set the printer
            if self.printer.connect_printer(ip, port):
                code = 200
                msg = b'printer connected successfully'

            # Send a response
            self.send_response(code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(msg)

        elif self.path == '/disconnect_printer':
            self.printer.close_printer()
            code = 200

            # Send a response
            self.send_response(code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'printer disconnected successfully')

        elif self.path == '/print':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = json.loads(post_data.decode('utf-8'))

            # Print the received JSON data
            print(json_data)

            for i in range(len(json_data)):
                item = json_data[i]

                print("Table Size:", len(json_data), "Item:", i)
                print(item)

                # Execute the appropriate method based on the command
                if item.startswith("PRINT:"):
                    command, text = item.split(':', 1)
                    self.printer.print_text(text)
                elif item.startswith("TABLE:"):
                    command, cols_width = item.split(':', 1)
                    cols_width = cols_width.split(',')  # example 20,8,8
                    # Convert each number from string to integer using map() and list comprehension
                    cols_width = [int(num_str) for num_str in cols_width]
                    table = []
                    table_finished = False
                    while not table_finished and i < len(json_data):
                        i = i + 1
                        item = json_data[i]
                        if item == "TABLE_END":
                            i = i + 1
                            table_finished = True
                        else:
                            # split the item by comma
                            row = item.split(',')
                            table.append(row)

                    # print the table after has been constructed
                    self.printer.print_table(table, cols_width)
                elif item == "NEW_LINE":
                    self.printer.print_text("\n")
                elif item == "CENTER":
                    self.printer.set_align("center")
                elif item == "LEFT":
                    self.printer.set_align("left")
                elif item == "RIGHT":
                    self.printer.set_align("right")
                elif item == "CUT_PAPER":
                    self.printer.cut_paper()
                elif item == "CLOSE_PRINTER":
                    self.printer.close_printer()
                elif item == "SET_FONT_A":
                    self.printer.set_font('a')
                elif item == "SET_FONT_B":
                    self.printer.set_font('b')
                elif item == "SET_SIZE":
                    cmd, width, height = map(int, item.split(','))
                    self.printer.set_size(width, height)
                elif item == "SET_BOLD":
                    self.printer.set_bold(True)
                elif item == "UNSET_BOLD":
                    self.printer.set_bold(False)
                elif item == "SET_UNDERLINE":
                    self.printer.set_underline(2)
                elif item == "UNSET_UNDERLINE":
                    self.printer.set_underline(0)
                elif item == "SET_INVERTED":
                    self.printer.set_inverted(True)
                elif item == "UNSET_INVERTED":
                    self.printer.set_inverted(False)
                elif item.startswith("WIDTH:"):
                    command, text = item.split(':', 1)
                    self.printer.set_width(int(text))
                elif item.startswith("HEIGHT:"):
                    command, text = item.split(':', 1)
                    self.printer.set_height(int(text))
                elif item == "TABLE_END":
                    pass
                elif item == "PRINT_IMAGE":
                    pass
                    # self.printer.print_image(text)
                else:
                    print("Unknown command:", item)

            # Send a response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Received POST request')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            if self.printer is not None:
                self.end_headers()
                self.wfile.write(b'<h2>Printing Test Page...</h2>')
                self.printer.print_test_text()
            else:
                self.send_response(430)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"""
                <h2>Printer not connected</h2><h3>Please connect to printer by sending a POST request
                to http://printer-ip-address:printer-port/connect_printer</h3>""")

        elif self.path == '/table':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            if self.printer is not None:
                self.end_headers()
                self.wfile.write(b'<h2>Printing Test Table...</h2>')
                self.printer.print_test_table()
            else:
                self.send_response(430)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"""
                <h2>Printer not connected</h2><h3>Please connect to printer by sending a POST request
                to http://printer-ip-address:printer-port/connect_printer</h3>""")

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    @classmethod
    def run_server(cls):
        server_address = ('', cls.port)
        httpd = HTTPServer(server_address, cls)
        print(f'Starting server on port {cls.port}...')
        httpd.serve_forever()



# PrintServer.run_server()
