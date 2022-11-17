from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail # https://docs.djangoproject.com/en/4.1/topics/email/
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile

# Signals are just a concern, a method to be triggered when some action on any model is fired.
# On Rails, the signals are already done within the models :)

@receiver(post_save, sender=User)
def create_profile_after_user_is_created(sender, instance, created, **kwargs):
  if created:
    user = instance
    profile = Profile.objects.create(
      user = user,
      username = user.username,
      email = user.email,
      name = user.first_name
    )
    print("New profile created:", profile)

    subject = "Welcome to My Project"
    message = "We are glad you were able to create an account :)"

    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [profile.email],
      fail_silently = False,
    )

@receiver(post_save, sender=Profile)
def update_user_after_profile_update(sender, instance, created, **kwargs):
  profile = instance
  user = profile.user

  if created == False:
    user.first_name = profile.name
    user.username = profile.username
    user.email = profile.email
    user.save()

@receiver(post_delete, sender=Profile)
def deleteUserAfterProfileDeleted(sender, instance, **kwargs):
    try:
      instance.user.delete()
    except:
      pass
    
# post_delete.connect(deleteUser, sender=Profile)
# post_save.connect(profileUpdated, sender=Profile)

# Those are ways of dealing with listeners. Deleting profile deletes user, and vice-versa. The first case, we delete with the listener, the other way is with cascade