# Diario Alimentare - Funzioni CRUD

Questo modulo fornisce funzioni complete per gestire il diario alimentare su Supabase.

## Configurazione

Prima di utilizzare le funzioni, assicurati di aver impostato le variabili d'ambiente:

```bash
export SUPABASE_URL="your_supabase_url"
export SUPABASE_API_KEY="your_supabase_api_key"
```

## Schema Tabella

La tabella `DiarioAlimentare` ha la seguente struttura:

- `id` (bigint) - Chiave primaria auto-incrementale
- `data` (timestamp) - Data e ora del pasto **[OBBLIGATORIO]**
- `pasto` (text) - Tipo di pasto (colazione, pranzo, cena, spuntino)
- `alimento` (text) - Nome dell'alimento
- `quantità` (bigint) - Quantità dell'alimento
- `unita_misura` (varchar) - Unità di misura (g, ml, porzioni, etc.)
- `carboidrati` (real) - Grammi di carboidrati
- `glicemia_iniziale` (bigint) - Valore glicemia prima del pasto
- `glicemia_dop_2h` (bigint) - Valore glicemia dopo 2 ore
- `unita_insulina` (real) - Unità di insulina somministrate
- `note` (text) - Note aggiuntive
- `dosi_correttive` (real) - Dosi correttive di insulina
- `tempo_dosi_correttive` (bigint) - Tempo delle dosi correttive in minuti

## Utilizzo

### Importazione

```python
from diario_alimentare import DiarioAlimentareDB
# oppure per funzioni più semplici:
from diario_alimentare import crea_voce_diario, ottieni_voce, ottieni_tutte_voci
```

### Operazioni CRUD

#### 1. CREATE - Creare una nuova voce

```python
from datetime import datetime

# Metodo classe
risultato = DiarioAlimentareDB.create_entry(
    data=datetime.now(),
    pasto="colazione",
    alimento="fette biscottate",
    quantita=40,
    unita_misura="g",
    carboidrati=28.5,
    glicemia_iniziale=95,
    unita_insulina=2.5,
    note="Colazione con marmellata"
)

# Funzione di convenienza
risultato = crea_voce_diario(
    data=datetime.now(),
    pasto="pranzo",
    alimento="pasta",
    quantita=80,
    carboidrati=56.0
)

if risultato["success"]:
    print(f"Voce creata con ID: {risultato['data']['id']}")
else:
    print(f"Errore: {risultato['error']}")
```

#### 2. READ - Leggere voci

```python
# Leggere una voce specifica
voce = DiarioAlimentareDB.get_entry_by_id(1)

# Leggere tutte le voci (con paginazione)
tutte_voci = DiarioAlimentareDB.get_all_entries(limit=10, offset=0)

# Leggere voci per intervallo di date
from datetime import datetime, timedelta
ieri = datetime.now() - timedelta(days=1)
oggi = datetime.now()
voci_recenti = DiarioAlimentareDB.get_entries_by_date_range(ieri, oggi)

# Leggere voci per tipo di pasto
colazioni = DiarioAlimentareDB.get_entries_by_meal_type("colazione")

# Cercare voci
ricerca = DiarioAlimentareDB.search_entries("pasta", field="alimento")
```

#### 3. UPDATE - Aggiornare una voce

```python
# Aggiornare campi specifici
risultato = DiarioAlimentareDB.update_entry(
    entry_id=1,
    glicemia_dop_2h=120,
    note="Aggiunta glicemia dopo 2 ore"
)

# Funzione di convenienza
risultato = aggiorna_voce(1, carboidrati=30.0, note="Carboidrati corretti")
```

#### 4. DELETE - Eliminare una voce

```python
risultato = DiarioAlimentareDB.delete_entry(1)

# Funzione di convenienza
risultato = elimina_voce(1)
```

### Funzioni Aggiuntive

#### Statistiche

```python
stats = DiarioAlimentareDB.get_statistics()
if stats["success"]:
    print(f"Totale voci: {stats['data']['total_entries']}")
    print(f"Media carboidrati: {stats['data']['average_carbs']}g")
```

#### Ricerca Avanzata

```python
# Cerca in diversi campi
ricerca_alimenti = DiarioAlimentareDB.search_entries("pasta", field="alimento")
ricerca_note = DiarioAlimentareDB.search_entries("marmellata", field="note")
```

## Gestione Errori

Tutte le funzioni restituiscono un dizionario con:
- `success` (bool) - Indica se l'operazione è riuscita
- `data` - I dati restituiti (se success=True)
- `error` - Messaggio di errore (se success=False)
- `count` - Numero di record (per operazioni di lettura multipla)

```python
risultato = DiarioAlimentareDB.get_all_entries()
if risultato["success"]:
    print(f"Trovate {risultato['count']} voci")
    for voce in risultato['data']:
        print(voce['alimento'])
else:
    print(f"Errore: {risultato['error']}")
```

## Esempi Completi

Vedi il file `esempio_utilizzo.py` per esempi completi di utilizzo di tutte le funzioni.

## Note Importanti

1. **Data obbligatoria**: Il campo `data` è l'unico campo obbligatorio
2. **Formato date**: Usa oggetti `datetime` di Python, verranno convertiti automaticamente
3. **Gestione null**: I campi con valore `None` non vengono inseriti nel database
4. **Ordinamento**: Le voci vengono restituite ordinate per data (più recenti prima)
5. **Paginazione**: Usa `limit` e `offset` per gestire grandi quantità di dati

## Tipi di Pasto Suggeriti

- "colazione"
- "pranzo" 
- "cena"
- "spuntino"
- "merenda"

## Unità di Misura Suggerite

- "g" (grammi)
- "ml" (millilitri)
- "porzioni"
- "fette"
- "cucchiai"
- "cucchiaini" 