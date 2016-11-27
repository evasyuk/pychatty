import json
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
    params = params_from_request(request)

    if params is None:
        response = json.dumps({'error': "unsupported content-type -> " + str(request.content_type)})
        return response, 400
    else:
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
        headers = request.headers
        # params
        params = params_from_request(request)

        if params is None:
            response = json.dumps({'error': "unsupported content-type -> " + str(request.content_type)})
            return response, 400
        else:
            return api.on_new_msg(params=params, headers=headers)

######
# users

@application.route('/user/add', methods=['POST'])
def route_user_add():
    # params
    params = params_from_request(request)

    if params is None:
        response = json.dumps({'error': "unsupported content-type -> " + str(request.content_type)})
        return response, 400
    else:
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


def params_from_request(request_this):
    """
    This method transforms parameters from different types or POST requests:
    - either application/json
    - either application/form-url-encoded

    :param request_this:
    :return:
    """
    if str(request_this.content_type) == 'application/x-www-form-urlencoded':
        params = dict()

        for key, value in zip(request_this.form.keys(), request_this.form.values()):
            params[key] = value
    elif str(request_this.content_type) == 'application/json':
        params = request_this.get_json()
    else:
        return None

    return params


if __name__ == '__main__' or __name__ == 'uwsgi_file_Chatty':
    print "main fired[%s]" % __name__

    application.run(host='0.0.0.0', port=8080)
