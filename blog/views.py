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


class CreateBlogRecord(LoginRequiredMixin,View):
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

            blog_template = os.path.join('blog', 'templates', 'articles',
                                         f'{slug}.html')

            thumbnail_path = f'/static/articles/{thumbnail.name}'


            with open(blog_template, 'w') as file:
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
    template_name = 'create_blog_record.html'
    def get(self, request, slug):
        path = f'articles/{slug}.html'

        with open(path, 'r') as file:
            lines = file.readlines()
            title = None
            thumbnail_url = None
            content = None

            for i, data in enumerate(lines):
                if data.strip() == '<h2>{{ title }}</h2>':
                    title = lines[i + 1].strip()
                elif data.strip() == '<img src="{{ thumbnail_url }}" alt="{{ title }} Thumbnail">':
                    thumbnail_url = lines[i + 1].strip()
                elif data.strip() == '<p>{{ content }}</p>':
                    content = lines[i + 1].strip()

        form = GenerateBlogForm(initial={'title': title, 'thumbnail_url': thumbnail_url, 'content': content})

        thumbnail_path = os.path.join('blog', 'static', 'articles',
                                      os.path.basename(thumbnail_url))
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        if os.path.exists(path):
            os.remove(path)
        return render(request, self.template_name,
                      {'form': form})



class BlogsListView(View):
    templates = 'blogs.html'
    template_files = glob.glob('blog/templates/articles/*.html')

    for file_path in template_files:
        print(file_path)
