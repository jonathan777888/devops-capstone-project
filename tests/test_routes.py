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
 
 
if __name__ == "__main__":
    unittest.main()
