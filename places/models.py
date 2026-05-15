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
    descripcion = models.TextField(max_length=600)
    direccion = models.TextField(max_length=200)  # Aquí va calle, ciudad, país todo junto
    imagen = models.ImageField(upload_to='places/', blank=True, null=True)
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    intereses = models.ManyToManyField(Interest, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1

            while Place.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre