import os
import unittest
import requests

from unittest.mock import patch
from src.exceptions import WithdrawalTimeRestrictionError
from src.bank_account import BankAccount

URI_USD_API = 'https://api.exchangerate-api.com/v4/latest/USD'


class BankAccountTest(unittest.TestCase):

    @staticmethod
    def _is_available_api():
        try:
            response = requests.get(URI_USD_API, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    ##
    def setUp(self) -> None:
        self.account = BankAccount(balance=1000, log_file='test_account_1.txt')
        self.target = BankAccount(balance=500)

    def tearDown(self) -> None:
        if os.path.exists('test_account_1.txt'):
            os.remove('test_account_1.txt')

    def _count_lines(self, file):
        with open(file, 'r') as f:
            return len(f.readlines())

    def _read_error_tag(self, file):
        """Verifica si la última línea del archivo contiene [400]."""
        with open(file, 'r') as f:
            lines = f.readlines()
            return '[400]' in lines[-1]

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500, 'El balance no es correcto')

    @patch('src.bank_account.datetime')
    def test_withdraw(self, mock_datetime):
        mock_datetime.now.return_value.hour = 10 
        new_balance = self.account.withdraw(500)
        self.assertEqual(new_balance, 500, 'El balance no es correcto')

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)

    @patch('src.bank_account.datetime')
    def test_transfer(self, mock_datetime):
        mock_datetime.now.return_value.hour = 10
        self.account.transfer(500, self.target)
        self.assertEqual(self.account.get_balance(), 500, 'El balance no es correcto')

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.transfer(1500, self.target)

    def test_transaction_log(self):
        self.account.deposit(500)
        self.assertTrue(os.path.exists('test_account_1.txt'))

    def test_count_transactions(self):
        self.assertEqual(self._count_lines(self.account.log_file), 1)
        self.account.deposit(500)
        self.assertEqual(self._count_lines(self.account.log_file), 2)

    def test_transaction_log_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.transfer(1500, self.target)
        self.assertTrue(self._read_error_tag(self.account.log_file))

    @unittest.skipUnless(_is_available_api(), "API no disponible")
    def test_currency_exchange(self):
        response = requests.get(URI_USD_API)
        data = response.json()
        self.assertEqual(data['base'], 'USD')
        self.assertIn('COP', data['rates'])

    @patch('src.bank_account.datetime')
    def test_withdraw_raises_bussiness_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 6  # Antes de las 7:00 AM
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(500)

    @patch('src.bank_account.datetime')
    def test_withdraw_success_bussiness_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 10  # Dentro del horario permitido
        new_balance = self.account.withdraw(500)
        self.assertEqual(new_balance, 500)

    def test_deposit_vr_ammounts(self):
        test_cases= [
                        {'amount': 0, 'expected': 1000},
                        {'amount': -500, 'expected': 1000},
                        {'amount': 500, 'expected': 1500}
                     ]
        for case in test_cases:
            with self.subTest(case=case):
                new_balance = self.account.deposit(case['amount'])
                self.assertEqual(new_balance, case['expected'])
        