import enum

from django.db import models


class MaterialModel(models.Model):
    material_name = models.CharField(max_length=50, verbose_name="材料名")
    # electronics_material_property_id = models.OneToOneField(to="ElectronicsMaterialProperty", null=False, blank=False, on_delete=models.CASCADE)
    workbench_material_property_id = models.OneToOneField(to="WorkbenchMaterialProperty", null=False, blank=False, on_delete=models.CASCADE)


class ElectronicsMaterialProperty(models.Model):
    pass


class ElectronicsMaterialNameOption(models.Model):
    pass


class WorkbenchMaterialProperty(models.Model):
    workbench_material_name = models.CharField(
        max_length=50,
        verbose_name="Workbench材料名字"
    )
    workbench_material_value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Workbench材料值"
    )
    workbench_material_unit = models.OneToOneField(
        to="WorkbenchMaterialUnitOption",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )


class WorkbenchMaterialNameOption(models.Model):
    workbench_type = models.CharField(
        max_length=50,
        verbose_name="Workbench材料名字"
    )
    # 材料库的类型名字
    workbench_classification = models.OneToOneField(
        to="WorkbenchMaterialClassificationOption",
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING
    )
    workbench_units = models.ManyToManyField(
        to="WorkbenchMaterialUnitOption",
        through="WorkbenchMaterialNameAndUnit",
        through_fields=('workbench_material_name_id', 'workbench_material_unit_id'),
        null=False,
        blank=False
    )


class WorkbenchMaterialClassificationOption(models.Model):
    workbench_material_classification_name = models.CharField(
        unique=True,
        null=True,
        blank=True,
        max_length=50,
        verbose_name="Workbench材料类型分类"
    )


class WorkbenchMaterialNameAndUnit(models.Model):
    id = models.AutoField(primary_key=True)
    workbench_material_name_id = models.ForeignKey(
        to="WorkbenchMaterialNameOption",
        on_delete=models.DO_NOTHING
    )
    workbench_material_unit_id = models.ForeignKey(
        to="WorkbenchMaterialUnitOption",
        on_delete=models.DO_NOTHING
    )


class WorkbenchMaterialUnitOption(models.Model):
    workbench_material_unit_name = models.CharField(
        unique=True,
        null=True,
        blank=True,
        max_length=50,
        verbose_name="Workbench材料单位"
    )
