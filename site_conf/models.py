from django.db import models

class SiteConfig(models.Model):
    is_active = models.BooleanField("Активен", default=False)
    title = models.CharField("Название пресета", max_length=50, help_text="Напр: Основной или Праздничный")
    description = models.TextField("Описание пресета", blank=True, null=True)
    
    # Твои настройки
    site_name = models.CharField(max_length=100, default="DailyDo")
    nav_color = models.CharField(max_length=7, default="#ffffff")
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурации"

    def save(self, *args, **kwargs):
        if self.is_active:
            # Если этот конфиг активен, выключаем is_active у всех остальных
            SiteConfig.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        """Метод для получения текущего активного конфига"""
        active_config = cls.objects.filter(is_active=True).first()
        if not active_config:
            # Если активного нет, берем самый первый или создаем дефолт
            active_config = cls.objects.first()
        return active_config

    def __str__(self):
        return f"{'🟢' if self.is_active else '🔴'} {self.title} {self.description[:min(len(self.description), 10)]}"