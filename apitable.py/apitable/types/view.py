from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class ViewTypeEnum(str, Enum):
    Grid = 'Grid'
    Gallery = 'Gallery'
    Kanban = 'Kanban'
    Gantt = 'Gantt'
    Calendar = 'Calendar'
    Architecture = 'Architecture'


class MetaView(BaseModel):
    id: str
    name: str
    type: Optional[Union[ViewTypeEnum, str]] = Field(default=None, union_mode='left_to_right')
