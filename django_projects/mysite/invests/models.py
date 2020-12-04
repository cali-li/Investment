from django.db import models
from django.core.validators import MinLengthValidator


class Type(models.Model):
    name = models.CharField(
            max_length=200,
            help_text='Enter a type (e.g. BlockChain)',
            validators=[MinLengthValidator(2, "Make must be greater than 1 character")]
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Invest(models.Model):
    nickname = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Invest nickname must be greater than 1 character")]
    )
    invest = models.PositiveIntegerField()
    comments = models.CharField(max_length=300)
    # datetime = forms.DateTimeField(widget=DateTimePicker(),)
    date = models.DateField("Invest Date (mm/dd/yyy)",auto_now_add=False, auto_now=False, blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, null=False,to_field='id', db_column="type-id")

    # Shows up in the admin list
    def __str__(self):
        return self.nickname
