#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import subprocess
import os
import time


def get_tycmd_boards():

    boards = []

    try:

        output = subprocess.check_output(["tycmd","list"]).decode()

        for line in output.splitlines():

            if "add" in line:

                parts = line.split()

                serial_num = parts[1].split("-")[0]

                boards.append(serial_num)

    except:
        pass

    return boards


def get_serial_ports():

    ports = {}

    for p in serial.tools.list_ports.comports():

        if "ttyACM" in p.device:

            ports[p.serial_number] = p.device

    return ports


def detect_modules():

    tycmd_boards = get_tycmd_boards()

    serial_ports = get_serial_ports()

    boards = []

    print("\nDetected Teensy modules:\n")

    for serial_num in tycmd_boards:

        module_name = None

        if serial_num in serial_ports:

            device = serial_ports[serial_num]

            try:

                ser = serial.Serial(device,115200,timeout=2)

                time.sleep(1)

                ser.write(b'm')

                time.sleep(0.3)

                line = ser.readline().decode(errors='ignore').strip()

                ser.close()

                if "|" in line:
                    module_name = line

            except:
                pass

        if module_name is None:

            module_name = serial_num + " | Unknown Module"

        boards.append(serial_num)

        print(str(len(boards)) + ". " + module_name)

    return boards


def choose_board(boards):

    choice = input("\nSelect board number: ")

    try:
        return boards[int(choice)-1]
    except:
        print("Invalid selection")
        return None


def find_hex_files():

    hex_files = []

    for root, dirs, files in os.walk("."):

        for f in files:

            if f.endswith(".hex"):

                hex_files.append(os.path.join(root,f))

    if not hex_files:

        print("\nNo .hex files found\n")
        return None

    print("\nAvailable firmware:\n")

    for i,f in enumerate(hex_files):

        print(str(i+1) + ". " + f)

    choice = input("\nSelect firmware number: ")

    try:
        return hex_files[int(choice)-1]
    except:
        return None


def upload(board, firmware):

    print("\nEntering bootloader...\n")

    subprocess.call([
        "tycmd",
        "reset",
        "--board",
        board,
        "--bootloader"
    ])

    time.sleep(1)

    print("\nUploading " + firmware + "\n")

    subprocess.call([
        "tycmd",
        "upload",
        "--board",
        board,
        firmware
    ])


def main():

    while True:

        print("\nType 'list' to show Teensy modules")
        print("Type 'q' to quit")

        cmd = input("\nCommand: ")

        if cmd == "list":

            boards = detect_modules()

            if not boards:
                print("No modules detected")
                continue

            board = choose_board(boards)

            if not board:
                continue

            firmware = find_hex_files()

            if firmware:
                upload(board, firmware)

        elif cmd == "q":
            break


if __name__ == "__main__":
    main()