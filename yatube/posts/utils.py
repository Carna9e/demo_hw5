from django.core.paginator import Paginator


def Page(request, post_list, LIMIT):
    paginator = Paginator(post_list, LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
