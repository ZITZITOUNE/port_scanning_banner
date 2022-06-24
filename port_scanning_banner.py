#!/usr/bin/env python3
import time
import sys
import os
import socket
import time
import concurrent.futures

banners = '''
███████ ██ ████████    ███████ ██ ████████  ██████  ██    ██ ███    ██ ███████    ██
   ███  ██    ██          ███  ██    ██    ██    ██ ██    ██ ████   ██ ██         ██
  ███   ██    ██         ███   ██    ██    ██    ██ ██    ██ ██ ██  ██ █████      ██
 ███    ██    ██        ███    ██    ██    ██    ██ ██    ██ ██  ██ ██ ██
███████ ██    ██       ███████ ██    ██     ██████   ██████  ██   ████ ███████    ██

************************************************************************************
*                          Copyright of Hamza MOUNIR, 2022                         *
*                           https://github.com/ZITZITOUNE                          *
************************************************************************************
'''

# clear
def clear_screen():
    # for windows OS
    if os.name == "nt":
        os.system("cls")

        # for linux / Mac OS
    else:
        os.system("clear")

# colored text and background
def colorRed(clr): print("\033[91m {}\033[00m".format(clr))
def colorGreen(clr): print("\033[92m {}\033[00m".format(clr))
def colorYellow(clr): print("\033[93m {}\033[00m".format(clr))
def colorLightPurple(clr): print("\033[94m {}\033[00m".format(clr))
def colorPurple(clr): print("\033[95m {}\033[00m".format(clr))
def colorCyan(clr): print("\033[96m {}\033[00m".format(clr))
def colorLightGray(clr): print("\033[97m {}\033[00m".format(clr))
def colorBlack(clr): print("\033[98m {}\033[00m".format(clr))
def colorReset(clr): print("\033[0m {}\033[00m".format(clr))

# example usage and help
if len(sys.argv) == 1:
    print(f'\nExample usage: python3 port_scanning_banner 127.0.0.1 -p 20-5000\n(Use "-h" option for more info)')
    sys.exit()
if '-h' in sys.argv or '--help' in sys.argv:
    print('''
Example usage: python3 port_scanning_banner 127.0.0.1 -p 20-5000 
-h                     To show this message
-p                     Range of ports to scan. (default : 1-65535)''')
    sys.exit()
min_range, max_range = 1, 65535
ip = sys.argv[1]
if '-p' in sys.argv:
    min_range, max_range = sys.argv[sys.argv.index('-p') + 1].split('-')

# function scanner
def scanner(port):
    open = "OPEN"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        print(
            f"Port {str(port).ljust(5)}{str(open).ljust(10)} {socket.getservbyport(port, 'tcp').ljust(14)} {grab_banner(ip, port)}")
    except socket.timeout:
        s.close()
# function for banner grabbing
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024).decode()
        s.close()
        return banner
    except:
        return

# main
def main():
    clear_screen()
    colorRed(banners)
    colorGreen("─" * 83)
    print(f"Scanning {str(int(max_range) + 1 - int(min_range))} ports in {ip}")
    colorGreen("─" * 83)
    print("PORT      STATE      SERVICE        BANNER")
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = [executor.submit(scanner, i) for i in range(
            int(min_range), int(max_range) + 1)]
        for f in concurrent.futures.as_completed(results):
            f.result()
    end = time.perf_counter()
    colorGreen("─" * 83)
    print(f"Scanning lasted {round(end - start, 2)}seconds")

# call main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)