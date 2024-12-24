# import socket

# UDP_IP = "10.150.149.137"
# UDP_PORT = 5005
# MESSAGE = "1"

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))

# print(f"Sent '{MESSAGE}' to {UDP_IP}:{UDP_PORT}")

import socket

UDP_IP = "211.182.230.537"  # 모든 네트워크 인터페이스에서 수신
UDP_PORT = 5008

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))  # 지정된 IP와 포트로 바인딩

print(f"Listening on {UDP_IP}:{UDP_PORT}")

while True:
    # 데이터 수신
    data, addr = sock.recvfrom(1024)  # 버퍼 크기: 1024 바이트
    print(f"Received message: {data.decode('utf-8')} from {addr}")