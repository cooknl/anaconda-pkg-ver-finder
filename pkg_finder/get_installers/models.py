from django.db import models

# Create your models here.

class Packages(models.Model):
    id = models.IntegerField(primary_key=True)
    pkg_name = models.TextField(blank=True, null=True)
    pkg_url = models.TextField(blank=True, null=True)
    pkg_summary = models.TextField(blank=True, null=True)
    installer_name = models.TextField(blank=True, null=True)
    installer_url = models.TextField(blank=True, null=True)
    anaconda_ver = models.TextField(blank=True, null=True)
    python_ver = models.TextField(blank=True, null=True)
    pkg_ver = models.TextField(blank=True, null=True)
    pkg_included = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return "pgk: " + self.pkg_name + "\t installer: " + self.installer_name

    class Meta:
        managed = True
        db_table = 'packages'