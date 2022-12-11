from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index_view, name='index'),
    path('upload/', upload_view, name='upload'),
    path('docs/', docs_view, name='docs'),
    path('doc/<str:doc_id>/', doc_view, name='doc'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

