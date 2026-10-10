from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Ad, AdImage, AdLike, AdFavorite
from .forms import AdForm, AdImageForm


def ad_list(request):
    q = request.GET.get("q", "").strip()
    ads = Ad.objects.filter(is_hidden=False).order_by("-created_at")
    if q:
        ads = ads.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q)
        )
    return render(request, "ads/ad_list.html", {"ads": ads, "q": q})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    likes_count = ad.likes.filter(vote='like').count()
    dislikes_count = ad.likes.filter(vote='dislike').count()
    is_favorited = False
    user_vote = None
    if request.user.is_authenticated:
        is_favorited = ad.favorites.filter(user=request.user).exists()
        user_like = ad.likes.filter(user=request.user).first()
        user_vote = user_like.vote if user_like else None
    return render(request, "ads/ad_detail.html", {
        "ad": ad,
        "likes_count": likes_count,
        "dislikes_count": dislikes_count,
        "is_favorited": is_favorited,
        "user_vote": user_vote,
    })


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        image_form = AdImageForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            # spremi sve uploadane slike
            for image in request.FILES.getlist('image'):
                AdImage.objects.create(ad=ad, image=image)
            messages.success(request, 'Oglas je objavljen!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
        image_form = AdImageForm()
    return render(request, 'ads/ad_create.html', {'form': form, 'image_form': image_form})


@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.owner != request.user:
        messages.error(request, 'Nemate pravo uređivati ovaj oglas.')
        return redirect('ad_detail', pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            for image in request.FILES.getlist('image'):
                AdImage.objects.create(ad=ad, image=image)
            messages.success(request, 'Oglas je ažuriran!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_update.html', {'form': form, 'ad': ad})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.owner != request.user:
        messages.error(request, 'Nemate pravo brisati ovaj oglas.')
        return redirect('ad_detail', pk=pk)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Oglas je obrisan.')
        return redirect('ad_list')
    return render(request, 'ads/ad_delete.html', {'ad': ad})


@login_required
def ad_vote(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    vote_type = request.POST.get('vote')  # 'like' ili 'dislike'

    if vote_type not in ('like', 'dislike'):
        return redirect('ad_detail', pk=pk)

    existing = AdLike.objects.filter(ad=ad, user=request.user).first()

    if existing:
        if existing.vote == vote_type:
            # klikne isti gumb → ukloni glas
            existing.delete()
        else:
            # klikne suprotni gumb → promijeni glas
            existing.vote = vote_type
            existing.save()
    else:
        AdLike.objects.create(ad=ad, user=request.user, vote=vote_type)

    return redirect('ad_detail', pk=pk)


@login_required
def ad_favorite(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    favorite = AdFavorite.objects.filter(ad=ad, user=request.user).first()

    if favorite:
        favorite.delete()
        messages.info(request, 'Uklonjeno iz omiljenih.')
    else:
        AdFavorite.objects.create(ad=ad, user=request.user)
        messages.success(request, 'Dodano u omiljene!')

    return redirect('ad_detail', pk=pk)


@login_required
def favorite_list(request):
    favorites = AdFavorite.objects.filter(user=request.user).select_related('ad')
    return render(request, 'ads/favorite_list.html', {'favorites': favorites})

