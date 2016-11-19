import json
import unittest
import core.API as api


class TestSet(unittest.TestCase):

    def test_add_user(self, uid="some@e.mail", usecret="1234"):
        uname = "user-" + uid

        params_invalid_0 = None

        params_invalid_1 = dict()
        params_invalid_1['uid'] = uid
        params_invalid_1['secret'] = usecret

        params_valid = dict(params_invalid_1)
        params_valid['name'] = uname

        invalid_response_0, inv_resp_code_0 = api.on_add_user(params=params_invalid_0)
        invalid_response_1, inv_resp_code_1 = api.on_add_user(params=params_invalid_1)
        valid_response, v_resp_code = api.on_add_user(params=params_valid)

        assert inv_resp_code_0 == 400, str(inv_resp_code_0) + invalid_response_0
        assert inv_resp_code_1 == 400, str(inv_resp_code_1) + invalid_response_1
        assert v_resp_code == 201, str(v_resp_code) + valid_response

        print "test[test_add_user] finished"

    def test_login(self, uid="some@e.mail", usecret="1234", result=False):
        self.test_add_user(uid=uid, usecret=usecret)

        params_invalid_0 = None

        params_invalid_1 = dict()
        params_invalid_1['uid'] = uid

        params_valid = dict(params_invalid_1)
        params_valid['secret'] = usecret

        invalid_response_0, inv_resp_code_0 = api.login(params=params_invalid_0)
        invalid_response_1, inv_resp_code_1 = api.login(params=params_invalid_1)
        valid_response, v_resp_code = api.login(params=params_valid)

        assert inv_resp_code_0 == 400, str(inv_resp_code_0) + invalid_response_0
        assert inv_resp_code_1 == 400, str(inv_resp_code_1) + invalid_response_1
        assert v_resp_code == 200, str(v_resp_code) + valid_response

        if result:
            return valid_response, v_resp_code
        else:
            print "test[test_auth] finished"

    def test_add_friend(self):
        uid_1 = "uid_user_1"
        uid_2 = "uid_user_2"

        usecret_1 = "usecret_1"
        usecret_2 = "usecret_2"

        resp, code = self.test_login(uid=uid_1, usecret=usecret_1, result=True)
        assert code == 200, resp

        resp_dict = json.loads(resp)

        headers = dict()
        headers['token'] = resp_dict['token']

        resp, code = api.on_add_friend(headers=headers, friend_uid=None)
        assert code == 400, str(code) + resp

        resp, code = api.on_add_friend(headers=headers, friend_uid="--")
        assert code == 400, str(code) + resp

        resp, code = self.test_login(uid=uid_2, usecret=usecret_2, result=True)
        assert code == 200, resp

        resp, code = api.on_add_friend(headers=headers, friend_uid=uid_2)
        assert code == 200, str(code) + resp

        print "test[test_add_friend] finished"

    def test_remove_friend(self):
        pass

    def test_new_msg(self):
        pass

    def test_update(self):
        pass

    def test_history(self):
        pass
