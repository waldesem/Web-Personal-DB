#!/bin/bash

# Определяем путь: текущая директория + PersonalDB
DEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/PersonalDB"

# Создаем директорию, если её нет
mkdir -p "$DEST_DIR"

# Записываем содержимое в settings.ini
cat > settings.ini << EOF
[Destination]
path=$DEST_DIR

[Password]
password=88888888
EOF

echo "Settings created"
