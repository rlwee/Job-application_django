from django.shortcuts import render,redirect, get_object_or_404
from .models import Job,Application,Category
from .forms import PostForm,SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.


def job_list(request):
    #import pdb; pdb.set_trace()
    jobs = Job.objects.all()
    app = Application.objects.all()
    return render(request, 'jobapp/job_list.html',{'jobs':jobs,'app':app})

@login_required
def job_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            return redirect('job_list')

    return render(request, 'jobapp/job_new.html',{'form':form})

def job_detail(request, pk):
    #import pdb; pdb.set_trace()
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobapp/job_detail.html',{'job':job})


def job_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('job_list')
    job = get_object_or_404(Job, pk=pk)
    form = PostForm(instance=job)
    if request.method == "POST":
        form = PostForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            return redirect('job_detail', pk=job.pk)
    return render(request, 'jobapp/job_new.html',{'form':form})

def job_delete(request,pk):
    job = Job.objects.get(id=pk,owner=request.user)
    job.delete()
    return redirect('job_list')

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user =  authenticate(username=username,password=raw_password)
            login(request, user)
            return redirect('login') 
    return render(request, 'accounts/signup.html',{'form':form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect('signup')

def login_request(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request = request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        messages.error(request, "Invalid username or password")

    return render(request = request, 
                  template_name = 'accounts/login.html',
                  context={'form':form})


def category(request, pk):
    categories = Job.objects.filter(category__id=pk)
    jobs = Job.objects.all()
    #import pdb; pdb.set_trace()
    return render(request,'jobapp/category.html', {'categories':categories, 'jobs':jobs})
