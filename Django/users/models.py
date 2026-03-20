from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class User(models.Model):
    username = models.CharField(max_length=100, unique=True, verbose_name='昵称')  # 昵称，假设最大长度为100
    email = models.EmailField(unique=True, verbose_name='邮箱')  # 用户邮箱
    password = models.CharField(max_length=128, verbose_name='密码')  # 登录密码
    avatar = models.ImageField(upload_to='users', null=True, blank=True, verbose_name='头像')  # 用户头像，允许为空

    is_active = models.BooleanField(default=True)

    @classmethod
    def create_user(cls, username, email, password):
        """
        创建一个新用户并返回该用户对象
        """
        user = cls(username=username, email=email, password=password)
        user.save()
        return user

    @classmethod
    def authenticate(cls, email, password):
        """
        验证用户的邮箱和密码是否匹配
        """
        user = cls.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            return True
        return False

    class Meta:
        verbose_name = "用户列表"
        verbose_name_plural = "用户列表"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)  # 使用make_password方法对密码进行加密
        super().save(*args, **kwargs)
