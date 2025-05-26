#!/usr/bin/env python3
import sys
sys.path.append('src')

from database.diario_alimentare import DiarioAlimentare
from datetime import datetime
import pandas as pd

def debug_operations():
    print('=== TEST DIRETTO ===')
    
    # Aggiungi un record
    record = DiarioAlimentare.aggiungi_record(
        data=datetime.now(),
        pasto='Test',
        alimento='Test Alimento',
        quantita=100.0,
        unita_misura='g',
        carboidrati=50.0,
        glicemia_iniziale=110.0
    )
    print(f'Record aggiunto: ID {record["id"]}')
    
    # Ottieni tutti i record
    records = DiarioAlimentare.ottieni_tutti_record()
    print(f'Totale record: {len(records)}')
    
    # Simula creazione DataFrame come in Streamlit
    data = []
    for r in records:
        data.append({
            'ID': r['id'],
            'Data': r['data'],
            'Pasto': r['pasto'],
            'Alimento': r['alimento'],
            'Quantità': r['quantita'],
            'Unità di Misura': r['unita_misura'],
            'Carboidrati (g)': r['carboidrati'],
            'Glicemia Iniziale': r['glicemia_iniziale'],
            'Glicemia dopo 2h': r['glicemia_dopo_2h'],
            'Unità Insulina': r['unita_insulina'],
            'Insulina Attiva': r['insulina_attiva']
        })
    df = pd.DataFrame(data)
    print(f'DataFrame creato con {len(df)} righe')
    
    # Trova il record appena creato
    test_row = df[df['ID'] == record['id']]
    if not test_row.empty:
        record_to_update = test_row.iloc[0]
        print(f'Record trovato: {record_to_update["Alimento"]}')
        print(f'ID del record: {record_to_update["ID"]} (tipo: {type(record_to_update["ID"])})')
        
        # Test aggiornamento
        print('\n=== TEST AGGIORNAMENTO ===')
        try:
            updated = DiarioAlimentare.aggiorna_record(
                int(record_to_update['ID']),  # Assicurati che sia int
                alimento='Alimento Modificato',
                quantita=150.0
            )
            if updated:
                print(f'Aggiornamento riuscito: {updated["alimento"]}')
                
                # Verifica aggiornamento
                records_after_update = DiarioAlimentare.ottieni_tutti_record()
                updated_record = next((r for r in records_after_update if r['id'] == record['id']), None)
                if updated_record:
                    print(f'Verifica: {updated_record["alimento"]}')
                else:
                    print('Record non trovato dopo aggiornamento')
            else:
                print('Aggiornamento fallito - returned None')
        except Exception as e:
            print(f'Errore aggiornamento: {e}')
        
        # Test eliminazione
        print('\n=== TEST ELIMINAZIONE ===')
        try:
            deleted = DiarioAlimentare.elimina_record(int(record_to_update['ID']))
            if deleted:
                print(f'Eliminazione riuscita: ID {deleted["id"]}')
                
                # Verifica eliminazione
                records_after_delete = DiarioAlimentare.ottieni_tutti_record()
                deleted_check = next((r for r in records_after_delete if r['id'] == record['id']), None)
                if deleted_check is None:
                    print('Verifica: record eliminato correttamente')
                else:
                    print('Verifica: record ancora presente!')
            else:
                print('Eliminazione fallita - returned None')
        except Exception as e:
            print(f'Errore eliminazione: {e}')
    else:
        print('Record non trovato nel DataFrame')

if __name__ == "__main__":
    debug_operations() 