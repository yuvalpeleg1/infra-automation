from pathlib import Path
from logger_config import setup_logger
from validation import VMConfig
from machine import Machine

# Const all paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "configs" / "instances.json"
SCRIPT_FILE = BASE_DIR / "scripts" / "install_nginx.sh"

# getting logger
logger = setup_logger("infra_simulator")


# getting input from user
def get_user_input():
    return {
        "name": input("Vm Name: "),
        "os": input(
            "OS (amazon linux / windows / red hat enterprise linux / ubuntu / ubuntu pro): "
        ),
        "instance_type": input("Instance type: "),
    }


# checking validation on input with VMConfig
def build_Vmconfig(instance: dict) -> VMConfig:
    return VMConfig(**instance)


def create_machine(config: VMConfig) -> Machine:
    resources = config.get_resources()

    return Machine(
        name=config.name,
        os=config.os,
        instance_type=config.instance_type,
        cpu=resources["cpu"],
        ram=resources["ram"],
    )
