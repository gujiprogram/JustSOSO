from django.views import View
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .forms import MovieInfo
from movies.models import Movie
from movie_poster.models import Poster
from users.models import User


class GetMovie(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search_keyword', openapi.IN_QUERY, description="搜索关键字", type=openapi.TYPE_STRING),
            openapi.Parameter('offset', openapi.IN_QUERY, description="偏移量", type=openapi.TYPE_INTEGER),
            openapi.Parameter('network', openapi.IN_QUERY, description="网盘类型", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        search_keyword = request.GET.get('search_keyword', None)
        offset = int(request.GET.get('offset', 0))  # 获取 offset 参数，默认为 0
        network = request.GET.get('network', '全部')
        if search_keyword:
            try:
                movies = Movie.objects.filter(search_keyword=search_keyword)
                # 从数据库中检索与传入的 search_keyword 相匹配的海报
                poster = Poster.objects.get(pk=search_keyword).poster.url
                if network != '全部':
                    movies = movies.filter(network=network)

                total_movies = movies.count()
                all_movie_info_list = [{'name': movie.name, 'description': movie.description, 'link': movie.link,
                                        'size': movie.size, 'access': movie.access, 'network': movie.network,
                                        'alias': movie.alias, 'detail': movie.detail, 'rate': movie.rate}
                                       for movie in movies]

                # 根据 offset 进行切片
                movie_info_list = all_movie_info_list[offset:offset + 10]

                return JsonResponse(
                    {'success': True, 'poster': poster, 'total': total_movies, 'movie_info_list': movie_info_list})
            except Movie.DoesNotExist:
                return JsonResponse(
                    {'success': False, 'message': 'No movie found for the given search_keyword'})
            except Poster.DoesNotExist:
                return JsonResponse(
                    {'success': False, 'message': 'No poster found for the given search_keyword'})
        else:
            return JsonResponse({'success': False, 'message': 'No search_keyword provided'})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_keyword': openapi.Schema(type=openapi.TYPE_STRING, description='搜索关键字'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='电影名称'),
                'link': openapi.Schema(type=openapi.TYPE_STRING, description='资源链接'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='资源描述'),
                'size': openapi.Schema(type=openapi.TYPE_STRING, description='资源大小'),
                'access': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否可访问'),
                'alias': openapi.Schema(type=openapi.TYPE_STRING, description='电影别名'),
                'network': openapi.Schema(type=openapi.TYPE_STRING, description='网盘类别'),
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='资源详情'),
                'rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='豆瓣评分'),
            },
            required=['search_keyword', 'name', 'link', 'description', 'size', 'access', 'alias', 'network', 'detail',
                      'rate']
        )
    )
    def post(self, request):
        form = MovieInfo(data=request.data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class GetUser(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="邮箱", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        email = request.GET.get('email', None)
        if email:
            try:
                # 从数据库中检索与传入的 search_keyword 相匹配的海报
                user = User.objects.get(email=email)
                # 将用户信息转换为字典列表
                user_info = {'email': user.email, 'avatar': user.avatar.url, 'nickname': user.nickname,
                             'is_active': user.is_active}

                return JsonResponse({'success': True, 'user_info': user_info})
            except (User.DoesNotExist, Movie.DoesNotExist):
                return JsonResponse(
                    {'success': False, 'message': 'No user found for the given email'})
        else:
            return JsonResponse({'success': False, 'message': 'No email provided'})
