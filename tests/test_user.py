import os
import unittest
from faker import Faker

from src.bank_account import BankAccount
from src.user import User

class UserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.faker = Faker(locale='es')
        self.user = User(name=self.faker.name(),email=self.faker.email())


    def tearDown(self) -> None:
        for account in self.user.account:
            os.remove(account.log_file)

    def test_user_creation(self):
        # Crear un usuario con datos conocidos para evitar la aleatoriedad
        name = "John Doe"
        email = "johndoe@example.com"
        user = User(name=name, email=email)

        # Verificar que los datos coincidan con los inicializados
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)


    def test_user_with_multiple_accounts(self):        
        for _ in range(3):
            bank_account = BankAccount(
                self.faker.random_int(min=1000, max=2000, step=25),
                self.faker.file_name(extension='txt')
            )
            self.user.add_account(bank_account)

        excepted_balance = self.user.get_total_balance()
        value = sum(account.get_balance() for account in self.user.account)
        self.assertEqual(value, excepted_balance)

    
    