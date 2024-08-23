from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, game_name, age, password, tag_line, tier, position, **kwargs):
        if not email: 
            raise ValueError('Users must have an email')
        if not game_name:
            raise ValueError('Users must have a game_name')
        user = self.model(
            email = email,

            name = name,
            game_name = game_name,
            age = age,
            tag_line = tag_line,
            tier = tier,
            position = position
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, age, password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
            age=age,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False, default="이름")
    game_name = models.CharField(max_length=100, null=False, blank=False , default="게임 닉네임")
    tag_line = models.CharField(max_length=100, blank = True, default="00")
    age = models.IntegerField(null=False, blank=False, default=0)
    school = models.CharField(max_length=100, blank = True)
    tier = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    puuid = models.CharField(max_length=200, blank = True, default="0")
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