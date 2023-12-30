from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import TagCreateForm
from .models import Tag
from utils import staff_or_superuser_required


class StaffSuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class TagListView(StaffSuperuserRequiredMixin, ListView):
    model = Tag
    template_name = 'Tag_ListTemplate.html'
    context_object_name = 'tags'
    paginate_by = 5


class CreateTagView(StaffSuperuserRequiredMixin, CreateView):
    model = Tag
    template_name = 'Tag_CreateTemplate.html'
    form_class = TagCreateForm
    success_url = reverse_lazy('tags:tag')


class DeleteTagView(View):
    @staff_or_superuser_required
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('tags:tag')


class TagChangeAvailabilityView(View):
    @staff_or_superuser_required
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        if tag.label == "unavailable":
            messages.error(request, 'You can not change this tag availability!')
            return redirect('tags:tag')
        tag.available = not tag.available
        tag.save()
        messages.success(request, 'Tag Changed successfully!')
        return redirect('tags:tag')
