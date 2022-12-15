from bottle import Bottle, request, static_file, template
import json
from CONFIG import config

main = Bottle()


class TemplateCenter:
    @staticmethod
    def page_main():
        return template(config.子页位置.page_main())

    @staticmethod
    def randomcall():
        return template(config.子页位置.randomcall())

    @staticmethod
    def randomcall_editor():
        return template(config.子页位置.randomcall_editor())


@main.route('/')
def home():
    return TemplateCenter.page_main()


@main.route('/page/main')
def home():
    return TemplateCenter.page_main()


@main.route('/page/randomcall')
def index():
    return TemplateCenter.randomcall()


@main.route('/page/randomcall_editor')
def index():
    return TemplateCenter.randomcall_editor()


@main.route('/test')
def test():
    name = request.params.get('name')
    data = {'name': name, 'age': 11223}
    data = json.dumps(data)
    return data


# 根
@main.route('/PROGRAMMER/css/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./PROGRAMMER/css')


# 主题
@main.route('/PROGRAMMER/css/theme/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./PROGRAMMER/css/theme')


# token
@main.route('/PROGRAMMER/css/theme/Colormixer/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./PROGRAMMER/css/theme/Colormixer')


main.run(host=config.host(), port=config.port(), reloader=True)
