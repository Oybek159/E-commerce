from django.contrib import admin

from .models import Category, Item, Conversation, ConversationMessage

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', "is_sold", 'image', 'created_at', 'created_by']

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(ConversationMessage)
admin.site.register(Conversation)

