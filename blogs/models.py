from django.db import models

# Create your models here.
from django.utils.text import slugify

from administration.models import Mentor
from ckeditor.fields import RichTextField
from AFM.validators import validate_file_size


STATUS = (
    (0, "Draft"),
    (1, "Submit for Review"),
    (2, "Publish"),
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    sub_title = models.CharField(max_length=120, null=True)
    # summary = models.CharField(max_length=120, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True)
    author = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='blog_posts', null=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    feature_image = models.ImageField(upload_to='blog_feature_image/', null=True, validators=[validate_file_size])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(null=True, default=False)
    publish = models.BooleanField(null=True, default=False)
    post_status = models.IntegerField(null=True, choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'post_image'
        verbose_name_plural = 'post_images'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/medical-school-application/{self.slug}/"

        

