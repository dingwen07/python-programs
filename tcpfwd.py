import socket
import threading
import argparse
import sys

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join([f"{x:0{digits}X}" for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append(f"{i:04X}   {hexa:<{length*(digits + 1)}}   {text}")
    return '\n'.join(result)

def forward_data(source, target, quiet):
    while True:
        data = source.recv(1024)
        if len(data) == 0:  # No more data, close the connection
            break
        if not quiet:
            print(hexdump(data))
        target.send(data)
    source.close()
    target.close()

def handle_client(client_socket, remote_host, remote_port, quiet):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    client_thread = threading.Thread(target=forward_data, args=(client_socket, remote_socket, quiet))
    remote_thread = threading.Thread(target=forward_data, args=(remote_socket, client_socket, quiet))
    client_thread.start()
    remote_thread.start()

def start_proxy(local_port, remote_host, remote_port, quiet):
    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    server.bind(("::", local_port))
    server.listen(5)
    print(f"[*] Listening on [::]:{local_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port, quiet))
        client_thread.start()

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Proxy Tool")
    parser.add_argument("-p", "--local-port", required=True, type=int, help="Local port to listen on")
    parser.add_argument("-R", "--remote-host", required=True, type=str, help="Remote host to forward to")
    parser.add_argument("-P", "--remote-port", required=True, type=int, help="Remote port to forward to")
    parser.add_argument("-q", "--quiet", action="store_true", help="Enable quiet mode (no data print)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    start_proxy(args.local_port, args.remote_host, args.remote_port, args.quiet)
