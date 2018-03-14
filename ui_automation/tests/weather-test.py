from selenium import webdriver
from ui_automation.pages.weather_page import WeatherPage
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class WeatherPageTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setUp(self):
        baseUrl="https://www.wunderground.com/us/ca/freedom/zmw:95073.1.99999"
        self.driver = self.getBrowser("chrome")
        self.driver.set_window_size(1024, 700)
        self.driver.maximize_window()
        self.driver.get(baseUrl)
        self.driver.set_page_load_timeout(12)
        self.wp = WeatherPage()

    def getBrowser(self,browser):
        if browser == 'firefox':
           return webdriver.Firefox()
        elif browser == 'chrome':
            chromepath ="/Users/Rashmi/Documents/Samba/ui_automation/ChromeDriver/chromedriver"
            return webdriver.Chrome(chromepath)

    @pytest.mark.run(order=1)
    def test_history(self):
        self.wp.history(self.driver)

    @pytest.mark.run(order=2)
    def test_CustomizeDropDown(self):
        self.driver.set_page_load_timeout(10)
        self.wp.customizeDropDown(self.driver)

    @pytest.mark.run(order=3)
    def test_mouseHoverGraph(self):
        self.driver.set_page_load_timeout(10)
        self.wp.mouseHoverGraph(self.driver)

    def tearDown(self):
        self.driver.close()