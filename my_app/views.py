from django.shortcuts import redirect, render
from .models import Member
from .forms import AddMemberForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import getWeatherData
from django.http import Http404
from django.contrib import messages
import csv
import io
from django.http import HttpResponse

@login_required
def index(request):
  header = ['ID', '名前', '年齢']
  query = request.GET.get('q')
  if query:
    members = Member.objects.filter(deleted=False).all()
    members = members.filter(
      Q(name__icontains=query)
      | Q(age__icontains=query)
    )
  else:
    members = Member.objects.filter(deleted=False).all()

  if request.GET.get('order'):
    order = request.GET.get('order') 
  else:
    order = request.COOKIES.get('member_order', 'id')
    
  members = members.order_by(order)

  weather = getWeatherData() 
  data = {
    'title' : 'indexページ',
    'members' : members,
    'header' : header,
    'weather' : weather,
  }
  
  response = render(request, 'my_app/index.html', data)
  response.set_cookie('member_order', order, max_age=60*60*24*30)
  return response


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
      obj = form.instance
      messages.success(request, print(f'ID:{obj.pk} のデータを追加しました。'))
      return redirect(to='/my_app/index')
    
    messages.error(request, 'データの追加に失敗しました。')
  else:
    data = {
      'title' : '入力ページ',
      'form' : AddMemberForm(),
    }
  return render(request, 'my_app/create.html', data)

@login_required
def update(request, num):
  member_obj = Member.objects.filter(id=num, deleted=False).first()
  if not member_obj:
    raise Http404
  data = {
    'title' : '更新ページ',
    'id' : num,
    'member': member_obj,
  }
  
  if request.method == 'POST':
    form = AddMemberForm(request.POST, request.FILES, instance=member_obj)

    data['form'] = form
    if form.is_valid():
      form.save()
      obj = form.instance
      messages.success(request, f'ID:{obj.pk} {obj.name} のデータを更新しました。')
      return redirect(to='/my_app/index')

    messages.error(request, f'ID:{member_obj.pk} {member_obj.name} の更新に失敗しました。')
  else:
    data['form'] = AddMemberForm(instance=member_obj)
  
  return render(request, 'my_app/update.html', data)

@login_required
def delete(request, num):
  member_obj = Member.objects.filter(id=num).first()

  if (request.method == 'POST'):
    member_obj.deleted = True
    member_obj.image.delete(save=False)
    member_obj.image = None
    member_obj.save()
    
    messages.success(request, f'ID:{member_obj.pk} {member_obj.name} の削除が完了しました。')
    return redirect(to='/my_app/index')
  
  data = {
    'title' : '削除ページ',
    'id' : num,
    'label' : ['ID', '名前', '年齢', '画像'],
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

def export_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="members.csv"'

  writer = csv.writer(response)
  writer.writerow(['id', 'name', 'age', 'deleted'])

  for member in Member.objects.all():
      writer.writerow([member.id, member.name, member.age, member.deleted])

  return response

def import_csv(request):
  if request.method != 'POST':
    return redirect('my_app:index')

  csv_file = request.FILES.get('csv_file')

  if not csv_file:
    messages.error(request, 'CSVファイルが選択されていません')
    return redirect('my_app:index')

  if not csv_file.name.endswith('.csv'):
    messages.error(request, 'CSVファイルを選択してください')
    return redirect('my_app:index')
  
  Member.objects.all().delete()

  data = csv_file.read().decode('utf-8')
  io_string = io.StringIO(data)
  reader = csv.reader(io_string)
  header = next(reader, None)

  for row in reader:
    try:
      Member.objects.create(
        name=row[1],
        age=int(row[2]),
        deleted=row[3],
      )
    except Exception as e:
      print(f"インポート失敗: {row}, {e}")

  messages.success(request, 'CSVインポートが完了しました')
  return redirect('my_app:index')

