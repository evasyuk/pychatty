import json
from model.models import User, Dialog
from util.datetime_utils import DateTimeUtils


class UpdateHistoryManager(object):
    def __init__(self):
        self.dict_of_users_updates = dict()
        self.dict_of_users_histories = dict()

    def on_new_msg(self, msg, dialog):
        dialog_id = msg.dialog_id

        for other_user_id in dialog.list_of_users:
            try:
                user_updates = self.dict_of_users_updates[other_user_id]
            except KeyError:
                user_updates = self.dict_of_users_updates[other_user_id] = UserUpdateHolder(user_id=other_user_id)

            user_updates.add(message=msg, dialog_id=dialog_id)

    def on_get_update(self, user_id):
        try:
            user_updates = self.dict_of_users_updates[user_id]

            return user_updates.get_as_json()
        except KeyError:
            return json.dumps({})

    def on_get_history(self, user_id, dialog_id=None):
        try:
            user_histories = self.dict_of_users_histories[user_id]
        except KeyError:
            user_histories = self.dict_of_users_histories[user_id] = UserHistoryHolder(user_id=user_id)

        return user_histories.get_as_json(dialog_id=dialog_id)


class UserUpdateHolder(object):
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
        result = json.dumps(self.storage)  # 1. prepare data as JSON
        # self.storage = dict()  # 2. wipe out data
        # # todo: is it memory safe to do such a thing

        return result

    def get_as_dict(self):
        return dict(self.__dict__)

    def clear(self):
        self.storage = dict()


class UserHistoryHolder(object):
    def __init__(self, user_id):
        self.storage = dict()
        self.user_id = user_id

    def on_add(self, user_update_dict):
        for dialog_id, dialog_list in user_update_dict.iteritems():
            try:
                local_dialog_list = self.storage[dialog_id]
            except KeyError:
                local_dialog_list = self.storage[dialog_id] = list()

            local_dialog_list.extend(dialog_list)

        user_update_dict.clear()

    def get_as_json(self, dialog_id):
        try:
            result = json.dumps(self.storage[dialog_id])
        except KeyError:
            return None

        return result


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


class DialogsHolders(object):

    __instance = None

    def __init__(self):
        self.storage = dict()

    @staticmethod
    def get_instance():
        if DialogsHolders.__instance is None:
            DialogsHolders.__instance = DialogsHolders()
        return DialogsHolders.__instance

    def get_dialog(self, did):
        if did in self.storage:
            return True, self.storage[did]
        else:


            list_of_users = list()
            dialog = Dialog(dialog_id=did, list_of_users=list_of_users, created=DateTimeUtils.get_today_full_datetime_milliseconds())
            self.storage[did] = dialog

            return True, dialog
