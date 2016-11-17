from flask import Flask

app = Flask(__name__)

########################################################################################################################
# front-end


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


########################################################################################################################
# api


@app.route('/get_updates', methods=['GET'])
def route_get_updates():
    return ""


@app.route('/post', methods=['POST'])
def route_post_new_message():
    return ""


@app.route('/history', methods=['GET'])
def route_history():
    return ""

if __name__ == '__main__':
    app.run()
