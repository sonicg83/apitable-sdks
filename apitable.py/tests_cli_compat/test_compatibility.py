"""Offline regressions for the CLI compatibility branch; never run test/ here."""
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from apitable.datasheet.datasheet import Datasheet
from apitable.node.node_manager import NodeManager
from apitable.space.space_manager import SpaceManager
from apitable.types.field import MetaField
from apitable.types.node import NodeDetail, NodeListItem, NodeTypeEnum
from apitable.types.response import GETRecordResponseData
from apitable.types.view import MetaView, ViewTypeEnum


class CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard = patch("requests.Session.send", side_effect=AssertionError("Offline tests prohibit HTTP"))
        cls.guard.start()
        cls.addClassCleanup(cls.guard.stop)

    def client(self):
        return SimpleNamespace(api_base="https://example.invalid", request=Mock())

    def test_known_node_preserves_enum(self):
        node = NodeListItem(id="dstTest", name="Test", type="Datasheet")
        self.assertIs(node.type, NodeTypeEnum.Datasheet)

    def test_unknown_node_preserves_type_without_display_properties(self):
        node = NodeListItem(id="nodeTest", name="Test", type="CustomPage")
        self.assertEqual(node.type, "CustomPage")
        self.assertIsNone(node.icon)
        self.assertIsNone(node.isFav)

    def test_folder_detail_accepts_unknown_children(self):
        node = NodeDetail(id="folderTest", name="Test", children=[{"id": "nodeTest", "name": "Test", "type": "FutureType"}])
        self.assertIs(node.type, NodeTypeEnum.Folder)
        self.assertEqual(node.children[0].type, "FutureType")

    def test_view_types_remain_distinguishable(self):
        self.assertIs(MetaView(id="viwTest", name="Test", type="Grid").type, ViewTypeEnum.Grid)
        self.assertEqual(MetaView(id="viwTest", name="Test", type="FutureType").type, "FutureType")
        self.assertIsNone(MetaView(id="viwTest", name="Test").type)

    def test_missing_known_field_property_remains_unknown(self):
        for kind in ("SingleText", "Number", "Formula"):
            with self.subTest(kind=kind):
                self.assertIsNone(MetaField(id="fldTest", name="Test", type=kind).property)

    def test_unknown_field_property_is_retained(self):
        value = {"futureConstraint": 4}
        self.assertEqual(MetaField(id="fldTest", name="Test", type="FutureType", property=value).property, value)

    def test_absent_pagination_is_not_fabricated(self):
        data = GETRecordResponseData(records=[])
        self.assertEqual((data.total, data.pageNum, data.pageSize), (None, None, None))

    def test_scoped_folder_route(self):
        client = self.client()
        with patch("apitable.node.node_manager.handle_response"):
            NodeManager(client, space_id="spcTest")._get_node_detail("folderTest")
        client.request.get.assert_called_once_with("https://example.invalid/fusion/v1/spaces/spcTest/nodes/folderTest")

    def test_unscoped_folder_route_remains_available(self):
        client = self.client()
        with patch("apitable.node.node_manager.handle_response"):
            NodeManager(client)._get_node_detail("folderTest")
        client.request.get.assert_called_once_with("https://example.invalid/fusion/v1/nodes/folderTest")

    def test_node_page_parameters_are_forwarded(self):
        client = self.client()
        with patch("apitable.node.node_manager.handle_response"):
            NodeManager(client)._get_nodes("spcTest", pageNum=2, pageSize=10)
        client.request.get.assert_called_once_with("https://example.invalid/fusion/v1/spaces/spcTest/nodes", params={"pageNum": 2, "pageSize": 10})

    def test_space_page_parameters_are_forwarded(self):
        client = self.client()
        with patch("apitable.space.space_manager.handle_response"):
            SpaceManager(client)._get_spaces(pageNum=2, pageSize=10)
        client.request.get.assert_called_once_with("https://example.invalid/fusion/v1/spaces", params={"pageNum": 2, "pageSize": 10})

    def test_field_and_view_page_parameters_are_forwarded(self):
        for method, resource in (("get_fields", "fields"), ("get_views", "views")):
            with self.subTest(method=method):
                client = self.client()
                client.request.get.return_value.json.return_value = {"code": 200, "success": True, "message": "OK", "data": {"views": []}}
                with patch("apitable.datasheet.datasheet.handle_response", return_value={"code": 200, "success": True, "message": "OK", "data": {"views": []}}):
                    getattr(Datasheet(client, "dstTest"), method)(pageNum=2, pageSize=10)
                client.request.get.assert_called_once_with("https://example.invalid/fusion/v1/datasheets/dstTest/" + resource, params={"pageNum": 2, "pageSize": 10})
