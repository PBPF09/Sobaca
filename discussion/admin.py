from django.contrib import admin
from discussion.models import DiscussionThread, DiscussionReply

# Register your models here.
admin.site.register(DiscussionThread)
admin.site.register(DiscussionReply)