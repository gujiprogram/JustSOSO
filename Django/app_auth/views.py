from users.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# 用户注册
class Register(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user_input_code = request.data.get('code')  # 用户输入的验证码
        session_code = cache.get('global_verify')  # 获取验证码

        if user_input_code == session_code:
            if User.objects.filter(email=email).exists():
                resp = {
                    'status': False,
                    'error': '邮箱已被注册'
                }
            else:
                user = User.create_user(username, email, password)

                resp = {
                    'status': True,
                    'emial': user.email,
                    'user_name': user.username,
                }
        else:
            # 验证码不匹配，注册失败
            resp = {
                'status': False,
                'error': '验证码错误',
                'verify': session_code,
            }
        return Response(resp)


# 用户登录
class Login(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # 使用邮箱和密码进行用户验证
        if User.authenticate(email, password):
            return Response({
                'status': True,
                'email': email,
            })
        else:
            # 用户验证失败
            return Response({
                'status': False,
                'message': 'Invalid credentials'
            })


class SendCode(APIView):
    def sendMessage(self, email):  # 发送邮件并返回验证码
        # 生成验证码
        import random
        str1 = '0123456789'
        rand_str = ''
        for i in range(0, 4):
            rand_str += str1[random.randrange(0, len(str1))]
        # 发送邮件：
        message = "您的验证码是：\n\n " + "              " + rand_str + " \n\n10分钟内有效，请尽快填写"
        emailBox = [email]
        send_mail("JUST搜搜验证码", message, '类人猿工作室 <17602319162@163.com>', emailBox, fail_silently=False)
        return rand_str

    # 验证该用户是否已存在 created = 1 存在
    def existUser(self, email):
        created = 1
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            created = 0
        return created

    def post(self, request):
        email = request.data.get('email')
        response = {"status": False, "msg": ""}

        if self.existUser(email):
            response['msg'] = '该用户已存在，请登录'
        else:
            try:
                rand_str = self.sendMessage(email)  # 发送邮件
                # 将验证码存入缓存
                cache.set('global_verify', rand_str, timeout=600)  # 设置过期时间为10分钟
                response['status'] = True
                response['msg'] = '验证码发送成功！'
            except:
                response['msg'] = '验证码发送失败，请检查邮箱地址'
        return Response(response)
