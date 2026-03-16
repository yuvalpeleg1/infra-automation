# Infra Automation Project

## Overview

This project simulates infrastructure provisioning using Python.
It allows users to define virtual machines, validates the configuration, saves it to a configuration file, and simulates service installation using a Bash script.

---

# Setup

## 1. Clone the repository

git clone <repository-url>
cd INFRA_AUTOMATION

## 2. Create a virtual environment

python -m venv .venv

## 3. Activate the virtual environment

Windows:

.venv\Scripts\activate

Linux / Mac:

source .venv/bin/activate

## 4. Install dependencies

pip install -r requirements.txt

## 5. Run the simulator

python src/infra_simulator.py ( # with or without args)

---

| Argument | Description                 | Example           |
| -------- | --------------------------- | ----------------- |
| `--name` | Name of the virtual machine | `--name yuval_the_king`      |
| `--os`   | Operating system of the VM  | `--os ubuntu`     |
| `--type` | Instance type               | `--type t2.medium` |


## Project Structure

```
INFRA_AUTOMATION
│
├── configs/
│   ├── ec2_types.json      # defines valid instance types and their CPU/RAM
│   └── instances.json      # stores created VM configurations
│
├── logs/
│   └── provisioning.log    # records provisioning events and errors
│
├── scripts/
│   └── install_nginx.sh    # installs and configures Nginx (simulated service installation)
│
├── src/
│   ├── infra_simulator.py  # main script that orchestrates the provisioning workflow
│   ├── machine.py          # dataclass representing a virtual machine
│   ├── validation.py       # Pydantic model used for validating VM input
│   └── logger_config.py    # centralized logging configuration
│
├── requirements.txt        # project dependencies
├── README.md               # project documentation
└── .gitignore              # ignored files and directories
```


---

# Features

* Dynamic VM creation via user input
* Validation of operating system and instance type
* Simulation of infrastructure provisioning
* Logging of all provisioning steps
* Configuration storage in JSON
* Automated service installation using Bash

---

# Logging

All provisioning actions are logged to:

logs/provisioning.log

Logs include timestamps, severity level, file name, function name, and message details to assist with debugging and auditing.

---

