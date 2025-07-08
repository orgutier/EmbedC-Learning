What you need to have before running automated flashing process with mcutool:

---- Install the toolchain (arm-none-eabi)
sudo apt install cmake gcc-arm-none-eabi build-essential libnewlib-arm-none-eabi git
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib

---- Setup
wget https://raw.githubusercontent.com/raspberrypi/pico-setup/master/pico_setup.sh
chmod +x pico_setup.sh
./pico_setup.sh

---- Download pico sdk, submodule command may take a while
mkdir -p ~/pico
cd ~/pico
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init
export PICO_SDK_PATH=/home/orgutier/pico/pico-sdk/       <-- Use your own path
source ~/.bashrc

---- Configure zero as pico probe
git clone https://github.com/raspberrypi/picotool.gi
cd picotool
sudo apt install libusb-1.0-0-dev

---- Build
cmake ../ -DPICO_BOARD=pico2 -DCMAKE_BUILD_TYPE=Debug


---- Upload and test code
// One terminal
sudo openocd -f interface/cmsis-dap.cfg -f target/rp2350.cfg -c "adapter speed 5000"
// Another
gdb blink.elf
target remote localhost:3333
load // That one actually flashes the code
monitor reset init
continue

---- Use owned mcutool to reset
python ~/EmbedC-Learning/mcutool/mcutool.py --enterapp 