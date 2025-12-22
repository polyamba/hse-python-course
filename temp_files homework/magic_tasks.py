class PositiveNumber:
    def __new__(cls, value):
        """
        ЗАДАНИЕ: Реализуйте проверку в методе __new__
        - Проверьте, что value > 0
        - Если значение отрицательное или ноль, вызовите ValueError с сообщением
        - Если значение положительное, создайте экземпляр через super().__new__(cls)
        """
        if value > 0:
            instance = super().__new__(cls)
            return instance
        else:
            raise ValueError('Только положительные числа!')

    def __init__(self, value):
        """
        Инициализатор - сохраняет значение в атрибут value
        """
        self.value = value

# Использование
try:
    pos1 = PositiveNumber(10) # 10
    pos2 = PositiveNumber(-5) # Только положительные числа!
except ValueError as e:
    print(f"Ошибка: {e}")

"""
super().__new__(cls) - это вызов "родительского" метода __new__, который:

    Выделяет память для нового объекта

    Создает "пустой" экземпляр класса

    Возвращает готовый к инициализации объект
"""

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return f"Пополнено: {amount}"

class PremiumAccount(BankAccount):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance) # TODO: Вызвать конструктор родителя
        self.balance += 100  # TODO: Добавить 100 бонусов к балансу

acc = PremiumAccount("Иван", 500)
print(f"Баланс: {acc.balance}")  # 600

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def get_price(self):
        return self.price

class DiscountedProduct(Product):
    def __init__(self, name, price, discount_percent):
        super().__init__(name, price) # TODO: Вызвать конструктор родителя
        self.discount_percent = discount_percent  # TODO: Инициализировать процент скидки
    
    def get_price(self):
        # TODO: Использовать родительский get_price и применить скидку
        return round(super().get_price() * (1 - self.discount_percent/100))


product = DiscountedProduct("Ноутбук", 100000, 15)
print(f"Цена со скидкой: {product.get_price()}")  # Должно быть: 85000
