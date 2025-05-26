import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
from database.diario_alimentare import DiarioAlimentare
import io

# Configurazione della pagina
st.set_page_config(
    page_title="Diario Alimentare",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titolo principale
st.title("🍽️ Diario Alimentare")
st.markdown("---")

# Sidebar per la navigazione
st.sidebar.title("Navigazione")
pagina = st.sidebar.selectbox(
    "Seleziona una pagina:",
    ["📝 Aggiungi Record", "📊 Visualizza Dati", "✏️ Modifica Record", "🗑️ Elimina Record", "📈 Analisi"]
)

# Funzione per convertire DataFrame in Excel

def converti_in_excel(df):
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='Diario_Alimentare')
    return output.getvalue()

# Funzione per ottenere tutti i dati come DataFrame
def ottieni_dati_come_df():
    try:
        records = DiarioAlimentare.ottieni_tutti_record()
        if records:
            data = []
            for record in records:
                # Ora i record sono già dizionari
                data.append({
                    'ID': record['id'],
                    'Data': record['data'],
                    'Pasto': record['pasto'],
                    'Alimento': record['alimento'],
                    'Quantità': record['quantita'],
                    'Unità di Misura': record['unita_misura'],
                    'Carboidrati (g)': record['carboidrati'],
                    'Glicemia Iniziale': record['glicemia_iniziale'],
                    'Glicemia dopo 2h': record['glicemia_dopo_2h'],
                    'Unità Insulina': record['unita_insulina'],
                    'Insulina Attiva': record['insulina_attiva'],
                    'Dosi Correttive': record['dosi_correttive'],
                    'Tempo Dose Correttiva (min)': record['tempo_dose_correttiva'],
                    'Note': record['note']
                })
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Errore nel recuperare i dati: {e}")
        return pd.DataFrame()

# PAGINA: Aggiungi Record
if pagina == "📝 Aggiungi Record":
    st.header("Aggiungi Nuovo Record")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_input = st.date_input("Data", value=date.today())
        pasto = st.selectbox("Pasto", ["Colazione", "Spuntino Mattina", "Pranzo", "Merenda", "Cena", "Spuntino Sera"])
        alimento = st.text_input("Alimento")
        quantita = st.number_input("Quantità", min_value=0.0, step=0.1)
        unita_misura = st.selectbox("Unità di Misura", ["g", "ml", "porzione", "cucchiaio", "cucchiaino", "tazza"])
        carboidrati = st.number_input("Carboidrati (g)", min_value=0.0, step=0.1)
    
    with col2:
        glicemia_iniziale = st.number_input("Glicemia Iniziale (mg/dl)", min_value=0.0, step=1.0)
        glicemia_dopo_2h = st.number_input("Glicemia dopo 2h (mg/dl)", min_value=0.0, step=1.0, value=0.0)
        unita_insulina = st.number_input("Unità Insulina", min_value=0.0, step=0.1, value=0.0)
        insulina_attiva = st.number_input("Insulina Attiva", min_value=0.0, step=0.1, value=0.0)
        dosi_correttive = st.number_input("Dosi Correttive", min_value=0.0, step=0.1, value=0.0)
        tempo_dose_correttiva = st.number_input("Tempo Dose Correttiva (minuti)", min_value=0, step=1, value=0, 
                                               help="Minuti trascorsi tra la dose principale e quella correttiva")
    
    # Campo note a tutta larghezza
    note = st.text_area("Note personali", placeholder="Inserisci qui le tue note personali (es. come ti sei sentito, reazioni particolari, ecc.)", height=100)
    
    if st.button("Aggiungi Record", type="primary"):
        if alimento and quantita > 0:
            try:
                data_datetime = datetime.combine(data_input, datetime.min.time())
                DiarioAlimentare.aggiungi_record(
                    data=data_datetime,
                    pasto=pasto,
                    alimento=alimento,
                    quantita=quantita,
                    unita_misura=unita_misura,
                    carboidrati=carboidrati,
                    glicemia_iniziale=glicemia_iniziale,
                    glicemia_dopo_2h=glicemia_dopo_2h if glicemia_dopo_2h > 0 else None,
                    unita_insulina=unita_insulina if unita_insulina > 0 else None,
                    insulina_attiva=insulina_attiva if insulina_attiva > 0 else None,
                    note=note if note.strip() else None,
                    dosi_correttive=dosi_correttive if dosi_correttive > 0 else None,
                    tempo_dose_correttiva=tempo_dose_correttiva if tempo_dose_correttiva > 0 else None
                )
                st.success("Record aggiunto con successo!")
                st.rerun()
            except Exception as e:
                st.error(f"Errore nell'aggiungere il record: {e}")
        else:
            st.error("Inserisci almeno l'alimento e la quantità!")

