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

@application.route('/update', methods=['GET', 'POST'])
def route_update():
    if request.method == 'GET':
        # headers
        headers = request.headers

        return api.on_update_request(headers=headers)
    elif request.method == 'POST':
        # headers
        # params
        params = request.get_json()
        headers = request.headers

        return api.on_new_msg(params=params, headers=headers)

######
# users

@application.route('/user/add', methods=['POST'])
def route_user_add():
    # params
    params = request.get_json()

    return api.on_add_user(params=params)


@application.route('/user/me', methods=['GET'])
def route_user_me():
    # headers
    headers = request.headers

    return api.on_get_me(headers=headers)


@application.route('/user/friends', methods=['GET'])
def route_user_friends():
    # headers
    headers = request.headers

    return api.on_get_friends(headers=headers)


@application.route('/user/friend/<string:friend_uid>', methods=['GET', 'DELETE'])
def route_user_add_friend(friend_uid):
    if request.method == 'GET':
        # headers
        headers = request.headers

        return api.on_add_friend(headers=headers, friend_uid=friend_uid)
    elif request.method == 'DELETE':
        # headers
        headers = request.headers

        return api.on_remove_friend(headers=headers, friend_uid=friend_uid)


if __name__ == '__main__' or __name__ == 'uwsgi_file_Chatty':
    print "main fired[%s]" % __name__

    application.run(host='0.0.0.0', port=8080)
