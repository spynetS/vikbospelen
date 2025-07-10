from django.db import models

# Create your models here.
class Mail(models.Model):
    subject = models.TextField()
    body = models.TextField()
    from_email = models.TextField()
    to= models.TextField()
    reply_to=models.TextField()
    error=models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} {str(self.created_at)} "
