from django.db import models
# Create your models here.
from django.utils.text import slugify

from AFM.validators import validate_file_size
from administration.models import CustomUser
from ckeditor.fields import RichTextField

STATUS = (
    (0, "Draft"),
    (1, "Publish"),
)


class Page(models.Model):
    title = models.CharField(max_length=200, unique=True)
    sub_title = RichTextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='page_author', null=True)
    content = RichTextField()
    feature_image = models.ImageField(upload_to='page_feature_image/', null=True, blank=True, validators=[validate_file_size])
    parent = models.ForeignKey('self', null=True, blank=True, related_name='parent_page', on_delete=models.CASCADE, )
    post_status = models.IntegerField(null=True, choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return f"/{self.slug}/"



