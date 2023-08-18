from django.db import models

# Create your models here.
class employees(models.Model):
    emp_id= models.PositiveIntegerField(blank=True,null=True,unique=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    role_position = models.CharField(max_length=200)
    joined_date = models.DateField(null=True)
    manager = models.CharField(max_length=200)
    email= models.EmailField(max_length=254)
    markytics_email = models.EmailField(max_length=254)
    manager_email = models.EmailField(max_length=254)
    address = models.CharField(max_length=200)
   # Is_Manager = models.BooleanField(default=False)
    def __str__(self):
        return self.name
class feedback(models.Model):
    employee_name = models.ForeignKey(employees, on_delete=models.CASCADE,related_name='feedbacks_recieved')
    manager_name = models.ForeignKey(employees,on_delete=models.CASCADE,related_name='feedbacks_given')
    overall_performance = models.PositiveIntegerField()
    behaviour = models.PositiveIntegerField()
    deadlines = models.PositiveIntegerField()
    positives = models.CharField(max_length=400)
    negatives = models.CharField(max_length=400)
    scope_of_improvement = models.CharField(max_length=400)

    def __str__(self):
        return self.employee