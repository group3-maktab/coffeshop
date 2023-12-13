from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GenerateBlogForm
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
    def get(self, request):
        template_name = 'create_blog_record.html'

        form = GenerateBlogForm()

        return render(request, template_name, {'form' : form})

    def post(self, request):

        title = request.POST['title']
        thumbnail = request.POST['thumbnail']
        content = request.POST['content']


class DeleteBlogRecord(View):
    pass


class UpdateBlogRecord(View):
    pass


class BlogsListView(View):
    pass


class BlogDetailView(View):
    pass
