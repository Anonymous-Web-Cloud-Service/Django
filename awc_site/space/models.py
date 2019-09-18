from django.db import models
from django.utils import timezone


# 공간 모델
class Space(models.Model):
    space_access = models.CharField(  # 공간 접근 권한
        max_length=10,
        blank=False,
    )
    space_name = models.CharField(    # 공간 이름
        max_length=35,
        blank=False,
    )
    space_password = models.CharField(  # 공간 비밀번호
        max_length=256,
        blank=False
    )
    space_category = models.CharField(  # 공간 비밀번호
        max_length=256,
        blank=True
    )
    date_created = models.DateTimeField(  # 공간 생성 날짜
        default=timezone.now
    )


# 게시글 모델
class Post(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=False)   # 공간의 기본키를 외래키로 설정
    writer = models.CharField(max_length=50)
    post_title = models.CharField(max_length=50)
    post_contents = models.TextField(blank=True)
    post_file = models.FileField(blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    # post_attached_file = models.FileField

    class Meta:
        ordering = ['-post_date']