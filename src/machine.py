import logging
from dataclasses import dataclass, asdict


@dataclass
class Machine:
    name: str
    os: str
    instance_type: str
    cpu: int
    ram: int

    def __post_init__(self):
        logging.info(
            f"Machine created: {self.name} | "
            f"{self.instance_type} (cpu: {self.cpu} , ram:{self.ram})"
        )

    def to_dict(self):
        return asdict(self)
