from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from entities.blog.models import Blog
from website import constants
from website.forms import ContactForm
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "website/main.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # getting recent three blog posts
        blogs = Blog.objects.filter(is_active=True).order_by('-id')[:3]

        context['blogs'] = blogs
        return context


class ContactUsView(TemplateView):

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, constants.HELLO_MESSAGE)
            return HttpResponseRedirect(reverse('website:home'))

        messages.error(request, constants.OPERATION_UNSUCCESSFUL)
        return HttpResponseRedirect(reverse('website:home'))


class BlogView(TemplateView):
    template_name = "website/blog.html"

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)

        blog_id = kwargs.get('blog_id', None)
        if blog_id:
            blog = Blog.objects.filter(id=blog_id).first()
            if blog:
                context['blog'] = blog
            else:
                messages.error(self.request, constants.OPERATION_UNSUCCESSFUL)
        else:
            messages.error(self.request, constants.OPERATION_UNSUCCESSFUL)
        return context


class BlogListView(TemplateView):
    template_name = "website/blog-list.html"

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)

        blogs = Blog.objects.filter(is_active=True).order_by('-id')
        context['blogs'] = blogs

        return context
