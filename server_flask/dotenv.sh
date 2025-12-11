#!/bin/bash

# Определяем путь: текущая директория + PersonalDB
DEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/PersonalDB"

# Создаем директорию, если её нет
mkdir -p "$DEST_DIR"

# Записываем содержимое в .env
cat > .env << EOF
BASE_PATH=$DEST_DIR

DEFAULT_PASSWORD=88888888

DATABASE_URI=postgresql://webapp:webapp@localhost:5433/personal
EOF

echo "env created"
