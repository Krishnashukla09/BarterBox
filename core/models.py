from django.contrib.auth.models import User
from django.db import models

# Skill Model (reusable)
class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    skills_offered = models.ManyToManyField(Skill, related_name='offered_by')
    skills_wanted = models.ManyToManyField(Skill, related_name='wanted_by')

    def __str__(self):
        return self.user.username

# Swap Request
class SwapRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    offered_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='offered_requests')
    wanted_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='wanted_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional direct feedback (basic)
    feedback = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} | {self.offered_skill} for {self.wanted_skill}"

# Detailed Feedback Model (optional & expandable)
class Feedback(models.Model):
    swap = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name='feedback_entries')  # ✅ fixed related_name
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_received')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.from_user} to {self.to_user} - {self.rating}"

# 🔥 Chat Model (Surprise Feature)
class ChatMessage(models.Model):
    swap = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name='chat_messages')  # ✅ added related_name for clarity
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}"
