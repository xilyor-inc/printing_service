from flask import Flask, request, jsonify
from print_lib import Printer
from flask_cors import CORS  # Import the CORS extension


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/', methods=['GET'])
def nik_ommk():
    return jsonify({"status": "ok"})


printer = Printer()


@app.route('/connect_printer', methods=['POST'])
def connect_printer():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    if ip and port:
        is_connected = printer.connect_printer(ip, port)
        if is_connected:
            return jsonify({"status": "connected"}), 200
        else:
            return jsonify({"error": "connection failed"}), 500
    return jsonify({"error": "invalid data"}), 400



@app.route('/disconnect_printer', methods=['POST'])
def disconnect_printer():
    printer.close_printer()
    return jsonify({"status": "disconnected successfully"}), 200

@app.route('/print', methods=['POST'])
def print__():

    json_data = request.json

    for i in range(len(json_data)):
        item = json_data[i]

        print("Table Size:", len(json_data), "Item:", i)
        print(item)

        # Execute the appropriate method based on the command
        if item.startswith("PRINT:"):
            command, text = item.split(':', 1)
            printer.print_text(text)
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
            printer.print_table(table, cols_width)
            print("Table printed was: ", table)
        elif item == "NEW_LINE":
            printer.print_text("\n")
        elif item == "CENTER":
            printer.set_align("center")
        elif item == "LEFT":
            printer.set_align("left")
        elif item == "RIGHT":
            printer.set_align("right")
        elif item == "CUT_PAPER":
            printer.cut_paper()
        elif item == "CLOSE_PRINTER":
            printer.close_printer()
        elif item == "SET_FONT_A":
            printer.set_font('a')
        elif item == "SET_FONT_B":
            printer.set_font('b')
        elif item == "SET_SIZE":
            cmd, width, height = map(int, item.split(','))
            printer.set_size(width, height)
        elif item == "SET_BOLD":
            printer.set_bold(True)
        elif item == "UNSET_BOLD":
            printer.set_bold(False)
        elif item == "SET_UNDERLINE":
            printer.set_underline(2)
        elif item == "UNSET_UNDERLINE":
            printer.set_underline(0)
        elif item == "SET_INVERTED":
            printer.set_inverted(True)
        elif item == "UNSET_INVERTED":
            printer.set_inverted(False)
        elif item.startswith("WIDTH:"):
            command, text = item.split(':', 1)
            printer.set_width(int(text))
        elif item.startswith("HEIGHT:"):
            command, text = item.split(':', 1)
            printer.set_height(int(text))
        elif item == "TABLE_END":
            pass
        elif item == "PRINT_IMAGE":
            pass
            # printer.print_image(text)
        else:
            print("Unknown command:", item)

    # Send a response
    return jsonify({"status": "ok"}), 200

# app = PrintServer.create_app()
app.run(host="0.0.0.0", port=8000)