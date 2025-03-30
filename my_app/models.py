from django.db import models

class Member(models.Model):
  name = models.CharField('名前', max_length=20, null=False)
  age = models.PositiveIntegerField('年齢', default=0)
  deleted = models.BooleanField('削除', default=False)

  def __str__(self):
    return self.name
