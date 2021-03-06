from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Dict
from urllib import parse


@dataclass
class Message:
    timestamp: datetime
    world: str
    user: str
    message: str

    @classmethod
    def from_new(cls, data: dict):
        return cls(
            datetime.now(),
            parse.unquote(data["world"]),
            parse.unquote(data["message"]),
            parse.unquote(data["user"]),
        )

    @property
    def as_tuple(self) -> Tuple:
        return (int(self.timestamp.timestamp()), self.world, self.message, self.user)

    @property
    def as_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.timestamp(),
            "world": self.world,
            "message": self.message,
            "user": self.user,
        }

    @classmethod
    def from_row(cls, data):
        return cls(
            datetime.fromtimestamp(float(data[0])),
            data[1],
            data[3],
            data[2],
        )
