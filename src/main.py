import os

import cli
import parse_config
from CustomException import Pass, Failed, Error
from Test import Tests

VERSION = 0.1


# called as a cli tool, with test config file path
# optional: if not config file path, search for in currrent folder

# config file in any text file with any extension if provided by cli or if searched for: .test

# modes:
# 1) command executed successfully


# Find file with .test file extension, return only first file found
def find_cfg_file_current_folder(current_folder: str) -> str:
    file_list = os.scandir(current_folder)
    for file in file_list:
        if ".test" in file.name:
            file_path = current_folder + "/" + file.name
            print(f"New config file found: {file_path}")
            return file_path


# extract config info from filepath from cli or in root folder
def extract_config():
    config_file_from_cli = cli.parse_config()
    tests: Tests
    if config_file_from_cli is None:
        config_file_from_root_folder = find_cfg_file_current_folder(os.getcwd())
        tests = parse_config.parse(config_file=config_file_from_root_folder)
    else:
        tests = parse_config.parse(config_file=config_file_from_cli)
    return tests


if __name__ == "__main__":
    print("Basic dev env test automation" + " - " + str(VERSION))
    print("STARTING")
    tests = extract_config()
    print("TESTS Loaded")
    print(tests.config_file)
    # tests.display()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    try:
        tests.do_test()
    except Pass:
        print("PASS: All tests have been done and results are succesfull")
        exit(0)
    except Failed:
        print("FAILED: All tests have been done and results are unsuccesfull")
        exit(-1)
    except Error:
        print("ERROR: Not all tests have been done")
        exit(-1)
