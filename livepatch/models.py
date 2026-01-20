from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class Component(models.Model):
    uid = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_current_state(self):
        """Get the latest value for each key"""
        from django.db.models import Max
        
        # Get the latest created_at for each key
        latest_patches = self.patches.values('key').annotate(
            latest=Max('created_at')
        )
        
        # Build a dict of key: latest_created_at
        latest_times = {p['key']: p['latest'] for p in latest_patches}
        
        # Get patches matching those times
        result = {}
        for key, latest_time in latest_times.items():
            patch = self.patches.filter(key=key, created_at=latest_time).first()
            if patch:
                result[key] = patch.value
        
        return result

class Patch(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='patches')
    key = models.TextField()
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['component', 'key', '-created_at'])
        ]
