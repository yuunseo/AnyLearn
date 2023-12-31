from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class Script(models.Model):
    class LevelChoices(models.TextChoices):  # 어떻게......AI...?
        LEVEL1 = ("level1", "Level1")
        LEVEL2 = ("level2", "Level2")
        LEVEL3 = ("level3", "Level3")

    title = models.CharField(
        max_length=200,
        primary_key=True,
    )
    hashtag = models.ManyToManyField(Tag)
    contents = models.TextField(null=True)
    level = models.CharField(
        max_length=10,
        choices=LevelChoices.choices,
    )
    learningDate = models.DateField()
    email = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="scripts",
    )
    add_diary = models.IntegerField(
        null=True,
        default=0,
        # 1인 경우, diaries에 script 추가하기
    )
    show_expr = models.IntegerField(
        null=True,
        default=0,
        # 1인 경우, diaries에 script 추가하기
    )
    input_expr = models.TextField(
        null=True,
        default=0,
    )
