from compressor_app import main
from models.database import create_tables, engine

if __name__ == '__main__':
    try:
        create_tables()
        main()
    except Exception as e:
        print(e)
        input('Press Enter to exit')
