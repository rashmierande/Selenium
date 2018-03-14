'''
    This script is a 'TestRunner'.
    It reads config values from config.json such as base url, response time, test data file etc
    It will read the data from data folder and execute the apis.
    To add a new api, just add a new row to the json file in data folder
    After executing the apis, it will print the result in console.
    We can use other Libraries to get report in PDF or HTML format but for simplicity, using "pytablewriter" library
'''

#!/usr/bin/python

import os.path
import sys
import unittest
from testLibs import core_lib
import datetime


class TestRunner(unittest.TestCase):
    global num_test, base_url, num_pass, num_fail, response_time, timeout, connect, test_data

    # Get the config values
    def setUp(self):
        config_val = core_lib.testCommon.parse_json(os.getcwd() + "/config.json")
        TestRunner.base_url = config_val["base_url"]
        TestRunner.response_time = config_val["response_time"]
        TestRunner.connect = config_val["connect"]
        TestRunner.timeout = config_val["timeout"]
        TestRunner.test_data = config_val["test_data"]

    def test_get_data(self):
        TestRunner.num_test = 0
        TestRunner.num_pass = 0
        TestRunner.num_fail = 0
        test_val = core_lib.testCommon.parse_json(os.getcwd()+TestRunner.test_data)
        Table = []
        # For all the tests in the data file
        for k in range(len(test_val)):
            TestRunner.num_test = TestRunner.num_test + 1
            user_dict1 = dict(test_val[k])
            endpoint = user_dict1["Endpoint"]
            desc_call = user_dict1["Desc"]
            req = user_dict1["Request"]
            exp_res = user_dict1["Exp_response"]
            Exp_Version = user_dict1["Exp_Version"]
            payload = user_dict1["payload"]
            url = core_lib.testCommon.get_url(TestRunner.base_url, endpoint)
            res = core_lib.testCommon.execute_api(self, req, url, TestRunner.timeout, TestRunner.connect, payload)
            res_li = list(res)
            resp_code = res_li[0]
            resp_json = res_li[1]
            resp_time = res_li[2]

            # If response code is equal to expected code,
            # check for verifications such as version,observation time,temperature
            response_code = core_lib.testCommon.verify_respcode(exp_res, resp_code)

            if response_code is True:
                resp_data = dict(resp_json)
                is_temp_converted = core_lib.testCommon.verify_temp_conv(self, resp_data['current_observation']['temp_c'],
                                                                        resp_data['current_observation']['temp_f'])

                is_version_match = core_lib.testCommon.verify_version(self, Exp_Version, resp_data['response']['version'])
                is_observation_time_match = core_lib.testCommon.verify_observation_time(self,
                                            datetime.datetime.now().strftime('%B %d'),
                                            resp_data['current_observation']['observation_time'])

                # If all the verifications passed, mark test pass else fail
                if not is_version_match and not is_observation_time_match and not is_temp_converted:
                    result_flag = "Pass"
                    TestRunner.num_pass = TestRunner.num_pass + 1
                else:
                    result_flag = "Fail"
                    TestRunner.num_fail = TestRunner.num_fail + 1
            else:
                result_flag = "Fail"
                TestRunner.num_fail = TestRunner.num_fail + 1

            result_list = []
            result_list.append(TestRunner.num_test)
            result_list.append(req)
            result_list.append(desc_call)
            result_list.append(endpoint)
            result_list.append(result_flag)
            result_list.append(resp_time)
            # Put data for result
            core_lib.testCommon.print_data(self, result_list)


if __name__ == '__main__':
    testSuite = unittest.TestLoader().loadTestsFromTestCase(TestRunner)
    testRunner = unittest.TextTestRunner(verbosity=2).run(testSuite)
