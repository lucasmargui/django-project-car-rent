from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.db.models import Q

from .forms import ClientForm, CarForm, RegisterLocationForm
from .models import Car, CarImage

# Create your views here.
def list_location(request):
    cars = Car.objects.filter(is_locate=False)
    context = {'cars': cars}
    return render(request, 'list-location.html', context)


def form_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')   
    return render(request, 'form-client.html', {'form': form})


def form_car(request):
    form = CarForm() 
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            files = request.FILES.getlist('car') ## pega todas as imagens
            if files:
                for f in files:
                    CarImage.objects.create( # cria instance para imagens
                        car=car, 
                        image=f)
            return redirect('list-location')   
    return render(request, 'form-car.html', {'form': form})



def form_location(request, id):
    get_locate = Car.objects.get(id=id) ## pega objeto

    form = RegisterLocationForm()  
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.car = get_locate ## salva id do imovel 
            location_form.save()  
            
            ## muda status do imovel para "Alugado"
            immo = Car.objects.get(id=id)
            immo.is_locate = True ## passa ser True
            immo.save() 

            return redirect('list-location') # Retorna para lista

    context = {'form': form, 'location': get_locate}
    return render(request, 'form-location.html', context)



## Relatório
def reports(request): ## Relatórios   
    car = Car.objects.all()
    
    get_client = request.GET.get('client') 
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item') 

    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')
    print(get_dt_start, get_dt_end)

    if get_client: ## Filtra por nome e email do cliente
        car = Car.objects.filter(
					Q(reg_location__client__name__icontains=get_client) | 
					Q(reg_location__client__email__icontains=get_client))
    
    if get_dt_start and get_dt_end: ## Por data
        car = Car.objects.filter(
						reg_location__create_at__range=[get_dt_start,get_dt_end])

    if get_locate:
        car = Car.objects.filter(is_locate=get_locate)

    if get_type_item:
        car = Car.objects.filter(type_item=get_type_item)

    return render(request, 'reports.html', {'cars':car})