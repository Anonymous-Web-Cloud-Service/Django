from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.views.generic import ListView
from space.forms import CreateSpaceForm, WritePostForm
from space.models import Space, Post
import time, os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 공간 리스트
def space_list(request):
    # 퍼블릭 공간만 모두 가져오기
    spaces = Space.objects.filter(space_access='public')
    post_count = 5
    page = request.GET.get('page')
    paginator = Paginator(spaces, post_count)
    page_count = range(1, paginator.num_pages + 1)  # 이전 1 2 3 4 다음
    try:
        spaces = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        spaces = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        spaces = paginator.page(paginator.num_pages)
    return render(request, 'space/space_list.html', {'spaces': spaces, 'page_count': page_count})


# 검색조건에 부합하는 공간 리스트
def search_space_list(request):
    search_flag = True
    # q값이 없으면 get()의 두번째 인자가 q에 할당된다.
    q = request.GET.get('q', '')

    # 검색 옵션 설정
    search_option = request.GET.get('search_option')
    option = search_option + '__contains'
    # 검색하기
    space = Space.objects.filter(space_access='public')
    post_count = 10
    paginator = Paginator(space, post_count)
    page_count = range(1, paginator.num_pages + 1)  # 이전 1 2 3 4 다음
    if q:
        spaces = Space.objects.filter(**{option: request.GET.get('q')}).order_by('-date_created')

    return render(request, 'space/space_list.html',
                  {'spaces': spaces, 'q': q, 'search_flag': search_flag, 'page_count': page_count})


# 공간 생성
def create_space(request):
    if request.method == 'POST':
        create_space_form = CreateSpaceForm(data=request.POST)

        if create_space_form.is_valid():
            create_space_form.save()
            time.sleep(1)  # s3에 공간이름으로 폴더를 생성하기 위한 시간을 주기 위해, render 전에 1초 대기함.
            return render(request, 'space/create_space_done.html',
                          {'space_name': create_space_form['space_name'].value()})

        else:
            print(create_space_form.errors)

    else:
        create_space_form = CreateSpaceForm()

    return render(request, 'space/create_space.html', {'create_space_form': create_space_form})


'''
# 공간 화면 출력
def show_space(request, space_name):

    # 존재하는 space_name 인지 검사
    space = Space.objects.get(space_name=space_name, space_access='public')

    if space:
        # space에 들어있는 게시글 가져오기
        posts = Post.objects.filter(space_id=space.id)

        return render(request, 'space/show_space.html', {'space': space, 'posts': posts})

    return HttpResponse('존재하지 않는 공간입니다.')
'''
# 공간 화면 출력 + #pagination code
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def show_space(request, space_name):
    # 존재하는 space_name 인지 검사
    space = Space.objects.get(space_name=space_name, space_access='public')
    if space:
        # space에 들어있는 게시글 가져오기
        post_count = 5  # Show 5 contacts per page
        posts = Post.objects.filter(space_id=space.id)
        page = request.GET.get('page')
        paginator = Paginator(posts, post_count)
        page_count = range(1, paginator.num_pages + 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)
            a = []
        # for i in posts.paginator.num_pages:
        #    a.append(i)

        return render(request, 'space/show_space.html', {'space': space, 'posts': posts, 'page_count': page_count})

    return HttpResponse('존재하지 않는 공간입니다.')


from space import malware_manager
from space import graph


# 글쓰기
def write_post(request, space_name):
    if request.method == 'POST':
        form = WritePostForm(request.POST, request.FILES)

        if form.is_valid():

            # s3에 파일이 업로드 되기까지 기다리기 위해 sleep()을 사용함.
            # code smell이 매우 역하지만, 해결하기 위해 투자할 시간과 기술이 현재로써는 없다.
            time.sleep(2.5)
            check_result = -1
            if form.cleaned_data['post_file'] is not None:
                file_name = form.cleaned_data['post_file'].name
                file_path = os.path.abspath(os.path.join('awc_site/MCDM_code/S3Control_Python/' + file_name, os.pardir))
                print('---file_path : ', file_path)
                with graph.as_default():
                    # 멀웨어 검사 (멀웨어면 1, 아니면 0 반환)
                    check_result = malware_manager.malware_check_s3(space_name, file_name)

            # 공간의 기본키 가져와서 Post 모델 객체에 지정해주기
            space = Space.objects.get(space_name=space_name)
            form.space = space
            # 작성자 닉네임 가져오기
            writer = request.user.nickname
            # DB에 저장
            form.save(space=space, writer=writer, check_result=check_result)

            return HttpResponseRedirect('/space/' + space_name)

    else:
        form = WritePostForm()

    return render(request, 'space/write_post.html', {'form': form, 'space_name': space_name})


# 게시글 보기
def post_detail(request, space_name, post_id):
    # 없는 포스트라면 404페이지로 넘겨준다.
    space = Space.objects.get(space_name=space_name)
    post = get_object_or_404(Post, space_id=space.id, id=post_id)
    return render(request, 'space/post_detail.html', {'post': post, 'space': space})


def search_name(request):
    return render(request, 'space/search_name.html')


def information(request):
    return render(request, 'space/information.html')
