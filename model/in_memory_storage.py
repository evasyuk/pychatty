import json
from model.models import User, Dialog
from util.datetime_utils import DateTimeUtils


class UpdateHistoryManager(object):
    def __init__(self, dialogs_holder):
        self.dict_of_users_updates = dict()
        self.dict_of_users_histories = dict()
        self.dialogs_holder = dialogs_holder

    def on_new_msg(self, msg):
        dialog_id = msg.dialog_id

        found, dialog = self.dialogs_holder.get_dialog(did=dialog_id)
        if found:
            for other_user_id in dialog.list_of_users:
                try:
                    user_updates = self.dict_of_users_updates[other_user_id]
                except KeyError:
                    user_updates = self.dict_of_users_updates[other_user_id] = UserUpdateHolder(user_id=other_user_id)

                user_updates.add(message=msg, dialog_id=dialog_id)

            return True, "OK"
        else:
            return False, "dialog with did[%s] not found" % dialog_id

    def on_get_update_json(self, user_id):
        try:
            user_updates = self.dict_of_users_updates[user_id]

            # copy to history storage
            try:
                user_histories = self.dict_of_users_histories[user_id]
            except KeyError:
                user_histories = self.dict_of_users_histories[user_id] = UserHistoryHolder(user_id=user_id)

            result = user_updates.get_as_json()

            for did, dialog_update in user_updates.storage.iteritems():
                user_histories.on_add(dialog_update_list=dialog_update)

            user_updates.clear()

            return result
        except KeyError:
            return json.dumps({})

    def on_get_history_json(self, user_id, dialog_id=None):
        # todo: not working yet
        try:
            user_histories = self.dict_of_users_histories[user_id]
        except KeyError:
            user_histories = self.dict_of_users_histories[user_id] = UserHistoryHolder(user_id=user_id)

        return user_histories.get_as_json(dialog_id=dialog_id)


# covered
class UserUpdateHolder(object):  # it is a data structure
    def __init__(self, user_id):
        self.storage = dict()
        self.user_id = user_id

    def add(self, message, dialog_id):
        try:
            dialog_list = self.storage[dialog_id]
        except KeyError:
            dialog_list = self.storage[dialog_id] = list()  # ?

        dialog_list.append(message)

    def get_as_json(self):
        result = self.to_json()
        # self.storage = dict()  # 2. wipe out data
        # # todo: is it memory safe to do such a thing

        return result

    def to_json(self):
        """
        Returns:
            str:
        """
        temp = self.to_dict()
        return json.dumps(temp)

    def to_dict(self, target_dict=None):
        """
        Recursive serialization to dict

        :param target_dict:
        :return:
        """
        if target_dict is None:
            target_dict = self.storage

        result_dict = dict()

        def to_inner_dict(actual_value):
            if hasattr(actual_value, 'to_dict'):
                return actual_value.to_dict()
            else:
                return actual_value

        for key, value in target_dict.iteritems():
            if value is not None:
                if isinstance(value, dict):
                    result_dict[key] = self.to_dict(target_dict=value)
                elif isinstance(value, list):
                    temp = list()

                    for item in value:
                        temp.append(to_inner_dict(actual_value=item))
                    result_dict[key] = temp
                else:
                    result_dict[key] = to_inner_dict(actual_value=value)

        return result_dict

    def get_as_dict(self):
        return dict(self.__dict__)

    def clear(self):
        self.storage = dict()


# covered
class UserHistoryHolder(object):  # it is a data structure
    def __init__(self, user_id):
        self.storage = dict()
        self.user_id = user_id

    def on_add(self, dialog_update_list):
        for msg in dialog_update_list:
            dialog_id = msg.dialog_id

            try:
                local_dialog_list = self.storage[dialog_id]
            except KeyError:
                local_dialog_list = self.storage[dialog_id] = list()

            local_dialog_list.append(msg)
        pass
        # user_id = user_update_dict['user_id']
        #
        # for did, d_list in user_update_dict['storage'].iteritems():
        #

        # for dialog_id, dialog_list in user_update_dict['storage'].iteritems():
        #     try:
        #         local_dialog_list = self.storage[dialog_id]
        #     except KeyError:
        #         local_dialog_list = self.storage[dialog_id] = list()
        #
        #     local_dialog_list.extend(dialog_list)
        #
        # # user_update_dict.clear()  # works only with direct object array -> call on top

    def get_as_json(self, dialog_id):
        try:
            result = json.dumps(self.to_dict()['storage'][dialog_id])
        except KeyError:
            return None

        return result

    def to_dict(self, target_dict=None):
        """
        Recursive serialization to dict

        :param target_dict:
        :return:
        """
        if target_dict is None:
            target_dict = self.storage

        result_dict = dict()

        def to_inner_dict(actual_value):
            if hasattr(actual_value, 'to_dict'):
                return actual_value.to_dict()
            else:
                return actual_value

        for key, value in target_dict.iteritems():
            if value is not None:
                if isinstance(value, dict):
                    result_dict[key] = self.to_dict(target_dict=value)
                elif isinstance(value, list):
                    temp = list()

                    for item in value:
                        temp.append(to_inner_dict(actual_value=item))
                    result_dict[key] = temp
                else:
                    result_dict[key] = to_inner_dict(actual_value=value)

        return result_dict


# covered
class UsersHolder(object):
    def __init__(self):
        self.storage = dict()

    def add_user(self, user):
        if isinstance(user, User):
            try:
                _temp = self.storage[user.uid]
                # has to fail with KeyError for the unique instance
            except KeyError:
                self.storage[user.uid] = user
                return True, "added"

            return False, "already exists"
        else:
            return False, "user has to be User instance"

    def remove_user(self, user_uid):
        if user_uid in self.storage:
            del self.storage[user_uid]
            return True, "deleted"
        else:
            return False, "user_id not found"

    def update_user(self, user):
        try:
            self.storage[user.uid] = user
            return True, "updated"
        except KeyError:
            return False, "user_id not found"

    def get_user(self, uid):
        try:
            result = self.storage[uid]
            return True, result
        except KeyError:
            return False, "user_uid not found"

    def get_all(self):
        result = dict(self.storage)
        return True, result


# covered
class DialogsHolders(object):

    __instance = None

    def __init__(self):
        self.storage = dict()

    @staticmethod
    def get_instance():
        if DialogsHolders.__instance is None:
            DialogsHolders.__instance = DialogsHolders()
        return DialogsHolders.__instance

    def create_dialog(self, list_of_users):
        if isinstance(list_of_users, list):
            success, did = Dialog.did_from_users_list(list_of_users)

            if success:
                dialog = Dialog(dialog_id=did,
                                list_of_users=list_of_users,
                                created=DateTimeUtils.get_today_full_datetime_milliseconds())
                self.storage[did] = dialog
                return True, dialog
            else:
                return False, did
        else:
            return False, "list of users has to be list instance"

    def remove_dialog(self, list_of_users):
        if isinstance(list_of_users, list):
            if len(list_of_users) > 1:
                did = ""

                # todo: this is a horrible idea for group chats with big number of participants
                for item in list_of_users:
                    did += item.uid

                del self.storage[did]

                return True, "deleted"
            else:
                return False, "dialog_holder, list len has to be > 1"
        else:
            return False, "dialog_holder, list of users has to be list instance"

    def get_dialog(self, did):
        if did in self.storage:
            return True, self.storage[did]
        else:
            return False, "not found"
