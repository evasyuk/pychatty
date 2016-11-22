from flask import Flask, request
from core import API as api

application = Flask(__name__)

########################################################################################################################
# front-end


@application.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


########################################################################################################################
# api

######
# login

@application.route('/login', methods=['POST'])
def route_login():
    # params
    params = request.get_json()

    return api.login(params=params)

######
# updates

@application.route('/update/post', methods=['POST'])
def route_update_post():
    # headers
    # params
    params = request.get_json()
    headers = request.headers

    return api.on_new_msg(params=params, headers=headers)

@application.route('/update/get', methods=['GET'])
def route_update_get():
    # headers
    headers = request.headers

    return api.on_update_request(headers=headers)

######
# users

@application.route('/user/add', methods=['POST'])
def route_user_add():
    # params
    params = request.get_json()

    return api.on_add_user(params=params)


@application.route('/user/friend/<string:friend_uid>/add', methods=['POST'])
def route_user_add_friend(friend_uid):
    # headers
    headers = request.headers

    return api.on_add_friend(headers=headers, friend_uid=friend_uid)

@application.route('/user/friend/<string:friend_uid>/remove', methods=['DELETE'])
def route_user_remove_friend(friend_uid):
    # headers
    headers = request.headers

    return api.on_remove_friend(headers=headers, friend_uid=friend_uid)


if __name__ == '__main__' or __name__ == 'uwsgi_file_Chatty':
    application.run()
