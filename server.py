from flask import Flask, request, jsonify
from print_lib import Printer
from flask_cors import CORS  # Import the CORS extension


class PrintServer:
    printer = None

    @classmethod
    def set_printer(cls, printer_instance):
        cls.printer = printer_instance

    @classmethod
    def create_app(cls):
        app = Flask(__name__)
        CORS(app)  # Enable CORS for all routes

        @app.route('/connect_printer', methods=['POST'])
        def connect_printer():
            data = request.json
            ip = data.get('ip')
            port = data.get('port')
            if ip and port:
                is_connected = cls.printer.connect_printer(ip, port)
                if is_connected:
                    return jsonify({"status": "connected"}), 200
                else:
                    return jsonify({"error": "connection failed"}), 500
            return jsonify({"error": "invalid data"}), 400

        @app.route('/print_test', methods=['GET'])
        def print_test():
            if cls.printer:
                cls.printer.print_text("This is a test page")
                return jsonify({"status": "test page printed"}), 200
            return jsonify({"error": "printer not connected"}), 400

        @app.route('/print_table', methods=['GET'])
        def print_table():
            if cls.printer:
                cls.printer.print_text("Printing test table")
                return jsonify({"status": "test table printed"}), 200
            return jsonify({"error": "printer not connected"}), 400

        return app

# Uncomment this to run the Flask server directly from this script (optional)
# if __name__ == "__main__":
#     printer = Printer()
#     PrintServer.set_printer(printer)
#     app = PrintServer.create_app()
#     app.run(host="0.0.0.0", port=8000 )
