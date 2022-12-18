from django.core.paginator import Paginator


def Page(request_, post_list, limit_):
    paginator = Paginator(post_list, limit_)
    page_number = request_.GET.get('page')
    return paginator.get_page(page_number)
