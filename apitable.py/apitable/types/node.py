from enum import Enum

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class NodeTypeEnum(str, Enum):
    Datasheet = 'Datasheet'
    Folder = 'Folder'
    Form = 'Form'
    Dashboard = 'Dashboard'
    Mirror = 'Mirror'
    Automation = 'Automation'
    ERROR = "ERROR NODE TYPE"


class NodeListItem(BaseModel):
    id: str
    name: str
    type: Union[NodeTypeEnum, str] = Field(union_mode='left_to_right')
    icon: Optional[str] = None
    isFav: Optional[bool] = None


class NodeDetail(NodeListItem):
    type: Union[NodeTypeEnum, str] = Field(default=NodeTypeEnum.Folder, union_mode='left_to_right')
    children: Optional[List[NodeListItem]] = None

class NodeSearchInfo(NodeListItem):
    permission: int
    parentId: Optional[str] = None
