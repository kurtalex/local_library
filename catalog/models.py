# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр книги (боевик, триллер, роман и т.д.)")

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр данной книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):

        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор данной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Недоступна'),
        ('o', 'Взаймы'),
        ('a', 'Доступна'),
        ('r', 'Зарезервированная'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Наличие книги')

    class Meta:
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '%s (%s) %s %s' % (self.id, self.book.title, self.status, self.due_back)


class Author(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    midle_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return '%s, %s, %s' % (self.last_name, self.first_name, self.midle_name)
