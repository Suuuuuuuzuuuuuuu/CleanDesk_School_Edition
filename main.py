import os
import shutil
import config as cfg


def ask_choice(question,default_yes):
    text=input(question).strip().lower()
    if text=="":
        return default_yes
    if text=="так" or text=="+" or text=="yes" or text=="y":
        return "так"
    return "ні"


def find_category(file_name,extension,school_dict):
    if extension=="":
        return "Інше"

    lower_name=file_name.lower()
    clean_name=lower_name.replace("к.р."," кр ").replace("с.р."," ср ")
    clean_name=clean_name.replace("д.з."," дз ").replace("м.о."," мо ")

    formatted_name=""
    for char in clean_name:
        if char in "._-/,()[]+=":
            formatted_name=formatted_name+" "
        else:
            formatted_name=formatted_name+char
    name_words=formatted_name.split()

    is_school="ні"
    for word in cfg.SCHOOL_LONG_WORDS:
        if word in lower_name:
            is_school="так"
            break

    if is_school=="ні":
        for short_word in cfg.SCHOOL_SHORT_WORDS:
            if short_word in name_words:
                is_school="так"
                break

    if is_school=="так":
        for cat in school_dict:
            if "Поробки" in cat:
                if "поробк" in lower_name or "аплікац" in lower_name or "ліпленн" in lower_name or "оригамі" in lower_name:
                    return cat
            if "Контрольні" in cat:
                if "контрольн" in lower_name or "діагностичн" in lower_name or "самостійн" in lower_name or "тест" in lower_name:
                    return cat
                if "кр" in name_words or "ср" in name_words:
                    return cat
            if "Виховна" in cat:
                if "виховн" in lower_name or "батьківськ" in lower_name or "збори" in lower_name or "воспитательн" in lower_name or "родительск" in lower_name:
                    return cat
            if "Методична" in cat:
                if "атестац" in lower_name or "педрад" in lower_name or "методичн" in lower_name or "портфоліо" in lower_name or "звіт" in lower_name:
                    return cat
                if "мо" in name_words:
                    return cat

        for cat,ext_list in school_dict.items():
            if extension in ext_list:
                return cat
    else:
        for cat,ext_list in cfg.CATEGORIES_GENERAL.items():
            if extension in ext_list:
                return cat

    return "Інше"


def remove_empty_folders(root_dir,all_roots,protected_dirs,is_dry):
    for cur_dir,inside_dirs,file_list in os.walk(root_dir,topdown=False):
        folder_name=os.path.basename(cur_dir)
        first_level=os.path.relpath(cur_dir,root_dir).split(os.sep)[0]

        if first_level in all_roots or cur_dir==root_dir:
            continue

        is_safe="ні"
        for p_dir in protected_dirs:
            if cur_dir==p_dir or cur_dir.startswith(p_dir+os.sep):
                is_safe="так"
                break
        if is_safe=="так":
            continue

        if len(os.listdir(cur_dir))==0:
            try:
                if is_dry!="так":
                    os.rmdir(cur_dir)
                if is_dry=="так":
                    print("├── [ТЕСТ: БУДЕ ВИДАЛЕНО ПОРОЖНЮ ПАПКУ] "+folder_name)
                else:
                    print("├── [ВИДАЛЕНО ПОРОЖНЮ ПАПКУ] "+folder_name)
            except Exception:
                pass


current_script=os.path.basename(__file__)

print("="*60)
print("  ШКІЛЬНИЙ ОРГАНАЙЗЕР ФАЙЛІВ (CleanDesk v1.0 School Edition)")
print("="*60)
print("(Підказка: якщо просто натиснути Enter, обереться варіант з великих літер)\n")