# PAGINA: Visualizza Dati
elif pagina == "📊 Visualizza Dati":
    st.header("Visualizza Dati")
    
    df = ottieni_dati_come_df()
    
    if not df.empty:
        
        
        
        # Mostra tabella
        st.subheader("Tabella Dati")
        st.dataframe(df, use_container_width=True,hide_index=True)
        
        # Pulsante download Excel
        if not df.empty:
            excel_data = converti_in_excel(df)
            st.download_button(
                label="📥 Scarica come Excel",
                data=excel_data,
                file_name=f"diario_alimentare_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # Statistiche rapide
        st.subheader("Statistiche Rapide")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Totale Record", len(df))
        with col2:
            st.metric("Media Glicemia Iniziale", f"{df['Glicemia Iniziale'].mean():.1f} mg/dl")
        with col3:
            carboidrati_totali = df['Carboidrati (g)'].sum()
            st.metric("Carboidrati Totali", f"{carboidrati_totali:.1f} g")
        with col4:
            dosi_correttive_totali = df['Dosi Correttive'].sum()
            st.metric("Dosi Correttive Totali", f"{dosi_correttive_totali:.1f} U")
    else:
        st.info("Nessun dato disponibile. Aggiungi alcuni record per iniziare!")

# PAGINA: Modifica Record
elif pagina == "✏️ Modifica Record":
    st.header("Modifica Record")
    
    df = ottieni_dati_come_df()
    
    if not df.empty:
        # Selezione record da modificare
        record_selezionato = st.selectbox(
            "Seleziona record da modificare:",
            options=df.index,
            format_func=lambda x: f"ID {df.loc[x, 'ID']} - {df.loc[x, 'Data'].strftime('%d/%m/%Y')} - {df.loc[x, 'Alimento']}"
        )
        
        if record_selezionato is not None:
            record = df.loc[record_selezionato]
            
            col1, col2 = st.columns(2)
            
            with col1:
                nuova_data = st.date_input("Data", value=record['Data'].date())
                nuovo_pasto = st.selectbox("Pasto", ["Colazione", "Spuntino Mattina", "Pranzo", "Merenda", "Cena", "Spuntino Sera"], 
                                         index=["Colazione", "Spuntino Mattina", "Pranzo", "Merenda", "Cena", "Spuntino Sera"].index(record['Pasto']))
                nuovo_alimento = st.text_input("Alimento", value=record['Alimento'])
                nuova_quantita = st.number_input("Quantità", min_value=0.0, step=0.1, value=float(record['Quantità']))
                nuova_unita = st.selectbox("Unità di Misura", ["g", "ml", "porzione", "cucchiaio", "cucchiaino", "tazza"],
                                         index=["g", "ml", "porzione", "cucchiaio", "cucchiaino", "tazza"].index(record['Unità di Misura']))
                nuovi_carboidrati = st.number_input("Carboidrati (g)", min_value=0.0, step=0.1, value=float(record['Carboidrati (g)']))
            
            with col2:
                nuova_glicemia_iniziale = st.number_input("Glicemia Iniziale", min_value=0.0, step=1.0, value=float(record['Glicemia Iniziale']))
                nuova_glicemia_2h = st.number_input("Glicemia dopo 2h", min_value=0.0, step=1.0, 
                                                   value=float(record['Glicemia dopo 2h']) if pd.notna(record['Glicemia dopo 2h']) else 0.0)
                nuova_insulina = st.number_input("Unità Insulina", min_value=0.0, step=0.1,
                                                value=float(record['Unità Insulina']) if pd.notna(record['Unità Insulina']) else 0.0)
                nuova_insulina_attiva = st.number_input("Insulina Attiva", min_value=0.0, step=0.1,
                                                       value=float(record['Insulina Attiva']) if pd.notna(record['Insulina Attiva']) else 0.0)
                nuove_dosi_correttive = st.number_input("Dosi Correttive", min_value=0.0, step=0.1,
                                                       value=float(record['Dosi Correttive']) if pd.notna(record['Dosi Correttive']) else 0.0)
                nuovo_tempo_dose_correttiva = st.number_input("Tempo Dose Correttiva (minuti)", min_value=0, step=1, value=int(record['Tempo Dose Correttiva (min)']) if pd.notna(record['Tempo Dose Correttiva (min)']) else 0, 
                                                             help="Minuti trascorsi tra la dose principale e quella correttiva")
            
            # Campo note a tutta larghezza
            nuove_note = st.text_area("Note personali", 
                                     placeholder="Inserisci qui le tue note personali (es. come ti sei sentito, reazioni particolari, ecc.)", 
                                     value=record['Note'] if pd.notna(record['Note']) else "", 
                                     height=100)
            
            if st.button("Aggiorna Record", type="primary"):
                try:
                    nuova_data_datetime = datetime.combine(nuova_data, datetime.min.time())
                    DiarioAlimentare.aggiorna_record(
                        record['ID'],
                        data=nuova_data_datetime,
                        pasto=nuovo_pasto,
                        alimento=nuovo_alimento,
                        quantita=nuova_quantita,
                        unita_misura=nuova_unita,
                        carboidrati=nuovi_carboidrati,
                        glicemia_iniziale=nuova_glicemia_iniziale,
                        glicemia_dopo_2h=nuova_glicemia_2h if nuova_glicemia_2h > 0 else None,
                        unita_insulina=nuova_insulina if nuova_insulina > 0 else None,
                        insulina_attiva=nuova_insulina_attiva if nuova_insulina_attiva > 0 else None,
                        note=nuove_note if nuove_note.strip() else None,
                        dosi_correttive=nuove_dosi_correttive if nuove_dosi_correttive > 0 else None,
                        tempo_dose_correttiva=nuovo_tempo_dose_correttiva if nuovo_tempo_dose_correttiva > 0 else None
                    )
                    st.success("Record aggiornato con successo!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nell'aggiornare il record: {e}")
    else:
        st.info("Nessun record disponibile per la modifica.")

# PAGINA: Elimina Record
elif pagina == "🗑️ Elimina Record":
    st.header("Elimina Record")
    
    df = ottieni_dati_come_df()
    
    if not df.empty:
        # Selezione record da eliminare
        record_da_eliminare = st.selectbox(
            "Seleziona record da eliminare:",
            options=df.index,
            format_func=lambda x: f"ID {df.loc[x, 'ID']} - {df.loc[x, 'Data'].strftime('%d/%m/%Y')} - {df.loc[x, 'Alimento']}"
        )
        
        if record_da_eliminare is not None:
            record = df.loc[record_da_eliminare]
            
            # Mostra dettagli del record
            st.subheader("Dettagli del record da eliminare:")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Data:** {record['Data'].strftime('%d/%m/%Y')}")
                st.write(f"**Pasto:** {record['Pasto']}")
                st.write(f"**Alimento:** {record['Alimento']}")
                st.write(f"**Quantità:** {record['Quantità']} {record['Unità di Misura']}")
            with col2:
                st.write(f"**Carboidrati:** {record['Carboidrati (g)']} g")
                st.write(f"**Glicemia Iniziale:** {record['Glicemia Iniziale']} mg/dl")
                if pd.notna(record['Dosi Correttive']) and record['Dosi Correttive'] > 0:
                    st.write(f"**Dosi Correttive:** {record['Dosi Correttive']} U")
                if pd.notna(record['Tempo Dose Correttiva (min)']) and record['Tempo Dose Correttiva (min)'] > 0:
                    st.write(f"**Tempo Dose Correttiva:** {record['Tempo Dose Correttiva (min)']} minuti")
            
            # Mostra le note se presenti
            if pd.notna(record['Note']) and record['Note'].strip():
                st.write("**Note:**")
                st.info(record['Note'])
            
            st.warning("⚠️ Questa azione non può essere annullata!")
            
            if st.button("🗑️ Elimina Record", type="secondary"):
                try:
                    DiarioAlimentare.elimina_record(record['ID'])
                    st.success("Record eliminato con successo!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nell'eliminare il record: {e}")
    else:
        st.info("Nessun record disponibile per l'eliminazione.")

# PAGINA: Analisi
elif pagina == "📈 Analisi":
    st.header("Analisi dei Dati")
    
    df = ottieni_dati_come_df()
    
    if not df.empty and len(df) > 1:
        # Grafici
        col1, col2 = st.columns(2)
        
        with col1:
            # Grafico glicemia nel tempo
            st.subheader("Andamento Glicemia")
            fig_glicemia = px.line(df, x='Data', y='Glicemia Iniziale', 
                                 title='Glicemia Iniziale nel Tempo',
                                 markers=True)
            if 'Glicemia dopo 2h' in df.columns and df['Glicemia dopo 2h'].notna().any():
                fig_glicemia.add_scatter(x=df['Data'], y=df['Glicemia dopo 2h'], 
                                       mode='lines+markers', name='Glicemia dopo 2h')
            st.plotly_chart(fig_glicemia, use_container_width=True)
        
        with col2:
            # Distribuzione per pasto
            st.subheader("Distribuzione per Pasto")
            pasto_counts = df['Pasto'].value_counts()
            fig_pasto = px.pie(values=pasto_counts.values, names=pasto_counts.index,
                              title='Distribuzione Record per Pasto')
            st.plotly_chart(fig_pasto, use_container_width=True)
        
        # Carboidrati per pasto
        st.subheader("Carboidrati per Pasto")
        carboidrati_per_pasto = df.groupby('Pasto')['Carboidrati (g)'].mean().sort_values(ascending=False)
        fig_carb = px.bar(x=carboidrati_per_pasto.index, y=carboidrati_per_pasto.values,
                         title='Media Carboidrati per Tipo di Pasto',
                         labels={'x': 'Pasto', 'y': 'Carboidrati (g)'})
        st.plotly_chart(fig_carb, use_container_width=True)
        
        # Tabella alimenti più frequenti
        st.subheader("Alimenti Più Frequenti")
        alimenti_freq = df['Alimento'].value_counts().head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(alimenti_freq.to_frame('Frequenza'))
        with col2:
            fig_alimenti = px.bar(x=alimenti_freq.values, y=alimenti_freq.index,
                                 orientation='h', title='Top 10 Alimenti')
            st.plotly_chart(fig_alimenti, use_container_width=True)
        
        # Correlazioni
        if len(df) > 5:
            st.subheader("Correlazioni")
            numeric_cols = ['Quantità', 'Carboidrati (g)', 'Glicemia Iniziale', 'Glicemia dopo 2h', 'Unità Insulina', 'Dosi Correttive', 'Tempo Dose Correttiva (min)']
            corr_data = df[numeric_cols].corr()
            fig_corr = px.imshow(corr_data, text_auto=True, aspect="auto",
                               title='Matrice di Correlazione')
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Analisi Dosi Correttive
        df_correttive = df[df['Dosi Correttive'].notna() & (df['Dosi Correttive'] > 0)]
        if not df_correttive.empty:
            st.subheader("Analisi Dosi Correttive")
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuzione tempi dosi correttive
                if df_correttive['Tempo Dose Correttiva (min)'].notna().any():
                    fig_tempo = px.histogram(df_correttive, x='Tempo Dose Correttiva (min)', 
                                           title='Distribuzione Tempi Dosi Correttive',
                                           labels={'x': 'Minuti', 'y': 'Frequenza'})
                    st.plotly_chart(fig_tempo, use_container_width=True)
            
            with col2:
                # Relazione tra dosi correttive e glicemia
                fig_dosi_glicemia = px.scatter(df_correttive, x='Glicemia Iniziale', y='Dosi Correttive',
                                             title='Relazione Glicemia - Dosi Correttive',
                                             labels={'x': 'Glicemia Iniziale (mg/dl)', 'y': 'Dosi Correttive (U)'})
                st.plotly_chart(fig_dosi_glicemia, use_container_width=True)
            
            # Statistiche dosi correttive
            st.write("**Statistiche Dosi Correttive:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Media Dosi Correttive", f"{df_correttive['Dosi Correttive'].mean():.1f} U")
            with col2:
                tempo_medio = df_correttive['Tempo Dose Correttiva (min)'].mean()
                if pd.notna(tempo_medio):
                    st.metric("Tempo Medio Correzione", f"{tempo_medio:.0f} min")
                else:
                    st.metric("Tempo Medio Correzione", "N/A")
            with col3:
                st.metric("Frequenza Correzioni", f"{len(df_correttive)}/{len(df)} ({len(df_correttive)/len(df)*100:.1f}%)")
    else:
        st.info("Aggiungi più dati per visualizzare le analisi!")

# Footer
st.markdown("---")
st.markdown("💡 **Suggerimento:** Usa il menu laterale per navigare tra le diverse funzionalità dell'app!")
