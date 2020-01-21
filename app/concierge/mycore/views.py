from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic.list import ListView

from django.views.decorators.cache import cache_page

from .models import Tenant

CACHE_TTL = 60 * 3 # 3 minutes

def get_users():
    ukey = 'users_all'
    users = cache.get(ukey)
    if not users:
        users = get_user_model().objects.all()
        cache.set(ukey, users, CACHE_TTL)
    return users

@login_required()
def simple_view(request):
    context = dict(
        title='simple view title',
        text='Lorem ipsum for you honor',
        months='Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(),
        users = get_users(),
    )
    return render(request, 'mycore/simple_view.html', context=context)


@cache_page(CACHE_TTL)
@permission_required('mycore.view_tenant')
def tenant_view(request):
    context = dict(
        title='Tenant list',
        object_list=Tenant.objects.all()
    )
    return render(request, 'mycore/tenant_list.html', context=context)


class TenantListView(ListView):
    model = Tenant
    paginate_by = 100
