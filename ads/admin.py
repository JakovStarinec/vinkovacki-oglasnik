from django.contrib import admin
from .models import Ad, AdImage, AdLike, AdFavorite

# Register your models here.

class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "price", "location", "created_at")
    search_fields = ("title", "description", "location", "owner__username")
    list_filter = ("location", "created_at")
    inlines = [AdImageInline]


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ("id", "ad", "uploaded_at")

@admin.register(AdLike)
class AdLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "ad", "user", "vote")

@admin.register(AdFavorite)
class AdFavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "ad", "user")