from flask import Flask

application = Flask(__name__)

########################################################################################################################
# front-end


@application.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


########################################################################################################################
# api


@application.route('/get_updates', methods=['GET'])
def route_get_updates():
    return ""


@application.route('/post', methods=['POST'])
def route_post_new_message():
    return ""


@application.route('/history', methods=['GET'])
def route_history():
    return ""

if __name__ == '__main__' or __name__ == 'uwsgi_file_Chatty':
    application.run()
