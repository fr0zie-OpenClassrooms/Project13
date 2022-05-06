from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import Client


class TestAccount(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        service = Service(executable_path=ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)
        self.client = Client()
        self.credentials = {
            "username": "Test",
            "email": "test@coinspace.com",
            "password1": "t8VhtmOUpYJ39Tb0",
            "password2": "t8VhtmOUpYJ39Tb0",
        }

    def test_register(self):
        self.browser.get(self.live_server_url + reverse("register"))
        username = self.browser.find_element(By.NAME, "username")
        username.send_keys("Test")
        email = self.browser.find_element(By.NAME, "email")
        email.send_keys("test@coinspace.com")
        password1 = self.browser.find_element(By.NAME, "password1")
        password1.send_keys("t8VhtmOUpYJ39Tb0")
        password2 = self.browser.find_element(By.NAME, "password2")
        password2.send_keys("t8VhtmOUpYJ39Tb0")
        button = self.browser.find_element(By.NAME, "register")
        button.click()
        message = self.browser.find_element(By.CLASS_NAME, "alert").find_element(
            By.TAG_NAME, "span"
        )

        self.assertEqual(message.text, "Registration successful.")

    def test_login(self):
        self.client.post(reverse("register"), self.credentials)
        self.browser.get(self.live_server_url + reverse("login"))
        username = self.browser.find_element(By.NAME, "username")
        username.send_keys("Test")
        password = self.browser.find_element(By.NAME, "password")
        password.send_keys("t8VhtmOUpYJ39Tb0")
        button = self.browser.find_element(By.NAME, "login")
        button.click()
        message = self.browser.find_element(By.CLASS_NAME, "alert").find_element(
            By.TAG_NAME, "span"
        )

        self.assertEqual(message.text, "You are now logged in as Test.")
