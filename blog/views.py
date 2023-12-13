from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import GenerateBlogForm
import glob
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

            slug = slugify(title)

            thumbnail_folder = 'blog/static/articles'
            os.makedirs(thumbnail_folder, exist_ok=True)

            thumbnail_path = os.path.join(thumbnail_folder, thumbnail.name)
            with open(thumbnail_path, 'wb') as destination:
                for chunk in thumbnail.chunks():
                    destination.write(chunk)

            blog_template = os.path.join('blog', 'templates', 'articles', f'{slug}.html')

            thumbnail_path = f'articles/{thumbnail.name}'
            thumbnail_path = f'{{% static "{thumbnail_path}" %}}'

            with open(blog_template, 'w') as file:
                file.write("{% load static %}\n")
                file.write(render_to_string('blog_base.html',
                                            {'title': title,
                                             'content': content,
                                             'thumbnail_url': thumbnail_path}))

            return redirect('blog:blog_detail', slug=slug)
        else:
            return render(request, self.template_name, {'form': form})


class BlogDetailView(View):
    def get(self, request, slug):
        template_name = f'articles/{slug}.html'
        return render(request, template_name)


class UpdateBlogRecord(View):
    pass


class BlogsListView(View):
    templates = 'blogs.html'
    template_files = glob.glob('blog/templates/articles/*.html')

    for file_path in template_files:
        print(file_path)
