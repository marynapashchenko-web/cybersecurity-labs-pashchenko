import re


# Функції оцінювання пароля
def structure_score(pw):
    """
    Оцінка структури пароля (0-4 бали)
    1 бал — наявність великої та малої літери
    1 бал — наявність цифр
    1 бал — наявність спецсимволів
    1 бал — використано >=3 типи символів
    """
    score = 0
    # Великий і малий регістр
    if re.search(r'[a-z]', pw) and re.search(r'[A-Z]', pw):
        score += 1
    # Цифри
    if re.search(r'\d', pw):
        score += 1
    # Спецсимволи
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|]', pw):
        score += 1
    # Використано >=3 типи символів
    types = sum([bool(re.search(r'[a-zA-Z]', pw)),
                 bool(re.search(r'\d', pw)),
                 bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|]', pw))])
    if types >= 3:
        score += 1
    return score

def safety_score(pw, name, birth):
    """
    Оцінка безпечності пароля (0-3 бали)
    1 бал — пароль не містить ім’я
    1 бал — пароль не містить дату народження (день, місяць, рік)
    1 бал — пароль не містить прості шаблони (1234, qwerty, password)
    """
    score = 0
    pw_lower = pw.lower()
    name_lower = name.lower()
    
    # Перевірка імені
    if name_lower not in pw_lower:
        score += 1
    
    # Перевірка дати народження (день, місяць, рік)
    day, month, year = re.findall(r'\d+', birth)
    patterns = [day, month, year, year[-2:]]  # рік та останні 2 цифри
    if not any(p in pw for p in patterns):
        score += 1
    
    # Перевірка простих шаблонів
    common = ['1234', 'qwerty', 'password', 'abcd']
    if not any(c in pw_lower for c in common):
        score += 1
    
    return score

def length_score(pw):
    """
    Оцінка довжини пароля (0-3 бали)
    0 — <8 символів
    1 — 8-11 символів
    2 — 12-15 символів
    3 — >15 символів
    """
    l = len(pw)
    if l < 8:
        return 0
    elif 8 <= l <= 11:
        return 1
    elif 12 <= l <= 15:
        return 2
    else:
        return 3

def analyze_password(pw, name, birth):
    """
    Основна функція аналізу пароля
    Повертає загальні бали, рівень безпеки та рекомендації
    """
    s_score = structure_score(pw)    # структура
    sa_score = safety_score(pw, name, birth)  # безпечність
    l_score = length_score(pw)       # довжина
    
    total = s_score + sa_score + l_score
    
    # Визначення рівня безпеки
    if total <= 3:
        level = "Слабкий"
    elif 4 <= total <= 6:
        level = "Середній"
    else:
        level = "Сильний"
    
    # Генерація рекомендацій
    tips = []
    if s_score < 4:
        tips.append("Додайте великі та малі літери, цифри та спецсимволи")
    if sa_score < 3:
        tips.append("Уникайте особистих даних та простих шаблонів")
    if l_score < 3:
        tips.append("Збільшіть довжину пароля до 12+ символів")
    
    return {
        "total": total,
        "level": level,
        "tips": tips
    }

# Меню користувача
def menu():
    print("Password Analyzer")
    name = input("Введіть ваше ім'я: ")
    birth = input("Введіть дату народження (дд.мм.рррр): ")
    
    while True:
        print("\nМеню:")
        print("1 - Перевірити пароль")
        print("2 - Вийти")
        choice = input("Ваш вибір: ")
        
        if choice == "1":
            pw = input("Введіть пароль для аналізу: ")
            result = analyze_password(pw, name, birth)
            
            print("\n--- Результат аналізу ---")
            print(f"Бали: {result['total']}/10")
            print(f"Рівень безпеки: {result['level']}")
            print("Рекомендації:")
            for t in result['tips']:
                print(f"- {t}")
        elif choice == "2":
            print("Вихід з програми...")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

menu()
