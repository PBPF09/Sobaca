from django.forms import ModelForm
from discussion.models import DiscussionThread, DiscussionReply

class ThreadForm(ModelForm):
    class meta:
        model = DiscussionThread
        fields = ["title", "content"]
        
class ReplyForm(ModelForm):
    class meta:
        model = DiscussionReply
        fields = ["content"]