import unittest
from model.models import User, Message


class TestSet(unittest.TestCase):

    def test_user_from_dict(self):
        uid = "urYr3"
        secret = "1111"
        params_valid = dict()
        params_valid['uid'] = uid
        params_valid['name'] = "Mario"
        params_valid['icon'] = ""
        params_valid['secret'] = secret

        success_valid, user = User.from_dict(params=params_valid)
        assert success_valid, "failed to get User from dict"
        assert user.uid == uid
        assert user.secret == secret
        print "[test_user_from_dict] test case 0 finished"

        params_invalid_0 = dict()
        params_invalid_0['uid'] = uid
        params_invalid_0['name'] = "Mario"
        params_invalid_0['secret'] = secret

        success_invalid_0, info = User.from_dict(params=params_invalid_0)
        assert not success_invalid_0, "expected KeyError, " + info
        print "[test_user_from_dict] test case 1 finished"

        params_invalid_1 = None

        success_invalid_1, info = User.from_dict(params=params_invalid_1)
        assert not success_invalid_0, info
        print "[test_user_from_dict] test case 2 finished"

    def test_message_from_dict(self):
        from_uid = "Fyu3"
        text = "this test is awesome"
        dialog_id = "d3oP"
        time_stamp = 3

        params_invalid_0 = None

        params_invalid_1 = dict()
        params_invalid_1['from_id'] = from_uid
        params_invalid_1['text'] = text
        params_invalid_1['dialog_id'] = dialog_id

        params_valid = dict(params_invalid_1)
        params_valid['time_stamp'] = time_stamp

        success_invalid_0, info = Message.from_dict(params=params_invalid_0)
        assert not success_invalid_0, info
        print "[test_message_from_dict] test case 0 finished"

        success_invalid_1, info = Message.from_dict(params=params_invalid_1)
        assert not success_invalid_1, info
        print "[test_message_from_dict] test case 1 finished"

        params_valid, info = Message.from_dict(params=params_valid)
        assert params_valid, info
        print "[test_message_from_dict] test case 2 finished"
