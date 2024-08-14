from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        'Title', 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Автор'
    )    
    pub_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        unique_together = ['title', 'author']

    def __str__(self):
        return f'{self.author} - {self.title}'
    
