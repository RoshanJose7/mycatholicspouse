from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag(takes_context=True)
def cloudinary_add(context, app, width, height):
    if not app.passport_photo:
        return f"https://res.cloudinary.com/marry-a-catholic/image/upload/w_{str(width)},h_{str(height)},c_fill/v1609162216/images/male_yqzmbk.svg" if app.gender == 'Male' else f"https://res.cloudinary.com/marry-a-catholic/image/upload/w_{str(width)},h_{str(height)},c_fill/v1609162234/images/female_qayib1.svg"
    t = app.passport_photo.url.split("/")
    return "/".join(t[:-2]) + f"/w_{str(width)},h_{str(height)},c_fill/l_icon:watermark,a_45,o_25,w_400,fl_relative.tiled/" + "/".join(t[-1:])

@register.simple_tag(takes_context=True)
def cloudinary_profile(context, app, width, height):
    if not app.passport_photo:
        return f"https://res.cloudinary.com/marry-a-catholic/image/upload/w_{str(width)},h_{str(height)},c_fill/v1609162216/images/male_yqzmbk.svg" if app.gender == 'Male' else f"https://res.cloudinary.com/marry-a-catholic/image/upload/w_{str(width)},h_{str(height)},c_fill/v1609162234/images/female_qayib1.svg"
    t = app.passport_photo.url.split("/")
    return "/".join(t[:-2]) + f"/w_{str(width)},h_{str(height)},c_fill/" + "/".join(t[-1:])

@register.simple_tag(takes_context=True)
def cloudinary_added(context, app_photo):
    if not app_photo:
        return f"https://res.cloudinary.com/marry-a-catholic/image/upload/v1609419100/images/56117400-9a911800-5f85-11e9-878b-3f998609a6c8_pnb08c.jpg" 
    t = app_photo.url.split("/")
    return "/".join(t[:-2]) + f"/l_icon:watermark,a_45,o_25,w_400,fl_relative.tiled/" + "/".join(t[-1:])

@register.simple_tag(takes_context=True)
def profile(context, app):
    if app.passport_photo_1:
        return f'/media/{app.passport_photo_1}'
    else:
        return '/media/male_yqzmbk.svg' if app.gender == 'Male' else '/media/female_qayib1.svg'

@register.simple_tag(takes_context=True)
def carousel(context, img):
    return f'/media/{img}' if img else '/media/56117400-9a911800-5f85-11e9-878b-3f998609a6c8_pnb08c.jpg'

@register.filter(name="split")
@stringfilter
def split(string, key):
    return string.split(key)[0]