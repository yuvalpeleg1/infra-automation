from pathlib import Path
from typing import Annotated
from pydantic import BaseModel, Field, field_validator
import json

# ec2 types json Path
BASE_DIR = Path(__file__).resolve().parent.parent
EC2_TYPE_FILE = BASE_DIR / "configs" / "ec2_types.json"


# Getting ec2 types json
def load_ec2_types():
    if not EC2_TYPE_FILE.exists():
        raise RuntimeError(f"EC2 types json not found at {EC2_TYPE_FILE}")
    with open(EC2_TYPE_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise RuntimeError(
                f"EC2 types json is empty! Check file contents: {EC2_TYPE_FILE}"
            )
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"EC2 types json invalid: {e}")


EC2_TYPES = load_ec2_types()


# Validation on the VM
class VMConfig(BaseModel):
    name: Annotated[str, Field(..., min_length=1)]
    os: str
    instance_type: str

    # checking the os
    @field_validator("os")
    def validate_os(cls, os):
        available_os = [
            "amazon linux",
            "windows",
            "red hat enterprise linux",
            "ubuntu",
            "ubuntu pro",
        ]
        os = os.lower()
        if os not in available_os:
            raise ValueError(f"Os must be one of: {available_os}")
        return os

    # Checking the instance type
    @field_validator("instance_type")
    def validate_instance_type(cls, instance_type):
        if instance_type not in EC2_TYPES:
            raise ValueError(
                f"Invalid instance type. These are the options: {list(EC2_TYPES.keys())}"
            )
        return instance_type

    # getting cpu and ram of the intance
    def get_resources(self):
        return EC2_TYPES[self.instance_type]
