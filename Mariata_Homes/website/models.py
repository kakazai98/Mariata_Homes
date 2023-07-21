from django.db import models

class Source(models.Model):
    SOURCE_TYPES = (
        ('Police Station', 'Police Station'),
        ('Prison Release', 'Prison Release'),
        ('Immigration Release', 'Immigration Release'),
        ('Other', 'Other')
    )
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, db_column='source', primary_key=True)
    source_address = models.CharField(max_length=255, db_column='address')

class Applicant(models.Model):
    name = models.CharField(max_length=255,db_column='name')
    dob = models.DateField(db_column='DOB')
    email = models.EmailField(db_column='email',primary_key=True)
    phone = models.CharField(max_length=20, db_column='phone')
    photo = models.ImageField(upload_to='photo/', db_column='photo')
    illnesses = models.CharField(max_length=255, blank=True, db_column='illnesses')
    disabilities = models.CharField(max_length=255, blank=True ,db_column='diabilities')
    last_residence = models.CharField(max_length=255, blank=True, db_column='last_residence')
    next_of_kin = models.CharField(max_length=255, blank=True, db_column='next_of_kin')
    recommendation = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source',db_column='recommendation')
    status_types = (
        ('Pending','Pending'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected')
    )
    status = models.CharField(max_length=20, choices=status_types, db_column='status')

    def __str__(self):
        return self.name+' '+self.email+' '+self.phone

class Admin(models.Model):
    username = models.CharField(max_length=255,db_column='username', primary_key=True)
    password = models.CharField(max_length=255, db_column='password')

class Notification(models.Model):
    Sent_to = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name='applicant',db_column='receiver')
    Sent_by = models.ForeignKey(Admin,on_delete=models.CASCADE, related_name='admin',db_column='sender')
    message = models.CharField(max_length=255, db_column='message')
    timestamp = models.DateTimeField(auto_now_add=True,db_column='timestamp')
    
