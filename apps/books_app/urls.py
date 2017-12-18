from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^/add$', views.book_add),
	url(r'^/process$', views.book_process),
	url(r'^/(?P<id>\d+)$', views.book_review),
	url(r'^/reviews/(?P<id>\d+)$', views.book_add_review),
	url(r'^/reviews/delete/(?P<book_id>\d+)/(?P<comment_id>\d+)$', views.delete_review)
]