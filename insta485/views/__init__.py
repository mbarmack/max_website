"""Views, one for each Insta485 page."""
from insta485.views.index import show_about
from insta485.views.writing import show_writing, show_post
from insta485.views.api import return_post, create_comment
from insta485.views.account import show_login, logout
from insta485.views.admin import show_admin, add_post, add_text