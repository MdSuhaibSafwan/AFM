from django.shortcuts import render, redirect
from feedback.models import Feedback
from feedback.forms import FeedbackFrom
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required


# Create your views here.


class AllFeedback(generic.ListView):
    model = Feedback


class FeedbackCreate(CreateView):
    model = Feedback
    form_class = FeedbackFrom
    success_url = reverse_lazy('')

@login_required
def thank_you(request):
    feedback_list = Feedback.objects.filter(user=request.user).all()
    return render(request, 'feedback/feedback_list.html', {'feedback_list': feedback_list})

@login_required
def student_feedback(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'feedback/feedback_list.html', {'feedback_list': feedback_list})

@login_required
def feedback_create(request):
    form = FeedbackFrom()
    if Feedback.objects.filter(user=request.user).exists():
        return redirect('feedback:thank-you')
    if request.method == 'POST':
        form = FeedbackFrom(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
        return redirect('feedback:thank-you')
    return render(request, 'feedback/feedback_form.html', {'form': form})
