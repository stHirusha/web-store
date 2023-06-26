from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemFrom,EditItemFrom
from django.db.models import Q


# Create your views here.
def items(requeset):
   query = requeset.GET.get('query','')
   categories = Category.objects.all()
   category_id = requeset.GET.get('category',0)
   items = Item.objects.filter(is_sold=False)
   
   if category_id:
      items= items.filter(category_id=category_id)
   
   if query:
      items= items.filter(Q(name__icontains=query) | Q(description_icontains=query))
   
   return render(requeset, "item/items.html",{
      'categories' : categories,
      'category_id': int(category_id),
      'items' : items,
      'query' : query,
   })

def detail(request, pk):
   item = get_object_or_404(Item,pk=pk)
   related_items = Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]
   
   return render(request, "item/detail.html",{
      'item' : item,
      'related_items' : related_items,
   })

@login_required   
def new(request):
   if request.method == 'POST':
      form = NewItemFrom(request.POST, request.FILES)
      
      if form.is_valid():
         item = form.save(commit=False)
         item.created_by = request.user
         item.save()
         
         return redirect('item:detail',pk=item.id)
   else:
      form = NewItemFrom()
   
   return render(request,'item/form.html',{
      'form':form,
      'title':'New Item',
   })
     
@login_required   
def edit(request,pk):
   item = get_object_or_404(Item,pk=pk, created_by=request.user)
   
   if request.method == 'POST':
      form = EditItemFrom(request.POST, request.FILES,instance=item)
      
      if form.is_valid():
         form.save()
         
         return redirect('item:detail',pk=item.id)
   else:
      form = EditItemFrom(instance=item)
   
   return render(request,'item/form.html',{
      'form':form,
      'title':'Edit Item',
   })
     
@login_required
def delete(request,pk):
   item = get_object_or_404(Item,pk=pk, created_by=request.user)
   item.delete()
   
   return redirect('dashboard:index')
   
   