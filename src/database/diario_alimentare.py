import supabase
import os
from typing import Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/Users/carlo/Desktop/SideQuests/DiarioAlimentare/.env")

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_API_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL e SUPABASE_API_KEY devono essere impostati nelle variabili d'ambiente")

supabase_client = supabase.create_client(supabase_url, supabase_key)

class DiarioAlimentareDB:
    """Classe per gestire le operazioni CRUD sulla tabella DiarioAlimentare"""
    
    TABLE_NAME = "DiarioAlimentare"
    
    @staticmethod
    def create_entry(
        data: datetime,
        pasto: Optional[str] = None,
        alimento: Optional[str] = None,
        quantita: Optional[int] = None,
        unita_misura: Optional[str] = None,
        carboidrati: Optional[float] = None,
        glicemia_iniziale: Optional[int] = None,
        glicemia_dop_2h: Optional[int] = None,
        unita_insulina: Optional[float] = None,
        note: Optional[str] = None,
        dosi_correttive: Optional[float] = None,
        tempo_dosi_correttive: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Crea una nuova voce nel diario alimentare
        
        Args:
            data: Data e ora del pasto (obbligatorio)
            pasto: Tipo di pasto (colazione, pranzo, cena, spuntino)
            alimento: Nome dell'alimento
            quantita: Quantità dell'alimento
            unita_misura: Unità di misura (g, ml, porzioni, etc.)
            carboidrati: Grammi di carboidrati
            glicemia_iniziale: Valore glicemia prima del pasto
            glicemia_dop_2h: Valore glicemia dopo 2 ore
            unita_insulina: Unità di insulina somministrate
            note: Note aggiuntive
            dosi_correttive: Dosi correttive di insulina
            tempo_dosi_correttive: Tempo delle dosi correttive in minuti
            
        Returns:
            Dict con i dati della voce creata o errore
        """
        try:
            entry_data = {
                "data": data.isoformat(),
                "pasto": pasto,
                "alimento": alimento,
                "quantita": quantita,
                "unita_misura": unita_misura,
                "carboidrati": carboidrati,
                "glicemia_iniziale": glicemia_iniziale,
                "glicemia_dop_2h": glicemia_dop_2h,
                "unita_insulina": unita_insulina,
                "note": note,
                "dosi_correttive": dosi_correttive,
                "tempo_dosi_correttive": tempo_dosi_correttive
            }
            
            # Rimuovi i campi None per non inserire valori null non necessari
            entry_data = {k: v for k, v in entry_data.items() if v is not None}
            
            response = supabase_client.table(DiarioAlimentareDB.TABLE_NAME).insert(entry_data).execute()
            
            if response.data:
                return {"success": True, "data": response.data[0]}
            else:
                return {"success": False, "error": "Errore durante l'inserimento"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_entry_by_id(entry_id: int) -> Dict[str, Any]:
        """
        Recupera una voce specifica per ID
        
        Args:
            entry_id: ID della voce da recuperare
            
        Returns:
            Dict con i dati della voce o errore
        """
        try:
            response = supabase_client.table(DiarioAlimentareDB.TABLE_NAME).select("*").eq("id", entry_id).execute()
            
            if response.data:
                return {"success": True, "data": response.data[0]}
            else:
                return {"success": False, "error": "Voce non trovata"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_all_entries(limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """
        Recupera tutte le voci del diario alimentare
        
        Args:
            limit: Numero massimo di voci da recuperare
            offset: Numero di voci da saltare (per paginazione)
            
        Returns:
            Dict con lista delle voci o errore
        """
        try:
            query = supabase_client.table(DiarioAlimentareDB.TABLE_NAME).select("*").order("data", desc=True)
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
                
            response = query.execute()
            
            return {"success": True, "data": response.data, "count": len(response.data)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_entries_by_date_range(
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Recupera le voci in un intervallo di date
        
        Args:
            start_date: Data di inizio
            end_date: Data di fine
            
        Returns:
            Dict con lista delle voci o errore
        """
        try:
            response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                       .select("*")
                       .gte("data", start_date.isoformat())
                       .lte("data", end_date.isoformat())
                       .order("data", desc=True)
                       .execute())
            
            return {"success": True, "data": response.data, "count": len(response.data)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_entries_by_meal_type(pasto: str) -> Dict[str, Any]:
        """
        Recupera le voci per tipo di pasto
        
        Args:
            pasto: Tipo di pasto da filtrare
            
        Returns:
            Dict con lista delle voci o errore
        """
        try:
            response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                       .select("*")
                       .eq("pasto", pasto)
                       .order("data", desc=True)
                       .execute())
            
            return {"success": True, "data": response.data, "count": len(response.data)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update_entry(entry_id: int, **kwargs) -> Dict[str, Any]:
        """
        Aggiorna una voce esistente
        
        Args:
            entry_id: ID della voce da aggiornare
            **kwargs: Campi da aggiornare
            
        Returns:
            Dict con i dati aggiornati o errore
        """
        try:
            # Rimuovi i campi None
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            
            if not update_data:
                return {"success": False, "error": "Nessun campo da aggiornare"}
            
            # Converti datetime in ISO string se presente
            if "data" in update_data and isinstance(update_data["data"], datetime):
                update_data["data"] = update_data["data"].isoformat()
            
            response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                       .update(update_data)
                       .eq("id", entry_id)
                       .execute())
            
            if response.data:
                return {"success": True, "data": response.data[0]}
            else:
                return {"success": False, "error": "Voce non trovata o non aggiornata"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_entry(entry_id: int) -> Dict[str, Any]:
        """
        Elimina una voce dal diario alimentare
        
        Args:
            entry_id: ID della voce da eliminare
            
        Returns:
            Dict con risultato dell'operazione
        """
        try:
            response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                       .delete()
                       .eq("id", entry_id)
                       .execute())
            
            if response.data:
                return {"success": True, "message": "Voce eliminata con successo"}
            else:
                return {"success": False, "error": "Voce non trovata"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def search_entries(search_term: str, field: str = "alimento") -> Dict[str, Any]:
        """
        Cerca voci per termine di ricerca
        
        Args:
            search_term: Termine da cercare
            field: Campo in cui cercare (default: alimento)
            
        Returns:
            Dict con lista delle voci trovate o errore
        """
        try:
            response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                       .select("*")
                       .ilike(field, f"%{search_term}%")
                       .order("data", desc=True)
                       .execute())
            
            return {"success": True, "data": response.data, "count": len(response.data)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """
        Recupera statistiche generali del diario alimentare
        
        Returns:
            Dict con statistiche o errore
        """
        try:
            # Conta totale voci
            total_response = supabase_client.table(DiarioAlimentareDB.TABLE_NAME).select("id", count="exact").execute()
            total_entries = total_response.count
            
            # Conta voci per tipo di pasto
            meals_response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                             .select("pasto", count="exact")
                             .execute())
            
            # Calcola media carboidrati
            carbs_response = (supabase_client.table(DiarioAlimentareDB.TABLE_NAME)
                             .select("carboidrati")
                             .not_.is_("carboidrati", "null")
                             .execute())
            
            avg_carbs = 0
            if carbs_response.data:
                carbs_values = [entry["carboidrati"] for entry in carbs_response.data if entry["carboidrati"]]
                avg_carbs = sum(carbs_values) / len(carbs_values) if carbs_values else 0
            
            return {
                "success": True,
                "data": {
                    "total_entries": total_entries,
                    "average_carbs": round(avg_carbs, 2),
                    "entries_with_carbs": len(carbs_response.data) if carbs_response.data else 0
                }
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}


# Funzioni di convenienza per uso diretto
def crea_voce_diario(**kwargs):
    """Funzione di convenienza per creare una voce"""
    return DiarioAlimentareDB.create_entry(**kwargs)

def ottieni_voce(entry_id: int):
    """Funzione di convenienza per ottenere una voce"""
    return DiarioAlimentareDB.get_entry_by_id(entry_id)

def ottieni_tutte_voci(limit=None, offset=None):
    """Funzione di convenienza per ottenere tutte le voci"""
    return DiarioAlimentareDB.get_all_entries(limit, offset)

def aggiorna_voce(entry_id: int, **kwargs):
    """Funzione di convenienza per aggiornare una voce"""
    return DiarioAlimentareDB.update_entry(entry_id, **kwargs)

def elimina_voce(entry_id: int):
    """Funzione di convenienza per eliminare una voce"""
    return DiarioAlimentareDB.delete_entry(entry_id)

def cerca_voci(search_term: str, field="alimento"):
    """Funzione di convenienza per cercare voci"""
    return DiarioAlimentareDB.search_entries(search_term, field)


