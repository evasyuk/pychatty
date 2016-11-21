import json


class User(object):
    """
    Name
    Icon URL
    id

    todo: define _eq_ and _ne_ methods

    """

    def __init__(self, uid=None, name=None, secret=None, icon="", friends=list(), dialogs=list(), _dict=None):
        if _dict is not None:
            self.__dict__ = _dict
            return

        assert uid is not None
        assert name is not None
        assert secret is not None
        assert uid is not None

        self.uid = uid
        self.name = name
        self.icon = icon
        self.friends = friends
        self.secret = secret
        self.dialogs = dialogs
        # self.pending_friends = pending_friends
        # self.blocked_users = blocked_users

    def to_json(self):
        """
        Returns:
            str:
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Returns:
            dict:
        """
        data = dict()

        for key in iter(self.__dict__):
            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        return data

    @staticmethod
    def from_dict(params):
        if params is None:
            return False, "params is None"
        else:
            if not isinstance(params, dict):
                return False, "params is not dict instance"
            else:
                try:
                    uid = params['uid']
                    name = params['name']
                    if not 'icon' in params:
                        icon = ""
                    else:
                        icon = params['icon']
                    secret = params['secret']

                    user = User(uid=uid, name=name, icon=icon, secret=secret)
                    return True, user
                except KeyError as exc:
                    return False, exc.message


class Dialog(object):
    """
    dialog_id
    List_of_users
    created

    """

    SEPARATOR = "::"

    def __init__(self, dialog_id, list_of_users, created):
        self.list_of_users = list_of_users
        self.created = created
        self.did = dialog_id

    @staticmethod
    def users_list_from_did(did):
        if not isinstance(did, str):
            return False, "wrong did type"
        if len(did) > 3:
            result = did.split(Dialog.SEPARATOR)
            return True, result
        else:
            return False, "did is wrong"

    @staticmethod
    def did_from_users_list(list_of_users):
        if len(list_of_users) > 0:
            did = ""
            # todo: this is a horrible idea for group chats with big number of participants

            index = 0
            for item in list_of_users:
                if 0 < index < len(list_of_users):
                    did += "::"
                did += item

                index += 1

            return True, did
        else:
            return False, "list len has to be > 0"

    def to_json(self):
        """
        Returns:
            str:
        """
        return json.dumps(self.to_dict())

    def to_dict(self, target_dict=None):
        """
        Recursive serialization to dict

        :param target_dict:
        :return:
        """
        if target_dict is None:
            target_dict = self.__dict__

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


class Message(object):
    """
    From_id
    Text
    Dialog_id
    Timestamp

    """
    def __init__(self, from_id, text, dialog_id, time_stamp):
        self.from_id = from_id
        self.text = text
        self.dialog_id = dialog_id
        self.time_stamp = time_stamp

    def to_json(self):
        """
        Returns:
            str:
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Returns:
            dict:
        """
        data = dict()

        for key in iter(self.__dict__):
            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        return data

    @staticmethod
    def from_dict(params):
        if params is None:
            return False, "params is None"
        else:
            if not isinstance(params, dict):
                return False, "params is not dict instance"
            else:  # todo: replace with one catch clause and detail parsing
                try:
                    from_id = params['from_id']
                except KeyError:
                    return False, "from_id key not found"

                try:
                    text = params['text']
                except KeyError:
                    return False, "text key not found"

                try:
                    dialog_id = params['dialog_id']
                except KeyError:
                    return False, "dialog_id key not found"

                try:
                    time_stamp = params['time_stamp']
                except KeyError:
                    return False, "time_stamp key not found"

                msg = Message(from_id=from_id, text=text, dialog_id=dialog_id, time_stamp=time_stamp)
                return True, msg

            pass

#
# class Update(object):
#     """
#     List_of_dialogs_ids
#         List_of_messages
#
#     """
#     def __init__(self, list_of_dialog_ids_with_msgs):
#         self.list_of_dialog_ids_with_msgs = list_of_dialog_ids_with_msgs
#
#
# class History(object):
#     """
#     Dialog_id
#     List_of_messages
#
#
#     """
#     def __init__(self, dialog_id, list_of_messages):
#         self.dialog_id = dialog_id
#         self.list_of_messages = list_of_messages
