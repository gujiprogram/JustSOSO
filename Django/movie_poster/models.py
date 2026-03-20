from django.db import models


class Poster(models.Model):
    search_keyword = models.CharField(max_length=100, primary_key=True, blank=False, verbose_name='搜索关键词')
    poster = models.ImageField(upload_to='movies', null=True, blank=True, verbose_name='电影海报', default=None)

    class Meta:
        verbose_name = "电影海报"
        verbose_name_plural = "电影海报"

    def __str__(self):
        return self.search_keyword
