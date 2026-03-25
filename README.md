# Teensy Multi-Board CLI Setup (Jetson)

# Install dependencies
sudo apt update
sudo apt install build-essential cmake libudev-dev

# Download TyTools source
wget https://github.com/Koromix/tytools/archive/refs/tags/v0.9.8.tar.gz
tar -xzf v0.9.8.tar.gz
cd tytools-0.9.8

# Build tycmd only (no GUI)
mkdir build
cd build
cmake .. -DCONFIG_TYCOMMANDER_BUILD=0 -DCONFIG_TYUPLOADER_BUILD=0
make -j$(nproc)

# Install tycmd
sudo cp tycmd /usr/local/bin/

# Verify installation
tycmd list

# Basic tycmd commands
tycmd list
tycmd upload --board <serial> firmware.hex
tycmd reset --board <serial>
tycmd reset --board <serial> --bootloader

# Check python version
python3 --version

# Create CLI tool
nano teensy_cli.py

# Make executable
chmod +x teensy_cli.py

# Run CLI tool
python3 teensy_cli.py