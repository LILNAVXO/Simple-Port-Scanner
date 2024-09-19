import socket
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    def __init__(self, target, port_range):
        self.target = target
        self.port_range = port_range

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    return port, True
                else:
                    return  port, False
        except Exception as error:
            print(f"An error occurred: {error}")
            return port, False
    def scan(self):
        open_ports = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.scan_port, range(self.port_range[0], self.port_range[1] + 1))
            for port, is_open in results:
                if is_open:
                    open_ports.append(port)
        return open_ports

if __name__ == "__main__":
    target = input("Enter Target IP address or HostName: ")
    port_range = input("Enter Port Range E.g(20, 80 etc): ").split("-")
    port_range = (int(port_range[0]), int(port_range[1]))
    scanner = PortScanner(target, port_range)
    print(f"Scanning {target} for Open ports in range {port_range[0]} to {port_range[1]}...\n")
    open_ports = scanner.scan()

    if open_ports:
        print(f"Open Ports: {open_ports}")
    else:
        print("No Open Ports Found")

