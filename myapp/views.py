from functools import wraps

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Study, CustomUser


def login_required_custom(view):
    """Redirect to the login page if nobody is logged in."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view(request, *args, **kwargs)
    return wrapper


def register(request):
    if request.method == "POST":
        uname = (request.POST.get('username') or '').strip()
        pwd = request.POST.get('password') or ''
        confirm = request.POST.get('confirm') or ''

        if not uname or not pwd:
            error = 'Username and password are required.'
        elif len(pwd) < 6:
            error = 'Password must be at least 6 characters.'
        elif pwd != confirm:
            error = 'Passwords do not match.'
        elif CustomUser.objects.filter(username=uname).exists():
            error = 'That username is already taken.'
        else:
            user = CustomUser.objects.create(username=uname, password=make_password(pwd))
            request.session['user_id'] = user.id
            return redirect('home')

        return render(request, 'myapp/register.html', {'error': error, 'username': uname})

    return render(request, 'myapp/register.html')


def login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pwd = request.POST.get('password') or ''

        user = CustomUser.objects.filter(username=uname).first()
        if user:
            if check_password(pwd, user.password):
                request.session['user_id'] = user.id
                return redirect('home')
            # old accounts saved before hashing: accept once, then upgrade to a hash
            if user.password == pwd:
                user.password = make_password(pwd)
                user.save(update_fields=['password'])
                request.session['user_id'] = user.id
                return redirect('home')

        return render(request, 'myapp/login.html', {'error': 'Invalid username or password'})

    return render(request, 'myapp/login.html')


def logout(request):
    request.session.flush()
    return redirect('login')


@login_required_custom
def home(request):
    studies = Study.objects.all().order_by('study_id')

    q = request.GET.get('q', '').strip()
    phase = request.GET.get('phase', '')
    status = request.GET.get('status', '')

    if q:
        studies = studies.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(sponsor_name__icontains=q)
        )
    if phase:
        studies = studies.filter(phase=phase)
    if status:
        studies = studies.filter(status=status)

    return render(request, 'myapp/index.html', {
        'study': studies,
        'phases': Study.PHASE_CHOICES,
        'statuses': [s[0] for s in Study.STATUS_CHOICES],
        'q': q,
        'selected_phase': phase,
        'selected_status': status,
    })


@login_required_custom
def add(request):
    return render(request, 'myapp/add.html')


@login_required_custom
@require_POST
def insert(request):
    stud_id = (request.POST.get('sid') or '').strip()

    if stud_id and Study.objects.filter(study_id=stud_id).exists():
        return render(request, 'myapp/add.html', {
            'error': f'Project id {stud_id} already exists. Use a different id or leave it blank.'
        })

    study = Study(
        name=request.POST.get('sname'),
        description=request.POST.get('sdesc'),
        phase=request.POST.get('sphase'),
        sponsor_name=request.POST.get('spon'),
        status=request.POST.get('sstatus') or 'Planned',
        start_date=request.POST.get('sstart') or None,
        end_date=request.POST.get('send') or None,
    )
    if stud_id:
        study.study_id = stud_id
    study.save()
    return redirect('home')


@login_required_custom
def edit(request, study_id):
    obj = get_object_or_404(Study, study_id=study_id)
    return render(request, 'myapp/edit.html', {'study': obj})


@login_required_custom
@require_POST
def save(request, study_id):
    obj = get_object_or_404(Study, study_id=study_id)
    obj.name = request.POST.get('sname')
    obj.description = request.POST.get('sdesc')
    obj.phase = request.POST.get('sphase')
    obj.sponsor_name = request.POST.get('spon')
    obj.status = request.POST.get('sstatus') or 'Planned'
    obj.start_date = request.POST.get('sstart') or None
    obj.end_date = request.POST.get('send') or None
    obj.save()
    return redirect('home')


@login_required_custom
def detail(request, study_id):
    obj = get_object_or_404(Study, study_id=study_id)
    return render(request, 'myapp/detail.html', {'study': obj})


@login_required_custom
def delete(request, study_id):
    obj = get_object_or_404(Study, study_id=study_id)

    if request.method == "POST":
        obj.delete()
        return redirect('home')

    return render(request, 'myapp/delete.html', {'study': obj})