
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('login/', login_view, name='login'),
        path('register/', register, name='register'),
        path('user-profile/', user_profile, name='user_profile'),
        path('home_page/',home_page, name='home_page' ),
        path('logout/', logout_view, name='logout_view'),
        path('create_post/', create_post, name='create_post'),
        path('like_post/<int:post_id>/', like_post, name='like_post'),
        path('thread/<int:post_id>/', thread, name='thread'),
        path('post/<int:post_id>/comment/', create_comment, name='create_comment'),


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
