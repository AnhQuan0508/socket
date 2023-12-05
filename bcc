import socket

def send_email(to_address, cc_addresses, bcc_addresses, subject, body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 2500))

    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)

    # Send EHLO as part of the initial connection
    client_socket.sendall("EHLO example.com\r\n".encode())
    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)

    # Email Headers
    email_headers = f"Subject: {subject}\r\n"
    email_headers += f"To: {','.join(to_address)}\r\n"
    email_headers += f"Cc: {','.join(cc_addresses)}\r\n"
    email_headers += f"Bcc: {','.join(bcc_addresses)}\r\n"

    # Send MAIL FROM
    client_socket.sendall((f'MAIL FROM:<sender@example.com>\r\n').encode())
    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)

    # Send RCPT TO for TO
    for to_address in to_address:
        client_socket.sendall((f'RCPT TO:<{to_address}>\r\n').encode())
        recv_msg = client_socket.recv(1024).decode()
        print(recv_msg)

    # Send RCPT TO for CC
    for cc_address in cc_addresses:
        client_socket.sendall((f'RCPT TO:<{cc_address}>\r\n').encode())
        recv_msg = client_socket.recv(1024).decode()
        print(recv_msg)

    # Send RCPT TO for BCC
    for bcc_address in bcc_addresses:
        client_socket.sendall((f'RCPT TO:<{bcc_address}>\r\n').encode())
        recv_msg = client_socket.recv(1024).decode()
        print(recv_msg)

    # Send DATA
    client_socket.sendall("DATA\r\n".encode())
    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)

    # Send email headers and body
    client_socket.sendall((email_headers + "\r\n" + body + "\r\n.\r\n").encode())
    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)

    # Close the connection
    client_socket.sendall("QUIT\r\n".encode())
    recv_msg = client_socket.recv(1024).decode()
    print(recv_msg)

    client_socket.close()

if __name__ == "__main__":
    to_addresses = ["recipient1@example.com", "recipient2@example.com"]
    cc_addresses = ["cc1@example.com", "cc2@example.com"]
    bcc_addresses = ["bcc1@example.com", "bcc2@example.com"]
    subject = "Example Subject"
    body = "Hello, this is the email body!"

    send_email(to_addresses, cc_addresses, bcc_addresses, subject, body)
