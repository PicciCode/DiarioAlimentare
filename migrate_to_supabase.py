#!/usr/bin/env python3
"""
Script per migrare i dati dal database SQLite locale a Supabase
"""

import sqlite3
import os
from datetime import datetime
from src.database.diario_alimentare import DiarioAlimentare, get_session

def migrate_data():
    """Migra tutti i dati da SQLite a Supabase"""
    
    # Percorso del database SQLite locale
    sqlite_db_path = "diarioalimentare.sqlite"
    
    if not os.path.exists(sqlite_db_path):
        print("❌ Database SQLite non trovato. Assicurati che il file 'diarioalimentare.sqlite' esista.")
        return
    
    try:
        # Connessione al database SQLite
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()
        
        # Leggi tutti i record dal database SQLite
        cursor.execute("SELECT * FROM diario_alimentare ORDER BY data")
        records = cursor.fetchall()
        
        # Ottieni i nomi delle colonne
        cursor.execute("PRAGMA table_info(diario_alimentare)")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        print(f"📊 Trovati {len(records)} record da migrare...")
        
        # Migra ogni record
        migrated_count = 0
        errors = []
        
        for record in records:
            try:
                # Crea un dizionario con i dati del record
                record_dict = dict(zip(column_names, record))
                
                # Rimuovi l'ID per permettere a Supabase di generarne uno nuovo
                record_dict.pop('id', None)
                
                # Converti la data se necessario
                if 'data' in record_dict and record_dict['data']:
                    if isinstance(record_dict['data'], str):
                        record_dict['data'] = datetime.fromisoformat(record_dict['data'])
                
                # Aggiungi il record a Supabase
                DiarioAlimentare.aggiungi_record(**record_dict)
                migrated_count += 1
                
                if migrated_count % 10 == 0:
                    print(f"✅ Migrati {migrated_count}/{len(records)} record...")
                    
            except Exception as e:
                error_msg = f"Errore nel record {record}: {str(e)}"
                errors.append(error_msg)
                print(f"⚠️  {error_msg}")
        
        conn.close()
        
        print(f"\n🎉 Migrazione completata!")
        print(f"✅ Record migrati con successo: {migrated_count}")
        
        if errors:
            print(f"❌ Errori riscontrati: {len(errors)}")
            print("\nDettagli errori:")
            for error in errors[:5]:  # Mostra solo i primi 5 errori
                print(f"  - {error}")
            if len(errors) > 5:
                print(f"  ... e altri {len(errors) - 5} errori")
        
    except Exception as e:
        print(f"❌ Errore durante la migrazione: {str(e)}")
        print("Assicurati che:")
        print("1. Le variabili d'ambiente di Supabase siano configurate correttamente")
        print("2. Il database Supabase sia accessibile")
        print("3. Il file SQLite esista e sia leggibile")

def verify_migration():
    """Verifica che la migrazione sia avvenuta correttamente"""
    try:
        # Conta i record in Supabase
        records = DiarioAlimentare.ottieni_tutti_record()
        print(f"📊 Record presenti in Supabase: {len(records)}")
        
        # Conta i record in SQLite
        sqlite_db_path = "diarioalimentare.sqlite"
        if os.path.exists(sqlite_db_path):
            conn = sqlite3.connect(sqlite_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM diario_alimentare")
            sqlite_count = cursor.fetchone()[0]
            conn.close()
            
            print(f"📊 Record presenti in SQLite: {sqlite_count}")
            
            if len(records) == sqlite_count:
                print("✅ Migrazione verificata: tutti i record sono stati trasferiti!")
            else:
                print("⚠️  Attenzione: il numero di record non corrisponde")
        
    except Exception as e:
        print(f"❌ Errore durante la verifica: {str(e)}")

if __name__ == "__main__":
    print("🚀 Avvio migrazione da SQLite a Supabase...")
    print("=" * 50)
    
    # Verifica che le variabili d'ambiente siano configurate
    required_vars = ["SUPABASE_URL", "SUPABASE_API_KEY", "SUPABASE_DB_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Variabili d'ambiente mancanti:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nConfigura le variabili d'ambiente prima di procedere.")
        print("Consulta il file SUPABASE_SETUP.md per le istruzioni.")
        exit(1)
    
    # Chiedi conferma
    response = input("\n⚠️  Questa operazione migrerà tutti i dati da SQLite a Supabase. Continuare? (s/N): ")
    if response.lower() not in ['s', 'si', 'sì', 'y', 'yes']:
        print("❌ Migrazione annullata.")
        exit(0)
    
    # Esegui la migrazione
    migrate_data()
    
    # Verifica la migrazione
    print("\n" + "=" * 50)
    print("🔍 Verifica migrazione...")
    verify_migration()
    
    print("\n✨ Processo completato!")
    print("💡 Ora puoi utilizzare l'applicazione con Supabase.") 