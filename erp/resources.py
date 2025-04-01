from import_export import resources
from .models import Estimate

class EstimateResource(resources.ModelResource):
    class Meta:
        model = Estimate
        fields = ('id', 'bk_estimate_id', 'customer__name', 'status')
        export_order = fields