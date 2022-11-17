from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

# imports to use static media 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path("admin/", admin.site.urls),
  path("projects", include("main.urls")),
  path("", include("users.urls")),
  path("api/", include("api.urls")), 

  # path(r'^web/', include('django.contrib.auth.urls')), # WTF????
  path("reset_password/", auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
  path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
  path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="password_reset_confirm"),
  path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),

]
# when asked for images/*, the app will redirect to static/images/* or something like this
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
