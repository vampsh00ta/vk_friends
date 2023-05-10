
from django.test import TestCase


# class RequestFactory:
#     pass
#
#
# class CreateTestCase(TestCase):
#     def success_create(self):
#         response =  RequestFactory().post('localhost:8000/auth/signup',data = {"username":"vlad","password":"vlad"})
#         self.assertEqual(response.status_code, 200)
#
#     def already_exist_create(self):
#
#
# class LoginTestCase(TestCase):
#     def success_login(self):
#         response = self.client.get('localhost:8000/auth/login',data = {"username":"vlad","password":"vlad"})
#         self.assertEqual(response.status_code, 200)
#     def unsuccess_login(self):
#         response = self.client.post('localhost:8000/auth/login',data = )
#         self.assertEqual(response.status_code, 200)