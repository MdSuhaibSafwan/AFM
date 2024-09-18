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



class ChatRoomManager(models.Manager):

    def get_or_create_room(self, user1, user2):
        if type(user1) == type(""):
            user1 = User.objects.get(id=user1)

        if type(user2) == type(""):
            user2 = User.objects.get(id=user2)

        if user1 == user2:
            raise ValueError("Users cannot create room between itself.")

        qs = self.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
        if not qs.exists():
            obj = self.create(user1=user1, user2=user2)
            return obj

        return qs.get()

    def get_user_rooms(self, user: CustomUser):
        assert isinstance(user, CustomUser)
        qs = self.filter(Q(user1=user) | Q(user2=user))
        return qs


class ChatRoom(models.Model):
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user1_rooms")
    
    user2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user2_rooms")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = ChatRoomManager()

    class Meta:
        ordering = ["-modified", ]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        user1 = self.user1
        user2 = self.user2

        if user1 == user2:
            raise ValueError("User cannot create between themselves")

        return super().save(*args, **kwargs)


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.SET_NULL, null=True, related_name="messages")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    message = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE, )
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created", ]

    def __str__(self):
        return f"msg-{self.id}"

    def get_time_in_words(self):
        now = timezone.now()
        if now.date() == self.created.date():
            pass
        
        time_delta = now - self.created
        if time_delta.days == 0:
            minutes = (time_delta.seconds // 60)
            
            if minutes == 0:
                return "now"

            if minutes > 60:
                hour = (minutes//60)
                return f"{hour} hour ago"
            
            return f"{minutes} mins ago"
        
        return f"{time_delta.days} days ago"


class ChatMessageFile(models.Model):
    message = models.ForeignKey(
        ChatMessage, on_delete=models.SET_NULL, null=True, related_name="files")
    file = models.CharField(max_length=20400, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    

class UserOnlineStatus(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="online_status")
    online = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        onlineMsg = "online" if self.online else "offline"
        return f"{self.user} {onlineMsg}"


