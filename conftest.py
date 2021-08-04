import allure
import pytest
from _pytest.nodes import Item
from _pytest.runner import CallInfo

from scripts.main import ReportTester


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    # All code prior to yield statement would be ran prior
    # to any other of the same fixtures defined

    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        try:  # capture a screenshot
            with allure.step('Capturing failure screenshot'):
                allure.attach(ReportTester.driver.get_screenshot_as_png(), name='Screenshot',
                              attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print("ERROR", e)
            pass
    if result.when == 'setup':
        ReportTester.validations_failed_count = 0
    if result.when == 'teardown':
        pass
