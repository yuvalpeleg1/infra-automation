import argparse
import json
from pathlib import Path
import platform
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


def parse_arguments():
    parser = argparse.ArgumentParser(description="Infra Automation Simulator")

    parser.add_argument("--name", help="VM name")
    parser.add_argument("--os", help="Operating System")
    parser.add_argument("--type", help="EC2 instance type")
    return parser.parse_args()


# getting input from user
def get_user_input(args):
    logger.info("Collecting user input")
    logger.info(
        f"Input source: name={'CLI' if args.name else 'USER'}, os={'CLI' if args.os else 'USER'}, type={'CLI' if args.type else 'USER'}"
    )
    return {
        "name": args.name or input("Vm Name: "),
        "os": args.os
        or input(
            "OS (amazon linux / windows / red hat enterprise linux / ubuntu / ubuntu pro): "
        ),
        "instance_type": args.type
        or input(
            "Instance type (t2.micro / t2.small / t2.medium / t3.micro / t3.small / t3.medium): "
        ),
    }


# checking validation on input with VMConfig
def build_VMconfig(instance: dict) -> VMConfig:
    logger.debug("Validating VM configuration")
    return VMConfig(**instance)


# after validation we can create the Machine
def create_machine(config: VMConfig) -> Machine:
    logger.info("Creating Machine")
    resources = config.get_resources()

    return Machine(
        name=config.name,
        os=config.os,
        instance_type=config.instance_type,
        cpu=resources["cpu"],
        ram=resources["ram"],
    )


def save_instance(machine: Machine):
    data = []

    if CONFIG_FILE.exists() and CONFIG_FILE.stat().st_size > 0:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

    data.append(machine.to_dict())
    with open(CONFIG_FILE, "w") as f:
        data = json.dump(data, f, indent=2)
    logger.info(f"Instance {machine.name} saved to instances.json")


def run_bash_script():
    try:
        if platform.system() == "Windows":
            logger.warning("Running on Windows, skipping Bash installation script\n")
            print("Skipping bash service installation (Windows detected)")
        else:
            subprocess.run(["bash", str(SCRIPT_FILE)], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Bash script failed: {e}\n")
        print("Provisioning failed during service installation.")
        exit(1)


def main():
    logger.info("Provisioning started")

    args = parse_arguments()

    try:
        raw_data = get_user_input(args)
        logger.debug(f"User Data: {raw_data}\n")

        config = build_VMconfig(raw_data)
        logger.info("Validation Successful\n")

        machine = create_machine(config)

        save_instance(machine)
        logger.info("Saved Instance Completed\n")

        run_bash_script()

        logger.info("Provisioning Completed Successfully\n")
        logger.info(f"{'-' * 80}\n")

        print("VM provisioned successfully!")

    except Exception as e:
        logger.error(f"Provisioning failed: {e}\n\n")
        print("Error:", e)


if __name__ == "__main__":
    main()
