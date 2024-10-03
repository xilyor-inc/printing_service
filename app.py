from server import PrintServer
from print_lib import Printer

# Initialize the printer and set it in the server
printer = Printer()
PrintServer.set_printer(printer)

# Create and run the Flask app
app = PrintServer.create_app()
app.run(host="0.0.0.0", port=8000)
