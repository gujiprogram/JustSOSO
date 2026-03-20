from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import MovieForm
from .models import Poster


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    elif request.method == 'GET':
        search_keyword = request.GET.get('search_keyword', None)
        print(search_keyword)
        if search_keyword:
            try:
                # 从数据库中检索与传入的 search_keyword 相匹配的海报
                get_poster = Poster.objects.get(pk=search_keyword)
                # 返回海报的 URL 或其他数据，例如 Base64 编码的图像数据
                return JsonResponse({'success': True, 'poster_url': get_poster.poster.url})
            except Poster.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No poster found for the given search_keyword'})
        else:
            return JsonResponse({'success': False, 'message': 'No search_keyword provided'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST and GET requests are allowed'})

