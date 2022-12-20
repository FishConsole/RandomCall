'''
Author: YUIJ 2645602049@qq.com
Date: 2022-12-14 15:45:52
LastEditors: YUIJ 2645602049@qq.com
LastEditTime: 2022-12-18 16:40:32
FilePath: \RandomCall\CONFIG\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from bottle import template

def port():
    # 改端口的话就要动这个
    return '9090'


def host():
    # 改端口的话就要动这个
    return '127.0.0.1'


def devmodel():
    # 调试模式会对网页加入FishconsoleForJavaScript.js调试辅助器，否则将会取消加入。
    return True

class 子页位置:
    # 这样就不会出现找不到资源文件的问题了
    @staticmethod
    def page_main():
        return template('PROGRAMMER/main.html')

    @staticmethod
    def randomcall():
        return template('PROGRAMMER/randomcall.html')

    @staticmethod
    def randomcall_editor():
        return template('PROGRAMMER/randomcall_editor.html')

    @staticmethod
    def randomcall_login():
        return template('PROGRAMMER/login_main.html')


class 资源管理器:
    class 主题:
        @staticmethod
        def 根():
            return '/PROGRAMMER/css/'

        @staticmethod
        def 主题():
            return '/PROGRAMMER/css/theme'

    class js:
        @staticmethod
        def encryption():
            return '/PROGRAMMER/js/encryption.js'

        @staticmethod
        def config():
            return '/PROGRAMMER/js/config.js'

        @staticmethod
        def ajax_helper():
            return '/PROGRAMMER/js/ajax_helper.js'

        @staticmethod
        def devtool():
            return '/PROGRAMMER/js/FishconsoleForJavaScript.js'