from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from django.views.generic import DetailView, UpdateView, CreateView
from django.views import generic
from AFM.settings import EMAIL_HOST_USER
from administration.login_check import super_admin_user_required, mentor_user_required, institute_user_required
from administration.models import Mentor
from notifications.signals import notify
from .filters import BlogFilter
from .forms import create_post_form, CreatPostForm, UpdateFeatureImageForm, EditPostForm
from .models import Post
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from personal_information.models import MentorPersonalInformation
from AFM.tasks import send_email_notification
from django.contrib.auth.decorators import login_required



def add_title_slug(request):
    posts = Post.objects.all()
    for post in posts:
        post.slug = slugify(post.title)
        post.save()
        messages.success(request, "All slugs are successfully updated")
    return redirect('administration:home')

@mentor_user_required
def PostList(request):
    pi_user = MentorPersonalInformation.objects.using(
        'afm_personal_information').get(admin__user_slug=request.user.slug)
    if not pi_user.consent4:
        return redirect('administration:upload_public_information_twfl')
    queryset = Post.objects.filter(author=request.user.mentor).order_by('-created_on')
    print(queryset)
    return render(request, "blogs/list_blogs.html", {'post_list': queryset})


@institute_user_required
def PostListAdmin(request):
    queryset = Post.objects.filter(post_status__in=[1, 2])
    filtered_qs = BlogFilter(request.GET, queryset)

    paginated_filtered = Paginator(filtered_qs.qs, 50)

    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'blogs/list_blogs_admin.html',
                  {'post_list': page_obj, 'form': filtered_qs.form,
                   'page_obj': page_obj})


# def PostDetail(request, post_id):
#     post = Post.objects.get(id=post_id)
#     return render(request, "blogs/post_detail.html", {'post': post})

@mentor_user_required
def PostDelete(request, post_id):
    post = Post.objects.get(id=post_id, author=request.user.mentor)
    post.delete()
    return redirect("blogs:blogs_list")


@mentor_user_required
def create_post_twfl(request):
    if request.method != "POST":
        post_form = create_post_form
        feature_image_form = UpdateFeatureImageForm
    else:
        post_form = create_post_form(request.POST)
        feature_image_form = UpdateFeatureImageForm(request.POST, request.FILES)
        if post_form.is_valid() and feature_image_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.author = request.user.mentor
            post_instance.save()
            feature_image_form = UpdateFeatureImageForm(request.POST, request.FILES, instance=post_instance)
            feature_image_form.save()

            messages.success(request, "Your blog have been submitted, we will show it when it gets approval. ")
            return redirect("blogs:blogs_list")
        else:
            print(feature_image_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "blogs/post_form.html", {'form': post_form, 'form2':feature_image_form,
                                                    'title': 'Create Blog'})


@mentor_user_required
def edit_post(request, pk, user_slug):
    if request.user.user_type in [0,1]:
        user_mentor = Mentor.objects.get(admin__slug=user_slug)
        post_instance = get_object_or_404(Post, pk=pk, author=user_mentor)
        form = EditPostForm(instance=post_instance)

    else:
        user_mentor = Mentor.objects.get(admin=request.user)
        post_instance = get_object_or_404(Post, pk=pk, author=user_mentor)
        form = CreatPostForm(instance=post_instance)

    feature_image_form = UpdateFeatureImageForm(instance=post_instance)
    if request.method == "POST":
        if request.user.user_type in [0, 1]:
            form = EditPostForm(request.POST, request.FILES, instance=post_instance)
        else:
            form = CreatPostForm(request.POST, request.FILES, instance=post_instance)

        feature_image_form = UpdateFeatureImageForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid() and feature_image_form.is_valid():
            form.save()
            feature_image_form.save()
            return redirect('blogs:PostDetail', post_instance.slug)
        else:
            print(form.errors)
            print(feature_image_form.errors)
            messages.error(request, "Failed to register, Form is not valid")

    return render(request, "blogs/post_form.html", {'form': form, 'form2':feature_image_form,
                                                    'title': post_instance.title})

@login_required
def change_status_is_active_twfl(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.status:
        post.status = False
    else:
        post.status = True
    post.save()
    return redirect('blogs:blogs_list')


@super_admin_user_required
def change_status_publish_twfl(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.post_status == 1:
        post.post_status = 2
    else:
        post.post_status = 1
    post.save()
    # if post.publish:
    user_mentor = Mentor.objects.get(admin=post.author.admin)
    students = user_mentor.student_set.all()
    parents = user_mentor.parent_set.all()
    url_name = '#'
    verb = 'New Blog is created by your mentor %s' % user_mentor.admin.first_name
    link = 'medical-school-application/%s/' % post.slug
    if students:
        for person in students:
            notify.send(post,
                        recipient=person.admin,
                        description=url_name,
                        target=person.admin,
                        level='info',
                        verb=verb)
    if parents:
        for person in parents:
            notify.send(post,
                        recipient=person.admin,
                        description=url_name,
                        target=person.admin,
                        level='info',
                        verb=verb)

    notify.send(post,
                recipient=user_mentor.admin,
                description=url_name,
                target=user_mentor.admin,
                level='success',
                verb='Congratulations !! Your Blog is Published')

    send_email_notification.delay('New Blog Published on ApplyPal',
                                  'administration/email/standard_template.html', [EMAIL_HOST_USER],
                                  {
                                      'first_name': 'Team',
                                      'link': link,
                                      'content': 'New Blog Published on ApplyPal. Please '
                                                 'Index this Blog URL.',
                                      'button_text': 'View Blog',
                                  }
                                  )
    # Sent mail to subscribers
    return redirect('blogs:PostListAdmin')


# class PostDetail(DetailView):
#     model = Post
#     user_mentor_pi = Mentor_PI.objects.using('afm_personal_information').get(
#         admin__user_slug=user_mentor.admin.slug)

def PostDetail(request, slug):
    # add the dictionary during initialization
    object = Post.objects.get(slug=slug)
    if object.post_status != 2 and not request.user.is_authenticated:
        return render(request, '404.html')
    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=object.author.admin.slug, currently_studying=6)
    user_mentor = Mentor.objects.get(
        admin__slug=object.author.admin.slug)
    return render(request, "blogs/post_detail.html",
                  {'object': object, 'user_mentor': user_mentor, 'user_mentor_pi': user_mentor_pi})



def public_blog_list(request):
    mentors_not_from_afu = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        currently_studying__in=[6, 7]).values_list('admin__user_slug')
    temp = []
    for slug in mentors_not_from_afu:
        temp.append(slug[0])
    queryset = Post.objects.filter(post_status=2, author__admin__slug__in=temp)[:10]
    filtered_qs = BlogFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 50)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'blogs/public_list_blog.html',
                  {'post_list': page_obj, 'page_obj': page_obj})