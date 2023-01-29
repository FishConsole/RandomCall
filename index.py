import sys

import bottle
from bottle import Bottle, request, static_file, ServerAdapter

from API import APIhelper
from API.CONFIG import config

main = Bottle()


#############################################################################################
# 网页
#############################################################################################

@main.route('/')
def home():
    try:
        return APIhelper.UA验证(config.子页位置.page_main())
    except config.统一报错.主页连接报错():
        pass


@main.route('/randomcall')
def index():
    try:
        return APIhelper.UA验证(config.子页位置.randomcall())
    except config.统一报错.主页连接报错():
        pass


@main.route('/editor')
def index():
    try:
        return APIhelper.UA验证(config.子页位置.randomcall_editor())
    except config.统一报错.主页连接报错():
        pass


@main.route('/login')
def index():
    try:
        return APIhelper.UA验证(config.子页位置.randomcall_login())
    except config.统一报错.主页连接报错():
        pass


@main.route('/randomcall_test')
def index():
    try:
        return APIhelper.UA验证(config.子页位置.randomcall_login())
    except config.统一报错.主页连接报错():
        pass


@main.route('/ChangeLog')
def index():
    try:
        return APIhelper.UA验证(config.子页位置.randomcall_ChangeLog())
    except config.统一报错.主页连接报错():
        pass


#############################################################################################
# API
#############################################################################################


@main.route('/test')
def index():
    try:
        return APIhelper.调控中心(request.params.items())
    except config.统一报错.主页连接报错():
        pass
    # data = {'name': name, 'age': 11223,'error':'Null','model':'login'}


#############################################################################################
# 主题
#############################################################################################


@main.route('' + config.资源管理器.主题.根() + '<filepath:path>')
def server_static(filepath):
    try:
        return static_file(filepath, root='.' + config.资源管理器.主题.根())
    except config.统一报错.主页连接报错():
        pass


@main.route(config.资源管理器.主题.主题() + '/<filepath:path>')
def server_static(filepath):
    try:
        return static_file(filepath, root='./PROGRAMMER/css/theme')
    except config.统一报错.主页连接报错():
        pass


@main.route(config.资源管理器.lib.mdui() + '/<filepath:path>')
def server_static(filepath):
    try:
        return static_file(filepath, root='./PROGRAMMER/lib')
    except config.统一报错.主页连接报错():
        pass


#############################################################################################
# js
#############################################################################################


@main.route('/js/ajax')
def index():
    try:
        return APIhelper.UA验证(config.资源管理器.js.ajax_helper())
    except config.统一报错.主页连接报错():
        pass


@main.route('/js/dev')
def index():
    try:
        return APIhelper.UA验证(config.资源管理器.js.devtool())
    except config.统一报错.主页连接报错():
        pass


@main.route('/js/encryption')
def index():
    try:
        return APIhelper.UA验证(config.资源管理器.js.encryption())
    except config.统一报错.主页连接报错():
        pass


@main.route('/js/config')
def index():
    try:
        return APIhelper.UA验证(config.资源管理器.js.config())
    except config.统一报错.主页连接报错():
        pass


@main.route('/js/APICallbackControlCenter')
def index():
    try:
        return APIhelper.UA验证(config.资源管理器.js.config())
    except config.统一报错.主页连接报错():
        pass


@main.route('/js/mdui')
def index():
    try:
        return APIhelper.UA验证(config.资源管理器.js.Mdui_js())
    except config.统一报错.主页连接报错():
        pass



@main.error(404)
def index():
    try:
        return APIhelper.关闭页()
    except config.统一报错.主页连接报错():
        pass


#############################################################################################
# 启动
#############################################################################################

main.run(host=config.host(), port=config.port())
