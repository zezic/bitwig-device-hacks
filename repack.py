#!/usr/bin/python3

import os.path
import sys

MOD_SRC_FILE = 'resources/Math.bwmodulator'
MOD_SRC_COMP = 'resources/Math.component.c'
MOD_SRC_MAPPING = 'resources/Math.mapping.txt'
MOD_TARGET_FILE = 'resources/MathX.bwmodulator'

MOD_NAME = 'MatX' # Length is strictly 4
MOD_NAME_OFFSET_1 = 0x0159
MOD_NAME_OFFSET_2 = 0x2218
MOD_SOURCE_LEN_OFFSET = 0x1A41
MOD_SOURCE_BEGIN_OFFSET = 0x1A45
MOD_SOURCE_END_OFFSET = 0x1C72

device_data = None
source_text = None

# Read the device bytecode
with open(MOD_SRC_FILE, 'rb') as file:
    device_data = [x for x in file.read()]

# Unpack sources
if not os.path.isfile(MOD_SRC_COMP):
    source_text = device_data[MOD_SOURCE_BEGIN_OFFSET:MOD_SOURCE_END_OFFSET]
    source_text = ''.join(chr(x) for x in source_text)
    with open(MOD_SRC_COMP, 'w') as text_file:
        text_file.write(source_text)
    print("A source file '%s' was created for you." % MOD_SRC_COMP)
    print("Edit it, then run repack.py again.")
    sys.exit()

# Read sources
print("Using sources: %s" % MOD_SRC_COMP)
with open(MOD_SRC_COMP, 'r') as file:
    source_text = file.read()
    source_text_len = len(source_text).to_bytes(4, byteorder = 'big', signed = False)

# Replace mod name
for i in range(0, 4):
    device_data[MOD_NAME_OFFSET_1 + i] = ord(MOD_NAME[i])
    device_data[MOD_NAME_OFFSET_2 + i] = ord(MOD_NAME[i])

# Replace mode names from mapping file
with open(MOD_SRC_MAPPING, 'r') as file:
    mapping_text = file.read().split('\n')
    mappings = {}
    for line in mapping_text:
        if len(line) == 0:
            continue
        columns = line.split(':')
        mappings[columns[0]] = columns[1]
    device_data_str = ''.join(chr(x) for x in device_data)
    for i, value in mappings.items():
        device_data_str = device_data_str.replace(i, value)
    device_data = [ord(i) for i in device_data_str]

# Replace source length
for i in range(0, 4):
    device_data[MOD_SOURCE_LEN_OFFSET + i] = source_text_len[i]

# Replace the source code
device_data_header = device_data[:MOD_SOURCE_BEGIN_OFFSET]
device_data_footer = device_data[MOD_SOURCE_END_OFFSET:]
device_data = device_data_header
device_data.extend(ord(x) for x in source_text)
device_data.extend(device_data_footer)

# Write the new device
print("Writing to: %s" % MOD_TARGET_FILE)
with open(MOD_TARGET_FILE, 'wb') as file:
    file.write(bytes(device_data))

print("Repack successful!")
