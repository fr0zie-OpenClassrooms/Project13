from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import Client


class TestTracker(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        service = Service(executable_path=ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)
        self.client = Client()
        self.credentials = {
            "username": "Test",
            "email": "test@coinspace.com",
            "password1": "t8VhtmOUpYJ39Tb0",
            "password2": "t8VhtmOUpYJ39Tb0",
        }
        self.login_credentials = {"username": "Test", "password": "t8VhtmOUpYJ39Tb0"}
        self.client.post(reverse("register"), self.credentials)
        self.client.post(reverse("login"), self.login_credentials)

    def test_connect_wallet(self):
        self.browser.get(self.live_server_url + reverse("connect-wallet"))
        label = self.browser.find_element(By.NAME, "label")
        label.send_keys("Test")
        public_key = self.browser.find_element(By.NAME, "public-key")
        public_key.send_keys("0x09a9fd2043e4c1ce330903abd73a3ddda970418c")
        button = self.browser.find_element(By.NAME, "connect")
        button.click()
        message = self.browser.find_element(By.CLASS_NAME, "alert").find_element(
            By.TAG_NAME, "span"
        )

        self.assertEqual(
            message.text,
            "Wallet 0x09a9fd2043e4c1ce330903abd73a3ddda970418c successfully connected!",
        )
