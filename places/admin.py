from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from users.models import Interest
from .models import Place, Category

admin.site.register(Category)

class PlaceResource(resources.ModelResource):
    intereses = fields.Field(
        column_name='intereses',
        attribute='intereses',
        widget=ManyToManyWidget(model=Interest, field='name', separator=',') # type: ignore
    )
    categoria = fields.Field(
        column_name='categoria',
        attribute='categoria',
        widget=ForeignKeyWidget(model=Category, field='name')# type: ignore
    )
    
    class Meta:
        model = Place       
        delimiter = ';'
        fields = ('id', 'nombre','categoria','descripcion', 'direccion','intereses')
        export_order = fields
        import_id_fields = ['id']

@admin.register(Place)
class PlaceAdmin(ImportExportModelAdmin):
    resource_class = PlaceResource
    exclude = ('slug',)