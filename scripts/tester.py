import json
import unittest

from scripts.common_script import CommonScript


def start_execution():

    with open('reports_to_test.json') as in_fh:
        reports_to_execute = json.load(in_fh)
        for report_data in reports_to_execute['reports']:
            url = report_data['url']
            title = report_data['title']
            automation_report_name = report_data['automation_report_name']
            script = CommonScript(url=url,
                                  report_title=title,
                                  automation_report_name=automation_report_name)
            # tests = unittest.TestLoader().loadTestsFromTestCase(CommonScript)
            # unittest.TextTestRunner(verbosity=3).run(tests)
            script.execute_tests()


if __name__ == '__main__':
    start_execution()
