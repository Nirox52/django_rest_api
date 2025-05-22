# from django.contrib.gis.db import models
#
# class Incident(models.Model):
#     STATUS_CHOICES = [
#         ('active', 'Активний'),
#         ('closed', 'Закритий'),
#         ('in_progress', 'В роботі'),
#     ]
#
#     title = models.CharField(max_length=200)
#     # location = models.PointField(geography=True, srid=4326)  # Точка на карті
#     location = models.PointField(
#       geography=True,
#       srid=4326,
#       null=True,
#       blank=True,
#       default=None,
#       verbose_name="Координаты"
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
#
#     objects = models.Manager()  # Стандартний менеджер
#     geo_objects = models.Manager()  # Менеджер для геоданих
#
#     class Meta:
#         verbose_name = "Інцидент"
#         verbose_name_plural = "Інциденти"
#         ordering = ['-created_at']
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_location(value):
    """Валидатор для проверки корректности координат"""
    if not isinstance(value, Point):
        raise ValidationError(_('Локация должна быть типом Point'))
    
    longitude, latitude = value.x, value.y
    
    if not (-180 <= longitude <= 180):
        raise ValidationError(_('Долгота должна быть между -180 и 180'))
    
    if not (-90 <= latitude <= 90):
        raise ValidationError(_('Широта должна быть между -90 и 90'))

def default_location():
    """Возвращает точку с координатами по умолчанию (Киев)"""
    return Point(30.523333, 50.450001, srid=4326)

class Incident(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Активний')
        IN_PROGRESS = 'in_progress', _('В роботі')
        CLOSED = 'closed', _('Закритий')
    
    # Основные поля
    title = models.CharField(
        max_length=200,
        verbose_name=_('Назва інциденту'),
        help_text=_('Короткий опис інциденту')
    )
    
    location = models.PointField(
        verbose_name=_('Координати'),
        geography=True,
        srid=4326,
        default=default_location,
        validators=[validate_location],
        help_text=_('Точка на карті у форматі GeoJSON (longitude, latitude)')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Час створення')
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_('Статус')
    )
    
    # Менеджеры
    objects = models.Manager()
    
    class Meta:
        verbose_name = _('Інцидент')
        verbose_name_plural = _('Інциденти')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def clean(self):
        """Дополнительная валидация модели"""
        super().clean()
        validate_location(self.location)
    
    @property
    def latitude(self):
        """Возвращает широту (для удобства)"""
        return self.location.y
    
    @property
    def longitude(self):
        """Возвращает долготу (для удобства)"""
        return self.location.x
