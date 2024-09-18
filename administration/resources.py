from import_export import resources
from .models import UserCSVImportedData

class UserCSVImportedDataResource(resources.ModelResource):
    class Meta:
        model = UserCSVImportedData