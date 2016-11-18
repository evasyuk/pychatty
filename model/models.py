
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
    def __init__(self, dialog_id, list_of_users, created):
        self.list_of_users = list_of_users
        self.created = created
        self.did = dialog_id


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
