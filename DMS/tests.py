from django.test import TestCase, Client
from django.urls import reverse,resolve
from DMS.views import DocCreateView, DocDeleteView,DocDetailView,tag,FolderListView,DocListView,DocUpdateView
from Users.models import CustomUser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
class TestUrls(TestCase):
   def test_list_documents(self):
    url= reverse('DMS-home')
    self.assertEquals(resolve(url).func.view_class, DocListView)

   def test_update(self):
    url= reverse('document-update',args=[1])
    self.assertEquals(resolve(url).func.view_class, DocUpdateView)

   def test_upload(self):
    url= reverse('DMS-upload')
    self.assertEquals(resolve(url).func.view_class, DocCreateView)

   def test_detail(self):
    url= reverse('document-detail',args=[1])
    self.assertEquals(resolve(url).func.view_class, DocDetailView)

   def test_delete(self):
    url= reverse('document-delete',args=[1])
    self.assertEquals(resolve(url).func.view_class, DocDeleteView)

   def test_tag(self):
    url= reverse('tag')
    self.assertEquals(resolve(url).func, tag)

   def test_folder(self):
    url= reverse('folders')
    self.assertEquals(resolve(url).func.view_class, FolderListView)
    

class TestViews(TestCase):

   def test_tag_GET(self):
      self.client=Client()
      self.user = CustomUser.objects.create_user(username='testuser', email='test@gmail.com', password='testpass')
      self.client.login(username='testuser', password='testpass')
      response=self.client.get(reverse('tag'))
      self.assertEquals(response.status_code, 200)
      self.assertTemplateUsed(response, 'DMS/tag.html')

   def test_tag_POST(self):
      url=reverse('tag')
      self.client=Client()
      self.user = CustomUser.objects.create_user(username='testuser', email='test@gmail.com', password='testpass')
      self.user.is_manager=True
      self.client.login(username='testuser',password='testpass')
      response=self.client.post(url, {'name':'TestTag'})
      self.assertEquals(response.status_code, 302)


class TestPage(StaticLiveServerTestCase):
  def setUp(self):
     options=webdriver.ChromeOptions()
     options.binary_location='C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe'
     self.browser=webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
  def TearDown(self):
     self.browser.close()

  def test_searchbar_displayed(self):
     self.browser.get(self.live_server_url)
     main=self.browser.find_element(By.TAG_NAME, "main")
     divs=main.find_elements(By.TAG_NAME, 'div')
     for div in divs:
       element=div.find_element(By.TAG_NAME, 'legend')
       if element is not None:
         break
     self.assertEquals(
       element.text,'Search bar'
     )
  def test_navbar_displayed(self):
     self.browser.get(self.live_server_url)
     nav=self.browser.find_element(By.TAG_NAME, "nav")
     div=nav.find_element(By.CLASS_NAME,'container-xxl')
     anchor=div.find_element(By.CLASS_NAME,'navbar-brand')
     element=anchor.find_element(By.TAG_NAME,'span')
     self.assertEquals(
       element.text,'EDMS')

  def test_OCR(self):
        self.browser.get(self.live_server_url)
        account=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[2]/li/a')
        account.click()
        login=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[2]/li/ul/li[2]/a')
        login.click()
        first_name = self.browser.find_element(By.ID,'id_first_name')
        last_name = self.browser.find_element(By.ID,'id_last_name')
        username = self.browser.find_element(By.ID,'id_username')
        email = self.browser.find_element(By.ID,'id_email')
        password1 = self.browser.find_element(By.ID,'id_password1')
        password2 = self.browser.find_element(By.ID,'id_password2')
        scrolldown = self.browser.find_element(By.TAG_NAME, 'html')
        scrolldown.send_keys(Keys.END)
        confirm=self.browser.find_element(By.XPATH,'//*[@id="id_terms_conditions"]')
        submit = self.browser.find_element(By.XPATH,'/html/body/main/form/button')

        first_name.send_keys('Prenume')
        last_name.send_keys('Nume')
        username.send_keys('usertest')
        email.send_keys('usertest@gmail.com')
        password1.send_keys('Parola1234')
        password2.send_keys('Parola1234')
        confirm.click()
        submit.click()

        username = self.browser.find_element(By.ID, "id_username")
        username.send_keys('usertest')
        password=self.browser.find_element(By.ID,'id_password')
        password.send_keys('Parola1234')
        login=self.browser.find_element(By.XPATH,'/html/body/main/form/button')
        login.click()
        ocr=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[1]/a')
        ocr.click()
        image=self.browser.find_element(By.ID,'file_id')
        image.send_keys('C:\\Users\\Superuser\\Desktop\\Proiect-licenta\\ivv2y.png')
        process=self.browser.find_element(By.XPATH,'//*[@id="OCR"]/button')
        process.click()
        self.browser.implicitly_wait(5)
        text=self.browser.find_element(By.XPATH,'//*[@id="render"]/div')
        self.assertEquals(text.text,'It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness...')

  def test_folder(self):
        self.browser.get(self.live_server_url)
        folders=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[1]/li[1]/a')
        folders.click()
        create_folder=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[1]/li[1]/ul/li[2]/a')
        create_folder.click()
        username = self.browser.find_element(By.ID, "id_username")
        username.send_keys('usertest')
        password=self.browser.find_element(By.ID,'id_password')
        password.send_keys('Parola1234')
        login=self.browser.find_element(By.XPATH,'/html/body/main/form/button')
        login.click()
        folder_name=self.browser.find_element(By.ID,'id_name')
        folder_name.send_keys('test_folder')
        create=self.browser.find_element(By.XPATH,'/html/body/main/form/button')
        create.click()
        folders=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[1]/li[1]/a')
        folders.click()
        my_folders=self.browser.find_element(By.XPATH,'//*[@id="main-nav"]/ul[1]/li[1]/ul/li[1]/a')
        my_folders.click()
        ok=1
        test_folder=self.browser.find_element(By.XPATH,'/html/body/main/table/tbody/tr[2]/td/p')
        if(test_folder.text.split(' ')[0]!='test_folder'):
         ok=test_folder.text
        delete=self.browser.find_element(By.XPATH,'/html/body/main/table/tbody/tr[2]/td/p/a')
        delete.click()
        confirm_delete=self.browser.find_element(By.XPATH,'/html/body/main/form/button')
        confirm_delete.click()
        no_element=self.browser.find_elements(By.XPATH,'/html/body/main/table/tbody/*')
        if(len(no_element)>1):
          ok=len(no_element)
        self.assertEquals(ok,1)
