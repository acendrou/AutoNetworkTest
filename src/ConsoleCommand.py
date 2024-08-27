from telnetlib import Telnet


class ConsoleCommand:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.telnet = Telnet(host=self.address, port=self.port)

    def write(self, command: str):
        self.telnet.write(command.encode())

    def read_line(self, timeout: int) -> str:
        return str(self.telnet.read_until(match=b"\n", timeout=timeout))

    def read_lines(self, timeout: int, number_lines: int) -> [str]:
        lines = []
        for _ in range(number_lines):
            lines.append(str(self.telnet.read_until(match=b"\n", timeout=timeout)))
            if lines[-1] is None:
                return None
        return lines

    def __del__(self):
        self.telnet.close()
