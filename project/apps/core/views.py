from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import render_to_string

from apps.core.models import Profile, GradientPalette, GradientColor


def load_home(request):

    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
        return load_palettes(request, post_objects, True)
    else:
        return render(request, 'homepage.html')


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


def featured_blend(request, blend_id):

    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
        return load_palettes(request, post_objects, True)
    else:
        blend = get_object_or_404(GradientPalette, id=blend_id)

        if blend.is_featured:
            return render(request, 'blend_details.html', {'object': blend, 'is_featured': True})
        else:
            raise Http404


def blend_details(request, blend_id):
    if request.method == 'POST' and request.is_ajax():
        post_objects = GradientPalette.objects.filter(is_featured=True).order_by('-date')
        return load_palettes(request, post_objects, True)
    else:
        blend = get_object_or_404(GradientPalette, id=blend_id)
        return render(request, 'blend_details.html', {'object': blend, 'is_featured': False})


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
