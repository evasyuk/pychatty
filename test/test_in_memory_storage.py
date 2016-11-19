import unittest
from model.in_memory_storage import DialogsHolders, UsersHolder, UserUpdateHolder
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
        user_holder = UsersHolder()

        user1 = User(uid="test0", name="test0", secret="1111")
        user2 = User(uid="test1", name="test1", secret="1111")

        # add user 1
        # add user 2
        user_holder.add_user(user=user1)
        user_holder.add_user(user=user2)

        # get all users
        success, all_users_dict = user_holder.get_all()

        assert success
        assert len(all_users_dict) == 2, "unexpected size"
        print "[test_user_holders] test case 1 finished"

        # get specific user
        success, user_get_1 = user_holder.get_user(uid=user1.uid)
        assert success, "user_uid not found"
        assert user1.uid == user_get_1.uid
        print "[test_user_holders] test case 2 finished"

        # update some user
        user1.icon = "wakawaka"
        user_holder.update_user(user=user1)

        success, user_get_1 = user_holder.get_user(uid=user1.uid)
        assert success, "user_uid not found"
        assert user1.uid == user_get_1.uid and user_get_1.icon == user1.icon, "not equal"
        print "[test_user_holders] test case 3 finished"

        # remove one user

        remove_success, info = user_holder.remove_user(user_uid=user2.uid)

        get_success, all_users_dict = user_holder.get_all()

        assert remove_success
        assert len(all_users_dict) == 1, "unexpected size"
        print "[test_user_holders] test case 4 finished"

    def test_user_update_holder(self):
        # 1. create users
        user1 = User(uid="test0", name="test0", secret="1111")
        user2 = User(uid="test1", name="test1", secret="1111")

        # 2. imitate dialog
        # dialog_holders = DialogsHolders.get_instance()
        #
        # list_of_users = list()
        # list_of_users.append(user1.uid)
        # list_of_users.append(user2.uid)
        #
        # success, dialog = dialog_holders.create_dialog(list_of_users=list_of_users)

        # 3. prepare messages
        msg1 = Message(dialog_id="test", text="test text", from_id=user1.uid, time_stamp=-1)
        msg2 = Message(dialog_id="test", text="text test", from_id=user2.uid, time_stamp=-2)

        # 4. prepare update holders
        update_holder_u1 = UserUpdateHolder(user_id=user1.uid)
        update_holder_u2 = UserUpdateHolder(user_id=user2.uid)

        update_holder_u1.add(message=msg1, dialog_id="test")
        update_holder_u1.add(message=msg2, dialog_id="test")

        update_holder_u1_dict = update_holder_u1.get_as_dict()
        update_holder_u2_dict = update_holder_u2.get_as_dict()

        j_result = update_holder_u1.get_as_json()
        pass  # do not know how to automate validation -> seems to be OK

    def test_user_history_holder(self):
        pass

    def test_update_history_manager(self):
        pass
