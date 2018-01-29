#-*- coding:utf-8 -*-

#PC端微信presell

import tornado.web,os
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.httpclient
import tornado.escape

import sys
sys.path.append('../')
import presell.UserFactory as UserFactory

#用户登录(返回二维码图片路径)
class login_handler(tornado.web.RequestHandler):

    def get(self):

        user_id = self.get_argument("user_id")
        factory=UserFactory.Factory();

        if (user_id == 0 or str(user_id) == "0"):
            msg="用户信息错误"
        else:
            msg = factory.InitUser(user_id);

        self.write("jsonCallback(['" + msg + "'])")
        self.finish()

#用户信息
class infos_handler(tornado.web.RequestHandler):

    def get(self):

        # 用户信息
        user_id = self.get_argument("user_id")
        user_name = self.get_argument("user_name")

        factory = UserFactory.Factory();
        instance=factory.InitInstance(user_id)

        count=0
        if (instance is not None):
            my_friend = instance.friends()  # 查询当前用户是否登录
            if (len(my_friend) > 0 ):
                first_name = str(my_friend[0]).replace('<Friend: ', '').replace('>', '')

                if (first_name == user_name):
                     count = 1

        if (count > 0):
            self.write("jsonCallback(['1'])") #登录成功
        else:
            self.write("jsonCallback(['0'])") #登录失败

        self.finish()

#发送消息
class send_handler(tornado.web.RequestHandler):

    def post(self):

            user_id = self.get_argument('user_id')  # 发送人的user_id
            to_user_name = self.get_argument('to_user_name')  # 消息接收人(投资人 + 空格（一个空格） + 机构)
            send_message = self.get_argument('msg')  # 消息内容

            if (user_id == 0 or str(user_id) == "0"):
                self.write("jsonCallback(['发送用户信息错误'])")
                self.finish()
                return;

            if (to_user_name == ""):
                self.write("jsonCallback(['接收用户信息错误(投资人姓名+(一个)空格+投资机构)'])")
                self.finish()
                return;

            if (send_message == ""):
                self.write("jsonCallback(['发送内容不能为空'])")
                self.finish()
                return;

            factory = UserFactory.Factory();
            friends = factory.GetInstance(user_id)

            try:
                friend=friends.search(to_user_name)[0]

                if (friend):
                    friend.send(send_message)
                    self.write("jsonCallback(['发送成功'])")
                else:
                    self.write("jsonCallback(['发送失败'])")
            except:
                self.write("jsonCallback(['不存在当前用户'"+to_user_name+"])")

            self.finish()

#页面测试显示二维码
class images_handler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html')


application=tornado.web.Application([
    (r'/wechat/login',login_handler),
    (r'/wechat/infos',infos_handler),
    (r'/wechat/send',send_handler),
    (r'/images', images_handler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)

if __name__=="__main__":

    server = HTTPServer(application,xheaders=True)
    server.listen(UserFactory.port)
    IOLoop.instance().start()


