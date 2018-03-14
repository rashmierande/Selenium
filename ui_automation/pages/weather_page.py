'''
# 1. Ensure a click on the "History" tab properly navigates to the history page.
# 2. On the 10-Day Weather Forecast section within the Forecast Page,
# ensure that a mouse hover reveals the vertical line displaying metadata
# (such as time, temperature, % chance of precipitation, etc.)
# 3. Ensure that the dropdown appears when the user clicks on the "Customize" menu within
the 10-Day Weather Forecast section.
Also ensure that the first empty checkbox (labelled "Dew Point") can be checked

'''

import time
import unittest

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WeatherPage(unittest.TestCase):

     # Locators
    _history_tab_id = "city-nav-history"
    _forecast_xpath = "//div[@id='forecast']"
    _customize_dropdown_xpath = "//a[@id='editMode']"
    _dew_point_xpath = "//div[@id='weather-graph-options']//div[@id='plotVariablesMenu']//ul[@class='no-bullet']//input[@id='cp_var_dewpoint']"
    _plot_needle_xpath = "//div[@class='plot-needle']"

    def history(self,driver):
      history = driver.find_element("id",self._history_tab_id)
      history.click()
      page_src = driver.page_source
      self.assertTrue("Weather History for KWVI" in page_src)
      self.assertTrue ("Daily Weather History Graph" in page_src)
      time.sleep(5)
      driver.back()
      driver.set_page_load_timeout(10)

    def customizeDropDown(self,driver):
        element = driver.find_element("xpath",self._forecast_xpath)

        driver.execute_script("return arguments[0].scrollIntoView();", element)
        drp_down = driver.find_element("xpath",self._customize_dropdown_xpath)
        dropdown_wait = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,self._customize_dropdown_xpath)))
        drp_down.click()
        dew_point_chkBox = driver.find_element("xpath",self._dew_point_xpath)
        dewpoint_wait = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,self._dew_point_xpath)))
        print(dew_point_chkBox.is_displayed())
        if not dew_point_chkBox.is_selected():
            driver.execute_script("document.getElementById('cp_var_dewpoint').click()")
            self.assertTrue(dew_point_chkBox.is_selected())
        else:
            driver.execute_script("document.getElementById('cp_var_dewpoint').click()")
            self.assertFalse(dew_point_chkBox.is_selected())

    def mouseHoverGraph(self,driver):
        forecast_element = driver.find_element("xpath",self._forecast_xpath)
        driver.execute_script("return arguments[0].scrollIntoView();", forecast_element)
        plot_wait = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,self._plot_needle_xpath)))
        plotNeedle = driver.find_element("xpath",self._plot_needle_xpath)
        Hover = ActionChains(driver).move_to_element(plotNeedle)
        Hover.click()

