# coding=utf-8
import json
from model.in_memory_storage import UpdateHistoryManager, UsersHolder, DialogsHolders
from model.models import Message, User
from util import jwt_util

# return "¯\_(ツ)_/¯: not implemented yet", 501
dialogs_storage = DialogsHolders.get_instance()
update_history_manager = UpdateHistoryManager(dialogs_holder=dialogs_storage)
users_storage = UsersHolder()


########################################################################################################################
# login

# done covered
def login(params):
    """
    To obtain access token user need to provide 2 basic parameters:
    - uid
    - secret

    Cases to cover:
        400 missing parameters
        400 uid not found
        400 wrong credentials
        200
        500 failed to obtain token

    :param params:
    :return:
    """
    if params is None:
        response = json.dumps({'error': "missing params"})
        return response, 400

    try:
        uid = params['uid']
        secret = params['secret']
    except KeyError as exc:
        response = json.dumps({'error': exc.message})
        return response, 400

    found, user = users_storage.get_user(uid=uid)

    if found:
        if user.secret == secret:
            try:
                token = jwt_util.encode_token(json_payload=user.to_dict())

                response = json.dumps({'token': token})
                return response, 200
            except Exception as exc:
                response = json.dumps({'error': exc.message})
                return response, 500
        else:
            response = json.dumps({'error': 'wrong credentials'})
            return response, 400
    else:
        response = json.dumps({'error': 'user not found'})
        return response, 400


# def logout(headers, params):
#     pass

# done covered
def check_auth(success_runnable, headers):
    try:
        decoded = jwt_util.decode_token(encoded_payload=headers['token'])

        if isinstance(decoded, dict):
            return success_runnable(User(_dict=decoded))
        else:
            response = json.dumps({'error': 'wrong token'})
            return response, 401
    except KeyError:
        response = json.dumps({'error': 'login required'})
        return response, 401


########################################################################################################################
# conversation
def on_new_msg(headers, params):
    """
    Expecting Message object in params
    {

    }

    Cases to cover:
        401 missing token
        401 wrong token
        400 missing message object
        200

    :param headers:
    :param params:
    :return:
    """
    def success(user_from):
        msg_correct, msg = Message.from_dict(params=params)

        if not msg_correct:
            response = json.dumps({'error': msg})
            return response, 400
        else:
            dialog_id = msg.dialog_id
            user_id = msg.user_id

            found_dialog, dialog = dialogs_storage.get_dialog(did=dialog_id)

            if found_dialog:
                update_history_manager.on_new_msg(msg=msg)

                response = update_history_manager.on_get_update_json(user_id=user_id)
                return response, 200
            else:
                response = json.dumps({'error': "dialog object with specified not found"})
                return response, 500

    return check_auth(headers=headers, success_runnable=success)


# done
def on_update_request(headers):
    """

    1. form JSON as list of Update objects
    2. copy models to history
    3. respond with JSON
    4. wipe update data

    :param headers:
    :return:
    """
    def on_success(user_from):
        user_id = user_from.uid

        response = update_history_manager.on_get_update_json(user_id=user_id)
        return response, 200

    return check_auth(headers=headers, success_runnable=on_success)


# done
def on_history_request(headers, dialog_id=None):
    def on_success(user_from):
        user_id = user_from.uid
        response = update_history_manager.on_get_history_json(user_id=user_id, dialog_id=dialog_id)
        return response, 200

    return check_auth(headers=headers, success_runnable=on_success)


########################################################################################################################
# dialog

# dialog could be p2p or group.
# def on_create_group_dialog(headers, params):
#     """
#
#
#     :param headers:
#     :param params:
#     :return:
#     """
#     pass
#
#
# def on_remove_group_dialog(headers, dialog_id):
#     pass
#
#
# def on_add_to_group_dialog(headers, params):
#     pass
#
#
# def on_remove_from_group_dialog():
#     pass

########################################################################################################################
# user

# done covered
def on_add_user(params):  # it is a kind of registration
    """
    To create user provide 3 basic parameters

    - uid - unique id (email for instance)
    - name - user name
    - icon - user url icon (optional)
    - secret - password

    Cases to cover:
        400 missing params
        201 created
        400 failed to add new user

    :param params:
    :return:
    """
    correct, user = User.from_dict(params=params)

    if not correct:
        response = json.dumps({'error': user})
        return response, 400
    else:
        result, info = users_storage.add_user(user)

        if result:
            response = user.to_json()
            return response, 201
        else:
            response = json.dumps({'error': info})
            return response, 400


# done
def on_add_friend(headers, friend_uid):  # it is a GET request
    """
    To remove friend provide 1 basic parameter via URL:
    - friend unique uid (to get their uid use QR on its client app)

    Cases to cover:
        400 missing friend uid
        400 already friends
        200 friend added

    Response:
    {
        "dialog": {
        }
    }

    :param headers:
    :return:
    """
    def on_success(user_from):
        if friend_uid is not None:
            found, actual_user = users_storage.get_user(uid=user_from.uid)
            if not found:
                response = json.dumps({'error': "user not existed"})
                return response, 400

            found, friend_user = users_storage.get_user(uid=friend_uid)
            if not found:
                response = json.dumps({'error': "friend not existed"})
                return response, 400

            if friend_uid in actual_user.friends:
                response = json.dumps({'error': "already friends"})
                return response, 400
            else:
                actual_user.friends.append(friend_uid)
                friend_user.friends.append(user_from.uid)

                _temp = list()
                _temp.append(actual_user)
                _temp.append(friend_user)
                created, dialog = dialogs_storage.create_dialog(list_of_users=_temp)

                if not created:
                    response = json.dumps({'error': dialog})
                    return response, 400

                users_storage.update_user(user=actual_user)
                users_storage.update_user(user=friend_user)

                response = json.dumps({'dialog': dialog.to_dict()})
                return response, 200
        else:
            response = json.dumps({'error': "friend uid missing"})
            return response, 400

    return check_auth(headers=headers, success_runnable=on_success)


# done
def on_remove_friend(headers, friend_uid):  # it is a GET request
    """
    To remove friend provide 1 basic parameter via URL:
    - friend unique uid (to get their uid use QR on its client app)

    Cases to cover:
        400 missing friend uid
        400 already friends
        200 friend added

    :param headers:
    :return:
    """
    def on_success(user_from):
        if friend_uid is not None:
            actual_user = users_storage.get_user(uid=user_from)

            if friend_uid in actual_user.friends:
                actual_user.friends.remove(friend_uid)

                users_storage.update_user(user=actual_user)

                response = json.dumps(actual_user)
                return response, 200
            else:
                response = json.dumps({'error': "already not friends"})
                return response, 400
        else:
            response = json.dumps({'error': "friend uid missing"})
            return response, 400

    return check_auth(headers=headers, success_runnable=on_success)


# def on_remove_user(headers, user_id):
#     pass

# def on_update_user(headers, params):
#     pass


class ConversationManager(object):

    def __init__(self):
        self.active_dialogs = dict()

    def on_new_msg(self, msg):
        dialog_id = msg.dialog_id

        try:
            dialog = self.active_dialogs[dialog_id]
        except KeyError:
            reason = "dialog[%s] not found" % dialog_id
            return False, reason

        return False, "not implemented"
