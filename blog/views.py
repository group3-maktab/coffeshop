from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import GenerateBlogForm
import os

# Create your views here.
"""
permissions:
------------------
create_blog_record
delete_blog_record
update_blog_record
"""


# from rolepermissions.decorators import has_permission_decorator
# @has_permission_decorator('create_medical_record')
# from rolepermissions.checkers import has_permission
# has_permission(user, 'create_medical_record')


class CreateBlogRecord(LoginRequiredMixin, View):
    template_name = 'create_blog_record.html'

    def get(self, request):
        form = GenerateBlogForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GenerateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            thumbnail = form.cleaned_data['thumbnail']
            content = form.cleaned_data['content']

            # Create a unique slug for the blog post
            slug = slugify(title)
            # Save the uploaded thumbnail to a designated folder

            thumbnail_folder = 'blog/blogs'
            os.makedirs(thumbnail_folder, exist_ok=True)  # Create the folder if it doesn't exist

            thumbnail_path = os.path.join(thumbnail_folder, thumbnail.name)
            with open(thumbnail_path, 'wb') as destination:
                for chunk in thumbnail.chunks():
                    destination.write(chunk)

            # Create a dynamic HTML template for the blog post
            blog_template = os.path.join('blog', 'blogs', f'{slug}.html')

            with open(blog_template, 'w') as file:
                file.write("{% extends 'blog_base.html' %}\n")
                file.write(render_to_string('blog_base.html',
                                            {'title': title,
                                             'content': content,
                                             'thumbnail_url': thumbnail_path}))

            # Redirect to the detail view of the created blog post
            return redirect('blog:blog_detail', slug=slug)
        else:
            return render(request, self.template_name, {'form': form})


class BlogDetailView(TemplateView):
    template_name = 'blog_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs['slug']
        blog_template_path = f'blogs/{slug}.html'

        if not os.path.exists(blog_template_path):
            raise Http404("Blog does not exist")

        # Read the content of the HTML file and pass it to the template
        with open(blog_template_path, 'r') as file:
            content = file.read()

        # Set the title based on the slug
        context['title'] = slugify(slug)
        context['content'] = content
        return context


class UpdateBlogRecord(View):
    pass


class BlogsListView(View):
    pass


class BlogDetailView(View):
    pass
