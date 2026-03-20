from django.contrib import admin
from django.db.models import F

from bboard.models import Bb, Rubric

# @admin.display(description='Название и рубрика')
# def title_and_rubric(self, rec):
#     return f'{rec.title} ({rec.rubric.name})'

class PriceListFilter(admin.SimpleListFilter):
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Низкая цена'),
            ('medium', 'Средняя цена'),
            ('high', 'Высокая цена'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=500, price__lte=5000)
        elif self.value() == 'high':
            return queryset.filter(price__gt=5000)


@admin.action(description='Уменьшить цену вдвое')
def discount(modeladmin, request, queryset):
    f = F('price')
    for rec in queryset:
        rec.price = f / 2
        rec.save()
    modeladmin.message_user(request, 'Действие выполнено')


@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    list_display = ('title_and_price', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')

    list_editable = ('price', 'rubric')
    # ordering = ['-price']

    search_fields = ('title', 'content')
    search_help_text = 'Поиск по названиям товаров и содержимому'

    # list_filter = ('title', 'rubric__name')
    list_filter = (PriceListFilter,)

    # fields = ('title', 'price', 'content')
    # fields = (('title', 'price'), 'content')
    # exclude = ('rubric', 'kind')
    # fields = ('title', 'content', 'price', 'published')
    # readonly_fields = ('published',)

    # radio_fields = {'rubric': admin.VERTICAL}

    actions = (discount,)

    def get_list_display(self, request):
        ld = ['title', 'content', 'price']
        if request.user.is_superuser:
            ld += ['published', 'rubric']
        return ld

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_hidden=False)

    @admin.display(description='Название и рубрика')
    def title_and_rubric(self, rec):
        return f'{rec.title} ({rec.rubric.name})'

    # title_and_rubric.short_description = 'Название и рубрика'


# @admin.register(Bb, Rubric, Machine, Spare)
# class UniversalAdmin(admin.ModelAdmin):
#     pass


class BbInline(admin.StackedInline):
    model = Bb
    extra = 1
    # can_delete = False


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    inlines = [BbInline]


# admin.site.register(Bb, BbAdmin)
# admin.site.register(Rubric)
