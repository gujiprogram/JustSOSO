import os
from pathlib import Path
from rest_framework.views import exception_handler
from rest_framework.schemas.openapi import AutoSchema

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 使用环境变量，不要在代码中硬编码
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # 生产环境必须设置为 False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']  # 替换为你的实际域名

# Application definition
INSTALLED_APPS = [
    'simpleui',  # DjangoUI
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "restfulapi",  # Restful API
    'rest_framework',  # Restful API
    'rest_framework_swagger',  # API 可视化
    'rest_framework.authtoken',
    'drf_yasg',
    'django_filters',  # Django过滤器
    "users",
    "movies",
    "corsheaders",
    "app_auth",
    "movie_poster",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 这个放到第一位
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS 配置 - 生产环境应该指定具体的域名
CORS_ALLOWED_ORIGINS = [
    'https://your-domain.com',
    'https://www.your-domain.com',
]
# 或者如果确实需要允许所有，但生产环境不推荐
# CORS_ORIGIN_ALLOW_ALL = False

# AUTH_USER_MODEL = 'users.User'
STATIC_URL = "static/"
ROOT_URLCONF = "Django.urls"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = "Django.wsgi.application"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # 默认的认证后端
]

# 数据库配置 - 使用环境变量
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'your-database-name'),
        'USER': os.environ.get('DB_USER', 'your-db-user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-db-password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# drf 配置，包含：异常、权限
REST_FRAMEWORK = {
    # API 可视化
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # 解析
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    # 异常
    'EXCEPTION_HANDLER': 'utils.custom_execption.custom_exception_handler',
}

# 更改默认语言为中文
LANGUAGE_CODE = 'zh-hans'

# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

# 隐藏首页的快捷操作和最近动作
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION = False

# 设置默认主题，指向主题css文件名。layui风格
SIMPLEUI_DEFAULT_THEME = 'layui.css'

# 修改左侧菜单首页设置
SIMPLEUI_HOME_PAGE = ''  # 指向页面
SIMPLEUI_HOME_TITLE = 'JUST搜搜'  # 首页标题
SIMPLEUI_HOME_ICON = 'fa fa-search'  # 首页图标

# 设置右上角Home图标跳转链接，会以另外一个窗口打开
SIMPLEUI_INDEX = ''

# 去掉默认Logo或换成自己Logo链接
# SIMPLEUI_LOGO = ''

SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单，自定义菜单时建议关闭。
    'system_keep': False,
    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。空列表[] 为全部不显示.
    'menu_display': ['电影管理', '电影海报','用户管理'],
    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': False,
    'menus': [
        {
            'name': '电影管理',
            'icon': 'fa fa-film',
            'models': [
                {
                    'name': '电影列表',
                    'url': '/admin/movies/movie/',
                    'icon': 'fa fa-tasks'
                },
            ]
        },
        {
            'name': '电影海报',
            'icon': 'fa fa-image',
            'models': [
                {
                    'name': '海报列表',
                    'url': '/admin/movie_poster/poster/',
                    'icon': 'fa fa-tasks'
                },
            ]
        },
        {
            'name': '用户管理',
            'icon': 'fa fa-user',
            'models': [
                {
                    'name': '用户列表',
                    'url': '/admin/users/user/',
                    'icon': 'fa fa-tasks'
                },
            ]
        },
    ]
}

# 用于发送邮件的邮箱配置 - 使用环境变量
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.example.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@example.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-email-password')