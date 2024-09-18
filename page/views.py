from django.shortcuts import render
from administration.login_check import super_admin_user_required
from .filters import PageFilter
from .forms import CreatePageForm, UpdateFeatureImageForm
from .models import Page
from django.core.paginator import Paginator


# Create your views here.

@super_admin_user_required
def PostListAdmin(request):
    queryset = Page.objects.all()
    print(queryset)
    filtered_qs = PageFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 50)

    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'page/list_pages.html',
                  {'post_list': page_obj, 'form': filtered_qs.form,
                   'page_obj': page_obj})

@super_admin_user_required
def create_page_twfl(request):
    if request.method != "POST":
        post_form = CreatePageForm
        feature_image_form = UpdateFeatureImageForm
    else:
        post_form = CreatePageForm(request.POST)
        feature_image_form = UpdateFeatureImageForm(request.POST, request.FILES)
        if post_form.is_valid() and feature_image_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.author = request.user
            post_instance.save()
            feature_image_form = UpdateFeatureImageForm(request.POST, request.FILES, instance=post_instance)
            feature_image_form.save()

            messages.success(request, "Your blog have been submitted, we will show it when it gets approval. ")
            return redirect("blogs:blogs_list")
        else:
            print(feature_image_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "page/post_form.html", {'form': post_form, 'form2':feature_image_form,
                                                    'title': 'Create Page'})

@super_admin_user_required
def PostDelete(request, post_id):
    post = Page.objects.get(id=post_id, author=request.user.mentor)
    post.delete()
    return redirect("page:PostListAdmin")

def PostDetail(request, slug):
    # add the dictionary during initialization
    object = Page.objects.get(slug=slug)
    return render(request, "blogs/post_detail.html",
                  {'object': object,})

@super_admin_user_required
def edit_page(request, pk):
    post_instance = get_object_or_404(Page, pk=pk)
    form = CreatPostForm(instance=post_instance)

    feature_image_form = UpdateFeatureImageForm(instance=post_instance)
    if request.method == "POST":
        form = CreatPostForm(request.POST, request.FILES, instance=post_instance)

        feature_image_form = UpdateFeatureImageForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid() and feature_image_form.is_valid():
            form.save()
            feature_image_form.save()
            return redirect('page:PostDetail', post_instance.slug)
        else:
            print(form.errors)
            print(feature_image_form.errors)
            messages.error(request, "Failed to register, Form is not valid")

    return render(request, "blogs/post_form.html", {'form': form, 'form2':feature_image_form,
                                                    'title': post_instance.title})