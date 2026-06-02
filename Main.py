import socket
import threading
import time
from scapy.all import ARP, Ether, srp


def grab_banner(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((target, port))

            # Try sending a basic HTTP request
            try:
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            except:
                pass

            banner = s.recv(1024).decode(errors="ignore").strip()

            if banner:
                return banner
            else:
                return "No banner returned"

    except:
        return "Banner unavailable"


def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)

        if s.connect_ex((target, port)) == 0:
            try:
                service = socket.getservbyport(port)
                result = f"Port {port} ({service}) is OPEN"
            except OSError:
                result = f"Port {port} is OPEN"

            # Banner grabbing
            banner = grab_banner(target, port)
            result += f" | Banner: {banner}"

            print(result)

            # Save to file
            with open("results.txt", "a") as f:
                f.write(result + "\n")


def threaded_scan(target, ports):
    threads = [threading.Thread(target=scan_port, args=(target, p)) for p in ports]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def find_ip(target_ip):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=False)[0]

    clients = []

    for sent, received in result:
        clients.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })

    print("\nAvailable devices in the network:")
    print("IP" + " " * 18 + "MAC")

    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))


# ---------------- MAIN ---------------- #
choice = input("Discover devices on network, does require Npcap to be installed? (y/n): ")
if choice.lower() == "y":
    find_ip("192.168.1.0/24")


ip = input("\nEnter the IP address you want to scan from the list above: ")

# Hostname lookup
try:
    hostname = socket.gethostbyaddr(ip)[0]
    print(f"Hostname found: {hostname}")
except socket.herror:
    print("Hostname not found")

start = int(input("Start port: "))
end = int(input("End port: "))

# Clear old results
open("results.txt", "w").close()

startTime = time.time()

threaded_scan(ip, range(start, end + 1))

print(f"\nTook {round(time.time() - startTime, 2)} seconds to scan")
print("Open ports + banners saved to results.txt")