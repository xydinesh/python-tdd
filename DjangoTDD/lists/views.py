from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/{0}/'.format(list_.id))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{0}/'.format(list_.id))
