from django.shortcuts import render,redirect
from .models import Job,Application
from .forms import PostForm

# Create your views here.


def job_list(request):
    jobs = Job.objects.all()
    app = Application.objects.all()
    return render(request, 'jobapp/job_list.html',{'jobs':jobs,'app':app})

def job_new(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            return redirect('job_list')

    return render(request, 'jobapp/job_edit.html',{'form':form})