from django.shortcuts import render
from django.views import View

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


class CreateBlogRecord(View):
    def get(self, request):
        template_name = 'create_blog_record.html'
        return render(request, template_name)

    def post(self, request):
        template_name = 'create_blog_record.html'
        title = request.POST['title']
        count = request.POST['count']
        content = [content for content in request.POST['content']]
        author = request.user


class DeleteBlogRecord(View):
    pass


class UpdateBlogRecord(View):
    pass


class BlogsListView(View):
    pass


class BlogDetailView(View):
    pass
