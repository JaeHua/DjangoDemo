from django.db import models


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)
    gdp = models.DecimalField(max_digits=10, decimal_places=2)
    gdp_growth = models.DecimalField(max_digits=5, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    inflation_rate = models.DecimalField(max_digits=5, decimal_places=2)
    jobless_rate = models.DecimalField(max_digits=5, decimal_places=2)
    gov_budget = models.DecimalField(max_digits=10, decimal_places=2)
    debt_gdp = models.DecimalField(max_digits=5, decimal_places=2)
    current_account = models.DecimalField(max_digits=10, decimal_places=2)
    population = models.IntegerField()

    def __str__(self):
        return self.name
