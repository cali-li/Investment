from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q

from blogs.models import Blog,Comment,Fav
from blogs.forms import CommentForm, CreateForm
from blogs.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class BlogListView(View):
    template_name = "blogs/blog_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        blog_list = Blog.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_things.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)
            objects = Blog.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            # try both versions with > 4 posts and watch the queries that happen
            objects = Blog.objects.all().order_by('-updated_at')[:10]
            # objects = Post.objects.select_related().all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'blog_list' : objects, 'search': strval, 'favorites': favorites}
        retval = render(request, self.template_name, ctx)

        # dump_queries()
        return retval;

# class ArticleListView(OwnerListView):
#     model = Ad
#     template_name = "ads/ad_list.html"

#     def get(self, request) :
#         ad_list = Ad.objects.all()
#         favorites = list()
        # if request.user.is_authenticated:
        #     # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
        #     rows = request.user.favorite_things.values('id')
        #     # favorites = [2, 4, ...] using list comprehension
        #     favorites = [ row['id'] for row in rows ]
        # ctx = {'ad_list' : ad_list, 'favorites': favorites}
        # return render(request, self.template_name, ctx)


class BlogDetailView(OwnerDetailView):
    model = Blog
    template_name = "blogs/blog_detail.html"
    def get(self, request, pk) :
        x = Blog.objects.get(id=pk)
        comments = Comment.objects.filter(blog=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'blog' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class BlogCreateView(OwnerCreateView):
    model = Blog
    # fields = ['title', 'text','price']

    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        blog = form.save(commit=False)
        blog.owner = self.request.user
        blog.save()
        return redirect(self.success_url)


class BlogUpdateView(OwnerUpdateView):
    model = Blog
    # fields = ['title', 'text','price']
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:all')

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, owner=self.request.user)
        form = CreateForm(instance=blog)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        blog = get_object_or_404(Blog, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=blog)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        blog = form.save(commit=False)
        blog.save()

        return redirect(self.success_url)


class BlogDeleteView(OwnerDeleteView):
    model = Blog

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Blog, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, blog=f)
        comment.save()
        return redirect(reverse('blogs:blog_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "blogs/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        blog = self.object.blog
        return reverse('blogs:blog_detail', args=[blog.id])

def stream_file(request, pk):
    pic = get_object_or_404(Blog, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Blog, id=pk)
        fav = Fav(user=request.user, blog=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Blog, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, blog=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
