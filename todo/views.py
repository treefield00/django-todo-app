from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView, 
    UpdateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from todo.models import Task

# Create your views here.
# class TaskListView(ListView):
#     model = Task
#     template_name = 'todo/task_list.html'

class TaskListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'todo/task_list.html'

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser: # スーパーユーザの場合、リストにすべてを表示する。
            return Task.objects.all()
        else: # 一般ユーザは自分のレコードのみ表示する。
            return Task.objects.filter(author=current_user.id)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todo/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    # fields = '__all__'
    fields = ['title','description','deadline']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
 

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    template_name = 'todo/task_delete.html'


# class TaskUpdateView(LoginRequiredMixin, UpdateView):
#     model = Task
#     fields = '__all__'
#     success_url = reverse_lazy('task-list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description','deadline']
    success_url = reverse_lazy('task-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

