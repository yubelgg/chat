# This code will in Unix-based systems (Linux/FreeBSD/MAC)
import sys
from select import select
from socket import *

BUFFER_SIZE = 65507


def main():
    # Create a UDP socket
    clientSock = socket(AF_INET, SOCK_DGRAM)

    user_name = input("Enter your name: ")

    # Initialize server address
    peer = ("localhost", 20000)

    clientSock.sendto(user_name.encode(), peer)

    timeout = 0.05

    while True:
        try:
            rset, _, _ = select([clientSock, sys.stdin], [], [], timeout)

            for ready in rset:
                if ready is clientSock:
                    data, addr = ready.recvfrom(BUFFER_SIZE)
                    print(data.decode())
                    print(end="", flush=True)
                elif ready is sys.stdin:
                    user_input = sys.stdin.readline().strip()

                    if user_input == "quit":
                        clientSock.close()
                        return

                    if user_input == "users":
                        clientSock.sendto("users".encode(), peer)
                        print(end="", flush=True)
                        continue

                    # Send the message to the server
                    if user_input.startswith("to "):
                        parts = user_input.split(" msg ")
                        if len(parts) != 2:
                            print("Invalid message format")
                            continue

                        recipients = parts[0][3:].strip()
                        message = parts[1].strip()

                        if recipients == "all":
                            formatted_msg = f"TO:all:{message}"
                        else:
                            formatted_msg = f"TO:{recipients}:{message}"
                        clientSock.sendto(formatted_msg.encode(), peer)

                    # user leaving the server
                    if user_input == "leave":
                        clientSock.sendto("leave".encode(), peer)
                        print("---> bye")
                        clientSock.close()
                        return

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

    clientSock.close()


if __name__ == "__main__":
    main()
