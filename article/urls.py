from django.urls import path
from .views import (ArticleListView, ArticleDetailView,
                    ArticleCreateView, ArticleUpdateView,
                    ArticleDeleteView,pdfView,ColumnListView)

app_name = 'article'
urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article_detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article_create/', ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
    path('', pdfView, name='pdf_development'),
    path('columns/', ColumnListView.as_view(), name='column_list'),
    path('articles/column/<int:column_id>/', ArticleListView.as_view(), name='article_list_by_column'),

]