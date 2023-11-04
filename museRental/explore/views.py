from django.shortcuts import get_object_or_404, render,redirect
from .forms import NewItemForm, EditItemForm
from .models import Category, Item
from django.db.models import Q

# Create your views here.
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'explore/explore.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'explore/detail.html', {
        'item': item,
        'related_items': related_items
    })


def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('explore:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'explore/form.html', {
        'form': form,
        'title': 'New item',
    })


def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('explore:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'explore/form.html', {
        'form': form,
        'title': 'Edit item',
    })


def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('index')