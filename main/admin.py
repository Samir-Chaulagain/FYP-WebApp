from django.contrib import admin
from .models import Dispute, Post

# for blogpost admin
admin.site.register(Post)
admin.site.register(Dispute)
