from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ImageFeed
from .mechanics import process_image
from .forms import ImageFeedForm


def images_home(request):
    content = {
        "title": "домашняя страница",
    }
    return render(request, 'images/home.html', content)


@login_required
def dashboard(request):
    # Получаем все изображения из базы данных
    image_feeds = ImageFeed.objects.filter(user=request.user)  # Фильтр по пользователю
    return render(request, 'images/dashboard.html', {'image_feeds': image_feeds})


@login_required
def process_image_feed(request, feed_id):
    image_feed = get_object_or_404(ImageFeed, id=feed_id, user=request.user)
    process_image(feed_id)
    return redirect('dashboard')


@login_required
def add_image_feed(request):
    if request.method == 'POST':
        form = ImageFeedForm(request.POST, request.FILES)
        if form.is_valid():
            image_feed = form.save(commit=False)
            image_feed.user = request.user
            image_feed.save()
            return redirect('dashboard')
    else:
        form = ImageFeedForm()
    return render(request, 'images/add_image_feed.html', {'form': form})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImageFeed, id=image_id,
                              user=request.user)  # Гарантируя, что только владелец может удалить
    image.delete()
    return redirect('dashboard')
