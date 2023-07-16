#!/usr/bin/python3
import socket
import time
from umodbus import conf
from umodbus.client import tcp

# Adjust modbus configuration
conf.SIGNED_VALUES = True

# Define the IP address and port of the Modbus server
SERVER_IP = '83.136.254.139'
SERVER_PORT = 37988

# Define the number of retries and delay between retries
MAX_RETRIES = 3
RETRY_DELAY = 5

def connect_to_modbus(slave_id, server_ip=SERVER_IP, server_port=SERVER_PORT):
    # Create a socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the Modbus server
    try:
        print(f"Attempting to connect to the Modbus server at {server_ip}:{server_port} with Slave ID {slave_id}...")
        sock.connect((server_ip, server_port))
        print(f"Connection to the Modbus server successful with Slave ID {slave_id}.")
        return sock
    except ConnectionRefusedError:
        print(f"Connection to the Modbus server at {server_ip}:{server_port} with Slave ID {slave_id} refused.")
    except Exception as e:
        print(f"Connection to the Modbus server at {server_ip}:{server_port} with Slave ID {slave_id} failed. Error: {e}")
    return None

def read_modbus_value(sock, slave_id, address, quantity=100):
    # Define the Modbus command to read holding registers
    request = tcp.read_holding_registers(slave_id=slave_id, starting_address=address, quantity=quantity)

    retry_count = 0
    while retry_count < MAX_RETRIES:  # Retry up to MAX_RETRIES times
        print(f"Sending Modbus command to read value at address {address} for Slave ID {slave_id}...")
        try:
            response = tcp.send_message(request, sock)

            # Check if the response contains an error code
            if isinstance(response, int):
                if response == 72:  # Retry if server is busy
                    print(f"Server is busy, retrying after {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                    retry_count += 1
                    print(f"Retry attempt {retry_count}/{MAX_RETRIES}")
                    continue  # Retry the request
                else:
                    print(f"Error reading value for address {address} and Slave ID {slave_id}. Error code: {response}")
                    return None
            else:
                # Response contains a single or multiple registers
                if hasattr(response, 'registers'):
                    # Response contains multiple registers
                    values = [register.value for register in response.registers]
                    print(f"Values successfully read from address {address} (Slave ID {slave_id}): {values}")
                    return values
                elif hasattr(response, 'value'):
                    # Response contains a single register
                    value = response.value
                    print(f"Value successfully read from address {address} (Slave ID {slave_id}): {value}")
                    return value
                else:
                    print(f"Unknown response format for address {address} and Slave ID {slave_id}. Response: {response}")
                    return None
        except Exception as e:
            print(f"Error reading value for address {address} and Slave ID {slave_id}. Error: {e}")
            return None

    print(f"Unable to read value for address {address} and Slave ID {slave_id} after {MAX_RETRIES} retries.")
    return None

def print_menu():
    print("\nMenu Options:")
    print("1. Read Modbus Value")
    print("2. Exit")

def main():
    slave_id = int(input("Enter the Slave ID: "))
    starting_addresses = [6, 10, 12, 16, 20, 21, 22, 26, 27, 31, 32, 36, 47, 52, 53, 57, 63, 69, 73, 77, 83, 86, 87, 88, 89, 93, 95, 96, 97, 99, 194, 195, 196, 114, 122, 123, 126, 128, 131, 133, 134, 137, 138, 139, 140, 141, 143, 144, 145, 146, 148, 149, 153, 154, 155, 157, 163, 166, 168, 173, 177, 178, 179, 180, 181, 183, 188, 189, 193, 203, 206, 207, 210, 214, 215, 216, 219, 220, 221, 224, 225, 226, 229, 231, 232, 234, 235, 236, 239, 241, 245, 249, 253, 255, 259, 263, 266, 270]

    sock = connect_to_modbus(slave_id)

    if sock:
        print(f"Connection to Slave ID {slave_id} established.")
        while True:
            print_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                address = int(input("Enter the Modbus address: "))
                print(f"Checking address {address} for Slave ID {slave_id}...")
                value = read_modbus_value(sock, slave_id, address)
                if value is not None:
                    print(f"Value at address {address} (Slave ID {slave_id}): {value}")
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")

            # Pause for 3 seconds before proceeding to the next address
            time.sleep(3)

        sock.close()
        print(f"Connection to Slave ID {slave_id} closed.")
    else:
        print("Connection failed. Exiting...")

if __name__ == "__main__":
    main()
