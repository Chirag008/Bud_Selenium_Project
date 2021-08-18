import re
import unittest

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helper import locators
from helper import creds
import time
from scripts.commons import Common_Utils
from reporter.HtmlReporter import HtmlReporter

class CommonScript(unittest.TestCase):
    # utils = Common_Utils()
    # driver = utils.get_browser_instance()
    # reporter = HtmlReporter(report_name='Automation Report -- CUAI Home Equity Analysis')
    validations_failed_count = 0

    def __init__(self, url, report_title, automation_report_name):
        super().__init__()
        self.url = url
        self.report_title = report_title
        self.utils = Common_Utils()
        self.driver = self.utils.get_browser_instance()
        self.automation_report_name = automation_report_name
        self.reporter = HtmlReporter(report_name=automation_report_name)

    def validate_result(self, scenario_name,
                        exp_result,
                        actual_result,
                        comment=''):
        if exp_result == actual_result:
            status = 'pass'
        else:
            status = 'fail'
            self.validations_failed_count += 1
        if comment != '':
            status = 'error'
        self.reporter.add_scenario_result(scenario_name, str(exp_result), str(actual_result),
                                          status, comment)
        # assert exp_result == actual_result

    def test_initializer(self):
        self.validations_failed_count = 0

    def execute_tests(self):
        self.login_and_load_report_page()
        # check if tabs are present -- if so, then iterate through each tab
        # Click the tab and wait to load the data, then execute all the tests
        tabs = self.driver.find_elements_by_xpath(
            "//div[contains(@class, 'explorationContainer')]//mat-list[@focus-nav-mode='Group']//li")
        if len(tabs) > 0:
            for tab in tabs:
                self.report_title = tab.find_element_by_xpath(".//span").text
                # Initialize the reporter again to capture report for this tab only
                self.automation_report_name = self.automation_report_name.replace('.html', '')
                self.reporter = HtmlReporter(report_name=self.automation_report_name + ' [' + self.report_title + '].html')

                # click the tab and wait for 10 seconds to load the page
                tab.click()
                time.sleep(10)

                self.test_report_title()
                self.test_page_background()
                self.test_all_report_dashboard_header_title()
                self.test_border_and_shadow_of_visuals()
                self.test_title_of_slicers_on_the_top()
                self.test_multiselect_for_slicers_on_the_top()
                self.reporter.save_report()
            self.exit_browser()
        else:
            self.test_report_title()
            self.test_page_background()
            self.test_all_report_dashboard_header_title()
            self.test_border_and_shadow_of_visuals()
            self.test_title_of_slicers_on_the_top()
            self.test_multiselect_for_slicers_on_the_top()
            self.test_tear_down()

    def login_and_load_report_page(self):
        # self.driver.get(self.url)
        self.driver.maximize_window()
        #
        # # sign in to PowerBi account
        # time.sleep(2)
        # self.driver.find_element_by_xpath(locators.sign_in_button).click()
        # time.sleep(2)
        # self.driver.find_element_by_xpath(locators.sign_in_email_box).send_keys(creds.username)
        # time.sleep(2)
        # self.driver.find_element_by_xpath(locators.sign_in_next_button).click()
        # time.sleep(2)
        # self.driver.find_element_by_xpath(locators.sign_in_password_box).send_keys(creds.password)
        # time.sleep(2)
        # self.driver.find_element_by_xpath(locators.sign_in_next_button).click()
        # time.sleep(2)
        #
        # # launch url again to go to report page
        self.driver.get(self.url)

    @pytest.mark.order(1)
    def test_report_title(self):
        try:
            self.test_initializer()

            # wait for report to display
            # locator_report_title = "//span[normalize-space(text()) = '" + self.report_title + "'][not(ancestor::ul)]"
            locator_report_title = locators.report_title
            ele_report_title = self.utils.wait_and_get_element(
                driver=self.driver,
                locator=locator_report_title,
                timeout=2
            )
            # waiting for report to appear on page
            # time.sleep(5)
            print('report title is - {}'.format(ele_report_title.text))

            self.validate_result('Validate report title', self.report_title,
                                 ele_report_title.text.strip())
            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Validating report tile ', self.report_title, 'NA',
                                 f'Error occurred  : {error.__repr__()}')

    @pytest.mark.order(2)
    def test_page_background(self):
        try:
            self.test_initializer()
            element = self.utils.wait_and_get_element(driver=self.driver,
                                                      locator=locators.page_background,
                                                      by=By.CSS_SELECTOR, timeout=40)
            actual_background_color = self.utils.get_property_using_js(driver=self.driver, element=element,
                                                                       property_name='background-color')
            actual_background_color = Color.from_string(actual_background_color).hex.upper()

            # E7EAEC  -- (231, 234, 236)
            expected_background_color = '#E7EAEC'
            self.validate_result('Report Background Color Validation', expected_background_color,
                                 actual_background_color)

            # Transparency
            expected_transparency = '0%'
            actual_transparency = 1 - int(self.utils.get_property_using_js(driver=self.driver, element=element,
                                                                           property_name='opacity'))
            actual_transparency = f'{actual_transparency}%'
            self.validate_result('Verifying opacity / transparency of Report background', expected_transparency,
                                 actual_transparency)
            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Validating Page Background ', 'backgound color - #E7EAEC, transparency = 0%', 'NA',
                                 f'Error occurred  : {error.__repr__()}')

    @pytest.mark.order(3)
    def test_all_report_dashboard_header_title(self):
        try:
            self.test_initializer()
            header = self.utils.wait_and_get_element(self.driver, locators.report_header, by=By.XPATH)
            actual_font_size = self.utils.get_property_using_js(self.driver, header, 'font-size')
            actual_font_size = str(int(int(actual_font_size.replace('px', '')) * 72 / 96)) + 'pts'
            actual_font_family = self.utils.get_property_using_js(self.driver, header, 'font-family')
            actual_color = self.utils.get_property_using_js(self.driver, header, 'color')
            actual_color = Color.from_string(actual_color).hex

            element_vc = self.utils.wait_and_get_element(self.driver, locators.visual_container, by=By.CLASS_NAME)
            vc_container_x = element_vc.location['x']
            vc_container_y = element_vc.location['y']

            header_x = header.location['x']
            header_y = header.location['y']
            header_height = header.size['height']

            self.validate_result('Report dashboard header title font family', 'GT America', actual_font_family)
            self.validate_result('Report dashboard header title font size', '24pts', actual_font_size)
            self.validate_result('Report dashboard header title color', '#252423', actual_color)
            self.validate_result('Report dashboard header Relative X location', 24, int(header_x - vc_container_x))
            self.validate_result('Report dashboard header Relative Y location', 24, int(header_y - vc_container_y))
            self.validate_result('Report dashboard header height', 58, int(header_height))

            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Validating Dashboard header title ', 'title color - #252423, '
                                                                       'font family = GT America%, '
                                                                       'font size = 24px,'
                                                                       'header X location = 24,'
                                                                       'header Y location = 24,'
                                                                       'header height = 58 px', 'NA',
                                 f'Error occurred  : {error.__repr__()}')

    @pytest.mark.order(4)
    def test_border_and_shadow_of_visuals(self):
        try:
            self.test_initializer()
            visuals = self.driver.find_elements_by_xpath(locators.visuals)
            for index, visual in enumerate(visuals):

                container = visual.find_element_by_xpath('.//div[contains(@class, "vcBody")]')

                border_color = container.value_of_css_property('border-color')
                border_color = Color.from_string(border_color).hex.upper()

                box_shadow = container.value_of_css_property('box-shadow')
                pattern = 'rgba\((\d+),\s(\d+),\s(\d+).*'
                if re.match(pattern, box_shadow):
                    rgb = re.search(pattern, box_shadow)
                    box_shadow = f'rgb({rgb.group(1)},{rgb.group(2)},{rgb.group(3)})'
                    box_shadow_color = Color.from_string(box_shadow).hex.upper()
                else:
                    box_shadow_color = box_shadow

                background_color = self.utils.get_property_using_js(self.driver, visual, 'background-color')
                background_color = Color.from_string(background_color).hex.upper()

                self.validate_result(f'Visual - {index + 1} [verify visual border radius]', '12px',
                                     container.value_of_css_property('border-radius'))
                self.validate_result(f'Visual - {index + 1} [verify visual border color]', '#576975', border_color)
                self.validate_result(f'Visual - {index + 1} [verify visual border shadow color]', '#B3B3B3',
                                     box_shadow_color)
                self.validate_result(f'Visual - {index + 1} [verify visual background color]', '#FBFBFB',
                                     background_color)

                # visual headers are off for buttons, slicers and report title
                visual_titles = visual.find_elements_by_xpath('.//div[contains(@class,"visualTitle")]')
                if len(visual_titles) > 0:
                    visual_title = visual_titles[0]
                    visual_title_color = visual_title.value_of_css_property('color')
                    visual_title_color = Color.from_string(visual_title_color).hex
                    font_size = visual_title.value_of_css_property('font-size')
                    if 'px' in font_size:
                        font_size = self.utils.pixel_to_pts(font_size)
                    self.validate_result(f'Visual - {index + 1} [verify visual title font size]', '14pt',
                                         font_size)
                    self.validate_result(f'Visual - {index + 1} [verify visual title font family]', 'GT America',
                                         self.utils.get_property_using_js(self.driver, visual_title, 'font-family'))
                    self.validate_result(f'Visual - {index + 1} [verify visual title color]', '#252423',
                                         visual_title_color)
                    self.validate_result(f'Visual - {index + 1} [verify visual title visibility]', 'visible',
                                         visual_title.value_of_css_property('visibility'))
            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Validating border / shadow of visuals ', 'title font size - 14pt, '
                                                                           'font family = GT America, '
                                                                           'visibility = visible,'
                                                                           'visual border radius = 12px,'
                                                                           'visual border color = #576975,'
                                                                           'visual border shadow color = #B3B3B3'
                                                                           'visual background color = #FBFBFB', 'NA',
                                 f'Error occurred  : {error.__repr__()}')

    @pytest.mark.order(5)
    def test_title_of_slicers_on_the_top(self):
        try:
            self.test_initializer()
            slicers = self.driver.find_elements_by_css_selector(locators.slicers)
            for index, slicer in enumerate(slicers):
                slicer_header_title = slicer.find_element_by_class_name('slicer-header-text')

                slicer_header_color = slicer_header_title.value_of_css_property('color')
                slicer_header_color = Color.from_string(slicer_header_color).hex
                slicer_header_font = self.utils.get_property_using_js(self.driver, slicer_header_title, 'font-family')
                slicer_header_font_size = slicer_header_title.value_of_css_property('font-size')
                slicer_header_visibility = self.utils.get_property_using_js(self.driver, slicer_header_title,
                                                                            'visibility')

                self.validate_result(f'Slicer - {index + 1} [verify slicer header color]', '#252423',
                                     slicer_header_color)
                self.validate_result(f'Slicer - {index + 1} [verify slicer header font size]', '12px',
                                     slicer_header_font_size)
                self.validate_result(f'Slicer - {index + 1} [verify slicer header font family]', 'GT America',
                                     slicer_header_font)
                self.validate_result(f'Slicer - {index + 1} [verify slicer header visibility]', 'visible',
                                     slicer_header_visibility)

            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Validating titles of slicers on the top', 'slicer title color - #252423, '
                                                                            'slicer title font size = 12px'
                                                                            'slicer title font family = GT America, '
                                                                            'slicer title visibility = visible,', 'NA',
                                 f'Error occurred  : {error.__repr__()}')

    @pytest.mark.order(6)
    def test_multiselect_for_slicers_on_the_top(self):
        try:
            self.test_initializer()
            slicers = self.driver.find_elements_by_css_selector(locators.slicers)
            for index, slicer in enumerate(slicers):
                # Test if multiple selection is ON
                slicer_dropdown_menu = slicer.find_elements_by_class_name('slicer-dropdown-menu')[0]
                slicer_dropdown_menu.click()
                # wait for 4 seconds to populate the list
                time.sleep(4)
                slicer_popup = self.driver.find_elements_by_css_selector(locators.slicer_dropdown_popup)[index]
                slicer_first_element = slicer_popup.find_elements_by_css_selector('.slicerText')[0]
                slicer_first_element_text = slicer_first_element.get_attribute('title')
                slicer_checkboxes = slicer_popup.find_elements_by_class_name(locators.slicer_checkboxes)
                if slicer_first_element_text.lower() == 'select all':
                    if len(slicer_checkboxes) < 3:
                        print('can not check multiple selections (few elements)')
                        assert True
                        continue
                    else:
                        index_item1 = 1
                        index_item2 = 2
                else:
                    index_item1 = 0
                    index_item2 = 1

                # if the status of the element is already checked, then don't select it again
                # (doing so will uncheck the element)
                if not slicer_checkboxes[index_item1].find_element_by_tag_name('input').is_selected():
                    ActionChains(self.driver) \
                        .key_down(Keys.CONTROL) \
                        .click(slicer_checkboxes[index_item1]) \
                        .key_up(Keys.CONTROL) \
                        .perform()
                    time.sleep(2)
                if not slicer_checkboxes[index_item2].find_element_by_tag_name('input').is_selected():
                    ActionChains(self.driver) \
                        .key_down(Keys.CONTROL) \
                        .click(slicer_checkboxes[index_item2]) \
                        .key_up(Keys.CONTROL) \
                        .perform()
                    time.sleep(2)

                chkbox_1_status = slicer_checkboxes[index_item1].find_element_by_tag_name('input').is_selected()
                chkbox_2_status = slicer_checkboxes[index_item2].find_element_by_tag_name('input').is_selected()

                if chkbox_1_status and chkbox_2_status:
                    multiselect_with_control = 'ON'
                else:
                    multiselect_with_control = 'OFF'

                self.validate_result(f'Slicer {index + 1} - [Validate multiselect with Control Key]', 'ON',
                                     multiselect_with_control)
                # uncheck the items
                # selecting any item again will remove all the selected items. So clicking on first item only
                if chkbox_1_status:
                    slicer_checkboxes[index_item1].click()
                    time.sleep(2)

            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Validating multiselect with CTRL is On in slicer', 'ON', 'NA',
                                 f'Error occurred  : {error.__repr__()}')

    @pytest.mark.order(7)
    def test_tear_down(self):
        try:
            self.test_initializer()
            self.utils.kill_browser_instance()
            self.reporter.save_report()

            # assert self.validations_failed_count == 0
        except Exception as error:
            if isinstance(error, AssertionError):
                raise error
            self.validate_result('Closing the browser', 'browser should be closed without any error', 'error occurred',
                                 f'error : {error.__repr__()}')

    def exit_browser(self):
        self.utils.kill_browser_instance()

# if __name__ == '__main__':
#     unittest.main()
