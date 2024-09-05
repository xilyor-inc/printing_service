from server import PrintServer
from print_lib import Printer

printer = Printer()
PrintServer.set_printer(printer)
PrintServer.run_server()