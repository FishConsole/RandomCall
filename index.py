from bottle import Bottle, request, static_file, error
from API import APIhelper

from API.CONFIG import config

main = Bottle()


#############################################################################################
# 网页
#############################################################################################

@main.route('/')
def home():
    return APIhelper.UA验证(config.子页位置.page_main())


@main.route('/randomcall')
def index():
    return APIhelper.UA验证(config.子页位置.randomcall())


@main.route('/editor')
def index():
    return APIhelper.UA验证(config.子页位置.randomcall_editor())


@main.route('/login')
def index():
    return APIhelper.UA验证(config.子页位置.randomcall_login())


@main.route('/randomcall_test')
def index():
    return APIhelper.UA验证(config.子页位置.randomcall_login())


#############################################################################################
# API
#############################################################################################


@main.route('/test')
def index():
    return APIhelper.调控中心(request.params.items())

    # data = {'name': name, 'age': 11223,'error':'Null','model':'login'}


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
    return APIhelper.UA验证(config.资源管理器.js.ajax_helper())


@main.route('/js/dev')
def index():
    return APIhelper.UA验证(config.资源管理器.js.devtool())


@main.route('/js/encryption')
def index():
    return APIhelper.UA验证(config.资源管理器.js.encryption())


@main.route('/js/config')
def index():
    return APIhelper.UA验证(config.资源管理器.js.config())


@main.route('/js/APICallbackControlCenter')
def index():
    return APIhelper.UA验证(config.资源管理器.js.config())

@main.error(404)
def index(error):
    return APIhelper.关闭页()
#############################################################################################
# 启动
#############################################################################################

main.run(host=config.host(), port=config.port(), reloader=True)
