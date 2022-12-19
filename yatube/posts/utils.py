from django.core.paginator import Paginator


def page(request, post_list, limit):
    paginator = Paginator(post_list, limit)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
