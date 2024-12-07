from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm, CustomUserCreationForm, UserProfileForm
from shop.forms import GoodForm
from shop.models import Good

from django.shortcuts import render, redirect


@login_required
def add_good(request):
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES)
        if form.is_valid():
            good = form.save(commit=False)  # Do not save to the database yet
            good.creator = request.user  # Set the creator to the currently logged-in user
            good.save()  # Now save it
            return redirect('home')  # Redirect to the homepage
    else:
        form = GoodForm()
    return render(request, 'shop/add_good.html', {'form': form})

@login_required
def edit_good(request, good_id):
    good = Good.objects.get(pk=good_id)
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GoodForm(instance=good)
    return render(request, 'shop/edit_good.html', {'form': form, 'good': good})


@login_required
def delete_good(request, good_id):
    try:
        good = Good.objects.get(pk=good_id, creator=request.user)
    except Good.DoesNotExist:
        messages.error(request, "Good not found or you don't have permission to delete it.")
        return redirect('home')

    if request.method == 'POST':
        good.delete()
        messages.success(request, 'Good successfully deleted.')
        return redirect('home')

    return render(request, 'shop/delete_good.html', {'good': good})

def goods_list(request):
    goods = Good.objects.all()
    return render(request, 'shop/oods_list.html', {'goods': goods})

def good_detail(request, pk):
    good = get_object_or_404(Good, pk=pk)
    return render(request, 'shop/good_detail.html', {'good': good})


from django.http import JsonResponse
from PIL import Image
import io
import base64

def save_cropped_image(request):
    if request.method == "POST":
        try:
            # Extract base64 image data from request
            image_data = request.POST.get("cropped_image")
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = base64.b64decode(imgstr)

            # Save the image using PIL
            img = Image.open(io.BytesIO(image_data))
            img = img.convert("RGB")  # Ensure it's in RGB format
            image_path = "media/cropped_image.jpg"
            img.save(image_path)

            return JsonResponse({"message": "Image saved successfully", "image_url": image_path})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

