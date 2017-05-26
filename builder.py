#!/usr/bin/python3
import sys
import argparse

from src.lib import fs
from src.lib import util

## Setup CLI
parser = argparse.ArgumentParser(description = 'Bitwig device multitool')

parser.add_argument('-C',
    dest = 'cleanup',
    action = 'store_true',
    default = False,
    help = 'clean up the device data')

parser.add_argument('device',
    action = 'store',
    help = 'path to device')


## Parse arguments
args = parser.parse_args()

## Device cleanup
if args.cleanup:
    ## Read device data
    device_data = fs.read(args.device)
    device = util.parse_bitwig_device(device_data)

    ## Serialize everything back
    device_data = util.serialize_bitwig_device(device)
    fs.write(args.device, device_data)
    print("Cleaned up '%s' successfully!" % args.device)
    sys.exit()

print("You did not specify the operation mode!")
sys.exit()
