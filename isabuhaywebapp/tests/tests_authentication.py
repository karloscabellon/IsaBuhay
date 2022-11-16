from django.test import TestCase
from django.urls import reverse_lazy

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse_lazy('CreateAccountPage')
        self.user = {
            'username' : 'testuser',
            'email' : 'testemail@gmail.com',
            'firstname' : 'testfname',
            'lastname' : 'testlname',
            'phone_number' : 'testNum',
            'password' : 'testPass123',
            'password2' : 'testPass123'
        }

        return super().setUp()

class RegistrationTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createAccountPage.html')
    
    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)