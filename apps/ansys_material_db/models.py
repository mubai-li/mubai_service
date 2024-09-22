import enum

from django.db import models


class MaterialModel(models.Model):
    material_name = models.CharField(max_length=50, verbose_name="材料名")
    electronics_material_property_id = models.OneToOneField(to="ElectronicsMaterialProperty", null=False, blank=False, on_delete=models.CASCADE)
    workbench_material_property_id = ...


class ElectronicsMaterialProperty(models.Model):
    pass


class WorkbenchMaterialProperty(models.Model):
    pass
