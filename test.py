try:
    import unittest
    import requests
    from main import app
except Exception as e:
    print(e)


class ApiTest(unittest.TestCase):
    def test_get_all_products_api(self):
        url = "http://localhost:5000"
        response = requests.get(f"{url}/products")
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(type(response.json()), list)

    def test_get_product_by_id(self):
        url = "http://localhost:5000"
        response = requests.get(f"{url}/product/1")
        status_code = response.status_code
        res = response.json()
        self.assertEqual(status_code, 200)
        self.assertEqual(type(res), dict)
        self.assertEqual(len(res.keys()), 5)

    def test_post_product(self):
        url = "http://localhost:5000/products"
        data = "{\"product_id\": 2,\"product_description\": \"home\",\"product_name\": \"karpet\"}"
        headers = {
            'content-type': "application/json"
        }
        response = requests.request("POST", url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        

if __name__ == "__main__":
    unittest.main()
