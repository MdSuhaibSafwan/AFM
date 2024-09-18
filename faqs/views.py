from django.shortcuts import render, redirect
from faqs.models import Faq, FaqCategory
from faqs.forms import FaqForm, FaqCategoryForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from faqs.filters import FaqFilter
from administration.login_check import super_admin_user_required
from django.core.paginator import Paginator
from django.contrib import messages


class FaqDetailView(DetailView):
    model = Faq

class FaqDeleteView(DeleteView):
    model = Faq
    success_url = reverse_lazy('faqs:list-faq')


def faq_cate_delete(request):
    if request.method == 'GET':
        cate_id = request.GET['cate_id']
        print(cate_id)
        p=FaqCategory.objects.get(id=cate_id)
        p.delete()
        return HttpResponse("Success!") 


@super_admin_user_required
def list_faq(request):
    queryset = Faq.objects.all().order_by('-created')
    filtered_qs = FaqFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)
    return render(request, 'faqs/faq_list.html',
                  {'list': page_obj, 'form': filtered_qs.form,
                   'page_obj': page_obj})

@super_admin_user_required
def create_faq(request):
    if request.method != "POST":
        form = FaqForm
    else:
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created")
            return redirect('faqs:list-faq')
        else:
            print(form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "faqs/faq_form.html", {'form': form, 'title': 'Create Faq'})

@super_admin_user_required
def edit_faq(request, pk):
    object = Faq.objects.get(id=pk)
    if request.method != "POST":
        form = FaqForm(instance=object)
    else:
        form = FaqForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created")
            return redirect('faqs:list-faq')
        else:
            print(form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "faqs/faq_form.html", {'form': form, 'title': 'Edit Faq'})