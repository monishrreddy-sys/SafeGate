import serial
import serial.tools.list_ports

print("script running")

class SerialHandler:
    def __init__(self):
        self.ser = None
        self.connected = False

    def list_available_ports(self):
        """
        Returns a list of available COM ports.
        Example:
        ['COM3', 'COM4']
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port, baudrate=9600):
        """
        Connect to Arduino.
        Example:
        connect("COM4")
        """
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=1
            )

            self.connected = True

            print(f"Connected to {port}")

            return True

        except Exception as e:
            print(f"Connection Error: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """
        Disconnect Arduino safely.
        """
        if self.ser and self.ser.is_open:
            self.ser.close()

        self.connected = False
        print("Disconnected")

    def read_message(self):
        """
        Reads one line from Arduino.

        Returns:
            str message
            None if nothing received
        """

        if not self.connected:
            return None

        try:
            if self.ser.in_waiting > 0:
                message = (
                    self.ser.readline()
                    .decode("utf-8")
                    .strip()
                )

                return message

        except Exception as e:
            print(f"Read Error: {e}")

        return None


# ----------------------------
# TESTING
# ----------------------------

if __name__ == "__main__":

    handler = SerialHandler()

    print("\nAvailable Ports:")
    print(handler.list_available_ports())

    port = input("\nEnter COM Port (Example COM4): ")

    if handler.connect(port):

        print("\nListening...\n")

        try:
            while True:

                msg = handler.read_message()

                if msg:
                    print(msg)

        except KeyboardInterrupt:
            print("\nStopped by user")

        finally:
            handler.disconnect()