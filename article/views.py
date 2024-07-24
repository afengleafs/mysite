from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import ArticlePost,ArticleColumn
from django.contrib.auth.mixins import LoginRequiredMixin

class ColumnListView(ListView):
    model = ArticleColumn
    template_name = 'article/column.html'  # 请确保创建这个模板
    context_object_name = 'columns'
    ordering = ['-created']  # 按创建时间倒序排列

class ArticleListView(ListView):

    model = ArticlePost
    template_name = 'article/list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = ArticlePost.objects.all()
        search = self.request.GET.get('search')

        # 栏目过滤
        column_id = self.kwargs.get('column_id')
        if column_id:
            self.column = get_object_or_404(ArticleColumn, id=column_id)
            queryset = queryset.filter(column=self.column)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        # 如果是按栏目过滤，添加栏目信息到上下文
        if hasattr(self, 'column'):
            context['column'] = self.column
        return context

class ArticleDetailView(DetailView):
    model = ArticlePost
    context_object_name = 'article'
    template_name = 'article/detail.html'

class ArticleCreateView(LoginRequiredMixin,CreateView):
    login_url = '/userprofile/login/'
    redirect_field_name = 'next'
    model = ArticlePost
    fields = ['title', 'body']
    template_name = 'article/create.html'
    success_url = reverse_lazy('article:article_list')  # 假设你有一个名为 'article_list' 的 URL pattern

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/userprofile/login/'
    redirect_field_name = 'next'
    model = ArticlePost
    fields = ['title', 'body']
    template_name = 'article/update.html'
    success_url = reverse_lazy('article:article_list')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    login_url = '/userprofile/login/'
    redirect_field_name = 'next'
    model = ArticlePost
    success_url = reverse_lazy('article:article_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def pdfView(request):
    return HttpResponse("PDF功能开发中")

