
from CustomException import Pass, Failed, Error
from src.ConsoleCommand import ConsoleCommand
from src.api.EveNgApi import EveNgApi


class TestReso:
    lab_name: str
    scenario_name: str
    machine_name: str
    type_machine: str
    action: str
    parameters: str

    def __init__(self, lab_name, name, machine_name, type_machine, action, parameters):
        self.lab_name = lab_name
        self.scenario_name = name
        self.machine_name = machine_name
        self.type_machine = type_machine
        self.action = action
        self.parameters = parameters

    def display(self):
        print("lab name: " + self.lab_name)
        print("TEST/SCENARIO NAME: ", end="")
        print(self.scenario_name)
        print("machine name: ", end="")
        print(self.machine_name)
        print("type machine: ", end="")
        print(self.type_machine)
        print("action: ", end="")
        print(self.action)
        print("parameters: ", end="")
        print(self.parameters)


class PlatformDev:
    software_platform: str
    api_ip_address: str
    api_credentials_user_name: str
    api_credentials_user_password: str

    def __init__(
        self,
        software_platform,
        api_ip_address,
        api_credentials_user_name,
        api_credentials_user_password,
    ):
        self.software_platform = software_platform
        self.api_ip_address = api_ip_address
        self.api_credentials_user_name = api_credentials_user_name
        self.api_credentials_user_password = api_credentials_user_password

    def display(self):
        print("software_platform: " + self.software_platform)
        print("api_ip_address: " + self.api_ip_address)
        print("api_credentials_user_name: " + self.api_credentials_user_name)
        print("api_credentials_user_password: " + self.api_credentials_user_password)


class TestResoType1(TestReso):
    platform: PlatformDev

    def __init__(
        self,
        lab_name,
        name,
        machine_name,
        type_machine,
        action,
        parameters,
        platform_dev: PlatformDev,
    ):
        super().__init__(
            lab_name=lab_name,
            name=name,
            machine_name=machine_name,
            type_machine=type_machine,
            action=action,
            parameters=parameters,
        )
        self.platform = platform_dev

    def display(self):
        print("TYPE 1: ")
        super().display()

    def do_test(self):
        if self.action.startswith("ping"):
            api = EveNgApi(
                url=self.platform.api_ip_address,
                username=self.platform.api_credentials_user_name,
                password=self.platform.api_credentials_user_password,
            )
            info_node = api.node(lab_name=self.lab_name, node_name=self.machine_name)
            telnet_url = info_node["url"]
            telnet_clean = telnet_url.split("//")[1].split(":")
            telnet_host = telnet_clean[0]
            telnet_port = telnet_clean[1]
            console = ConsoleCommand(address=telnet_host, port=telnet_port)
            console.write(
                "\x03\n"
            )  # send ctrl+c, to clear any command already executing
            command = self.action + " " + self.parameters + "\n"
            print(f"command: {command}")
            console.write(command=command)
            success = False
            while True:
                lines = console.read_lines(timeout=4, number_lines=4)
                for line in lines:
                    print(line)
                    if "bytes from" in line:
                        print("ping successful")
                        success = True
                        break
                    else:
                        print("ping failed")
                        success = False
                console.write(
                    "\x03\n"
                )  # send ctrl+c, to clear any command already executing
                if success:
                    raise Pass()
                else:
                    raise Failed()
        else:
            print("action unsupported")


class Tests:
    config_file: str
    tests: [TestReso]

    def __init__(self, config_file=None):
        self.tests = []
        self.config_file = config_file

    def add_test(self, test: TestReso):
        self.tests.append(test)

    def display(self):
        for test in self.tests:
            print("**********************")
            test.display()

    def do_test(self):
        number_pass = 0
        number_failed = 0
        number_error = 0
        for test in self.tests:
            try:
                test.display()
                test.do_test()
            except Pass:
                number_pass = number_pass + 1
            except Failed:
                number_failed = number_failed + 1
            except Error:
                number_error = number_error + 1
        number_tests = len(self.tests)
        print(f"Passed ; {number_pass}/{number_tests}")
        print(f"Failed ; {number_failed}/{number_tests}")
        print(f"Error ; {number_error}/{number_tests}")
        if number_pass == number_tests:
            raise Pass
        if number_error >= 1:
            raise Error
        raise Failed
