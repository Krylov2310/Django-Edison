from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView, info
from image_job.views import dashboard, add_image_feed, process_image_feed, delete_image, images_home
from users.forms import LoginForm

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('', include('users.urls')),

                  path('info/', info, name='info'),

                  path('login/',
                       CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                               authentication_form=LoginForm), name='login'),

                  path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
                       name='password_reset_confirm'),

                  path('password-reset-complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
                       name='password_reset_complete'),

                  path('password-change/', ChangePasswordView.as_view(), name='password_change'),

                  re_path(r'^oauth/', include('social_django.urls', namespace='social')),

                  path('images_home/', images_home, name='images_home'),

                  path('dashboard/', dashboard, name='dashboard'),

                  path('process/<int:feed_id>/', process_image_feed, name='process_feed'),

                  path('add-image-feed/', add_image_feed, name='add_image_feed'),

                  path('image/delete/<int:image_id>/', delete_image, name='delete_image'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
