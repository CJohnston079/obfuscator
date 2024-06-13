from faker import Faker

fake = Faker("en_GB")


def generate_data(*generate, num_records=3):
    data = {key: [] for key in generate}

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()

        if "shallow" in generate:
            shallow_data = {"name": name, "age": age, "city": city}
            data["shallow"].append(shallow_data)
        if "shallow_obfuscated" in generate:
            obfuscated_date = {"name": "***", "age": age, "city": city}
            data["obfuscated"].append(obfuscated_date)

    return data


def generate_shallow_data_old(num_records=3):
    shallow_data = []
    obfuscated_shallow_data = []

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()

        shallow_data.append({"name": name, "age": age, "city": city})
        obfuscated_shallow_data.append(
            {"name": "***", "age": str(age), "city": city})

    return shallow_data, obfuscated_shallow_data


def generate_deep_array_based_data(num_records=3):
    deep_data = []
    obfuscated_deep_data = []

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()
        email_address = fake.email()
        phone_number = fake.phone_number()

        deep_data.append({
            "name": name,
            "age": age,
            "city": city,
            "contact": [{"email": email_address}, {"phone": phone_number}]
        })

        obfuscated_deep_data.append({
            "name": "***",
            "age": age,
            "city": city,
            "contact": [{"email": "***"}, {"phone": "***"}]
        })

    return deep_data, obfuscated_deep_data


def generate_deep_object_based_data(num_records=3):
    deep_data = []
    obfuscated_deep_data = []

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()
        email_address = fake.email()
        phone_number = fake.phone_number()

        deep_data.append({
            "name": name,
            "age": age,
            "city": city,
            "contact": {"email": email_address, "phone": phone_number}
        })

        obfuscated_deep_data.append({
            "name": "***",
            "age": age,
            "city": city,
            "contact": {"email": "***", "phone": "***"}
        })

    return deep_data, obfuscated_deep_data
