from rest_framework import serializers
from movies.models import Movie
from users.models import User


# 序列化模型为其他格式

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # 序列化所有的字段
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 序列化所有的字段
        fields = '__all__'
