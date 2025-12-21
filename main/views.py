from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, WorkForm
from .models import Work

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_works'] = Work.objects.filter(is_active=True).order_by('-created_at')[:3]
        return context

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class WorkListView(ListView):
    model = Work
    template_name = 'main/work_list.html'
    context_object_name = 'works'
    paginate_by = 10

    def get_queryset(self):
        queryset = Work.objects.filter(is_active=True).order_by('-created_at')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class WorkDetailView(DetailView):
    model = Work
    template_name = 'main/work_detail.html'
    context_object_name = 'work'

class WorkCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'main/work_form.html'
    success_url = reverse_lazy('work_list')

    def test_func(self):
        return self.request.user.role == 'client' or self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)
