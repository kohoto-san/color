from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from apps.core.models import Profile, GradientPalette, GradientColor, ColorPalette, Color, ImagePalette

import urllib.request
from PIL import Image

import io


def load_home(request):
    gradients = GradientPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    palettes = ColorPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    images = ImagePalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    return render(request, 'homepage.html', {'gradients': gradients, 'palettes': palettes, 'images': images})


def load_gradients(request):
    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
        return load_palettes(request, post_objects, True)
    else:
        return render(request, 'gradients.html')


def load_palettes(request, post_objects, is_featured):

    if not post_objects:
        return HttpResponse('empty')

    # if request.method == 'GET':
    #    if request.is_ajax():

    # profile_id = request.GET.get('profile')
    # is_featured = False

    # Показываем только посты для определённого профиля
    """
    if profile_id:
        post_objects = GradientPalette.objects.filter(is_featured=True, likes=profile_id).order_by('-date')
    else:
        is_featured = True
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
    """

    paginator = Paginator(post_objects, 15)
    page = request.POST.get('page')

    try:
        posts_paginator = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        return HttpResponseBadRequest()

    context = {'object_list': posts_paginator.object_list, 'user': request.user, 'is_featured': is_featured}

    html = render_to_string('items-palette.html', context)
    return HttpResponse(html)


def like(request, palette_id):
    blend = get_object_or_404(GradientPalette, id=palette_id)

    if request.user.is_authenticated() and request.method == 'POST':
        user = request.user.profile
        method = request.POST.get('method')
        if method == 'CREATE':
            blend.likes.add(user)
            # post.upvotes_count += 1
            blend.save()
            return HttpResponse('OK')
        if method == 'DELETE':
            blend.likes.remove(user)
            # post.upvotes_count -= 1
            blend.save()
            return HttpResponse('OK')
    else:
        raise Http404


def blend(request):
    return render(request, 'blend.html')


def blend_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            profile = request.user.profile
            gradient_palette = GradientPalette.objects.create(profile=profile, degrees=90)
        else:
            gradient_palette = GradientPalette.objects.create(degrees=90)

        bgOne = request.POST.get('bgOne')
        grad0 = request.POST.get('grad0')

        bgTwo = request.POST.get('bgTwo')
        grad100 = request.POST.get('grad100')


        GradientColor.objects.create(palette=gradient_palette, color=bgOne, percentages=grad0, priority=0)
        GradientColor.objects.create(palette=gradient_palette, color=bgTwo, percentages=grad100, priority=1)

        return HttpResponse(gradient_palette.id)
    else:
        raise Http404


def featured_blend(request, blend_id):

    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
        return load_palettes(request, post_objects, True)
    else:
        blend = get_object_or_404(GradientPalette, id=blend_id)

        gradients = GradientPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
        palettes = ColorPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
        images = ImagePalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
        context = {'object': blend, 'is_featured': True, 'gradients': gradients, 'palettes': palettes, 'images': images}

        return render(request, 'blend_details.html', context)

        if blend.is_featured:
            return render(request, 'blend_details.html', context)
        else:
            raise Http404


def blend_details(request, blend_id):
    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
        return load_palettes(request, post_objects, True)
    else:
        blend = get_object_or_404(GradientPalette, id=blend_id)

        gradients = GradientPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
        palettes = ColorPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
        images = ImagePalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
        context = {'object': blend, 'is_featured': False, 'gradients': gradients, 'palettes': palettes, 'images': images}

        return render(request, 'blend_details.html', context)


def profile_details(request, id_profile):
    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(profile_id=id_profile).order_by('-date')
        return load_palettes(request, post_objects, False)
    else:
        profile = get_object_or_404(Profile, user_id=id_profile)
        return render(request, 'profile.html', {'profile': profile, 'active': 'gradients'})


def profile_likes(request, id_profile):
    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(likes=id_profile).order_by('-date')
        return load_palettes(request, post_objects, False)
    else:
        profile = get_object_or_404(Profile, user_id=id_profile)
        return render(request, 'profile.html', {'profile': profile, 'active': 'likes'})


def palette(request):
    return render(request, 'palette_create.html')


def palette_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            profile = request.user.profile
            palette = ColorPalette.objects.create(profile=profile)
        else:
            palette = ColorPalette.objects.create()

        colors_list = request.POST.get('colors').split(',')

        for color_str in colors_list:
            color, created = Color.objects.get_or_create(color=color_str)
            palette.colors.add(color)

        palette.save()

        return HttpResponse(palette.id)
    else:
        raise Http404


        # GradientColor.objects.create(palette=gradient_palette, color=bgOne, percentages=grad0, priority=0)
        # GradientColor.objects.create(palette=gradient_palette, color=bgTwo, percentages=grad100, priority=1)


def palette_details(request, palette_id):
    palette = get_object_or_404(ColorPalette, id=palette_id)

    gradients = GradientPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    palettes = ColorPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    images = ImagePalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    context = {'palette': palette, 'is_featured': False, 'gradients': gradients, 'palettes': palettes, 'images': images}

    return render(request, 'palette_details.html', context)


