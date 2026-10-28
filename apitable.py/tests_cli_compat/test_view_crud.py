"""Offline view CRUD tests for the CLI compatibility branch."""
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from apitable.datasheet.datasheet import Datasheet


class ViewCrudTests(unittest.TestCase):
    def client(self):
        return SimpleNamespace(api_base="https://example.invalid", request=Mock())

    def test_create_view_posts_body(self):
        client = self.client()
        response = SimpleNamespace(data=SimpleNamespace(views=["sentinel"]))
        with patch("apitable.datasheet.datasheet.handle_response", return_value=response):
            result = Datasheet(client, "dstTest").create_view(
                {"name": "Grid", "type": "Grid"})
        self.assertEqual(result, ["sentinel"])
        client.request.post.assert_called_once_with(
            "https://example.invalid/fusion/v1/datasheets/dstTest/views",
            json={"name": "Grid", "type": "Grid"})

    def test_duplicate_view_posts_without_body(self):
        client = self.client()
        response = SimpleNamespace(data=SimpleNamespace(views=["sentinel"]))
        with patch("apitable.datasheet.datasheet.handle_response", return_value=response):
            result = Datasheet(client, "dstTest").duplicate_view("viwOld")
        self.assertEqual(result, ["sentinel"])
        client.request.post.assert_called_once_with(
            "https://example.invalid/fusion/v1/datasheets/dstTest/views/viwOld/duplicate")

    def test_delete_view_returns_success(self):
        client = self.client()
        response = SimpleNamespace(success=True)
        with patch("apitable.datasheet.datasheet.handle_response", return_value=response):
            result = Datasheet(client, "dstTest").delete_view("viwOld")
        self.assertTrue(result)
        client.request.delete.assert_called_once_with(
            "https://example.invalid/fusion/v1/datasheets/dstTest/views/viwOld")
