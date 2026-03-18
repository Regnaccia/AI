from pydantic import BaseModel, Field
from typing import Literal
from pathlib import Path

from utils.set_id import generate_id

STATUS = Literal[
    "WAITING_USER_PROMPT",
    "PROCESSING_PROMPT"
    ]

class BaseProject(BaseModel):
    id: str = Field(default_factory=generate_id)
    status : STATUS = Field(default="WAITING_USER_PROMPT")

    def save_to_disk(self):
        file_path = Path(__file__).parent.parent / "Export" / f"{self.id}.txt"
        with open(file_path, "w") as f:
            f.write(self.model_dump_json(indent= 4))