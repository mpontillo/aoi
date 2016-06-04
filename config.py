#!/usr/bin/env python3

import argparse
import json
import os
import sys

def write_config(config_file, config):
    config_json = json.dumps(config)
    with open(config_file, 'w') as f:
        f.write(config_json)
        f.write("\n")
    aoi_config = {}

def get_config_dir():
    home = os.path.expanduser('~')
    config_dir = home + "/.aoi"
    return config_dir

def get_config_filename():
    config_file = get_config_dir() + "/config"
    return config_file

def read_or_create_config():
    config_dir = get_config_dir()
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    config_file = get_config_filename()
    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            aoi_config = json.loads(f.read())
    else:
        # Create the initial configuraton file.
        aoi_config = {}
        write_config(config_file, aoi_config)
    return aoi_config

def show_command():
    aoi_config = read_or_create_config()
    config_json = json.dumps(aoi_config, indent=4, sort_keys=True)
    print(config_json)

def get_command(key, default=None):
    aoi_config = read_or_create_config()
    if default is not None and key not in aoi_config:
        print(default)
    else:
        if key not in aoi_config:
            sys.stderr.write("Key not found: %s\n" % key)
            sys.exit(1)
        print(aoi_config[key])

def set_command(key, value):
    aoi_config = read_or_create_config()
    aoi_config[key] = value
    write_config(get_config_filename(), aoi_config)

def delete_command(key):
    aoi_config = read_or_create_config()
    if key not in aoi_config:
        # The key is already gone. Nothing to do.
        return
    del aoi_config[key]
    write_config(get_config_filename(), aoi_config)

def configure_subparser(parser):
    subparsers = parser.add_subparsers()
    # show
    show_parser = subparsers.add_parser(
        'show', aliases=['read', 'print'],
        help="Print the configuration (in JSON form).")
    show_parser.set_defaults(func=show_command)
    # set <key> <value>
    set_parser = subparsers.add_parser(
        'set', help="Set the configuration for the specified key.")
    set_parser.add_argument(
        'key', type=str, help="Key name to set.")
    set_parser.add_argument(
        'value', type=str, help="Value to set.")
    set_parser.set_defaults(func=set_command)
    # get <key> [default]
    get_parser = subparsers.add_parser(
        'get', help="Get the configuration for the specified key.")
    get_parser.set_defaults(func=get_command)
    get_parser.add_argument('key', type=str, help="Key name to get.")
    get_parser.add_argument(
        'default', nargs='?', default=None, type=str,
        help="Default value (optional).")
    get_parser.set_defaults(func=get_command)
    # delete <key>
    delete_parser = subparsers.add_parser(
        'delete', aliases=['del', 'rm'], help="Delete the specified key.")
    delete_parser.add_argument('key', type=str, help="Key name to delete.")
    delete_parser.set_defaults(func=delete_command)

def main():
    parser = argparse.ArgumentParser(prog="config.py")
    configure_subparser(parser)
    parser.set_defaults(func=show_command)
    out = parser.parse_args(sys.argv[1:])
    kwargs = vars(out)
    func = kwargs.get('func', None)
    if func is not None:
        del kwargs['func']
        func(**vars(out))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
