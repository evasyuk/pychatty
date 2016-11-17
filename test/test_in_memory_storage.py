import unittest
from model.in_memory_storage import DialogsHolders
from model.models import User, Message


class TestSet(unittest.TestCase):

    def test_dialog_holders(self):
        dialog_holders = DialogsHolders.get_instance()

        list_of_users = list()
        list_of_users.append("df1")
        list_of_users.append("qq3")

        success, dialog = dialog_holders.create_dialog(list_of_users=list_of_users)
        assert success
        assert len(dialog.list_of_users) == len(list_of_users)
        print "[test_dialog_holders] test case 0 finished"

        success, dialog2 = dialog_holders.get_dialog(did=dialog.did)
        assert success
        assert dialog2.did == dialog.did, "should be the same did, but it is not"
        print "[test_dialog_holders] test case 1 finished"

        success, info = dialog_holders.create_dialog(list_of_users=dialog)
        assert not success, info
        print "[test_dialog_holders] test case 2 finished"

        success, info = dialog_holders.create_dialog(list_of_users=list())
        assert not success, info
        print "[test_dialog_holders] test case 3 finished"

    def test_user_holders(self):
        user1 = User()
        user2 = User()

        # add user 1
        # add user 2

        # get all users

        # get specific user

        # update some user

        # remove one user

        pass

    def test_user_history_holder(self):
        pass

    def test_user_update_holder(self):
        pass

    def test_update_history_manager(self):
        pass
