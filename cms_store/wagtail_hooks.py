from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.utils.html import format_html


@hooks.register('register_admin_menu_item')
def register_unfold_admin_menu_item():
    return MenuItem(
        'Django Admin',
        reverse('admin:index'),
        icon_name='cog',
        order=1000
    )


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="/static/css/wagtail_custom.css">')


@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    # Customize menu items if needed
    pass