from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
from datetime import datetime

import utils.rest_utils as rest_utils


from application_services.BookmarksResource.bookmarks_resource import BookmarksResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

##################################################################################################################

@app.route('/')
def index():
    return '<u>bookmark micro service for E6156 project!</u>'

@app.route('/bookmarks', methods=['POST'])
def create_bookmark():
    user_id = request.args.get('user_id')
    post_id = request.args.get('post_id')
    BookmarksResource.create(user_id, post_id)
    rsp = Response("Created", status=201, content_type="text/plain")
    return rsp

@app.route('/bookmarks/<user_id>', methods=['GET'])
def get_bookmarks(user_id):
    template = {'user_id': user_id}
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    res = BookmarksResource.get_bookmarks(template, limit, offset)
    if res is not None:
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route('/bookmarks', methods=['DELETE'])
def delete_bookmark():
    user_id = request.args.get('user_id')
    post_id = request.args.get('post_id')
    res = BookmarksResource.delete(user_id, post_id)
    if res == 0:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    else:
        rsp = Response("Deleted", status=200, content_type="text/plain")

    return rsp

@app.route('/bookmarked', methods=['GET'])
def is_bookmarked():
    user_id = request.args.get('user_id')
    post_id = request.args.get('post_id')
    res = BookmarksResource.is_bookmarked(user_id, post_id)
    rsp = Response(str(res['count(*)']), status=200, content_type="text/plain")

    return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
