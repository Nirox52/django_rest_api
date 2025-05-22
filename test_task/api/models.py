from django.db import models

class Incident(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активний'),
        ('closed', 'Закритий'),
        ('in_progress', 'В роботі'),
    ]

    # Унікальний ID (автоматично створюється Django)
    title = models.CharField(max_length=200, verbose_name="Назва інциденту")
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        verbose_name="Широта"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Довгота"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Час створення"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Інцидент"
        verbose_name_plural = "Інциденти"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