ans_help=ask_choice("Потрібні додаткові інструкції? [ні/ТАК]: ","так")
if ans_help=="так":
    print("\n"+"="*60)
    print("                ДОДАТКОВІ ІНСТРУКЦІЇ ТА ПІДКАЗКИ")
    print("="*60)
    print("1. Сортування робочого столу:")
    print("   - 'так' — програма сама знайде ваш робочий стіл (навіть з OneDrive).")
    print("   - 'ні'  — вам треба буде ввести точний шлях до потрібної папки.")
    print("\n2. Перевірка підпапок:")
    print("   - 'так' — скрипт загляне в усі вкладені папки і збере звідти файли.")
    print("             Порожні папки після цього будуть акуратно видалені.")
    print("   - 'ні'  — сортуються тільки ті файли, що лежать на самій поверхні.")
    print("\n3. Захист папок класів:")
    print("   - Якщо обрати 'так', папки окремих класів (наприклад, '7-Б', '5A клас')")
    print("     разом із їхнім вмістом залишаться повністю неторканими.")
    print("\n4. Режим та окрема папка 'Школа':")
    print("   - Програма автоматично аналізує назви файлів на наявність шкільних слів.")
    print("   - Можна скласти всі шкільні матеріали в окрему велику папку 'Школа'.")
    print("\n5. Режим перегляду без переміщення (Тест):")
    print("   - Дозволяє безпечно переглянути звіт без будь-яких змін на комп'ютері.")
    print("\nВАЖЛИВО: Дію реального сортування не можна скасувати через Ctrl + Z!")
    print("="*60)

    ans_deep=ask_choice("\nПотрібні ще глибші роз'яснення та приклади? [ні/ТАК]: ","ні")
    if ans_deep=="так":
        print("\n"+"~"*60)
        print("          РОЗШИРЕНІ ПОЯСНЕННЯ З ПРИКЛАДАМИ ДЛЯ ВЧИТЕЛЯ")
        print("~"*60)
        print("А. ЯК ПРАЦЮЄ ЗАХИСТ ПАПОК КЛАСІВ:")
        print("   - Якщо у вас є папка '9-А клас' або '6-B', у якій збережені різні")
        print("     матеріали та внутрішні папки (наприклад, 'Фото з екскурсії'),")
        print("     програма повністю обійде її стороною і нічого не змінить.")
        print("\nБ. ЯК РОЗПІЗНАЮТЬСЯ ШКІЛЬНІ ФАЙЛИ:")
        print("   - Файл 'математика_5_клас.docx' піде в 'Плани, конспекти та КТП'.")
        print("   - Файл 'презентація_до_уроку.pptx' піде в 'Презентації до уроків'.")
        print("   - Скорочення на зразок 'К.Р.' чи 'Д.З.' правильно визначаються як шкільні.")
        print("   - Звичайний файл (наприклад, 'квитанція.pdf') піде у звичайні 'Документи'.")
        print("\nВ. ЗАХИСТ ВІД ХИБНИХ СЛІВ:")
        print("   - Короткі скорочення шукаються окремо, тому файли 'крем', 'ікра'")
        print("     чи 'дімон' залишаться у своїх звичайних папках.")
        print("~"*60+"\n")

ans_desktop=ask_choice("Сортувати робочий стіл? [ТАК/ні]: ","так")
if ans_desktop=="так":
    home=os.path.expanduser("~")
    onedrive=os.path.join(home,"OneDrive","Desktop")
    if os.path.exists(onedrive):
        folder_path=onedrive
    else:
        folder_path=os.path.join(home,"Desktop")
else:
    while True:
        folder_path=input("Введіть точний шлях до папки: ").strip('"\'')
        if os.path.exists(folder_path):
            break
        print("Помилка: такої папки не існує. Спробуйте ще раз.")

ans_sub=ask_choice("Перевіряти підпапки? [ні/ТАК]: ","ні")
protect_classes="ні"
if ans_sub=="так":
    protect_classes=ask_choice("Не чіпати папки окремих класів (наприклад, 5-А, 7-B)? [ТАК/ні]: ","так")

ans_school_dir=ask_choice("Створити окрему папку 'Школа' для уроків? [ТАК/ні]: ","так")
ans_dry=ask_choice("Тільки переглянути без переміщення (тест)? [ні/ТАК]: ","ні")

if ans_dry!="так":
    print("\n"+"!"*60)
    print("УВАГА: Зараз файли будуть реально переміщені!")
    print("Цю дію НЕ можна буде скасувати через Ctrl + Z.")
    confirm=ask_choice("Ви впевнені, що хочете розпочати? [ТАК/ні]: ","так")
    if confirm!="так":
        print("Операцію скасовано. Жоден файл не змінено.")
        input("\nНатисніть Enter для виходу...")
        exit()
    print("!"*60)

CATEGORIES_SCHOOL={}
for name in cfg.CATEGORIES_SCHOOL_BASE:
    exts=cfg.CATEGORIES_SCHOOL_BASE[name]
    if ans_school_dir=="так":
        full_sub_path=os.path.join("Школа",name)
        CATEGORIES_SCHOOL[full_sub_path]=exts
    else:
        CATEGORIES_SCHOOL[name]=exts

ALL_ROOTS=["Зображення","Документи","Відео","Аудіо","Архіви","Скрипти","Школа","Інше"]
for name in cfg.CATEGORIES_SCHOOL_BASE:
    ALL_ROOTS.append(name)

