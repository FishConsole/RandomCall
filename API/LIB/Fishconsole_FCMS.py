def __类型验证__(数据源: list):
    """
    第一个是指定变量，第二个是

    :param 数据源: 任意数据
    :return: 报错信息
    """
    类型 = type(数据源)
    if str(type(数据源)) != f"<class 'list'>":
        raise TypeError(f'数据源错误，请指定list类型的”目标类型“ - {类型}')
    try:
        for __b__ in 数据源:
            if str(type(__b__[1])) != f"<class 'str'>":
                raise TypeError(f'数据源标识错误，请指定正确的数据源 - {type(__b__[0])}')
            if str(type(__b__[0])) != f"<class '{__b__[1]}'>":
                raise TypeError(
                    f'数据源错误，请指定“{__b__[1]}”类型的数据源 - {__b__[0]}：{__b__[1]}')
    except IndexError as e:
        raise IndexError(f'格式异常，请检查后重试 - {e}')


class Sqlserver:
    """

    这是Fishconsole的sql中文辅助模块，它可以实现简单的mysql的功能

    ----

    它到目前为止有这几种功能:

    - 配置登录：登录你的mysql服务器并返回一个对象，这个对象可以拿到这个程序的任意一个地方使用

    - 创建database：顾名思义

    - 创建table：顾名思义

    - 增加行：顾名思义

    - 删除行：顾名思义

    - 删除table：顾名思义

    - 删除database： 顾名思义

    - 查找：顾名思义

    - 更新：顾名思义

    """

    # 我们创建sql的这个对象时需要让它需要具备如下特性
    # 1. mysql链接地址
    # 2. 用户名
    # 3. 密码
    @staticmethod
    def 版本号():
        return 202301060857
    
    def __init__(self, 链接地址: str, 用户名: str, 密码: str, databases: str = '__fc_wait__', tables: str = '__fc_wait__'):
        # 导入库
        try:
            import pymysql
        except ImportError:
            print('你没有安装pymysql，请安装pymysql后重试')
            exit()
            
        try:
            import cryptography
        except ImportError:
            print('你没有安装cryptography，请安装cryptography后重试')
            exit()
            
        __类型验证__([[链接地址, 'str'], [用户名, 'str'], [密码, 'str'],
                  [databases, 'str'], [tables, 'str']])

        self.链接地址 = 链接地址
        self.用户名 = 用户名
        self.密码 = 密码
        self.databases = databases
        self.tables = tables

    def 配置登录(self, no_databases=False):
        """

        :return: 登录成功了的pymysql对象
        """
        # 导入库
        import pymysql
        # 尝试登录目标数据库
        connect = pymysql.connect(host=self.链接地址,  # 'localhost'
                                 user=self.用户名,
                                 password=self.密码,
                                 database=self.databases,
                                 charset='utf8')
        if no_databases:
            return connect
        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            print('请注意，你的参数中存在__fc_wait__,我们将返回未加载表的内容')
            return [connect]
        else:
            try:
                temp = connect.cursor()
                temp.execute(f'use {self.databases}')
                return [temp, connect]
            except pymysql.err.OperationalError as e:
                raise pymysql.err.OperationalError(f'出现报错，目标databases不存在 - {e}')

    def 获取全部tables(self):
        cur = Sqlserver.配置登录(self)[0]
        try:
            cur.execute(f'show tables')
            return cur.fetchall()
        except Exception as e:
            raise Exception(f'出现报错 - {e}')

    def 切换数据源(self, tables='__fc_stay__', databases='__fc_stay__'):
        """

        这个是切换数据源，如果您不想切换您的表或者databases，请使用'__fc_stay__'来保持当前设置

        ----

        :param databases: 准备修改的databases
        :param tables: 准备修改的tables
        :return: 修改后的实例化对象，可以直接覆盖
        """
        __类型验证__([[tables, 'str'], [databases, 'str']])
        if databases == '__fc_stay__':
            pass
        else:
            self.databases = databases
        if tables == '__fc_stay__':
            pass
        else:
            if databases == '__fc_stay__':
                raise ValueError(f'出现报错 - 在设置table之前必须先指定databases\n{"-" * 10}\ndatabases = {self.databases}')
            self.tables = tables
        """
            这是登录验证判断，看看能不能操作
        """
        try:
            Sqlserver.配置登录(self)[0]
        except Exception as e:
            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                """
                    这个地方是给没给databases和tables参数用的用的
                    因为我们要的是登录后的对象，而不是select的返回值
                """
                pass
            else:
                raise Exception(
                    f'\n{"-" * 10}\n出现报错 - {e}\n有可能是你填错了什么\ntables = {self.tables}\n密码 = {self.密码}\n链接地址 = {self.链接地址}\n用户名 = {self.用户名}\n{"-" * 10}')

        return Sqlserver.配置登录(self)[0]

    def 创建databases(self):
        """

        创建databases

        ----

        :return: 成功返回True，否则返回False

        """
        connect = Sqlserver.配置登录(self, no_databases=True)
        cur = connect.cursor()
        try:
            cur.execute(f'create database if not exists  {self.databases}')
        except Exception as e:
            raise Exception(f'出现报错 - {e}')

    def 创建tables(self, 字段名类型大小: list, 主键: list):
        """

        创建table

        ----

        :param 字段名类型大小:字段的名字，类型，大小，格式 ：[["字段名","类型","大小"],["字段名","int",'11']]

        :param 主键: 就是主键呗，格式：[['主键名','类型','大小'],['主键名','类型','大小']]

        :return:成功返回True，否则返回False

        """
        __类型验证__([[字段名类型大小, 'list'], [主键, 'list']])

        cur = Sqlserver.配置登录(self)[0]
        # 使用databases
        清洗后的字段名类型大小 = ''
        清洗后的主键名类型大小 = ''

        # 预处理字段名类型大小，如果第三个值没有用，那么就把它改成伪布尔值，迭代的时候就根据值来操作
        def 格式验证(类型大小):
            格式验证结果 = []
            for __a__ in 类型大小:

                if int(len(__a__)) != 3:
                    raise Exception(f'数据源错误：每组参数只能有三个值 --- {__a__} --- ,你有可能没有使用嵌套列表，请使用嵌套列表[[]]完成操作')
                else:
                    格式验证结果.append(__a__)
            return 格式验证结果

        # 验证字段结构
        for __a__, b, c in 格式验证(字段名类型大小):
            if __a__ and b and c == 主键[0]:
                raise Exception(f'主键：“{主键[0]}”不应该出现在定义字段名的语句中')
            清洗后的字段名类型大小 = 清洗后的字段名类型大小 + f'{__a__} {b}({c}),'

        # 验证主键结构
        主键集合 = ''
        主键清洗 = 格式验证(主键)
        主键项数 = int(len(主键清洗)) - 1
        计数器 = 0
        for __a__, b, c in 主键清洗:
            清洗后的主键名类型大小 = 清洗后的主键名类型大小 + f'{__a__} {b}({c}),'
            if 计数器 != 主键项数:
                主键集合 = 主键集合 + __a__ + ','
            else:
                主键集合 = 主键集合 + __a__
            计数器 = 计数器 + 1

        try:
            sql = f'create table IF NOT EXISTS {self.tables}({清洗后的字段名类型大小}{清洗后的主键名类型大小} primary key({主键集合}))'
            cur.execute(sql)
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')
        return True

    def 增加(self, 数据: list, 主键: list):
        """

        在指定的表中插入数据

        ----

        :param 数据: 实例：增加([[`事件`,'14'],[`name`,'Alex']])》对id为17的行插入,事件：14,名字：Alex
        :param 主键: 实例：增加([`id`,'17'])》锁定名字为id的主键的第17行
        :return: 成功返回True,否则返回False
        """
        cur, 更新器 = Sqlserver.配置登录(self)
        __类型验证__([[数据, 'list'], [主键, 'list']])

        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            raise ValueError(
                f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

        def 结构验证(__数据__):
            开关 = False
            数据集 = ''
            字段集 = ''
            for 单项数据 in __数据__:
                if 开关:
                    字段集 = 字段集 + ',' + 单项数据[0]
                    数据集 = 数据集 + ',' + 单项数据[1]
                else:
                    字段集 = str(单项数据[0])
                    数据集 = str(单项数据[1])
                开关 = True
            return [数据集, 字段集]

        数据总集 = 结构验证(数据)[0] + ',' + 结构验证(主键)[0]
        字段总集 = 结构验证(数据)[1] + ',' + 结构验证(主键)[1]
        try:
            sql = f"insert into {self.tables}" + \
                  f"({字段总集})" + f"value ({数据总集})"
            # 如果是插入数据， 一定要提交数据， 不然数据库中找不到要插入的数据;
            cur.execute(sql)
            更新器.commit()
            return True
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}\n'+'''常见错误：不是嵌套字符串，请确保你的字符串是["`字符串`","'字符串'"](区分大小写和反引号)而不是其他类型\n要不然就是你没有设置默认值（1364）\n主键重复(1062)''')

    def 删除行(self, 主键: list):
        """

        对指定的行进行删除

        ----

        :param 主键: 实例 ：['id',17]》删除主键id为17的行
        :return: 成功返回True，错误返回False
        """
        __类型验证__([[主键, 'list']])

        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            raise ValueError(
                f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

        try:
            cur = Sqlserver.配置登录(self)[0]

            sql = f'delete from {self.tables} where {主键[0]}={主键[1]}'
            result = cur.execute(sql)
            # connect.commit()
            if result == 1:
                print('删除成功!')
                return True
            else:
                raise Exception('删除失败')
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

    def 删除database(self):
        """

        就是删除database

        ----

        :return: 成功返回True,错误返回False
        """
        connect = Sqlserver.配置登录(self)[0]
        cur = connect.cursor()
        try:
            cur.execute(f'drop database {self.databases};')
        except Exception as e:
            raise Exception(f'出现报错 - {e}')
        print('删除database成功')
        return True

    def 删除table(self):
        """

        就是删除table

        ----

        :return: 成功返回True，否则返回False
        """
        cur = Sqlserver.配置登录(self)[0]

        try:
            sql = f'drop table {self.tables};'
            cur.execute(sql)
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')
        print('删除table成功')
        return True

    def 查找(self, 目标字段: list = [], 需求字段: list = [], 匹配器: str = "__fc_find_wait__", 去重=False):
        """

        就是查找

        ----

        :param 匹配器: 请查看https://www.runoob.com/mysql/mysql-like-clause.html以查看可用函数

        :param 需求字段: 如果你需要用这个表中的其他数据的话就加上这个。实例['id'],作用相当于select ...,id from tbl

        :param 去重: 默认不开启，如需开启请手动给一个True

        :param 目标字段:格式：[[字段名,'值'],[字段名,'值']]，你可以将值设置为"__fc_all__"来获得这个字段的全部内容

        :return: 成功返回内容，否则报错
        """

        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            raise ValueError(
                f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')
        if 需求字段 is None:
            需求字段 = []
        __类型验证__([[需求字段, 'list'], [目标字段, 'list'], [去重, "bool"], [匹配器, "str"]])
        if int(len(目标字段)) != 2:
            raise ValueError(f'目标字段必须为两个参数，第一个是目标字段名，第二个是待查找的值 - {目标字段}')
        if 去重:
            去重 = 'distinct'
        else:
            去重 = ''
        if 匹配器 == '__fc_find_wait__':
            匹配器 = ''
        else:
            匹配器 = f'like "{匹配器}"'
        try:
            def 格式加载(数据源, 目标字段模式=False):
                结果 = ''
                第一次迭代 = True
                for temp in 数据源:
                    try:
                        if temp in "__fc_all__":  # select id,name from test;
                            if not 目标字段模式:
                                raise ValueError(f'出现报错 - 传入参数错误，不可有保留关键字 "__fc_all__" - {temp}')
                            else:
                                continue
                        if 第一次迭代:
                            第一次迭代 = False
                            结果 = temp
                        else:
                            结果 = 结果 + ',' + temp
                    except TypeError as e:
                        raise TypeError(f'出现错误 - 数据源错误：{e}\n{"-" * 10}\n报错点： {temp}')
                return 结果

            if not 需求字段:
                需求字段集 = ""
            else:
                需求字段集 = 格式加载(需求字段, True) + ','
            ##########################################################
            cur = Sqlserver.配置登录(self)[0]
            try:
                if 目标字段[1] == '__fc_all__':
                    print('fc_all模式启动')
                    sql = f"SELECT  {去重} {需求字段集 + 目标字段[0]} from {self.tables} where {目标字段[0]} {匹配器}"
                    cur.execute(sql)
                    # 获取所有记录列表
                    return cur.fetchall()
                else:
                    sql = f"SELECT {去重} {需求字段集 + 目标字段[0]} from {self.tables} where {目标字段[0]}='{目标字段[1]}'"
                    cur.execute(sql)
                    # 获取所有记录列表
                    return cur.fetchall()
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')
        except UnboundLocalError as e:
            raise UnboundLocalError(f'给定的参数错误 - [字段名,"值"]或者是[字段名,"__fc_all__"] - {e}\n{10 * "-"}\n{sql}')

    def 查找_日期(self, 目标字段: str, 目标日期: str, 预期格式: str, 去重=False):
        """

        就是查找

        ----

        :param 去重: 默认不开启，如需开启请手动给一个True

        :param 预期格式: 请查阅https://www.w3school.com.cn/sql/func_date_format.asp

        :param 目标日期: 你想要的日期，比如获得2022年4月的数据【202204】【%Y%m】

        :param 目标字段:格式：[字段名]，选择你准备进行查找的内容

        :return: 成功返回内容，否则报错
        """

        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            raise ValueError(
                f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

        __类型验证__([[目标字段, 'str'], [目标日期, 'str'], [预期格式, 'str'], [去重, 'bool']])
        if 去重:
            去重 = 'distinct'
        else:
            去重 = ''
        try:
            cur = Sqlserver.配置登录(self)[0]
            if 目标日期 == '__fc_all__':
                sql = f"select {去重} date_format(date,'{预期格式}') from {self.tables};"
                cur.execute(sql)
                # 获取所有记录列表
                return cur.fetchall()
            sql = f"SELECT {去重} * FROM {self.tables}  WHERE  DATE_FORMAT(date,'{预期格式}') = '{目标日期}'"
            cur.execute(sql)
            # 获取所有记录列表
            return cur.fetchall()
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

    def 更新(self, 主键: list, 值: list):
        """

        就是更新

        ----

        :param 主键: 实例 ：['id',17]》锁定主键id为17的行
        :param 值: 实例：更新(['id',10],['准备项','22']]))》对id为10的行修改字段'准备项'为22
        :return: 成功返回True，否则报错
        """

        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            raise ValueError(
                f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

        cur = Sqlserver.配置登录(self)[0]
        __类型验证__([[主键, 'list'], [值, 'list']])

        try:
            sql = f'update {self.tables} set {值[0]}="{值[1]}" where {主键[0]} = {主键[1]}'
            cur.execute(sql)
            # connect.commit()
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')
        return True

    def 获得字段最大值(self, 字段名: str):
        """

        获得目标字段最大的值

        ----
        :param 字段名: 选择你准备使用的字段

        :return: 成功返回结果，数据为空时返回空，否则报错
        """
        if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
            raise ValueError(
                f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

        __类型验证__([[字段名, 'str']])
        cur = Sqlserver.配置登录(self)[0]

        try:
            sql = f'SELECT  MAX({字段名}) FROM {self.tables}'
            cur.execute(sql)
            temp = cur.fetchall()[0][0]
            if temp is None:
                return ()
            else:
                return temp
        except Exception as e:
            raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

    class Sqlserver_分组:
        """
        这是Fishconsole的sql中文辅助模块的继承模块，它可以实现简单的分组功能

        ----

        它到目前为止有这几种功能:

        - 求记录

        - 求合计

        - 求平均

        - 求最大

        - 求最小

        - 求相同 【就是找相同的字段值出现了多少次，例子（统计有那些相同价格的值）】

        """

        def __init__(self, 链接地址: str, 用户名: str, 密码: str, databases: str = '__fc_wait__', tables: str = '__fc_wait__'):
            # 导入库
            try:
                import pymysql
            except ImportError:
                print('你没有安装pymysql，请安装pymysql后重试')
                exit()
            __类型验证__([[链接地址, 'str'], [用户名, 'str'], [密码, 'str'],
                      [databases, 'str'], [tables, 'str']])

            self.链接地址 = 链接地址
            self.用户名 = 用户名
            self.密码 = 密码
            self.databases = databases
            self.tables = tables

        def 分组_求记录(self, 字段名: list):
            """

                就是获得字段的总列数

                ----

                :param 字段名: 这是一个list，他的用处就是使用查看字段的大小。实例：获得字段总列数(['userid','username','Password']) -
                获得userid，username，Password的字段总列数

                :return: 返回的是目标字段的总列数
                """

            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                raise ValueError(
                    f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

            __类型验证__([[字段名, 'list']])

            cur = Sqlserver.配置登录(self)[0]
            if str(type(字段名)) == "<class 'str'>":
                raise Exception("请指定list数据源")
            if not 字段名:
                raise Exception("请指定数据")
            待查找字段 = ''
            开关 = True
            for __a__ in 字段名:
                if 开关:
                    待查找字段 = __a__
                    开关 = False
                else:
                    待查找字段 = 待查找字段 + ',' + __a__
            try:
                sql = f'select count(distinct {待查找字段}) from {self.tables};'
                cur.execute(sql)
                temp = cur.fetchall()
                return temp
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

        def 分组_求最大(self, 字段名: str):
            """

            求最大值

            ----

            :param 字段名: 就是你将要查的字段名
            :return: tuple数据
            """
            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                raise ValueError(
                    f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

            __类型验证__([[字段名, 'str']])

            try:
                cur = Sqlserver.配置登录(self)[0]
                sql = f'select max({字段名}) from {self.tables};'
                cur.execute(sql)
                temp = cur.fetchall()
                return temp
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

        def 分组_求最小(self, 字段名: str):
            """

            求最小值

            ----

            :param 字段名: 就是你将要查的字段名
            :return: tuple数据
            """

            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                raise ValueError(
                    f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

            __类型验证__([[字段名, 'str']])

            try:
                cur = Sqlserver.配置登录(self)[0]
                sql = f'select min({字段名}) from {self.tables};'
                cur.execute(sql)
                temp = cur.fetchall()
                return temp
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

        def 分组_求合计(self, 字段名: str):
            """

            求和

            ----

            :param 字段名: 就是你将要查的字段名
            :return: tuple数据
            """

            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                raise ValueError(
                    f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

            __类型验证__([[字段名, 'str']])
            try:
                cur = Sqlserver.配置登录(self)[0]
                sql = f'select sum({字段名}) from {self.tables};'
                cur.execute(sql)
                temp = cur.fetchall()
                return temp
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

        def 分组_求平均(self, 字段名: str):
            """

            求平均值

            ----

            :param 字段名: 就是你将要查的字段名
            :return: tuple数据
            """

            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                raise ValueError(
                    f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

            __类型验证__([[字段名, 'str']])
            try:
                cur = Sqlserver.配置登录(self)[0]
                sql = f'select avg({字段名}) from {self.tables};'
                cur.execute(sql)
                temp = cur.fetchall()
                return temp
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

        def 分组_求相同(self, 字段名: str):
            """

            求相同的值出现的次数

            ----

            :param 字段名: 就是你将要查的字段名
            :return: dict键值对，键为字段值，值为次数
            """

            if self.databases == '__fc_wait__' or self.tables == '__fc_wait__':
                raise ValueError(
                    f'你的参数中存在“__fc_wait__”保留关键字，该操作无法进行\n{"-" * 10}\ndatabases = {self.databases}\ntable = {self.tables}')

            __类型验证__([[字段名, 'str']])
            try:
                cur = Sqlserver.配置登录(self)[0]
                sql = f'select {字段名},count(*) from {self.tables} group by {字段名};'
                cur.execute(sql)
                temp = cur.fetchall()
                try:
                    return dict(temp)
                except TypeError:
                    __a__ = {temp[0]: None}
                    return __a__
            except Exception as e:
                raise Exception(f'出现报错 - {e}\n{10 * "-"}\n{sql}')

# 实例化对象 = Sqlserver('154.31.31.138', 'Maybe_Sql', 'LhzB5iztp46nGrBw', 'maybe_sql', 'test')



# print(实例化对象.查找(['Field_1','__fc_all__']))
# 实例化对象 = Sqlserver('localhost', 'root', '123456', 'testdemo', 'test')
# ###################第一步##################
# 获取到的月份 = 实例化对象.查找_日期('date', '__fc_all__', '%Y%m', True)
# print(获取到的月份)
# ###################第二步##################
# 处理后的月份 = []
# for a in 获取到的月份:
#     处理后的月份.append(a[0])
# print(处理后的月份)
# ###################迭代搜索##################
# 完成dict = {}
# for a in 处理后的月份:
#     temp = 实例化对象.查找_日期('date', a, '%Y%m')
#     完成dict[a] = temp


# print(Sqlserver.Sqlserver_分组('localhost', 'root', '123456', 'testdemo', 'test').分组_求记录(['name']))
