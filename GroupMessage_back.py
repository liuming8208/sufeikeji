# -*- coding:utf-8 -*-

from wxpy import *
sys.path.append("../")
from DbHelper import *
import json,requests

from datetime import datetime,timedelta

bot = Bot()

# 青桐小助手，群消息文件存放路径
group_message_path = "../assistant/static/images/"
host="http://www.xxxxx.com"

key=""
login_number=0
change_key_time=None

def get_login():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if(key==""):
        return login()
    elif(now>=change_key_time):
        return login()
    else:
        return key

def login():

    global key,login_number,change_key_time
    # 用户登录，获取用户key
    request_user_url = host + "/public/login"
    data_user = {'username': 'liuming', 'password': 'xxxxx'}
    response_user = requests.post(request_user_url, data=data_user)
    user = json.loads(response_user.text)

    key = user['key']
    login_number=1
    change_key_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 08:00:00')

    return key

#微信小助手，接收群消息
@bot.register(run_async=False)
def print_others(msg):

    group_name = str(msg.sender).replace('<Group: ', '').replace('>', '')
    nick_name = str(msg.member).replace('<Member: ', '').replace('>', '')

    nick_name=rm_bm8(nick_name)

    content = msg.text
    msg_type = msg.type
    add_time = msg.create_time  # 说话时间

    if (msg_type == 'Picture' or msg_type == 'Recording' or msg_type == 'Video' or msg_type == 'Attachment'):

        content = msg.file_name
        file_path=group_message_path + content
        msg.get_file(file_path) #保存文件

    try:

       sql="insert into think_wechat_message(group_name,nick_name,content,msg_type,add_time) values(%s,%s,%s,%s,%s)"
       param=[group_name,nick_name,content,msg_type,str(add_time)]

       insert_safe(sql, param, 'assistant')

    except Exception as e:

        insert_sql = "insert into think_log(log,add_time) VALUES(%s,%s) "
        insert_param = [str(e), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        insert_safe(insert_sql, insert_param, 'assistant')

    # 如果是语音、视频、附件就保存到PC端的群文件加下
    if (msg_type == 'Attachment'):
        key = get_login()
        token = ""

        if (key != ""):
            # 上传文件，获取token
            request_upload_url = host + "/storage/wechat-upload-file?key=" + key
            headers = {
                'content-type': "text/plain;charset=utf-8",
                'Fname': file_path.encode('utf-8'),
            }

            try:
                response = requests.post(request_upload_url, data=open(file_path, 'rb'), headers=headers)
                upload = json.loads(response.text)
                token = upload['token']

            except Exception as e:
                token = ""

                insert_sql = "insert into think_log(log,add_time) VALUES(%s,%s) "
                insert_param = ["token获取失败", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                insert_safe(insert_sql, insert_param, 'assistant')

        if (token != ""):
            group = group_name.split('】');
            project_name = group[1];
            request_project_url = host + "/storage/sync-to-project-file?key=" + key
            data_project = {'project_name': project_name, 'token': token, 'nick_name': nick_name}

            insert_response = requests.post(request_project_url, data=data_project)

            insert_sql = "insert into think_log(log,add_time) VALUES(%s,%s) "
            insert_param = [str(data_project) + str(insert_response.text),
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            insert_safe(insert_sql, insert_param, 'assistant')


def rm_bm8(bm8_string):

    ss=[]
    for s in bm8_string[:]:
        if len(s.encode('utf-8'))<4:
            ss.append(s)

    return "".join(ss)

embed()
