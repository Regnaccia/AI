from pydantic import BaseModel, Field
from pathlib import Path

from enum import Enum
import json

from utils.set_id import generate_id

class ProjectStatus(str, Enum):
    WAITING_PROMPT = "WAITING_USER_PROMPT"
    PROCESSING = "PROCESSING_PROMPT"
    AWAITING_FEEDBACK = "AWAITING_USER_FEEDBACK"
    READY_FOR_CTO = "READY_FOR_CTO"
    DONE = "DONE"

class BaseProject(BaseModel):
    id: str = Field(default_factory=generate_id)
    status : str = Field(default=ProjectStatus.WAITING_PROMPT)
    hystory: list

    def save_message_in_hystory(self, message:dict):
        self.hystory.append(message)

    def save_to_disk(self):
        file_path = Path(__file__).parent.parent / "Export" / f"{self.id}.txt"
        with open(file_path, "w") as f:
            f.write(self.model_dump_json(indent= 4))

    