#!/usr/bin/env python3

import json
import os
import sys
from pprint import pprint

def write_config(config_file, config):
    config_json = json.dumps(config)
    with open(config_file, 'w') as f:
        f.write(config_json)
        f.write("\n")
    aoi_config = {}

def get_config_filename():
    home = os.path.expanduser('~')
    config_file = home + "/.aoi/config"
    return config_file

def read_or_create_config():
    config_file = get_config_filename()
    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            aoi_config = json.loads(f.read())
    else:
        # Create the initial configuraton file.
        write_config(config_file, {})
    return aoi_config

def main(args):
    aoi_config = read_or_create_config()
    if len(args) == 0 or args[0] == 'show':
        config_json = json.dumps(aoi_config, indent=4, sort_keys=True)
        print(config_json)
    elif args[0] == 'get':
        print(aoi_config[args[1]])
    elif args[0] == 'set':
        aoi_config[args[1]] = args[2]
        write_config(get_config_filename(), aoi_config)

if __name__ == "__main__":
    main(sys.argv[1:])
