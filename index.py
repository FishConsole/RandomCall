"""
Author: YUIJ 2645602049@qq.com
Date: 2022-12-14 15:19:40
LastEditors: YUIJ 2645602049@qq.com
LastEditTime: 2022-12-18 16:50:32
FilePath: \RandomCall\index.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""
from bottle import Bottle, request, static_file, template
import json
from CONFIG import config

main = Bottle()


#############################################################################################
# 网页
#############################################################################################

@main.route('/')
def home():
    return config.子页位置.page_main()


@main.route('/randomcall')
def index():
    return config.子页位置.randomcall()


@main.route('/editor')
def index():
    return config.子页位置.randomcall_editor()


@main.route('/login')
def index():
    return config.子页位置.randomcall_login()


@main.route('/randomcall_test')
def index():
    return config.子页位置.randomcall_login()


#############################################################################################
# API
#############################################################################################


@main.route('/test')
def index():
    name = request.params.items()
    name = dict(name)
    # data = {'name': name, 'age': 11223,'error':'Null','model':'login'}
    data = json.dumps(name)
    print(data)
    return data


#############################################################################################
# 主题
#############################################################################################


@main.route('' + config.资源管理器.主题.根() + '<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='.' + config.资源管理器.主题.根())


@main.route(config.资源管理器.主题.主题() + '/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./PROGRAMMER/css/theme')


#############################################################################################
# js
#############################################################################################

@main.route('/js/ajax')
def index():
    return config.资源管理器.js.ajax_helper()


@main.route('/js/dev')
def index():
    return config.资源管理器.js.devtool()


@main.route('/js/encryption')
def index():
    return config.资源管理器.js.encryption()


@main.route('/js/config')
def index():
    return config.资源管理器.js.ajax_helper()


main.run(host=config.host(), port=config.port(), reloader=True)
