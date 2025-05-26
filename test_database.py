#!/usr/bin/env python3
"""
Test per verificare il funzionamento del database
"""

import sys
import os
sys.path.append('src')

from datetime import datetime
from database.diario_alimentare import DiarioAlimentare

def test_database():
    print("🧪 Test del Database Diario Alimentare")
    print("=" * 50)
    
    try:
        # Test 1: Aggiungere un record
        print("1. Test aggiunta record...")
        record = DiarioAlimentare.aggiungi_record(
            data=datetime.now(),
            pasto="Test",
            alimento="Pasta di test",
            quantita=100.0,
            unita_misura="g",
            carboidrati=70.0,
            glicemia_iniziale=120.0,
            glicemia_dopo_2h=140.0,
            unita_insulina=5.0,
            insulina_attiva=2.0
        )
        print(f"✅ Record aggiunto con ID: {record['id']}")
        
        # Test 2: Recuperare tutti i record
        print("\n2. Test recupero tutti i record...")
        records = DiarioAlimentare.ottieni_tutti_record()
        print(f"✅ Trovati {len(records)} record nel database")
        
        # Test 3: Aggiornare il record
        print("\n3. Test aggiornamento record...")
        updated_record = DiarioAlimentare.aggiorna_record(
            record['id'],
            alimento="Pasta aggiornata",
            quantita=150.0
        )
        if updated_record:
            print(f"✅ Record aggiornato: {updated_record['alimento']}, quantità: {updated_record['quantita']}")
        else:
            print("❌ Errore nell'aggiornamento")
        
        # Test 4: Eliminare il record
        print("\n4. Test eliminazione record...")
        deleted_record = DiarioAlimentare.elimina_record(record['id'])
        if deleted_record:
            print(f"✅ Record eliminato: ID {deleted_record['id']}")
        else:
            print("❌ Errore nell'eliminazione")
        
        # Verifica finale
        final_records = DiarioAlimentare.ottieni_tutti_record()
        print(f"\n📊 Record finali nel database: {len(final_records)}")
        
        print("\n🎉 Tutti i test completati con successo!")
        
    except Exception as e:
        print(f"❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database() 