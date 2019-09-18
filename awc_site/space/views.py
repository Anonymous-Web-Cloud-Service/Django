from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from django.views.generic import ListView
from space.forms import CreateSpaceForm, WritePostForm
from space.models import Space, Post


# 공간 생성
def create_space(request):
    if request.method == 'POST':
        create_space_form = CreateSpaceForm(data=request.POST)

        if create_space_form.is_valid():
            create_space_form.save()
            return render(request, 'space/create_space_done.html',
                          {'space_name': create_space_form['space_name'].value()})

        else:
            print(create_space_form.errors)

    else:
        create_space_form = CreateSpaceForm()
    return render(request, 'space/create_space.html', {'create_space_form': create_space_form})


# 공간 화면 출력
def show_space(request, space_name):

    # 존재하는 space_name 인지 검사
    space = Space.objects.get(space_name=space_name, space_access='public')

    if space:
        # space에 들어있는 게시글 가져오기
        posts = Post.objects.filter(space_id=space.id)

        return render(request, 'space/show_space.html', {'space': space, 'posts': posts})

    return HttpResponse('존재하지 않는 공간입니다.')


# 글쓰기
def write_post(request, space_name):
    if request.method == 'POST':
        form = WritePostForm(request.POST, request.FILES)

        if form.is_valid():
            # 공간의 기본키 가져와서 Post 모델 객체에 지정해주기
            space = Space.objects.get(space_name=space_name)
            form.space = space
            form.save(space=space)

            return HttpResponseRedirect('/space/'+space_name)

    else:
        form = WritePostForm()

    return render(request, 'space/write_post.html', {'form': form})


# 파일 업로드
