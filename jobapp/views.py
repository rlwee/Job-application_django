from django.shortcuts import render,redirect, get_object_or_404
from .models import Job,Application
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate


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
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user =  authenticate(username=username,password=raw_password)
            login(request, user)
            return redirect('job_list')
    return render(request, 'jobapp/signup.html',{'form':form})