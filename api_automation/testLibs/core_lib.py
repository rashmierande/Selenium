'''
    This is a core library for all the common functions
    Not using assert, because do not want hard assert that is,
    we do not want to  terminate execution if test fail
'''
#!/usr/bin/python
import unittest
import requests
import json
import math
import pytablewriter


class testCommon(unittest.TestCase):
    global session
    session = requests.session()

    # It will form the url from base url, endpoint and protocol(http)
    def get_url(base_url, endpoint):
        url = "http://" + base_url + endpoint
        return url

    def verify_respcode(exp_code, resp_code):
        if exp_code != resp_code:
            return False
        else:
            return True

    # execute based on the method.
    def execute_api(self, req, url, timeout, connect, data=None):
            req_session = req
            payload = data
            if req_session == 'Post':
                req = session.post(url, data=payload, verify=False, timeout=(connect, timeout))
            elif req_session == 'Put':
                req = session.put(url, data=payload, verify=False, timeout=(connect, timeout))
            elif req_session == 'Delete':
                req = session.delete(url, data=payload, verify=False, timeout=(connect, timeout))
            elif req_session == 'Get':
                req = session.get(url, verify=False, timeout=(connect, timeout))
            return req.status_code, req.json(), req.elapsed.total_seconds()

    # Get Json file
    def parse_json(data):
            with open(data, 'r') as fp:
                val = json.load(fp)
            dict_val = dict(val)
            li = dict_val.get("getUrl")
            return li

    # Verify version, we can have assertEqual for hard assert- specified in commented code
    def verify_version(self, exp_version, actual_version):
        if exp_version == actual_version:
            return None
        else:
            return "Version verification failed"
         # self.assertEqual(exp_version,actual_version,"Version does not matched")

    # Verify observation time is current time
    def verify_observation_time(self, current_time, resp_observation_time):
        if current_time in resp_observation_time:
            return None
        else:
            return "Observation verification failed"
        # self.assertIn(current_time,resp_observation_time)

    # Verify temperature, convert temp to celcius and fahrenheit to check if it is converetd correctly
    def verify_temp_conv(self, temp_c, temp_f):
        cal_temp_f = round(((temp_c * 9/5)+32), 2)
        cal_temp_c = round(((temp_f - 32)* 5/9), 2)
        if math.isclose(cal_temp_f, temp_f, rel_tol=0.9) and math.isclose(cal_temp_c, temp_c, rel_tol=0.9):
                return None
        else:
                return "Temperature verification failed"
         # self.assertAlmostEqual(temp_c,cal_temp_c,msg="Celcius temp does not match",delta=0.9)
         # self.assertAlmostEqual(temp_f,cal_temp_f,msg="Fahrenheit temp does not match",delta=0.9)

    # To print the result
    def print_data(self, res_list):
        writer = pytablewriter.MarkdownTableWriter()
        writer.table_name = "Api Report \n"
        writer.header_list = ["Num", "Req Method", "Desc", "Endpoint", "Result", "Response Time "]
        writer.value_matrix = [res_list]
        writer.write_table()
