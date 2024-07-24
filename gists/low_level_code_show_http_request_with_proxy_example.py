import socket
import ssl

# Proxy server details
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 7890

# Target website details
TARGET_HOST = 'www.baidu.com'
TARGET_PORT = 443

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((PROXY_HOST, PROXY_PORT))

# Send CONNECT request to the proxy server
request = f"CONNECT {TARGET_HOST}:{TARGET_PORT} HTTP/1.1\r\n" \
          f"Host: {TARGET_HOST}\r\n\r\n"
sock.sendall(request.encode())

# Receive response from the proxy server
response = sock.recv(1024 * 1024).decode()
print(response)

# Check if the connection was successful
if "200 Connection established" in response:
    # Wrap the socket with SSL if the target website uses HTTPS
    context = ssl._create_unverified_context()
    ssl_sock = context.wrap_socket(sock, server_hostname=TARGET_HOST)

    # Send HTTP GET request to the target website
    get_request = f"GET / HTTP/1.1\r\n" \
                  f"Host: {TARGET_HOST}\r\n\r\n"
    ssl_sock.sendall(get_request.encode())

    # Receive the response from the target website
    data = ssl_sock.recv(1024 * 1024).decode()
    print(data)

    # Close the connection
    ssl_sock.close()

else:
    print("Proxy connection failed!")
    sock.close()
