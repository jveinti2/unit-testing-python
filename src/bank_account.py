from datetime import datetime
from src.exceptions import WithdrawalTimeRestrictionError

class BankAccount:
    def __init__(self, balance=0, log_file=None):
        self.balance = balance
        self.log_file = log_file
        self._log_transaction(f'Cuenta creada')

    def _log_transaction(self, message):
        if self.log_file: 
            with open(self.log_file, 'a') as file: 
                file.write(f'{message}\n')

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction(f'Deposito de: {amount}')
        return self.balance


    def withdraw(self, amount):
        now = datetime.now()
        if now.hour < 7 or now.hour > 17:
            raise WithdrawalTimeRestrictionError('El horario de retiro es de 7:00 a 17:00')

        if amount > 0:
            self.balance -= amount
            self._log_transaction(f'Retiro de: {amount}')
        return self.balance 

    def get_balance(self):
        return self.balance

    def transfer(self, amount, target):
        """
        Transferir dinero a otra cuenta
        target: instancia de nueva cuenta de banco
        """
        if self.balance < amount:
            raise_message = '[400] No hay saldo suficiente'
            self._log_transaction(raise_message)
            raise ValueError(raise_message)
        
        self.withdraw(amount)
        target.deposit(amount)
        self._log_transaction(f'Transferencia de: {amount}')
        

