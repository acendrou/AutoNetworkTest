import configparser
from collections import namedtuple


import Test
from Test import TestReso, TestResoType1
from src.Test import PlatformDev

ConfEnviro = namedtuple(
    "ConfEnviro",
    [
        "software_platform",
        "api_ip_address",
        "api_credentials_user_name",
        "api_credentials_user_password",
    ],
)

Lab = namedtuple("Lab", "lab_name")

Scenario = namedtuple(
    "Scenario",
    ["scenario_name", "machine_name", "type_machine", "action", "parameters"],
)


def parse(config_file: str = None) -> [TestReso]:
    config = configparser.ConfigParser()
    config.read(config_file)
    tests = Test.Tests(config_file=config_file)
    print("**********************")
    try:
        scenarios = []
        for section in config.sections():
            if section.startswith("config_test_environment"):
                conf_enviro = parse_environnment(config[section])
            if section.startswith("config_lab"):
                conf_lab = parse_lab(config[section])
            if section.startswith("scenario"):
                conf_scenario = parse_scenarios(config[section])
                scenarios.append(conf_scenario)
        return create_tests(
            tests, conf_enviro=conf_enviro, conf_lab=conf_lab, scenarios=scenarios
        )
    except KeyError:
        print("Config file not formatted correctly or empty!")


def create_tests(
    tests: Test, conf_enviro: ConfEnviro, conf_lab: Lab, scenarios: [Scenario]
) -> [TestReso]:
    platform_dev = PlatformDev(
        software_platform=conf_enviro.software_platform,
        api_ip_address=conf_enviro.api_ip_address,
        api_credentials_user_name=conf_enviro.api_credentials_user_name,
        api_credentials_user_password=conf_enviro.api_credentials_user_password,
    )

    for scenario in scenarios:
        test = TestResoType1(
            lab_name=conf_lab.lab_name,
            name=scenario.scenario_name,
            machine_name=scenario.machine_name,
            type_machine=scenario.type_machine,
            action=scenario.action,
            parameters=scenario.parameters,
            platform_dev=platform_dev,
        )
        tests.add_test(test)
    return tests


def parse_environnment(config: configparser) -> ConfEnviro:
    software_platform: str
    api_ip_address: str
    api_credentials_user_name: str
    api_credentials_user_password: str

    try:
        software_platform = config["software_platform"]
        print(f"config file parsing: software platform key: {software_platform}")
    except KeyError:
        print(
            "Config file parsing error: software platform key missing, mandatory, program will exit"
        )
        exit(1)
    try:
        api_ip_address = config["api_ip_address"]
        print(f"config file parsing: api_ip_address key: {api_ip_address}")
    except KeyError:
        print(
            "Config file parsing error: api_ip_address key missing, mandatory, program will exit"
        )
        exit(1)
    try:
        api_credentials_user_name = config["api_credentials_user_name"]
        print(
            f"config file parsing: api_credentials_user_name key: {api_credentials_user_name}"
        )
    except KeyError:
        print(
            "Config file parsing error: api_credentials_user_name key missing, mandatory, program will exit"
        )
        exit(1)
    try:
        api_credentials_user_password = config["api_credentials_user_password"]
        print(
            f"config file parsing: api_credentials_user_password key: {api_credentials_user_password}"
        )
    except KeyError:
        print(
            "Config file parsing error: api_credentials_user_password key missing, mandatory, program will exit"
        )
        exit(1)
    return ConfEnviro(
        software_platform,
        api_ip_address,
        api_credentials_user_name,
        api_credentials_user_password,
    )


def parse_lab(config: configparser) -> Lab:
    lab_name: str
    try:
        lab_name = config["lab_name"]
        print(f"config file parsing: lab name key: {lab_name}")
    except KeyError:
        print("Config file parsing error: lab_name key missing")
    return Lab(lab_name)


def parse_scenarios(config: configparser) -> Scenario:
    scenario_name: str
    machine_name: str
    type_machine: str
    action: str
    parameters: str
    try:
        scenario_name = config["scenario_name"]
        print(f"config file parsing: scenario_name key: {scenario_name}")
    except KeyError:
        print("Config file parsing error: scenario_name key missing")
    try:
        machine_name = config["machine_name"]
        print(f"config file parsing: machine_name key: {machine_name}")
    except KeyError:
        print("Config file parsing error: machine_name key missing")
    try:
        type_machine = config["type_machine"]
        print(f"config file parsing: type_machine key: {type_machine}")
    except KeyError:
        print("Config file parsing error: type_machine key missing")
    try:
        action = config["action"]
        print(f"config file parsing: action key: {action}")
    except KeyError:
        print("Config file parsing error: action key missing")
    try:
        parameters = config["parameters"]
        print(f"config file parsing: parameters key: {parameters}")
    except KeyError:
        print("Config file parsing error: parameters key missing")
    return Scenario(scenario_name, machine_name, type_machine, action, parameters)
