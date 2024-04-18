
from flask import jsonify, request
from . import tpbp

@tpbp.route('/', methods=['post'])
def execTask():
    if request.is_json:
        data = request.get_json()
        return jsonify({'code': 200, 'msg': 'Accepted', 'data': data})
    else:
        return jsonify({'code': 400, 'msg': '请求参数格式错误'})

