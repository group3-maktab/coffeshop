from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

from utils import staff_or_superuser_required
from .forms import GenerateBlogForm
import glob
import os

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


class CreateBlogView(View):
    template_name = 'Blog_CreateTemplate.html'
    template_files = glob.glob('blog/templates/articles/*.html')
    @staff_or_superuser_required
    def get(self, request):
        form = GenerateBlogForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = GenerateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            thumbnail = form.cleaned_data['thumbnail']
            content = form.cleaned_data['content']

            slug = slugify(title)

            urls = []
            for file_path in self.template_files:
                if os.name == 'nt':  # wwindows
                    url = file_path.split('/')[-1][9:-5]
                else:
                    url = file_path.split('/')[-1].split('.')[0]
                urls.append(url)

            if slug in urls:
                messages.error(request, 'We have another blog with that name already.')
                return render(request, self.template_name, {'form': form})

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
                file.write(render_to_string('templates/Blog_Base.html',
                                            {'title': title,
                                             'time': datetime.now().strftime("%y-%b-%d"),
                                             'content': content,
                                             'thumbnail_url': thumbnail_path}))
            messages.success(request, 'Blog Created Successfully.')
            return redirect('blog:detail-blog', slug=slug)
        else:
            messages.error(request, 'Invalid Data.')
            return render(request, self.template_name, {'form': form})


class DetailBlogView(View):
    def get(self, request, slug):
        template_name = f'articles/{slug}.html'
        return render(request, template_name)


class UpdateBlogView(LoginRequiredMixin, View):
    template_name = 'Blog_CreateTemplate.html'

    @staff_or_superuser_required
    def get(self, request, slug):
        path = f'blog/templates/articles/{slug}.html'

        with open(path, 'r') as file:
            contents = file.read()
            title = None
            thumbnail_url = None

            # Extract content between <p> tags
            start_tag = '<p id="content">'
            end_tag = '</p>'

            start_index = contents.find(start_tag)
            end_index = contents.find(end_tag)

            if start_index != -1 and end_index != -1:
                content = contents[start_index + len(start_tag):end_index].strip()

            # Extract title and thumbnail_url from content
            # You may need to adjust these patterns based on the actual structure of your HTML content
            title_start = '<h1 class="text-center fw-bolder display-1 text-capitalize">'
            title_end = '</h1>'
            title_index_start = contents.find(title_start)
            title_index_end = contents.rfind(title_end)
            if title_index_start != -1 and title_index_end != -1:
                title = contents[title_index_start + len(title_start):title_index_end].strip()

            thumbnail_start = '<div class="rounded-3 justify-content-center align-items-center" id="thumbnail"><img class="rounded-3 justify-content-center align-items-center" id="thumbnail" src="'
            thumbnail_end = f'"alt="'
            thumbnail_index_start = contents.find(thumbnail_start)
            thumbnail_index_end = contents.find(thumbnail_end)

            if thumbnail_index_start != -1 and thumbnail_index_end != -1:
                thumbnail_url = contents[thumbnail_index_start + len(thumbnail_start):thumbnail_index_end].strip()

        form = GenerateBlogForm(initial={'title': title, 'thumbnail_url': thumbnail_url, 'content': content})

        thumbnail_path = f'blog{thumbnail_url}'
        print(thumbnail_path)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        if os.path.exists(path):
            os.remove(path)
            messages.success(request, 'Blog Initialize Successfully.')

        return render(request, self.template_name, {'form': form})


class ListBlogView(View):
    templates = 'Blog_ListTemplate.html'
    template_files = glob.glob('blog/templates/articles/*.html')

    def get(self, request):
        urls = []
        for file_path in self.template_files:
            if os.name == 'nt':  # wwindows
                url = file_path.split('/')[-1][9:-5]
            else:
                url = file_path.split('/')[-1].split('.')[0]
            urls.append(url)
        return render(request, self.templates, {'urls': urls})


class DeleteBlogView(LoginRequiredMixin, View):
    def get(self, request, slug):
        path = f'blog/templates/articles/{slug}.html'

        with open(path, 'r') as file:
            lines = file.readlines()
            thumbnail_url = None
            for i, data in enumerate(lines):
                if '<div class="rounded-3 justify-content-center align-items-center" id="thumbnail"><img class="rounded-3 justify-content-center align-items-center" id="thumbnail" src="' in data:
                    thumbnail_url = lines[i + 1].strip()

        thumbnail_path = f'blog/{thumbnail_url}'

        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        if os.path.exists(path):
            os.remove(path)
            messages.success(request, 'Blog Deleted Successfully.')
        return redirect('blog:create-blog')
