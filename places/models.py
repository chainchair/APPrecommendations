from django.db import models
from users.models import Interest
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

class Place(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField()
    direccion = models.TextField()  # Aquí va calle, ciudad, país todo junto
    imagen = models.ImageField(upload_to='places/', blank=True, null=True)
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    intereses = models.ManyToManyField(Interest, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre