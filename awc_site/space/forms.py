from django import forms
from django.core.validators import RegexValidator
from space.models import Space, Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


# 공간(space) 생성 폼
class CreateSpaceForm(forms.ModelForm):

    ACCESS_CHOICES = [('public', 'Public'), ('private', 'Private')]
    # 공간 접근 권한
    space_access = forms.ChoiceField(
        label="생성할 공간의 접근 권한을 선택하세요.",
        choices=ACCESS_CHOICES,
        initial='public',
        widget=forms.RadioSelect(),
        required=True,
    )

    # 공간 이름
    space_name = forms.CharField(
        label="생성할 공간의 이름",
        required=True,
        validators=[
            # 공간 이름 검증
            RegexValidator(
                regex=r"^.{4,30}$",
                message="공간 이름은 최소 4글자 이상, 최대 30글자 이하여야 합니다.",
                code='Invalid'),

            RegexValidator(
                regex=r"^[\w가-힣]+$",
                message="특수문자는 _ 만 사용할 수 있습니다.",
                code='Invalid')
        ]
    )
    # 공간 비밀번호
    space_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'create-space-form',
                'placeholder': '공간 비밀번호',
                'required': 'True'
            }
        ),
        label='공간 비밀번호',
        required=True,
        validators=[
            # 공간 패스워드 검증
            RegexValidator(
                regex=r"^.{4,50}$",
                message="공간 비밀번호는 최소 4자리 이상, 최대 50자리 이하여야 합니다.",
                code='Invalid'),
        ],
    )

    # 공간 비밀번호 확인
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'create-space-form',
                'placeholder': '공간 비밀번호 확인',
                'required': 'True'
            }
        ),
        label='Password confirmation'
    )

    # 공간 카테고리
    space_category = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'create-space-form',
                'placeholder': '카테고리를 입력하세요',
            }
        ),
    )

    class Meta:
        model = Space
        fields = ('space_access', 'space_name', 'space_password', 'confirm_password', 'space_category')

    def clean(self):
        # 패스워드 일치 확인
        cleaned_data = super(CreateSpaceForm, self).clean()
        password = cleaned_data.get('space_password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "입력한 비밀번호가 서로 다릅니다."
            )

        # 공간이름 중복 확인
        space_name = cleaned_data.get('space_name')
        if Space.objects.filter(space_name=space_name).exists():
            raise forms.ValidationError(
                "이미 사용중인 공간 이름입니다."
            )


# 게시글 작성 폼
class WritePostForm(forms.ModelForm):
    
    
    class Meta:
        model = Post
        fields = ('post_title', 'post_contents', 'post_file')
        widgets = {
            'post_contents': SummernoteWidget(),
        }

    # is_valid()로 유효성 검증할 때, 파일은 없어도 되게 설정
    def __init__(self, *args, **kwargs):
        super(WritePostForm, self).__init__(*args, **kwargs)
        self.fields['post_file'].required = False

    # save() 재정의
    def save(self, **kwargs):
        post = super(WritePostForm, self).save(commit=False)
        post.space = kwargs.get('space', None)
        post.writer = kwargs.get('writer', None)
        post.malware_result = kwargs.get('check_result', None)
        post.save()

        return post
