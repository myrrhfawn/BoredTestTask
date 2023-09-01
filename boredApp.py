import argparse

# Створюємо парсер аргументів
parser = argparse.ArgumentParser(description="My Program")

# Додаємо аргументи командного рядка


def parse_command(parser):
    parser.add_argument('command', help='Команда')
    parser.add_argument('--type', help='Тип', required=True)
    parser.add_argument('--participants', type=int, help='Кількість учасників')
    parser.add_argument('--price_min', type=float, help='Мінімальна ціна')
    parser.add_argument('--price_max', type=float, help='Максимальна ціна')
    parser.add_argument('--accessibility_min', type=float, help='Мінімальна доступність')
    parser.add_argument('--accessibility_max', type=float, help='Максимальна доступність')

    args = parser.parse_args()

    if args.command == "new":
        print(f"Команда: {args.command}")
        print(f"Тип: {args.type}")
        print(f"Кількість учасників: {args.participants}")
        print(f"Мінімальна ціна: {args.price_min}")
        print(f"Максимальна ціна: {args.price_max}")
        print(f"Мінімальна доступність: {args.accessibility_min}")
        print(f"Максимальна доступність: {args.accessibility_max}")


# Розбираємо аргументи командного рядка
parse_command(parser)
print(type(parser))

# Виводимо значення аргументів



