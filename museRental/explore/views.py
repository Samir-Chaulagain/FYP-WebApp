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

def upload_instrument(request):
    instrument_name=request.POST.get('instrument_name','')
    instrument_company=request.POST.get('instrument_company','')
    instrument_model=request.POST.get('instrument_model','')
    instrument_type=request.POST.get('instrument_type','')
    instrument_fuel=request.POST.get('instrument_fuel','')
    instrument_No_of_Seats=request.POST.get('instrument_No_of_Seats','')
    instrument_color=request.POST.get('instrument_color','')
    instrument_license_plate=request.POST.get('instrument_license_plate','')
    
    instrument_uploaded_by=request.session.get('user_email')

    isGeared=request.POST.get('isGeared','')
    instrument_description=request.POST.get('instrument_description','')
    instrument_price=request.POST.get('instrument_price','')
    instrument_image1=request.FILES['instrument_image1']
    instrument_image2=request.FILES['instrument_image2']
    instrument_image3=request.FILES['instrument_image3']

    result_instrument = instrument.objects.filter(instrument_license_plate=instrument_license_plate)
    result_owner = Owner.objects.filter(Owner_email=instrument_uploaded_by)
    result_manager = Manager.objects.filter(Manager_email=instrument_uploaded_by)

    if result_instrument.exists():
        if result_owner.exists():
            Message = "This instrument already exist!!"
            return render(request,'Owner_Upload_instrument.html',{'Message':Message})
        if result_manager.exists():
            Message = "This instrument already exist!!"
            return render(request,'Manager_Upload_instrument.html',{'Message':Message})
    else:
        instrument=instrument(instrument_name=instrument_name,instrument_company=instrument_company,
        instrument_model=instrument_model,instrument_type=instrument_type,instrument_fuel=instrument_fuel,
        instrument_No_of_Seats=instrument_No_of_Seats,instrument_color=instrument_color,
        instrument_license_plate=instrument_license_plate,
        instrument_uploaded_by=instrument_uploaded_by,isGeared=isGeared,instrument_description=instrument_description,
        instrument_price=instrument_price,instrument_image1=instrument_image1,instrument_image2=instrument_image2,
        instrument_image3=instrument_image3)
        
        instrument.save()
        if result_owner.exists():
            return redirect('/Owner/Allinstruments')
        if result_manager.exists():
            return redirect('/Manager/Allinstruments')