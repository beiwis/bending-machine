from pyax12.connection import Connection

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyAMA0", baudrate=1000000)

# Ping the dynamixel unit(s)
ids_available = serial_connection.scan()

for dynamixel_id in ids_available:
    print(dynamixel_id)

serial_connection.pretty_print_control_table(1)

# Close the serial connection
serial_connection.close()