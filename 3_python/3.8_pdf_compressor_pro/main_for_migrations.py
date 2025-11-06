# main_for_migrations.py
from compressor_app import main
from models.database import create_tables, get_db
from crud.operations import DBOperations

if __name__ == '__main__':
    try:
        create_tables()

        # ВРЕМЕННЫЙ КОД ДЛЯ МИГРАЦИИ
        print("=== НАЧАЛО МИГРАЦИИ БАЗЫ ДАННЫХ ===")
        db = next(get_db())
        db_ops = DBOperations(db)

        # Проверяем дубликаты до миграции
        print("Проверка дубликатов ДО миграции:")
        db_ops.check_duplicates()

        # Запускаем миграцию
        db_ops.normalize_existing_paths()

        # Проверяем дубликаты после миграции
        print("Проверка дубликатов ПОСЛЕ миграции:")
        db_ops.check_duplicates()

        print("=== МИГРАЦИЯ ЗАВЕРШЕНА ===")
        input("Нажмите Enter для запуска программы...")
        # КОНЕЦ ВРЕМЕННОГО КОДА

        main()
    except Exception as e:
        print(f"Ошибка: {e}")
        input('Press Enter to exit')