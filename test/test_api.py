import json
import unittest
import core.API as api
from model.models import User, Message, Dialog


class TestSet(unittest.TestCase):

    def test_add_user(self, uid="some@e.mail", usecret="1234", result=False):
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

        if result:
            if v_resp_code == 201:
                return
            elif v_resp_code == 400 and "already exists" in valid_response:
                return
        else:
            assert inv_resp_code_0 == 400, str(inv_resp_code_0) + invalid_response_0
            assert inv_resp_code_1 == 400, str(inv_resp_code_1) + invalid_response_1
            if not v_resp_code == 201 or v_resp_code == 400 and "already exists" in valid_response:
                pass
            else:
                assert v_resp_code == 201, str(v_resp_code) + valid_response

            print "test[test_add_user] finished"

    def test_login(self, uid="some@e.mail", usecret="1234", result=False):
        self.test_add_user(uid=uid, usecret=usecret, result=result)

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

        resp, code = api.on_remove_friend(headers=headers, friend_uid=uid_2)
        assert code == 200, str(code) + resp

        resp, code = api.on_remove_friend(headers=headers, friend_uid=uid_2)
        assert code == 400, str(code) + resp

        print "test[test_remove_friend] finished"

    def test_new_msg(self):
        uid_1 = "uid_user_1"
        uid_2 = "uid_user_2"

        usecret_1 = "usecret_1"
        usecret_2 = "usecret_2"

        self.test_add_friend()

        resp, code = self.test_login(uid=uid_1, usecret=usecret_1, result=True)
        assert code == 200, resp

        resp_dict = json.loads(resp)

        headers = dict()
        headers['token'] = resp_dict['token']

        success, dialog_id = Dialog.did_from_users_list([uid_1, uid_2])
        assert success, dialog_id

        msg1 = Message(dialog_id=dialog_id, text="test text", from_id=uid_1, time_stamp=-1)
        msg2 = Message(dialog_id=dialog_id, text="text test", from_id=uid_2, time_stamp=-2)

        valid_params = msg1.to_dict()

        resp, code = api.on_new_msg(headers=headers, params=valid_params)
        assert code == 200, str(code) + resp

        print "test[test_update] finished"

    def test_update(self):
        uid_1 = "uid_user_1"
        uid_2 = "uid_user_2"

        usecret_1 = "usecret_1"
        usecret_2 = "usecret_2"

        self.test_add_friend()

        resp, code = self.test_login(uid=uid_1, usecret=usecret_1, result=True)
        assert code == 200, resp

        resp_dict = json.loads(resp)

        headers = dict()
        headers['token'] = resp_dict['token']

        success, dialog_id = Dialog.did_from_users_list([uid_1, uid_2])
        assert success, dialog_id

        msg1 = Message(dialog_id=dialog_id, text="test text", from_id=uid_1, time_stamp=-1)
        msg2 = Message(dialog_id=dialog_id, text="text test", from_id=uid_2, time_stamp=-2)

        valid_params = msg1.to_dict()

        resp, code = api.on_new_msg(headers=headers, params=valid_params)
        assert code == 200, str(code) + resp

        resp, code = api.on_update_request(headers=headers)
        assert code == 200, str(code) + resp

        print "test[test_update] finished"

    # def test_history(self):
    #     pass
