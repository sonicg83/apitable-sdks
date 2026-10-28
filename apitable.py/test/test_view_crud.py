import unittest
from unittest.mock import patch

from apitable import Apitable


class TestViewCrud(unittest.TestCase):
    def _response(self, payload, status=201):
        response = unittest.mock.Mock()
        response.status_code = status
        response.json.return_value = payload
        response.text = "{}"
        return response

    @patch("requests.Session.request")
    def test_create_view(self, request):
        request.return_value = self._response({
            "success": True, "code": 200, "message": "SUCCESS",
            "data": {"views": [{"id": "viwNew", "name": "Grid", "type": "Grid"}]},
        })
        client = Apitable("synthetic-token", api_base="https://host.test")
        views = client.datasheet("dstTest").create_view(
            {"name": "Grid", "autoSave": True, "type": "Grid", "columns": []})
        self.assertEqual(views[0].id, "viwNew")
        self.assertEqual(views[0].type, "Grid")
        args, kwargs = request.call_args
        self.assertEqual(args[0], "POST")
        self.assertTrue(args[1].endswith("/fusion/v1/datasheets/dstTest/views"))
        self.assertEqual(kwargs["json"]["type"], "Grid")

    @patch("requests.Session.request")
    def test_duplicate_view(self, request):
        request.return_value = self._response({
            "success": True, "code": 200, "message": "SUCCESS",
            "data": {"views": [{"id": "viwCopy", "name": "Grid copy", "type": "Grid"}]},
        })
        client = Apitable("synthetic-token", api_base="https://host.test")
        views = client.datasheet("dstTest").duplicate_view("viwOld")
        self.assertEqual(views[0].id, "viwCopy")
        args, kwargs = request.call_args
        self.assertEqual(args[0], "POST")
        self.assertTrue(args[1].endswith("/datasheets/dstTest/views/viwOld/duplicate"))
        self.assertIsNone(kwargs.get("json"))

    @patch("requests.Session.request")
    def test_delete_view_allows_empty_data(self, request):
        request.return_value = self._response({
            "success": True, "code": 200, "message": "SUCCESS", "data": None,
        }, status=200)
        client = Apitable("synthetic-token", api_base="https://host.test")
        self.assertTrue(client.datasheet("dstTest").delete_view("viwOld"))
        args, _ = request.call_args
        self.assertEqual(args[0], "DELETE")
        self.assertTrue(args[1].endswith("/datasheets/dstTest/views/viwOld"))


if __name__ == "__main__":
    unittest.main()
