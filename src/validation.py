from typing import Annotated
from pydantic import BaseModel, Field, field_validator


class VMConfig(BaseModel):
    name: Annotated[str, Field(..., min_length=1)]
    os: str
    cpu: Annotated[str, Field(..., gt=0)]
    ram: Annotated[str, Field(..., gt=0)]

    @field_validator("os")
    def check_os(cls, os):
        os = os.lower()
        if os not in [
            "amazon linux",
            "windows",
            "red hat enterprise linux",
            "ubuntu",
            "ubuntu pro",
        ]:
            raise ValueError(
                "Os must be amazon linux | windows | red hat enterprise linux | ubuntu | ubuntu pro"
            )
        return os
