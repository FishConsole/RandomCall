'''
Author: YUIJ 2645602049@qq.com
Date: 2022-12-21 09:42:12
LastEditors: YUIJ 2645602049@qq.com
LastEditTime: 2023-01-08 20:01:04
FilePath: \RandomCall\API\test.py
Description: 这是默认设置,请设置'customMade', 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import base64
import time
from bottle import request
import importlib

Fishconsole_FCMS = importlib.import_module('API.LIB.Fishconsole_FCMS')
config = importlib.import_module('API.CONFIG.config')
数据库位置 = config.远程数据库控制.IP地址()
数据库密码 = config.远程数据库控制.密码()
数据库用户 = config.远程数据库控制.用户名()
数据库连接 = Fishconsole_FCMS.Sqlserver(数据库位置, 数据库用户, 数据库密码, 'maybe', 'user_info')


def 关闭页():
    """
        如需访问，请使用这个ua，否则不允许进入
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Maybe/1.16 Safari/537.36
    """
    return """
    <html>
        <head></head>
        </body>
            <script>
                window.close()
                window.history.go(-1);
            </script>
        </body>
    </html>
    """


def UA验证(目标):
    try:
        数据 = request.headers.get('User-Agent').split(' ')[-2]
        数据 = 数据.split(r'/')[0]
        if 数据 != 'Maybe':
            return 关闭页()
        else:
            return 目标
    except:
        return 关闭页()


def token验证(token):
    try:
        token = base64.b64decode(token)
        token = base64.b64decode(token)
        token = base64.b64decode(token)
        token = base64.b64decode(token)
        token = int(str(int(token))[0:10])
        now = int(time.time())
        if (now - token < 30):
            return True
        else:
            return False
    except TypeError:
        return False


class 回调器:
    """
    code 1：返回成功\n
    code 2：没有指定参数\n
    code 21：模式未找到\n
    code 22：token校验失败\n
    code 23:API内部错误\n
    code 3：登录状态过期\n
    code 4: 数据库错误\n
    code 41：数据库（注册错误）\n
    code 421：数据库（登录错误(密码)）
    code 422：数据库（登录错误(其他)）

    """

    @staticmethod
    def 统一回调():
        return {
            "model": 'ok',
            "code": '1',
            "message": '',
        }

    @staticmethod
    def 报错回调(code, message):
        """
            code: 报错代码\n
            message：要说的话
        """
        result_data = 回调器.统一回调()
        result_data['code'] = code
        result_data['model'] = 'error'
        result_data['message'] = message
        return result_data


class API:
    class 杂项:
        @staticmethod
        def 网址():
            from .CONFIG import config
            result = {'GetUrl': f"{config.host()}:{config.port()}"}
            result.update(API.统一回调())
            return result

    class 用户系统:
        # CREATE TABLE 'maybe'.'User_info' ('User_Name' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , 'Password' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , 'EmailAddress' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , 'Count_LoginDate' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , 'Count_Answer' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , 'LastLogin_IP' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , 'LastLogin_Date' VARCHAR(20) NOT NULL COLLATE utf8mb4_0900_ai_ci , PRIMARY KEY ('User_Name')) COMMENT='', COLLATE='utf8mb4_0900_ai_ci', ENGINE=InnoDB
        @staticmethod
        def 注册(data):
            邮箱地址 = data['EmailAddress']
            密码 = data['Password']
            用户名 = data['name']
            try:
                数据库连接.增加([["`User_Name`", f"'{用户名}'"], ["`Password`", f"'{密码}'"]],
                         [["`EmailAddress`", f"'{邮箱地址}'"]])
            except Exception:
                return 回调器.报错回调('41', '用户已存在')
            result = {'UserName': 用户名, 'Password': 密码, 'EmailAddress': 邮箱地址}
            result.update(回调器.统一回调())

            return result

        @staticmethod
        def 登录(data):
            邮箱地址 = data['EmailAddress']
            密码 = data['Password']
            匹配信息 = 数据库连接.查找(['EmailAddress', 邮箱地址], ['Password', '__fc_all__'])
            try:
                用户密码 = 匹配信息[0][0]
                if 用户密码 == 密码:
                    return 回调器.统一回调()
                else:
                    return 回调器.报错回调('421', '账户或密码错误')
            except IndexError:
                return 回调器.报错回调('422', '账户或密码错误')

    class 更新:
        @staticmethod
        def 用户名():
            pass

        @staticmethod
        def 密码():
            pass

        @staticmethod
        def 答题数():
            pass


def 调控中心(数据源):
    data = dict(数据源)
    # try:
    if (token验证(data['token'])):
        if (data['model'] == 'registration'):
            return API.用户系统.注册(data)
        if (data['model'] == 'login'):
            return API.用户系统.登录(data)
        elif (data['model'] == 'GetUrl'):
            return API.杂项.网址()
        else:
            return 回调器.报错回调('21', 'Maybe_Api调控中心》模式选择》未知的模式')
    else:
        return 回调器.报错回调('22', 'Maybe_Api调控中心》token验证》token已失效，请刷新')
    # except:
    #     return 报错回调('23', 'Maybe_Api调控中心》API内部错误')
