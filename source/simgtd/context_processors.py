from simgtd import settings


def admin_urls(request):
    return {'SITE_ROOT': settings.SITE_ROOT}
