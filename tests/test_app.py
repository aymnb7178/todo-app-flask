import os
import re
import tempfile
import unittest

from app import create_app


class TodoTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "t.db")
        self.client = create_app(self.path).test_client()

    def tearDown(self):
        self.dir.cleanup()

    def ids(self):
        return re.findall(r"/complete/([0-9a-f-]{36})", self.client.get("/").get_data(as_text=True))

    def counter(self, name):
        html = self.client.get("/").get_data(as_text=True)
        return int(re.search(rf'id="{name}">(\d+)<', html).group(1))

    def test_empty_page_loads(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_add_complete_delete(self):
        self.client.post("/add", data={"task": "buy milk"})
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("buy milk", html)
        (tid,) = self.ids()
        self.client.post(f"/complete/{tid}")
        self.assertEqual(self.counter("completed-tasks"), 1)
        self.client.post(f"/complete/{tid}")   # toggles back
        self.assertEqual(self.counter("completed-tasks"), 0)
        self.client.post(f"/delete/{tid}")
        self.assertEqual(self.ids(), [])

    def test_blank_task_ignored(self):
        self.client.post("/add", data={"task": "   "})
        self.client.post("/add", data={})
        self.assertEqual(self.ids(), [])

    def test_html_is_escaped(self):
        self.client.post("/add", data={"task": "<script>alert(1)</script>"})
        html = self.client.get("/").get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_long_task_is_truncated(self):
        self.client.post("/add", data={"task": "x" * 1000})
        self.assertNotIn("x" * 301, self.client.get("/").get_data(as_text=True))

    def test_data_survives_a_new_app_instance(self):
        self.client.post("/add", data={"task": "persist me"})
        again = create_app(self.path).test_client()
        self.assertIn("persist me", again.get("/").get_data(as_text=True))

    def test_unknown_id_is_harmless(self):
        self.assertEqual(self.client.post("/complete/nope").status_code, 302)
        self.assertEqual(self.client.post("/delete/nope").status_code, 302)

    def test_sql_injection_attempt_is_treated_as_text(self):
        self.client.post("/add", data={"task": "x'); DROP TABLE todos;--"})
        self.client.post("/add", data={"task": "still here"})
        self.assertEqual(len(self.ids()), 2)


if __name__ == "__main__":
    unittest.main()
