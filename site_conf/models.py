from django.db import models
from django.core.cache import cache

class SiteConfig(models.Model):
    is_active = models.BooleanField("Активен", default=False)
    title = models.CharField("Название пресета", max_length=50, help_text="Напр: Основной или Праздничный")
    description = models.TextField("Описание пресета", blank=True, null=True)

    # Твои настройки
    site_name = models.CharField(max_length=100, default="DailyDo")
    nav_color = models.CharField(max_length=7, default="#ffffff")
    maintenance_mode = models.BooleanField(default=False)
    can_signup = models.BooleanField(default=True, null=False, blank=False, help_text="Разрешить регистрацию")

    def save(self, *args, **kwargs):
        if self.is_active:
            # Если этот конфиг активен, выключаем is_active у всех остальных
            SiteConfig.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
            # Очищаем кэш при изменении активного конфига
            cache.delete('site_config_current')
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        """Метод для получения текущего активного конфига с кэшированием"""
        cache_key = 'site_config_current'
        active_config = cache.get(cache_key)

        if active_config is None:
            active_config = cls.objects.filter(is_active=True).first()
            if not active_config:
                # Если активного нет, берем самый первый или создаем дефолт
                active_config = cls.objects.first()
            # Кэшируем на 5 минут
            cache.set(cache_key, active_config, 300)

        return active_config

    def __str__(self):
        return f"{'[+]' if self.is_active else '[-]'} {self.title} {self.description[:min(len(self.description), 10)]}"
