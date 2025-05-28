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
    
        
    

############### saad work ############################

class Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    a_transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    generated_video_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.url

class Question(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_text[:50]
