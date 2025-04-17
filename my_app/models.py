from django.db import models
# import os

class Member(models.Model):
  name = models.CharField('名前', max_length=20, null=False)
  age = models.PositiveIntegerField('年齢', default=0)
  deleted = models.BooleanField('削除', default=False)
  image = models.ImageField('画像', upload_to="member/", blank=True, null=True)

  def __str__(self):
    return self.name

  # delete関数をオーバーライド
  # def delete(self, *args, **kwargs):
  #     # ファイルが存在すれば削除
  #     if self.image and os.path.isfile(self.image.path):
  #       os.remove(self.image.path)
  #     super().delete(*args, **kwargs)