from django.shortcuts import redirect, render
from .models import Member
from .forms import AddMemberForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
  header = ['ID', '名前', '年齢']
  members = Member.objects.filter(deleted=False).all()
  data = {
    'members' : members,
    'header' : header,
  }
  return render(request, 'my_app/index.html', data)

@login_required
def create(request):
  if (request.method == 'POST'):
    form = AddMemberForm(request.POST)
    data = {
      'title' : '入力ページ',
      'form' : form,
    }
    if form.is_valid():
      form.save()
      return redirect(to='/my_app/index')
  else:
    data = {
      'title' : '入力ページ',
      'form' : AddMemberForm(),
    }
  return render(request, 'my_app/create.html', data)

@login_required
def update(request, num):
  member_obj = Member.objects.filter(id=num, deleted=False).first()
  data = {
    'title' : '更新ページ',
    'id' : num,
  }
  if request.method == 'POST':
    form = AddMemberForm(request.POST, instance=member_obj)
    data['form'] = form
    if form.is_valid():
      form.save()
      return redirect(to='/my_app/index')
  else:
    data['form'] = AddMemberForm(instance=member_obj)
  
  return render(request, 'my_app/update.html', data)

@login_required
def delete(request, num):
  member_obj = Member.objects.filter(id=num).first()

  if (request.method == 'POST'):
    member_obj.deleted = True
    member_obj.delete()
    return redirect(to='/my_app/index')
  
  data = {
    'title' : '削除ページ',
    'id' : num,
    'label' : ['ID', '名前', '年齢'],
    'member' : member_obj,
  }
  return render(request, 'my_app/delete.html', data)


def signup(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('my_app:login')
  else:
    form = SignUpForm()
  
  return render(request, 'accounts/signup.html', {'form': form})