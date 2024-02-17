from django.db import models
from datetime import datetime
# Create your models here.

## Cadastro de Clientes     
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return "{} - {}".format(self.name, self.email)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


## Opções de Imóveis
class TypeCar(models.TextChoices):
    ESPORTIVO = 'ESPORTIVO','ESPORTIVO'
    CONVERSIVEL = 'CONVERSIVEL','CONVERSIVEL'
    SUV = 'SUV','SUV'



## Cadastro de Imóveis
class Car(models.Model):
    code = models.CharField(max_length=100)
    type_item = models.CharField(max_length=100, choices=TypeCar.choices)
    address = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    is_locate = models.BooleanField(default=False)
    
    
    def __str__(self):
        return "{} - {}".format(self.code, self.type_item)
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-id']


## Cadastrar as Imagens do Imóvel
class CarImage(models.Model):
    image = models.ImageField('Images',upload_to='images')
    car = models.ForeignKey(Car, related_name='car_images', on_delete=models.CASCADE)
 
    def __str__(self):
        return self.car.code



## Registrar Locação
class RegisterLocation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reg_location')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    dt_start = models.DateTimeField('Inicio')
    dt_end = models.DateTimeField('Fim')
    create_at = models.DateField(default=datetime.now, blank=True)
    
    def __str__(self):
        return "{} - {}".format(self.client, self.car)
    
    class Meta:
        verbose_name = 'Registrar Locação'
        verbose_name_plural = 'Registrar Locação'
        ordering = ['-id']