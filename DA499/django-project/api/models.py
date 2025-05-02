from django.db import models


# class item(models.Model):
#     name=models.CharField(max_length=30)
#     create=models.DateTimeField(auto_now_add=True)


# class Video(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name



class Video(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
        
    


