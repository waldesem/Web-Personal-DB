#!/bin/bash

config_file="settings.ini"
base_path=""

# Проверяем, существует ли settings.ini
if [[ ! -f "$config_file" ]]; then
    echo "Error: settings.ini not found"
    return 1
fi

# Извлекаем путь из секции [Destination] -> path
base_path=$(grep -A 10 "^\[Destination\]$" "$config_file" | grep "^path=" | cut -d'=' -f2- | xargs)

# Проверяем, найден ли путь
if [[ -z "$base_path" ]]; then
    echo "Error: 'path' not found in [Destination] section"
    return 1
fi

# Проверяем, существует ли директория
if [[ -d "$base_path" ]]; then
    main_office="$base_path/Главный офис"
    
    # Создаём родительскую папку
    mkdir -p "$main_office" 2>/dev/null || {
        echo "Error: Cannot create directory $main_office"
        return 1
    }

    # Перебираем кириллические буквы
    for letter in А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я; do
        mkdir -p "$main_office/$letter" 2>/dev/null
    done

    echo "Folders created"
else
    echo "BASE_PATH is not a directory or does not exist: $base_path"
    return 1
fi

