import socket
import threading

from scapy.all import ARP, Ether, srp


def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            print(f"Port {port} is OPEN")

def threaded_scan(target, ports):
    threads = [threading.Thread(target=scan_port, args=(target, p)) for p in ports]
    for t in threads: t.start()
    for t in threads: t.join()

def find_ip(target_ip):

    
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether/arp
    result = srp(packet, timeout=3)[0]
    # a list of clients, we will fill this in the upcoming loop
    clients = []
    for sent, received in result:
    # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))
    


# Button to retrieve the value

# Usage: threaded_scan("127.0.0.1", range(1, 1025))
find_ip("192.168.1.0/24")
ip = input("ip address do you want to scan for ports from teh list of ports")
threaded_scan(ip,range(1,1025))

