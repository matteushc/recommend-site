#!flask/bin/python
from Controller import Controller
from flask import Flask, jsonify
from flask import request, abort, make_response 


app = Flask(__name__)
controll = Controller()


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': 'Pagina nao encontrada. ', "details": str(e)}), 404)  

@app.errorhandler(500)
def not_found(e):
    return make_response(jsonify({'error': 'Ocorreu algum erro no servidor. ', "details": str(e)}), 500)  


@app.route('/<path:url>/view', methods=['POST'])
def send_url(url):
    document = {'userId': request.json['userId'], 'url': url}
    result = controll.send_url(document)
    if not result:
        abort(404)
    return jsonify(result)


@app.route('/<path:url>/similar', methods=['GET'])
def get_similar_urls(url):
    result = controll.get_similar_url(url)
    if not result or len(result) == 0:
        abort(404)
    return jsonify(result)


@app.route('/process', methods=['GET'])
def process_similar_urls():
    result = controll.process_urls_similar()
    if not result or len(result) == 0:
        abort(404)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)