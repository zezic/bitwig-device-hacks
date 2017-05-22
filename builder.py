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

    ## Extract top level JSON objects
    objects = util.find_top_level_json(device_data)
    if len(objects) != 2:
        raise Exception('Invalid or non-plaintext Bitwig device')

    ## Construct an object
    device = {
        'header': device_data[:40],
        'meta': objects[0],
        'contents': objects[1],
    }

    ## Remove all hashes from keys
    device['meta'] = util.remove_bracketed_hashes(device['meta'])
    device['contents'] = util.remove_bracketed_hashes(device['contents'])

    ## Serialize everything back
    device_data = (device['header'] + '\n\n'
        + util.json_encode(device['meta']) + '\n\n'
        + util.json_encode(device['contents']) + '\n')

    fs.write(args.device, device_data)
    print("Cleaned up '%s' successfully!" % args.device)
    sys.exit()

print("You did not specify the operation mode!")
sys.exit()
