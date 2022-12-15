def port():
    # 改端口的话就要动这个
    return '9090'


def host():
    # 改端口的话就要动这个
    return '127.0.0.1'


class 子页位置:
    # 这样就不会出现找不到资源文件的问题了
    @staticmethod
    def page_main():
        return 'PROGRAMMER/main.html'

    @staticmethod
    def randomcall():
        return 'PROGRAMMER/randomcall.html'

    @staticmethod
    def randomcall_editor():
        return 'PROGRAMMER/randomcall_editor.html'
