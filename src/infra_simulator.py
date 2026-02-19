import json
from pathlib import Path
import subprocess
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
def build_VMconfig(instance: dict) -> VMConfig:
    return VMConfig(**instance)


# after validation we can create the Machine
def create_machine(config: VMConfig) -> Machine:
    resources = config.get_resources()

    return Machine(
        name=config.name,
        os=config.os,
        instance_type=config.instance_type,
        cpu=resources["cpu"],
        ram=resources["ram"],
    )


def save_instance(machine: Machine):
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(machine.to_dict())
    with open(CONFIG_FILE, "w") as f:
        data = json.dump(data, f, indent=2)


def run_bash_script():
    try:
        subprocess.run(["bash", str(SCRIPT_FILE)], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Bash script failed: {e}")
        print("Provisioning failed during service installation.")
        exit(1)


def main():
    logger.info("Provisioning started at main")
    try:
        raw_data = get_user_input()

        config = build_VMconfig(raw_data)
        machine = create_machine(config)

        save_instance(machine)
        run_bash_script()

        logger.info("Provisioning completed successfully")
        print("VM provisioned successfully!")

    except Exception as e:
        logger.error(f"Provisioning failed: {e}")
        print("Error:", e)


if __name__ == "__main__":
    main()
