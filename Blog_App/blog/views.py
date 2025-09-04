
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  )
from .models import Post,Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name= 'posts'
    ordering=['-date_post']
    paginate_by = 5

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name= 'posts'
    paginate_by = 5

    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_post')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-date_post')
        context['form'] = CommentForm()
        return context

#Create Post
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields = ['title','content']

    def form_valid(self,form):   #auther is equal to current logedin user
        form.instance.author=self.request.user
        return super().form_valid(form)
#Update Post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields = ['title','content']

    def form_valid(self,form):   #auther is equal to current logedin user
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):  #test user to update blog
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
#Delete Post
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'

    def test_func(self):  #test user to update blog
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
# Create Comment
class PostComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

def about(request):
    return render(request,'blog/about.html')