from main import app, database

def clean_database():
    
    # Context manager to ensure that all database operations are scoped within this function
    with app.app_context():
        # Drop all database tables
        database.drop_all()
        
        # Recreate the tables
        database.create_all()

if __name__ == '__main__':
    clean_database()