from django import template
from menu.models import MenuItem
from django.template.loader import render_to_string

register = template.Library()


def build_menu_dict(menu_items: list) -> dict:
    """
    Создаёт словарь с элементами меню.

    Параметры:
    menu_items (list): Список элементов меню из БД.

    Возвращает:
    dict: Словарь, представляющий элементы меню с дочерними элементами и флагами is_active / expand.
    """
    menu_dict = {}

    # Создание общего списка всех элементов
    for item in menu_items:
        node = {
            'item': item,
            'children': [],
            'is_active': False,
            'expand': False
        }
        menu_dict[item.id] = node

    # Прикрепляем дочерние элементы к родительским
    for item in menu_items:
        if item.parent_id and item.parent_id in menu_dict:
            parent_node = menu_dict[item.parent_id]
            parent_node['children'].append(menu_dict[item.id])

    return menu_dict


def set_active_and_expand_flags(menu_dict: dict, path: str) -> None:
    """
    Устанавливает флаги is_active / expand для элементов меню (и их родителей) на основе указанного активного пути.

    Параметры:
        menu_dict (dict): Словарь с элементами меню.
        path (str): Путь для проверки флагов.
    """
    for node in menu_dict.values():
        if path == node['item'].get_absolute_url():
            current = node
            while current:
                current['is_active'] = True
                current['expand'] = True
                current = menu_dict.get(current['item'].parent_id)


def filter_menu_items(menu_dict: dict, menu_name: str) -> list:
    """
    Фильтрует список элементов меню по имени, чтобы возвращать только запрашиваемое меню.

    Параметры:
    menu_dict (dict): Словарь с элементами меню.
    menu_name (str): Имя меню для фильтрации.

    Возвращает:
    list: Список элементов меню, отфильтрованный по имени.
    """
    return [node for node in menu_dict.values() if not node['item'].parent and node['item'].title == menu_name]


@register.simple_tag(takes_context=True)
def draw_menu(context: dict, menu_name: str) -> str:
    """
    Отрисовывает меню в виде HTML-шаблона.

    Параметры:
    context (dict): Контекст запроса.
    menu_name (str): Имя меню для отрисовки.

    Возвращает:
    str: HTML-шаблон с отрисованным меню.
    """
    request = context['request']
    menu_items = MenuItem.objects.select_related('parent')

    # Собираем словарь меню
    menu_dict = build_menu_dict(menu_items)

    # Устанавливаем флаги активности и раскрытия
    set_active_and_expand_flags(menu_dict, request.path)

    # Фильтруем, оставляя только запрашиваемое меню
    menu_dict = filter_menu_items(menu_dict, menu_name)

    # Отрисовка меню в виде HTML-шаблона
    return template.loader.render_to_string('menu_template.html', {'menu_items': menu_dict})
