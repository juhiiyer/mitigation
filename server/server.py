import socket
import sys
import threading

def handle_client(client_socket, address):
    print(f"[+] Accepted connection from {address[0]}:{address[1]}")
    try:
        # Just send a simple welcome message and close
        client_socket.send(b"TCP Server Ready\n")
        client_socket.close()
    except Exception as e:
        print(f"[-] Error handling client {address}: {e}")

def start_server(host='0.0.0.0', port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
    except Exception as e:
        print(f"[-] Bind failed: {e}")
        sys.exit(1)
        
    server.listen(128) # Backlog size
    print(f"[*] Listening on {host}:{port}")

    while True:
        client, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
