from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25, unique=True)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
    class Meta:
        abstract = True
        
class Client(User):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Client: {self.username}"

class Mechanic(User):
    salary = models.FloatField(max_length=9)

    def __str__(self):
        return f"Mécanicien: {self.username}"
    
class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="vehicules")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointment")
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name="appointment")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="appointment")
    date = models.DateTimeField()
    description = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"RDV: {self.client.username} avec {self.mechanic.username} - {self.date}"
  
class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="factures")
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Facture #{self.id} - {self.client.username} - ${self.amount}"
