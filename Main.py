import socket
import threading

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            print(f"Port {port} is OPEN")

def threaded_scan(target, ports):
    threads = [threading.Thread(target=scan_port, args=(target, p)) for p in ports]
    for t in threads: t.start()
    for t in threads: t.join()
# Usage: threaded_scan("127.0.0.1", range(1, 1025))
threaded_scan("127.0.0.1",range(1,1025))