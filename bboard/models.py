from django.db import models


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('name',)


class Bb(models.Model):
    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    # KINDS = (
    #     ('Купля-продажа', (
    #         ('b', 'Куплю'),
    #         ('s', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     )),
    # )

    KINDS = (
        (None, 'Выберите тип публикуемого объявления'),
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
        verbose_name='Тип объявления',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Цена',
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']