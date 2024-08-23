from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password, **kwargs):
        if not email: 
            raise ValueError('Users must have an email')
        if not nickname:
            raise ValueError('Users must have a nickname')
        user = self.model(
            email = email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname='관리자', password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            nickname=nickname, 
            password=password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(max_length=20, unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=100, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는학번으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email