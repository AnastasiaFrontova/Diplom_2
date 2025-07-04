from faker import Faker

fake = Faker()

def generate_user_data():
    """Генерирует данные для пользователя"""
    return {
        "email": fake.email(),
        "password": fake.password(length=12),
        "name": fake.name()
    }

def generate_user_data_without_field(field_to_exclude):
    """Генерирует данные пользователя без указанного поля"""
    data = generate_user_data()
    del data[field_to_exclude]
    return data