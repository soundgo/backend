from django.contrib.auth.models import BaseUserManager


class UserAccountManager(BaseUserManager):

    def create_user_account(self, nickname, password=None, is_active=False, is_admin=False):

        if not nickname:
            raise ValueError("Users accounts must have a nickname.")
        if not password:
            raise ValueError("Users accounts must have a password.")

        user_account = self.model(
            nickname=nickname
        )

        user_account.set_password(password)
        user_account.active = is_active
        user_account.admin = is_admin

        user_account.save(using=self._db)

        return user_account

    def create_super_user_account(self, nickname, password=None):

        user_account = self.create_user_account(
            nickname,
            password=password,
            is_admin=True,
            is_active = True
        )

        return user_account
