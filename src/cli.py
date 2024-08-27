import argparse

from main import VERSION


def parse_config() -> str:
    config_file: str = None
    try:
        parse = argparse.ArgumentParser(
            description='Basic network test automation for prototyping platforms' + " - " + str(VERSION))

        parse.add_argument('-c', '--config-file', nargs='?', type=str, help='config file path', dest='config_file_path',
                           default=None, required=False)

        args = parse.parse_args()
        if args:
            if args.config_file_path:
                config_file = args.config_file_path
    except argparse.ArgumentError as e:
        print("Parsing values from cli entrypoint failed... abort")
        print(e)
        exit(-1)
    return config_file
