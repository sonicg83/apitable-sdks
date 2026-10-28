from typing import List

from apitable.types import MetaView


class ViewManager:

    def __init__(self, dst: 'Datasheet'):
        self.dst = dst

    def all(self) -> List[MetaView]:
        """
        Query all views of the current datasheet
        @return: List[MetaView]
        """
        return self.dst.get_views()

    def create(self, data) -> List[MetaView]:
        """
        Create a view in the current datasheet.
        """
        return self.dst.create_view(data)

    def duplicate(self, view_id: str) -> List[MetaView]:
        """
        Duplicate an existing view in the current datasheet.
        """
        return self.dst.duplicate_view(view_id)

    def delete(self, view_id: str) -> bool:
        """
        Delete an existing view in the current datasheet.
        """
        return self.dst.delete_view(view_id)
