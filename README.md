# 🍽️ Diario Alimentare

Un'applicazione web per tenere traccia dell'alimentazione e della glicemia, sviluppata con Streamlit e SQLAlchemy.

## 🚀 Funzionalità

- **📝 Aggiungi Record**: Inserisci nuovi pasti con dettagli su alimenti, quantità, carboidrati e glicemia
- **📊 Visualizza Dati**: Consulta tutti i record con filtri per data e tipo di pasto
- **✏️ Modifica Record**: Aggiorna i record esistenti
- **🗑️ Elimina Record**: Rimuovi record non più necessari
- **📈 Analisi**: Visualizza grafici e statistiche sui tuoi dati alimentari
- **📥 Export Excel**: Scarica i tuoi dati in formato Excel

## 📋 Requisiti

- Python 3.8+
- Le dipendenze sono elencate in `requirements.txt`

## 🛠️ Installazione

1. Clona il repository:
```bash
git clone <url-repository>
cd DiarioAlimentare
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## 🎯 Utilizzo

```bash
cd src
streamlit run main.py
```

L'applicazione si aprirà automaticamente nel browser all'indirizzo `http://localhost:8501`

## 📊 Struttura del Database

Il database SQLite (`diarioalimentare.db`) contiene una tabella con i seguenti campi:

- **ID**: Identificativo univoco
- **Data**: Data e ora del pasto
- **Pasto**: Tipo di pasto (Colazione, Pranzo, Cena, etc.)
- **Alimento**: Nome dell'alimento
- **Quantità**: Quantità consumata
- **Unità di Misura**: Unità (g, ml, porzione, etc.)
- **Carboidrati**: Grammi di carboidrati
- **Glicemia Iniziale**: Valore glicemico prima del pasto
- **Glicemia dopo 2h**: Valore glicemico dopo 2 ore (opzionale)
- **Unità Insulina**: Unità di insulina somministrata (opzionale)
- **Insulina Attiva**: Insulina ancora attiva (opzionale)

## 📈 Analisi Disponibili

- Andamento della glicemia nel tempo
- Distribuzione dei pasti
- Media carboidrati per tipo di pasto
- Alimenti più frequenti
- Matrice di correlazione tra variabili numeriche

## 🔧 Struttura del Progetto

```
DiarioAlimentare/
├── src/
│   ├── main.py                 # Applicazione Streamlit principale
│   └── database/
│       └── diario_alimentare.py # Modelli database e operazioni CRUD
├── requirements.txt            # Dipendenze Python
├── run_app.py                 # Script di avvio
└── README.md                  # Questo file
```

## 💡 Suggerimenti d'Uso

1. **Inserimento Dati**: Compila almeno i campi obbligatori (alimento, quantità, carboidrati, glicemia iniziale)
2. **Filtri**: Usa i filtri nella sezione "Visualizza Dati" per analizzare periodi specifici
3. **Export**: Scarica i dati in Excel per analisi esterne o backup
4. **Analisi**: Consulta regolarmente la sezione "Analisi" per identificare pattern nei tuoi dati

## 🐛 Risoluzione Problemi

- **Database non trovato**: Il database viene creato automaticamente al primo avvio
- **Errori di dipendenze**: Assicurati di aver installato tutti i pacchetti in `requirements.txt`
- **Porta occupata**: Se la porta 8501 è occupata, Streamlit ne sceglierà automaticamente un'altra

## 📝 Note

- I dati vengono salvati localmente nel file `diarioalimentare.db`
- L'applicazione è progettata per uso personale
- Fai backup regolari del database per sicurezza
