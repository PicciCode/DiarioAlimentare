import sqlite3
import os

def migrate_database():
    """
    Aggiunge la colonna dosi_correttive alla tabella esistente se non esiste già
    """
    db_path = "diarioalimentare.sqlite"
    
    # Controlla se il database esiste
    if not os.path.exists(db_path):
        print("Database non trovato. Verrà creato automaticamente al primo avvio.")
        return
    
    try:
        # Connessione al database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Controlla se la colonna dosi_correttive esiste già
        cursor.execute("PRAGMA table_info(diario_alimentare)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'dosi_correttive' not in columns:
            print("Aggiunta colonna 'dosi_correttive' alla tabella...")
            cursor.execute("ALTER TABLE diario_alimentare ADD COLUMN dosi_correttive REAL")
            conn.commit()
            print("✅ Colonna 'dosi_correttive' aggiunta con successo!")
        else:
            print("✅ La colonna 'dosi_correttive' esiste già.")
        
        # Controlla se la colonna note esiste già (per sicurezza)
        if 'note' not in columns:
            print("Aggiunta colonna 'note' alla tabella...")
            cursor.execute("ALTER TABLE diario_alimentare ADD COLUMN note TEXT")
            conn.commit()
            print("✅ Colonna 'note' aggiunta con successo!")
        else:
            print("✅ La colonna 'note' esiste già.")
        
        # Controlla se la colonna tempo_dose_correttiva esiste già
        if 'tempo_dose_correttiva' not in columns:
            print("Aggiunta colonna 'tempo_dose_correttiva' alla tabella...")
            cursor.execute("ALTER TABLE diario_alimentare ADD COLUMN tempo_dose_correttiva INTEGER")
            conn.commit()
            print("✅ Colonna 'tempo_dose_correttiva' aggiunta con successo!")
        else:
            print("✅ La colonna 'tempo_dose_correttiva' esiste già.")
            
        conn.close()
        print("🎉 Migrazione del database completata!")
        
    except Exception as e:
        print(f"❌ Errore durante la migrazione: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database() 