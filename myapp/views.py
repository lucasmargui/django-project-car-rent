from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.db.models import Q

from .forms import ClientForm, CarForm, RegisterLocationForm
from .models import Car, CarImage

# Create your views here.
def list_location(request):  # Define uma função de visualização chamada list_location que recebe um objeto de requisição como entrada.
    cars = Car.objects.filter(is_locate=False)  # Consulta o modelo Car para recuperar todos os carros que não estão localizados.
    context = {'cars': cars}  # Cria um dicionário chamado contexto contendo os carros consultados.
    return render(request, 'list-location.html', context)  # Renderiza o modelo list-location.html com os dados do contexto e retorna como uma resposta HTTP.


def form_client(request):  # Define uma função de visualização chamada form_client que recebe um objeto de requisição como entrada.
    form = ClientForm()  # Instancia um formulário vazio para o modelo de Cliente.

    if request.method == 'POST':  # Verifica se a requisição é do tipo POST.
        form = ClientForm(request.POST)  # Preenche o formulário com os dados do POST.
        if form.is_valid():  # Verifica se os dados do formulário são válidos.
            form.save()  # Salva os dados do formulário no banco de dados.
            return redirect('list-location')  # Redireciona para a view 'list-location'.

    return render(request, 'form-client.html', {'form': form})  # Renderiza o template 'form-client.html' com o formulário como contexto.


def form_car(request):  # Define uma função de visualização chamada form_car que recebe um objeto de requisição como entrada.
    form = CarForm()  # Instancia um formulário vazio para o modelo de Carro.

    if request.method == 'POST':  # Verifica se a requisição é do tipo POST.
        form = CarForm(request.POST, request.FILES)  # Preenche o formulário com os dados do POST, incluindo arquivos enviados.
        if form.is_valid():  # Verifica se os dados do formulário são válidos.
            car = form.save()  # Salva os dados do formulário no banco de dados e retorna uma instância de carro.

            files = request.FILES.getlist('car')  # Obtém a lista de arquivos de imagem enviados.
            if files:  # Verifica se há arquivos de imagem enviados.
                for f in files:  # Itera sobre cada arquivo de imagem enviado.
                    CarImage.objects.create(  # Cria uma instância para cada imagem de carro.
                        car=car, 
                        image=f
                    )

            return redirect('list-location')  # Redireciona para a view 'list-location'.

    return render(request, 'form-car.html', {'form': form})  # Renderiza o template 'form-car.html' com o formulário como contexto.


def form_location(request, id):  # Define uma função de visualização chamada form_location que recebe um objeto de requisição e um ID como entrada.
    get_locate = Car.objects.get(id=id)  # Obtém o objeto de carro com base no ID fornecido.

    form = RegisterLocationForm()  # Instancia um formulário vazio para o modelo de Registro de Localização.
    
    if request.method == 'POST':  # Verifica se a requisição é do tipo POST.
        form = RegisterLocationForm(request.POST)  # Preenche o formulário com os dados do POST.
        if form.is_valid():  # Verifica se os dados do formulário são válidos.
            location_form = form.save(commit=False)  # Salva os dados do formulário no banco de dados, mas não realiza o commit.
            location_form.car = get_locate  # Associa o carro ao objeto de registro de localização.
            location_form.save()  # Salva o objeto de registro de localização no banco de dados.

            # Muda o status do carro para "Alugado"
            car_instance = Car.objects.get(id=id)  # Obtém a instância do carro com base no ID.
            car_instance.is_locate = True  # Define o status de localização como True (alugado).
            car_instance.save()  # Salva as alterações no banco de dados.

            return redirect('list-location')  # Redireciona para a view 'list-location'.

    # Cria um contexto com o formulário e o objeto de carro para passar para o template.
    context = {'form': form, 'location': get_locate}
    
    # Retorna o template 'form-location.html' com o contexto.
    return render(request, 'form-location.html', context)


## Relatório
def reports(request):  # Define uma função de visualização chamada reports para gerar relatórios.
    car = Car.objects.all()  # Obtém todos os carros.

    # Obtém os parâmetros de consulta da URL.
    get_client = request.GET.get('client')
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item')
    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')

    print(get_dt_start, get_dt_end)  # Imprime os parâmetros de data de início e fim.

    # Filtra os carros com base nos parâmetros de consulta.

    if get_client:  # Filtra por nome e email do cliente.
        car = Car.objects.filter(
            Q(reg_location__client__name__icontains=get_client) |
            Q(reg_location__client__email__icontains=get_client)
        )

    if get_dt_start and get_dt_end:  # Filtra por intervalo de data.
        car = Car.objects.filter(
            reg_location__create_at__range=[get_dt_start, get_dt_end]
        )

    if get_locate:  # Filtra por status de localização.
        car = Car.objects.filter(is_locate=get_locate)

    if get_type_item:  # Filtra por tipo de item.
        car = Car.objects.filter(type_item=get_type_item)

    # Renderiza o template 'reports.html' com os carros filtrados como contexto.
    return render(request, 'reports.html', {'cars': car})