import serial
# import keyboard
from shared_memory_dict import SharedMemoryDict


def initialize_shared_memory():
	"""Initialize shared memory dictionaries."""
	smd_RVL = SharedMemoryDict(name='RVL', size=1024)
	smd_BZZ = SharedMemoryDict(name='BZZ', size=1024)
	return smd_RVL, smd_BZZ


def initialize_serial_connection(port='/dev/ttyACM0', baudrate=115200):
	"""Initialize and return the serial connection to Arduino."""
	return serial.Serial(
		port=port,
		baudrate=baudrate,
		parity=serial.PARITY_NONE,
		bytesize=serial.EIGHTBITS,
		stopbits=serial.STOPBITS_ONE,
		timeout=1,
	)


def process_statuses(arduino, smd_RVL, smd_BZZ):
	"""Process shared memory status updates and communicate with Arduino."""
	temp_RVL_Status = ''
	temp_BZZ_Status = ''
	Data_Sent_Status = False

	while True:

			# if keyboard.is_pressed('q'):  # Exit on 'q' key press
			# 	print("Exiting program...")
			# 	break
		try:
			val_RVL = smd_RVL['RVL']
			val_BZZ = smd_BZZ['BZZ']

			if Data_Sent_Status != 'Sending':
				if temp_BZZ_Status != val_BZZ or temp_RVL_Status != val_RVL:
					temp_BZZ_Status = val_BZZ
					temp_RVL_Status = val_RVL

					if val_RVL == 'RVL_ON' and val_BZZ == 'BZZ_OFF':
						arduino.write(bytes('a', 'utf-8'))
						Data_Sent_Status = 'Sending'
						print("Data Sent: 'a'.")
					elif val_RVL == 'RVL_ON' and val_BZZ == 'BZZ_ON':
						arduino.write(bytes('b', 'utf-8'))
						Data_Sent_Status = 'Sending'
						print("Data Sent: 'b'.")
					elif val_RVL == 'RVL_OFF' and val_BZZ == 'BZZ_OFF':
						arduino.write(bytes('c', 'utf-8'))
						Data_Sent_Status = 'Sending'
						print("Data Sent: 'c'.")
					else:
						print("Invalid command! Please try again.")

			data = arduino.readline()
			if data:
				data_decoded = data.decode('utf-8').strip()
				if data_decoded in {'a', 'b', 'c'}:
					if Data_Sent_Status == 'Sending':
						print(f"Data Received: {data_decoded}")
						Data_Sent_Status = 'Done'
						print(f"Sent Status: {Data_Sent_Status}")


		except Exception as e:
			print(f"Error: Forklift.py not Running {e}")
			if Data_Sent_Status != 'Sending':
				arduino.write(bytes('z', 'utf-8'))
				Data_Sent_Status = 'Sending'
				print("Data Sent: 'z'.")
			data = arduino.readline()
			if Data_Sent_Status == 'Sending':
				print(f"Data Received: {data.decode('utf-8').strip()}")
				Data_Sent_Status = 'Done'
				print(f"Sent Status: {Data_Sent_Status}")


def main():
	"""
    Entry point for the script.
    Initializes shared memory and serial connection,
    then processes statuses in a loop.
    """
	smd_RVL, smd_BZZ = initialize_shared_memory()
	arduino = initialize_serial_connection()
	process_statuses(arduino, smd_RVL, smd_BZZ)


if __name__ == "__main__":
	main()
