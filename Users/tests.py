from django.test import TestCase, Client
from .forms import CustomUserRegisterForm
from django.urls import reverse,resolve
from .models import CustomUser
class RegisterForms(TestCase):

    def test_register_form_valid(self):
        form=CustomUserRegisterForm(data=
                            {
            'email':'testemail@gmail.com',
            'last_name':'Pop',
            'first_name':'Ion',
            'terms_conditions':True,
            'username':'usernametest',
            'password1':'TestPass1532',
            'password2':'TestPass1532'
                            })
        self.assertTrue(form.is_valid())

    def test_register_missmatch_password(self):

        form=CustomUserRegisterForm(data=
                            {
            'email':'testemail@gmail.com',
            'last_name':'Pop',
            'first_name':'Ion',
            'terms_conditions':True,
            'username':'usernametest',
            'password1':'TestPass1532',
            'password2':'TestPass1535'
                            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_register_no_data(self):

        form=CustomUserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)

class TestViews(TestCase):
    def test_group_access(self):

        self.client=Client()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@gmail.com', password='testpass', is_manager=True)
        self.client.login(username='testuser', password='testpass')
        response=self.client.get(reverse('Users-Groups'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Users/groups.html')


    def test_group_redirect(self):

        self.client=Client()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@gmail.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response=self.client.get(reverse('Users-Groups'))
        self.assertEquals(response.status_code, 302)