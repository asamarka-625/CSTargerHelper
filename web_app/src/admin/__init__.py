from web_app.src.admin.user import UserAdmin
from web_app.src.admin.map import MapAdmin
from web_app.src.admin.category import CategoryAdmin
from web_app.src.admin.card import CardAdmin
from web_app.src.admin.card_image import CardImageAdmin
from web_app.src.admin.authentication import BasicAuthBackend

from web_app.src.core import cfg


authentication_backend = BasicAuthBackend(secret_key=cfg.SECRET_KEY)