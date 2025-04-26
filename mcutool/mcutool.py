import argparse
from tools import enterboot, enterapp

parser = argparse.ArgumentParser(
    description="MCU control tool")
group = parser.add_manually_exclusive_group(required=True)

group.add_argument(
    '--enterboot', 
    action='store_true',
    help='Put MCU into bootloader mode')

group.add_argument(
    '--enterapp', 
    action='store_true',
    help='Put MCU into app mode')

args, unknown = parser.parse_known_args()

if args.enterboot:
    enterboot.main(unknown)

elif args.enterapp:
    enterapp.main(unknown)