from django.db import models

# Create your models here.
from administration.models import CustomUser


class Messaging(models.Model):
    COMMENT_STATUS = (
        (True, 'published'),
        (False, 'draft'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='message_sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='message_receiver')
    comment = models.TextField(null=True)
    comment_status = models.BooleanField(null=True, choices=COMMENT_STATUS, default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE, )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "Messages"


class ReportUser(models.Model):
    reported_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='blocked_user')
    report_by_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='blocked_by')
    reason_to_report = models.CharField(null=True, max_length=100)
    message = models.TextField(null=True, blank=True)
    is_removed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class PraiseUserChoice(models.Model):
    option = models.CharField(unique=True, max_length=100, null=True)

    def __str__(self):
        return str(self.option)


class PraiseUser(models.Model):
    praised_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='praised_user')
    praise_by_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='praised_by')
    reason_to_praise = models.ManyToManyField('PraiseUserChoice')
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
