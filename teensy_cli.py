#!/usr/bin/env python3

import subprocess
import os


def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode("utf-8")


def list_boards():
    output = run_cmd(["tycmd", "list"])
    lines = [l for l in output.splitlines() if l.startswith("add")]

    boards = []

    print("\nConnected Teensy boards:\n")

    for i, line in enumerate(lines):
        parts = line.split()
        serial = parts[1].split("-")[0]
        boards.append(serial)

        print(str(i + 1) + ". " + line)

    return boards


def choose_board(boards):

    choice = input("\nSelect board number: ")

    try:
        idx = int(choice) - 1
        return boards[idx]
    except:
        print("Invalid selection")
        return None


def browse_hex(start_dir="."):

    current = os.path.abspath(start_dir)

    while True:

        print("\nCurrent directory:", current)
        print("\nFolders and .hex files:\n")

        items = []

        if current != "/":
            print("0. .. (go up)")
            items.append("..")

        files = sorted(os.listdir(current))

        for f in files:
            path = os.path.join(current, f)

            if os.path.isdir(path):
                items.append(f)
                print(str(len(items)) + ". [DIR] " + f)

            elif f.endswith(".hex"):
                items.append(f)
                print(str(len(items)) + ". [HEX] " + f)

        choice = input("\nSelect item (or 'q' to cancel): ")

        if choice == "q":
            return None

        try:
            idx = int(choice)

            if idx == 0:
                current = os.path.dirname(current)
                continue

            selected = items[idx - 1]
            path = os.path.join(current, selected)

            if os.path.isdir(path):
                current = path
                continue

            if selected.endswith(".hex"):
                return path

        except:
            print("Invalid selection")


def upload(board, firmware):

    print("\nUploading firmware:", firmware, "\n")

    subprocess.call([
        "tycmd",
        "upload",
        "--board",
        board,
        firmware
    ])


def reset_board(board):

    subprocess.call([
        "tycmd",
        "reset",
        "--board",
        board
    ])


def bootloader(board):

    subprocess.call([
        "tycmd",
        "reset",
        "--board",
        board,
        "--bootloader"
    ])


def main():

    while True:

        print("\nCommands:")
        print("list  - list boards")
        print("exit  - quit")

        cmd = input("\nCommand: ")

        if cmd == "list":

            boards = list_boards()

            if not boards:
                print("No boards detected")
                continue

            board = choose_board(boards)

            if not board:
                continue

            print("\nOptions:")
            print("1 Upload firmware")
            print("2 Reset board")
            print("3 Enter bootloader")
            print("4 Back")

            opt = input("\nSelect option: ")

            if opt == "1":

                firmware = browse_hex()

                if firmware:
                    upload(board, firmware)

            elif opt == "2":

                reset_board(board)

            elif opt == "3":

                bootloader(board)

        elif cmd == "exit":
            break


if __name__ == "__main__":
    main()