def resize_and_crop(img, size, crop_type='middle'):
    """
    Resize and crop an image to fit the specified size.

    args:
    img_path: path for the image to resize.
    modified_path: path to store the modified image.
    size: `(width, height)` tuple.
    crop_type: can be 'top', 'middle' or 'bottom', depending on this
    value, the image will cropped getting the 'top/left', 'middle' or
    'bottom/right' of the image to fit the size.
    raises:
    Exception: if can not open the file in img_path of there is problems
    to save the image.
    ValueError: if an invalid `crop_type` is provided.
    """
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
                         Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                   int(round((img.size[1] + size[1]) / 2)))
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
                         Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = (int(round((img.size[0] - size[0]) / 2)), 0,
                   int(round((img.size[0] + size[0]) / 2)), img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    else:
        img = img.resize((size[0], size[1]),
                         Image.ANTIALIAS)
    # If the scale is the same, we do not need to crop
    return img


def resize_without_crop(img, size, crop_type='middle'):

    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    # The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
                         Image.ANTIALIAS)
    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
                         Image.ANTIALIAS)
    else:
        img = img.resize((size[0], size[1]),
                         Image.ANTIALIAS)
    # If the scale is the same, we do not need to crop
    return img


def resize(img, box, fit=False):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
    @param out: file-like-object - save the image into the output stream
    '''
    # preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0]/factor > 2*box[0] and img.size[1]*2/factor > 2*box[1]:
        factor *= 2
    if factor > 1:
        img.thumbnail((img.size[0]/factor, img.size[1]/factor), Image.NEAREST)

    # calculate the cropping box and get the cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2/box[0]
        hRatio = 1.0 * y2/box[1]
        if hRatio > wRatio:
            y1 = int(y2/2-box[1]*wRatio/2)
            y2 = int(y2/2+box[1]*wRatio/2)
        else:
            x1 = int(x2/2-box[0]*hRatio/2)
            x2 = int(x2/2+box[0]*hRatio/2)
        img = img.crop((x1, y1, x2, y2))

    # Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)
    return img
# resize


def image_load(request):

    if request.method == 'POST':

        image_url = request.POST.get('image_url')

        pos_img_format = image_url.rfind('.')
        img_format = image_url[pos_img_format:]

        img_temp = NamedTemporaryFile(delete=True)
        try:
            img_temp.write(urllib.request.urlopen(image_url).read())
        except ValueError:
            return HttpResponseBadRequest()
        img_temp.flush()

        # new_image = Image.open(img_temp).resize((470, 245))
        # new_image = resize_and_crop(Image.open(img_temp), (570, 345))
        new_image = resize(Image.open(img_temp), (380, 480))

        if img_format == ".jpg":
            img_format = ".JPEG"

        image_io = io.BytesIO()
        new_image.save(image_io, format=img_format[1:])
        image_file = ContentFile(image_io.getvalue())

        if request.user.is_authenticated():
            profile = request.user.profile
            image_palette = ImagePalette.objects.create(profile=profile)
        else:
            image_palette = ImagePalette.objects.create()

        image_palette.original_url = image_url
        image_palette.save()

        image_palette.image.save(image_url, image_file, save=True)
        # File(img_temp)

        meta_img = Image.open(image_palette.image)
        meta_img = meta_img.resize((50, 50))

        result = meta_img.convert('P', palette=Image.ADAPTIVE, colors=5)
        result.putalpha(0)

        colors = result.getcolors(50*50)

        for count, color_rgb in colors:
            color_hex = '%02x%02x%02x' % (color_rgb[0], color_rgb[1], color_rgb[2])
            color, created = Color.objects.get_or_create(color=color_hex)
            image_palette.colors.add(color)

        return HttpResponse(image_palette.id)
    else:
        raise Http404


def image_details(request, image_id):
    image = get_object_or_404(ImagePalette, id=image_id)

    gradients = GradientPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    palettes = ColorPalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    images = ImagePalette.objects.filter(is_featured=True).order_by('-date_featured')[:10]
    context = {'image': image, 'is_featured': False, 'gradients': gradients, 'palettes': palettes, 'images': images}

    return render(request, 'image_details.html', context)


def image(request):
    return render(request, 'image_create.html')


def images_list(request):

    if request.method == 'POST' and request.is_ajax():

        post_objects = ImagePalette.objects.filter(is_featured=True).order_by('-date')

        if not post_objects:
            return HttpResponse('empty')

        paginator = Paginator(post_objects, 15)
        page = request.POST.get('page')

        try:
            posts_paginator = paginator.page(page)
        except PageNotAnInteger:
            return HttpResponseBadRequest()
        except EmptyPage:
            return HttpResponseBadRequest()

        context = {'object_list': posts_paginator.object_list, 'user': request.user, 'is_featured': False}

        html = render_to_string('image-item.html', context)
        return HttpResponse(html)
    else:
        return render(request, 'images-list.html')
