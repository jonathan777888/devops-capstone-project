import unittest

from service import app
from service.routes import reset_accounts


class TestAccountRoutes(unittest.TestCase):

    def setUp(self):
        reset_accounts()
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Customer Accounts Service", response.get_json()["message"])

    def test_create_account(self):
        response = self.client.post(
            "/accounts",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "address": "123 Main Street"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "John Doe")

    def test_list_accounts(self):
        self.client.post(
            "/accounts",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "address": "123 Main Street"
            }
        )
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_read_account(self):
        self.client.post(
            "/accounts",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "address": "123 Main Street"
            }
        )
        response = self.client.get("/accounts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "john@example.com")

    def test_update_account(self):
        self.client.post(
            "/accounts",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "address": "123 Main Street"
            }
        )
        response = self.client.put(
            "/accounts/1",
            json={
                "name": "John Updated",
                "email": "john.updated@example.com",
                "address": "456 New Street"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "John Updated")

    def test_delete_account(self):
        self.client.post(
            "/accounts",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "address": "123 Main Street"
            }
        )
        response = self.client.delete("/accounts/1")
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/accounts/1")
        self.assertEqual(response.status_code, 404)

    def test_security_headers(self):
        response = self.client.get("/")
        self.assertIn("X-Frame-Options", response.headers)

    def test_cors_headers(self):
        response = self.client.get("/", headers={"Origin": "http://example.com"})
        self.assertIn("Access-Control-Allow-Origin", response.headers)

    def test_unknown_accounts_return_404(self):
        """Missing resources must return an HTTP 404 instead of a success."""
        self.assertEqual(self.client.get("/accounts/999").status_code, 404)
        self.assertEqual(
            self.client.put(
                "/accounts/999",
                json={"name": "Missing"},
            ).status_code,
            404,
        )
        self.assertEqual(self.client.delete("/accounts/999").status_code, 404)

    def test_ids_are_assigned_in_order(self):
        """Newly created accounts receive unique, increasing identifiers."""
        payload = {
            "name": "Test Customer",
            "email": "test@example.com",
            "address": "123 Example Street",
        }
        first = self.client.post("/accounts", json=payload)
        second = self.client.post("/accounts", json=payload)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.get_json()["id"], 1)
        self.assertEqual(second.get_json()["id"], 2)


if __name__ == "__main__":
    unittest.main()
