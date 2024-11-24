from socket import *


def main():
    # Create a UDP socket
    serverSock = socket(AF_INET, SOCK_DGRAM)

    # Initialize server address
    serverAddress = ("", 20000)

    # Bind the socket to the address
    try:
        serverSock.bind(serverAddress)
    except Exception as e:
        print("Bind error:", e)
        serverSock.close()
        return

    BUFFER_SIZE = 65507
    print("Server is ready and waiting for messages at UDP port 20000")

    users = {}  # {clientAddress: username}

    while True:
        try:
            # Receive message from client
            data, clientAddress = serverSock.recvfrom(BUFFER_SIZE)
            if not data:
                break

            if clientAddress not in users:
                users[clientAddress] = data.decode()
                print(f"{data.decode()} joined the chat")
            elif data.decode() == "users":
                user_list = "Online users: " + ", ".join(users.values())
                serverSock.sendto(user_list.encode(), clientAddress)
            elif data.decode() == "leave":
                user_name = users[clientAddress]
                del users[clientAddress]
                print(f"{user_name} left the chat")
            elif data.decode().startswith("TO:all:"):
                sender = users[clientAddress]
                message = data.decode().split(":")[2]
                for addr, name in users.items():
                    if addr != clientAddress:
                        formatted_msg = f"{sender} says: {message}"
                        serverSock.sendto(formatted_msg.encode(), addr)
            elif data.decode().startswith("TO:"):
                sender = users[clientAddress]
                _, recipients, message = data.decode().split(":")
                recipients = recipients.split(" ")
                for recipient in recipients:
                    recipient_address = None
                    for addr, name in users.items():
                        if name == recipient:
                            recipient_address = addr
                            break

                    if recipient_address:
                        formatted_msg = f"{sender} says: {message}"
                        serverSock.sendto(formatted_msg.encode(), recipient_address)
                    else:
                        formatted_msg = f"Error message: {recipient} is not online"
                        serverSock.sendto(formatted_msg.encode(), clientAddress)

        except Exception as e:
            print("Error receiving from client:", e)
            break

    serverSock.close()


if __name__ == "__main__":
    main()
