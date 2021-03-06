from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AskForm, AnswerForm, UserSignupForm, UserLoginForm
from .models import Question, Answer
# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def detail_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            answer.author = request.user
            answer.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = AnswerForm(initial={"question": question.pk})

    context = {
        "question": question,
        "form": form
        }
    return render(request, "qa/detail.html", context)


def paginate(request, qs):
    try:
        page_number = int(request.GET.get("page", 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, 10)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return page_obj


def new_list(request):
    qs = Question.objects.new()
    page_obj = paginate(request, qs)
    context = {
        "page_obj": page_obj
    }
    return render(request, "qa/list.html", context)


def popular(request):
    qs = Question.objects.popular()
    page_obj = paginate(request, qs)
    context = {
        "page_obj": page_obj
    }
    return render(request, "qa/list.html", context)


def question_add(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            question.author = request.user
            question.save()
            url = question.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    context = {
        "form": form
    }
    return render(request, "qa/ask_question.html", context)


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        form = UserSignupForm()
    context = {
        "form": form,
        "action": "Sign up"
    }
    return render(request, "qa/signup.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()
    context = {
        "form": form,
        "action": "Login"
    }
    return render(request, "qa/signup.html", context)