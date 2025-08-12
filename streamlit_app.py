import io
import json
import requests
import streamlit as st

st.set_page_config(page_title="CSI API - Frontend", layout="wide")
st.title("CSI API — Interface simple (Streamlit)")

# ---- Configuration ----
default_api = st.secrets.get("API_BASE_URL", "http://localhost:8080").rstrip("/")
api_base = st.text_input("URL de l'API CSI", value=default_api, help="Ex: https://mon-api.exemple.com ou http://localhost:8080")
analyze_url = f"{api_base}/analyze/"
categories_url = f"{api_base}/categories/weights"
export_rules_csv_url = f"{api_base}/export/rules.csv"
export_categories_csv_url = f"{api_base}/export/categories.csv"

st.divider()

# ---- Analyse de document ----
st.header("1) Analyser un document")
col1, col2 = st.columns([2,1])
with col1:
    up = st.file_uploader("Fichier à analyser (.txt, .pdf, .docx)", type=["txt","pdf","docx"])
with col2:
    export_pdf = st.toggle("Générer le PDF de rapport", value=False)

if st.button("Lancer l'analyse", type="primary", disabled=(up is None)):
    if up is None:
        st.warning("Choisis un fichier d'abord.")
    else:
        files = {"file": (up.name, up.getvalue())}
        data = {"export_pdf": str(export_pdf).lower()}
        with st.spinner("Analyse en cours..."):
            try:
                resp = requests.post(analyze_url, files=files, data=data, timeout=180)
                if resp.ok:
                    res = resp.json()
                    st.success("Analyse terminée ✅")
                    st.subheader("Résumé")
                    st.write(res.get("summary"))
                    st.subheader("Statistiques")
                    st.json(res.get("stats", {}))
                    st.subheader("Manquements détectés")
                    st.json(res.get("findings", []))
                    # Lien vers PDF (si demandé)
                    pdf_path = res.get("report_pdf_path")
                    if pdf_path:
                        st.info("Un rapport PDF a été généré sur le serveur (champ `report_pdf_path`).")
                        st.code(pdf_path)
                        st.caption("Astuce: expose un endpoint /analyze/report?path=... pour le télécharger depuis l'interface.")
                else:
                    st.error(f"Erreur {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Appel à l'API impossible: {e}")

st.divider()

# ---- Catégories & poids ----
st.header("2) Catégories — poids courants")
if st.button("Rafraîchir les poids de catégories"):
    try:
        r = requests.get(categories_url, timeout=60)
        if r.ok:
            st.json(r.json())
        else:
            st.error(f"Erreur {r.status_code}: {r.text}")
    except Exception as e:
        st.error(f"Impossible d'interroger {categories_url}: {e}")

# ---- Exports CSV ----
st.header("3) Exports CSV")
c1, c2 = st.columns(2)
with c1:
    if st.button("Télécharger rules.csv"):
        try:
            r = requests.get(export_rules_csv_url, timeout=60)
            if r.ok:
                st.download_button("Sauvegarder rules.csv", data=r.content, file_name="rules.csv", mime="text/csv")
            else:
                st.error(f"Erreur {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"Impossible de récupérer rules.csv: {e}")
with c2:
    if st.button("Télécharger categories.csv"):
        try:
            r = requests.get(export_categories_csv_url, timeout=60)
            if r.ok:
                st.download_button("Sauvegarder categories.csv", data=r.content, file_name="categories.csv", mime="text/csv")
            else:
                st.error(f"Erreur {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"Impossible de récupérer categories.csv: {e}")

st.divider()
st.caption("Frontend Streamlit minimal — relie-toi à ton instance de CSI API via l'URL ci-dessus.")