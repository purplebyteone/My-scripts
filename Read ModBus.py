#!/usr/bin/env python
import socket
from umodbus import conf
from umodbus.client import tcp
from datetime import datetime
import json
import time

# datetime object containing current date and time
def current_time():
    now = datetime.now().isoformat()
    return now

host = '94.237.49.147'   # IP address of your target Modbus server
port = 40274
client = tcp.ModbusTcpClient(host, port)  # Creating an instance of ModbusTcpClient with the target IP and port

while True:
    try:
        # Step 1: Establish TCP connection to the Modbus server
        print("Connecting to the Modbus server...")
        client.connect()
        print("Connection successful!")

        # Step 2: Read coils (function code 01)
        print("Reading coils...")
        rr_coils = client.read_coils(1, 0, 5)  # Read 5 coils starting from address 0, unit ID is 1
        print("Coils data:", rr_coils.bits)  # The data read from the coils will be stored in the 'bits' attribute of the response object (rr_coils)

        # Step 3: Read discrete inputs (function code 02)
        print("Reading discrete inputs...")
        rr_discrete_inputs = client.read_discrete_inputs(1, 0, 5)  # Read 5 discrete inputs starting from address 0, unit ID is 1
        print("Discrete inputs data:", rr_discrete_inputs.bits)  # The data read from the discrete inputs will be stored in the 'bits' attribute of the response object (rr_discrete_inputs)

        # Step 4: Read holding registers (function code 03)
        print("Reading holding registers...")
        rr_holding_registers = client.read_holding_registers(1000, 5, unit=1)  # Read 5 holding registers starting from address 1000, unit ID is 1
        print("Holding registers data:", rr_holding_registers.registers)  # The data read from the holding registers will be stored in the 'registers' attribute of the response object (rr_holding_registers)

        # Step 5: Read input registers (function code 04)
        print("Reading input registers...")
        rr_input_registers = client.read_input_registers(1000, 5, unit=1)  # Read 5 input registers starting from address 1000, unit ID is 1
        print("Input registers data:", rr_input_registers.registers)  # The data read from the input registers will be stored in the 'registers' attribute of the response object (rr_input_registers)

        # Step 6: Prepare data for output
        data = {
            "datetime": current_time(),  # Get the current date and time
            "coils_data": rr_coils.bits,
            "discrete_inputs_data": rr_discrete_inputs.bits,
            "holding_registers_data": rr_holding_registers.registers,
            "input_registers_data": rr_input_registers.registers
        }
        print(json.dumps(data))  # Print the data in JSON format

        # Step 7: Wait for 5 seconds before repeating the process
        print("Waiting for 5 seconds...")
        time.sleep(5)
    except Exception as e:
        # Handle exceptions, such as connection errors
        print(f"Error: {e}")
        print("Attempting to reconnect...")
        client.close()  # Close the current connection
        time.sleep(5)  # Wait for 5 seconds before attempting to reconnect
