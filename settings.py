# Pylogs settings file
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'mysql' 
DATABASE_NAME = 'pylogs'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''

TIME_ZONE = 'Asia/Chongqing'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'E:\projects\python\pylogs\media'
ALLOW_FILE_TYPES = ('.jpg','.gif','.png')
# URL that handles the media served from MEDIA_URL.
MEDIA_URL = '/media'
# the theme name 'default, techicon, beijing2008'
THEME_NAME = 'techicon'

STATIC_PATH = './media'

ADMIN_MEDIA_PREFIX = '/admin_media/'

#Send Email settings
EMAIL_HOST = 'smtp.sohu.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''

SECRET_KEY = 'zb2&a4g41snkt&*c92s=djl+*fcp((i85w(k&&)#$5j!+zz!!*'
#setting session expire after half a hour.
#SESSION_COOKIE_AGE =  60 * 30

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    "./templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'blog',
    'todo',
    'filemanager',
    #'tests',
)
VERSION = (1, 14, 'beta')	
