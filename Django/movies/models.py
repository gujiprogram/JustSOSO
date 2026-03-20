from django.db import models


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    search_keyword = models.CharField(max_length=100, blank=False, verbose_name='搜索关键词')
    name = models.CharField(max_length=100, verbose_name='电影名称')
    description = models.TextField(verbose_name="资源描述")
    link = models.CharField(max_length=400, verbose_name="资源链接")
    size = models.CharField(max_length=20, verbose_name="资源大小")
    access = models.BooleanField(verbose_name="是否可访问")
    network = models.CharField(max_length=10, choices=(('阿里', '阿里网盘'), ('百度', '百度网盘'), ('夸克', '夸克网盘'),('迅雷','迅雷网盘')),
                               verbose_name="网盘类别")
    alias = models.CharField(max_length=100, verbose_name="电影别名", default=None)
    detail = models.TextField(verbose_name="资源详情", default=None)
    rate = models.FloatField(verbose_name="豆瓣评分", default=None)

    class Meta:
        verbose_name = "电影列表"
        verbose_name_plural = "电影列表"

    def __str__(self):
        return self.name
