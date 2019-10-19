import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"

OPENID_PROVIDERS = [
    {"name": "Google", "url": "https://www.google.com/accounts/o8/id"},
    {"name": "Yahoo", "url": "https://me.yahoo.com"},
    {"name": "AOL", "url": "http://openid.aol.com/<username>"},
    {"name": "Flickr", "url": "http://www.flickr.com/<username>"},
    {"name": "MyOpenID", "url": "https://www.myopenid.com"},
]

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
# SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/quickhowto'
# SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost:5432/myapp'
# SQLALCHEMY_ECHO = True

BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_FOLDER = "translations"
LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
    "de": {"flag": "de", "name": "German"},
    "ru": {"flag": "ru", "name": "Russian"},
    "uk": {"flag": "ua", "name": "Ukrainian"},
}


# ------------------------------
# GLOBALS FOR GENERAL APP's
# ------------------------------
UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
AUTH_TYPE = 1
# AUTH_LDAP_SERVER = "ldap://dc.domain.net"
# AUTH_LDAP_USE_TLS = False
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "Rework"
# APP_THEME = ""  # default
# APP_THEME = "cerulean.css"      # COOL
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"        #not bad
# APP_THEME = "cyborg.css"       # COOL
# APP_THEME = "flatly.css"       #not bad
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
APP_THEME = "simplex.css"       #prettl theme
# APP_THEME = "slate.css"          # COOL
# APP_THEME = "spacelab.css"      # not bad
# APP_THEME = "united.css"
