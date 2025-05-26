import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
import os

Base = declarative_base()

def migrate_database_if_needed():
    """
    Controlla e aggiunge le colonne mancanti al database esistente
    """
    db_path = "diarioalimentare.sqlite"
    
    if not os.path.exists(db_path):
        return  # Il database verrà creato automaticamente
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Controlla le colonne esistenti
        cursor.execute("PRAGMA table_info(diario_alimentare)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Aggiungi colonne mancanti
        if 'note' not in columns:
            cursor.execute("ALTER TABLE diario_alimentare ADD COLUMN note TEXT")
            
        if 'dosi_correttive' not in columns:
            cursor.execute("ALTER TABLE diario_alimentare ADD COLUMN dosi_correttive REAL")
            
        if 'tempo_dose_correttiva' not in columns:
            cursor.execute("ALTER TABLE diario_alimentare ADD COLUMN tempo_dose_correttiva INTEGER")
            
        conn.commit()
        conn.close()
    except Exception:
        pass  # Ignora errori, SQLAlchemy gestirà la creazione

## create a local sqlite database
def create_database():
    engine = sqlalchemy.create_engine("sqlite:///diarioalimentare.sqlite")
    migrate_database_if_needed()
    Base.metadata.create_all(engine)
    return engine

def get_engine():
    engine = sqlalchemy.create_engine("sqlite:///diarioalimentare.sqlite")
    # Assicurati che le tabelle esistano e siano aggiornate
    migrate_database_if_needed()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

## create a table
class DiarioAlimentare(Base):
    __tablename__ = "diario_alimentare"
    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    pasto = Column(String)
    alimento = Column(String)
    quantita = Column(Float)
    unita_misura = Column(String)
    carboidrati = Column(Float)
    glicemia_iniziale = Column(Float)
    glicemia_dopo_2h = Column(Float)
    unita_insulina = Column(Float)
    insulina_attiva = Column(Float)
    note = Column(Text)
    dosi_correttive = Column(Float)
    tempo_dose_correttiva = Column(Integer)  # minuti dopo la dose principale

    @classmethod
    def aggiungi_record(cls, data, pasto, alimento, quantita, unita_misura, 
                       carboidrati, glicemia_iniziale, glicemia_dopo_2h=None, 
                       unita_insulina=None, insulina_attiva=None, note=None, 
                       dosi_correttive=None, tempo_dose_correttiva=None):
        session = get_session()
        try:
            nuovo_record = cls(
                data=data,
                pasto=pasto,
                alimento=alimento,
                quantita=quantita,
                unita_misura=unita_misura,
                carboidrati=carboidrati,
                glicemia_iniziale=glicemia_iniziale,
                glicemia_dopo_2h=glicemia_dopo_2h,
                unita_insulina=unita_insulina,
                insulina_attiva=insulina_attiva,
                note=note,
                dosi_correttive=dosi_correttive,
                tempo_dose_correttiva=tempo_dose_correttiva
            )
            session.add(nuovo_record)
            session.commit()
            # Refresh per ottenere l'ID generato
            session.refresh(nuovo_record)
            # Crea un nuovo oggetto con i dati per evitare problemi di sessione
            record_data = {
                'id': nuovo_record.id,
                'data': nuovo_record.data,
                'pasto': nuovo_record.pasto,
                'alimento': nuovo_record.alimento,
                'quantita': nuovo_record.quantita,
                'unita_misura': nuovo_record.unita_misura,
                'carboidrati': nuovo_record.carboidrati,
                'glicemia_iniziale': nuovo_record.glicemia_iniziale,
                'glicemia_dopo_2h': nuovo_record.glicemia_dopo_2h,
                'unita_insulina': nuovo_record.unita_insulina,
                'insulina_attiva': nuovo_record.insulina_attiva,
                'note': nuovo_record.note,
                'dosi_correttive': nuovo_record.dosi_correttive,
                'tempo_dose_correttiva': nuovo_record.tempo_dose_correttiva
            }
            return record_data
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def ottieni_tutti_record(cls):
        session = get_session()
        try:
            records = session.query(cls).order_by(cls.data.desc()).all()
            # Converti in dizionari per evitare problemi di sessione
            result = []
            for record in records:
                result.append({
                    'id': record.id,
                    'data': record.data,
                    'pasto': record.pasto,
                    'alimento': record.alimento,
                    'quantita': record.quantita,
                    'unita_misura': record.unita_misura,
                    'carboidrati': record.carboidrati,
                    'glicemia_iniziale': record.glicemia_iniziale,
                    'glicemia_dopo_2h': record.glicemia_dopo_2h,
                    'unita_insulina': record.unita_insulina,
                    'insulina_attiva': record.insulina_attiva,
                    'note': record.note,
                    'dosi_correttive': record.dosi_correttive,
                    'tempo_dose_correttiva': record.tempo_dose_correttiva
                })
            return result
        except Exception as e:
            raise e
        finally:
            session.close()

    @classmethod
    def ottieni_record_per_data(cls, data):
        session = get_session()
        try:
            records = session.query(cls).filter(cls.data == data).all()
            # Converti in dizionari per evitare problemi di sessione
            result = []
            for record in records:
                result.append({
                    'id': record.id,
                    'data': record.data,
                    'pasto': record.pasto,
                    'alimento': record.alimento,
                    'quantita': record.quantita,
                    'unita_misura': record.unita_misura,
                    'carboidrati': record.carboidrati,
                    'glicemia_iniziale': record.glicemia_iniziale,
                    'glicemia_dopo_2h': record.glicemia_dopo_2h,
                    'unita_insulina': record.unita_insulina,
                    'insulina_attiva': record.insulina_attiva,
                    'note': record.note,
                    'dosi_correttive': record.dosi_correttive,
                    'tempo_dose_correttiva': record.tempo_dose_correttiva
                })
            return result
        except Exception as e:
            raise e
        finally:
            session.close()

    @classmethod
    def aggiorna_record(cls, id, **kwargs):
        session = get_session()
        try:
            record = session.query(cls).filter(cls.id == int(id)).first()
            if not record:
                return None
            
            # Lista dei campi aggiornabili (esclude id che è primary key)
            campi_aggiornabili = {
                'data', 'pasto', 'alimento', 'quantita', 'unita_misura', 
                'carboidrati', 'glicemia_iniziale', 'glicemia_dopo_2h', 
                'unita_insulina', 'insulina_attiva', 'note', 'dosi_correttive',
                'tempo_dose_correttiva'
            }
            
            # Valida che i campi siano aggiornabili
            for key in kwargs.keys():
                if key not in campi_aggiornabili:
                    raise ValueError(f"Campo '{key}' non è aggiornabile")
            
            # Aggiorna solo i campi validi
            for key, value in kwargs.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            
            session.commit()
            session.refresh(record)
            
            # Restituisci i dati aggiornati
            updated_data = {
                'id': record.id,
                'data': record.data,
                'pasto': record.pasto,
                'alimento': record.alimento,
                'quantita': record.quantita,
                'unita_misura': record.unita_misura,
                'carboidrati': record.carboidrati,
                'glicemia_iniziale': record.glicemia_iniziale,
                'glicemia_dopo_2h': record.glicemia_dopo_2h,
                'unita_insulina': record.unita_insulina,
                'insulina_attiva': record.insulina_attiva,
                'note': record.note,
                'dosi_correttive': record.dosi_correttive,
                'tempo_dose_correttiva': record.tempo_dose_correttiva
            }
            return updated_data
            
        except ValueError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Errore durante l'aggiornamento del record: {str(e)}")
        finally:
            session.close()

    @classmethod
    def elimina_record(cls, id):
        session = get_session()
        id=int(id)
        try:
            record = session.query(cls).filter(cls.id == id).first()
            if record:
                # Salva i dati prima di eliminare
                deleted_data = {
                    'id': record.id,
                    'data': record.data,
                    'pasto': record.pasto,
                    'alimento': record.alimento,
                    'quantita': record.quantita,
                    'unita_misura': record.unita_misura,
                    'carboidrati': record.carboidrati,
                    'glicemia_iniziale': record.glicemia_iniziale,
                    'glicemia_dopo_2h': record.glicemia_dopo_2h,
                    'unita_insulina': record.unita_insulina,
                    'insulina_attiva': record.insulina_attiva,
                    'note': record.note,
                    'dosi_correttive': record.dosi_correttive,
                    'tempo_dose_correttiva': record.tempo_dose_correttiva
                }
                session.delete(record)
                session.commit()
                return deleted_data
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return f"<DiarioAlimentare(id={self.id}, data={self.data}, alimento={self.alimento})>"