from logger_config import setup_logger
from dataclasses import dataclass, asdict

logger = setup_logger("machine")


@dataclass
class Machine:
    name: str
    os: str
    instance_type: str
    cpu: int
    ram: int

    def __post_init__(self):
        logger.debug(
            f"Machine created: {self.name} | {self.os} | {self.instance_type} (cpu: {self.cpu} , ram:{self.ram})\n"
        )

    def to_dict(self):
        return asdict(self)