files_to_sort=[]
protected_class_dirs=[]

if ans_sub=="так":
    for cur_dir,inside_dirs,file_list in os.walk(folder_path):
        f_name_lower=os.path.basename(cur_dir).lower()
        first_level=os.path.relpath(cur_dir,folder_path).split(os.sep)[0]

        if first_level in ALL_ROOTS:
            inside_dirs.clear()
            continue

        skip_dir="ні"
        for p_dir in protected_class_dirs:
            if cur_dir==p_dir or cur_dir.startswith(p_dir+os.sep):
                skip_dir="так"
                break
        if skip_dir=="так":
            inside_dirs.clear()
            continue

        if protect_classes=="так":
            for pat in cfg.CLASS_PATTERNS:
                if pat in f_name_lower:
                    protected_class_dirs.append(cur_dir)
                    skip_dir="так"
                    break
        if skip_dir=="так":
            inside_dirs.clear()
            continue

        for f in file_list:
            files_to_sort.append([cur_dir,f])
else:
    for f in os.listdir(folder_path):
        full_p=os.path.join(folder_path,f)
        if os.path.isfile(full_p):
            files_to_sort.append([folder_path,f])

total_moved=0
total_duplicates=0
stats={"Інше":0}
for c in cfg.CATEGORIES_GENERAL:
    stats[c]=0
for c in CATEGORIES_SCHOOL:
    stats[c]=0

planned_destinations_lower=[]

print("\n[ ПОЧАТОК СОРТУВАННЯ ]")
if ans_dry=="так":
    print(">>> УВАГА: УВІМКНЕНО ТЕСТОВИЙ РЕЖИМ (ФАЙЛИ НЕ ПЕРЕМІЩУЮТЬСЯ) <<<\n")

for item in files_to_sort:
    f_dir,f_name=item[0],item[1]
    f_path=os.path.join(f_dir,f_name)

    if f_name==current_script or f_name=="config.py" or f_name.startswith("~$"):
        continue

    clean_f_name=f_name.rstrip(".") if f_name.endswith(".") else f_name
    name,ext=os.path.splitext(clean_f_name)
    ext=ext.lower()
    if ext==".":
        ext=""

    if ext in cfg.IGNORED_EXTENSIONS:
        continue

    target_cat=find_category(clean_f_name,ext,CATEGORIES_SCHOOL)
    target_dir=os.path.join(folder_path,target_cat)

    if ans_dry!="так":
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

    dest_path=os.path.join(target_dir,clean_f_name)
    counter=1
    is_dup="ні"

    while os.path.exists(dest_path) or (dest_path.lower() in planned_destinations_lower):
        is_dup="так"
        dest_path=os.path.join(target_dir,name+"_"+str(counter)+ext)
        counter=counter+1

    planned_destinations_lower.append(dest_path.lower())

    try:
        if ans_dry!="так":
            shutil.move(f_path,dest_path)

        total_moved=total_moved+1
        if is_dup=="так":
            total_duplicates=total_duplicates+1
        stats[target_cat]=stats[target_cat]+1

        final_name=os.path.basename(dest_path)
        status_tag="БУДЕ ПЕРЕМІЩЕНО" if ans_dry=="так" else "ПЕРЕМІЩЕНО"
        print("├── ["+status_tag+"] "+f_name+" -> "+target_cat)
        if is_dup=="так":
            print("│\t└── Дублікат! Нова назва: "+final_name)

    except PermissionError:
        print("├── [ПОМИЛКА] "+f_name+" (зайнятий іншою програмою)")
    except Exception as err:
        print("├── [ЗБІЙ] "+f_name+" ("+str(err)+")")

if ans_sub=="так":
    remove_empty_folders(folder_path,ALL_ROOTS,protected_class_dirs,ans_dry)

print("└── [ СОРТУВАННЯ ЗАВЕРШЕНО ]\n")
print("="*60)
if ans_dry=="так":
    print("        ТЕСТОВИЙ ЗВІТ (ЖОДЕН ФАЙЛ НЕ БУЛО ПЕРЕМІЩЕНО)")
else:
    print("                    ПІДСУМКОВИЙ ЗВІТ")
print("="*60)
print("Всього оброблено файлів:\t"+str(total_moved))
print("Перейменовано дублікатів:\t"+str(total_duplicates))
print("-" * 60)
for cat in stats:
    if stats[cat]>0:
        print("\t- "+cat+": "+str(stats[cat])+" шт.")
print("="*60)

input("\nНатисніть Enter, щоб вийти з програми...")