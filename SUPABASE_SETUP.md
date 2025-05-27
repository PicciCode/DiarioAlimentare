# Configurazione Supabase per Diario Alimentare

## Prerequisiti

1. Account Supabase (gratuito su [supabase.com](https://supabase.com))
2. Progetto Supabase creato

## Configurazione

### 1. Crea un nuovo progetto su Supabase

1. Vai su [supabase.com](https://supabase.com) e accedi
2. Clicca su "New Project"
3. Scegli un nome per il progetto (es. "diario-alimentare")
4. Imposta una password sicura per il database
5. Seleziona una regione vicina a te

### 2. Ottieni l'URL del database

Nel dashboard del tuo progetto Supabase:

1. Vai su **Settings** → **Database**
2. Nella sezione **Connection string**, copia l'**URI** 
3. Sostituisci `[YOUR-PASSWORD]` con la password del database che hai impostato

### 3. Configura le variabili d'ambiente

1. Copia il file `env.example` in `.env`:
   ```bash
   cp env.example .env
   ```

2. Modifica il file `.env` con il tuo URL del database:
   ```
   SUPABASE_DB_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
   ```

### 4. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 5. Inizializza il database

Il database e le tabelle verranno create automaticamente al primo avvio dell'applicazione.

## Migrazione dei dati esistenti (opzionale)

Se hai già dati nel database SQLite locale, puoi utilizzare lo script di migrazione:

```bash
python migrate_to_supabase.py
```

## Vantaggi di Supabase

- **Database cloud**: I tuoi dati sono accessibili da qualsiasi dispositivo
- **Backup automatici**: Supabase gestisce automaticamente i backup
- **Scalabilità**: Il database può crescere con le tue esigenze
- **Sicurezza**: Connessioni crittografate e gestione delle autorizzazioni
- **Dashboard**: Interfaccia web per visualizzare e gestire i dati

## Come funziona

L'applicazione utilizza **SQLAlchemy** per connettersi direttamente al database PostgreSQL di Supabase. Non è necessario utilizzare l'API REST di Supabase o le sue chiavi API - SQLAlchemy gestisce tutto attraverso la connessione PostgreSQL standard.

## Risoluzione problemi

### Errore di connessione
- Verifica che la variabile `SUPABASE_DB_URL` sia configurata correttamente
- Controlla che la password del database sia corretta
- Assicurati che il progetto Supabase sia attivo

### Tabelle non create
- Le tabelle vengono create automaticamente al primo avvio
- Se ci sono errori, controlla i log dell'applicazione

### Errore di autenticazione PostgreSQL
- Verifica che l'URL del database sia corretto
- Controlla che la password sia quella giusta 