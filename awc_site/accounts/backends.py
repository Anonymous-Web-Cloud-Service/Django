from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# 이메일로 로그인하기 위한 custom authenticate
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email__exact=username)

        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        else:
            # 패스워드 확인되면, 활성화된 회원만 로그인 가능하게 하기
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return None
