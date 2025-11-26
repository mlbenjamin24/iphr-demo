import json
import html
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Helper: render two synced scroll panes
# ---------------------------------------------------------
def render_synced_documents(left_text: str, right_text: str, left_label: str, right_label: str, height: int = 500):
    """Render two scrollable text panes that stay in sync vertically."""
    left_esc = html.escape(left_text)
    right_esc = html.escape(right_text)

    html_block = f"""
    <div style="display:flex; gap:16px; width:100%;">
      <div style="flex:1;">
        <div style="font-size:12px; margin-bottom:4px;">{left_label}</div>
        <div id="left-pane" style="
            border:1px solid #ddd;
            padding:8px;
            height:{height}px;
            overflow:auto;
            white-space:pre-wrap;
            font-family:monospace;">
          {left_esc}
        </div>
      </div>
      <div style="flex:1;">
        <div style="font-size:12px; margin-bottom:4px;">{right_label}</div>
        <div id="right-pane" style="
            border:1px solid #ddd;
            padding:8px;
            height:{height}px;
            overflow:auto;
            white-space:pre-wrap;
            font-family:monospace;">
          {right_esc}
        </div>
      </div>
    </div>
    <script>
    const left = document.getElementById("left-pane");
    const right = document.getElementById("right-pane");

    if (left && right) {{
        let syncingFromLeft = false;
        let syncingFromRight = false;

        function syncScroll(from, to, fromFlag, toFlag) {{
            if (fromFlag.current) return;

            fromFlag.current = true;

            const fromMax = from.scrollHeight - from.clientHeight || 1;
            const toMax = to.scrollHeight - to.clientHeight || 1;
            const ratio = from.scrollTop / fromMax;
            to.scrollTop = ratio * toMax;

            fromFlag.current = false;
        }}

        const leftFlag = {{ current: false }};
        const rightFlag = {{ current: false }};

        left.addEventListener("scroll", () => syncScroll(left, right, leftFlag, rightFlag));
        right.addEventListener("scroll", () => syncScroll(right, left, rightFlag, leftFlag));
    }}
    </script>
    """

    components.html(html_block, height=height + 40)

# ---------------------------------------------------------
# Sample data for the demo
# ---------------------------------------------------------

# Turkish sample record
ORIGINAL_TR = """Taburcu Özeti
Tarih: 18/09/2024
Hasta: M. Demir
Doğum Tarihi: 12/05/1984
Dosya No: TKR-44821

Başvuru Nedeni:
Son 3 gündür artan nefes darlığı, göğüs basısı ve alt ekstremite ödemi.

Tanılar:
- Tip 2 Diyabet
- Hipertansiyon
- Hafif konjestif kalp yetmezliği (NYHA Sınıf II)

Alerjiler:
- Penisilin

Laboratuvar Sonuçları:
- HbA1c: 8.4 percent
- Kreatinin: 1.2 mg/dL
- BNP: 210 pg/mL
- Sodyum: 138 mmol/L
- Potasyum: 4.2 mmol/L

Görüntüleme:
Ekokardiyografi: Sol ventrikül ejeksiyon fraksiyonu yaklaşık 45 percent.
Hafif global hipokinezi. Akut patoloji yok.

Reçete / Taburculuk İlaçları:
- Metformin 1000 mg günde iki kez
- Losartan 50 mg günde bir kez
- Furosemid 20 mg günde bir kez
- Atorvastatin 20 mg günde bir kez

Tedavi Özeti:
Hastanın semptomları diüretik tedavi ve kan basıncı kontrolü ile belirgin şekilde
düzeldi. Akut enfeksiyon veya iskemi bulgusu yok. Diyabet düzenli glukoz yönetimi
ile stabil hale getirildi.

Taburculuk Planı:
- Tuz kısıtlı diyet önerildi.
- 1 hafta sonra kardiyoloji kontrolü.
- Evde günlük kilo takibi yapılması.
- Nefes darlığı artışı, kilo alımı veya göğüs ağrısı gelişirse acile başvurması önerildi.
"""

TRANSLATION_TR_EN = """Discharge Summary
Date: 09/18/2024
Patient: M. Demir
Date of Birth: 05/12/1984
File No: TKR-44821

Reason for Admission:
Shortness of breath, chest pressure, and lower extremity swelling worsening over the last 3 days.

Diagnoses:
- Type 2 Diabetes
- Hypertension
- Mild congestive heart failure (NYHA Class II)

Allergies:
- Penicillin

Laboratory Results:
- HbA1c: 8.4 percent
- Creatinine: 1.2 mg/dL
- BNP: 210 pg/mL
- Sodium: 138 mmol/L
- Potassium: 4.2 mmol/L

Imaging:
Echocardiogram: Left ventricular ejection fraction approximately 45 percent.
Mild global hypokinesis. No acute findings.

Discharge Medications:
- Metformin 1000 mg twice daily
- Losartan 50 mg once daily
- Furosemide 20 mg once daily
- Atorvastatin 20 mg once daily

Treatment Summary:
Symptoms improved significantly with diuretic therapy and blood pressure control.
No signs of acute infection or ischemia. Diabetes stabilized with regular glucose management.

Discharge Plan:
- Low sodium diet recommended.
- Follow up with cardiology in 1 week.
- Monitor daily weight at home.
- Return to the emergency department if shortness of breath worsens,
  weight increases, or chest pain develops.
"""

# Spanish sample record
ORIGINAL_ES = """Informe de alta
Fecha: 18/09/2024
Paciente: M. Demir
Fecha de nacimiento: 12/05/1984
Número de historia: ESP-55219

Motivo de ingreso:
Disnea progresiva de 3 días de evolución, opresión torácica y edema en ambas piernas.

Diagnósticos:
- Diabetes mellitus tipo 2
- Hipertensión arterial
- Insuficiencia cardíaca congestiva leve (NYHA II)

Alergias:
- Penicilina

Resultados de laboratorio:
- HbA1c: 8.4 percent
- Creatinina: 1.2 mg/dL
- BNP: 210 pg/mL
- Sodio: 138 mmol/L
- Potasio: 4.2 mmol/L

Ecocardiograma:
Fracción de eyección del ventrículo izquierdo aproximadamente 45 percent.
Hipocinesia global leve. Sin hallazgos agudos.

Tratamiento al alta:
- Metformina 1000 mg cada 12 horas
- Losartán 50 mg cada 24 horas
- Furosemida 20 mg cada 24 horas
- Atorvastatina 20 mg cada 24 horas
"""

TRANSLATION_ES_EN = """Discharge Summary
Date: 09/18/2024
Patient: M. Demir
Date of Birth: 05/12/1984
File No: ESP-55219

Reason for Admission:
Three day history of progressive shortness of breath, chest pressure, and bilateral leg swelling.

Diagnoses:
- Type 2 Diabetes Mellitus
- Hypertension
- Mild congestive heart failure (NYHA Class II)

Allergies:
- Penicillin

Laboratory Results:
- HbA1c: 8.4 percent
- Creatinine: 1.2 mg/dL
- BNP: 210 pg/mL
- Sodium: 138 mmol/L
- Potassium: 4.2 mmol/L

Imaging:
Echocardiogram: Left ventricular ejection fraction approximately 45 percent.
Mild global hypokinesis. No acute findings.

Discharge Medications:
- Metformin 1000 mg every 12 hours
- Losartan 50 mg daily
- Furosemide 20 mg daily
- Atorvastatin 20 mg daily

Treatment Summary:
Symptoms improved with diuretics and blood pressure control.
No evidence of acute infection or ischemia. Diabetes remains suboptimally controlled.

Discharge Plan:
- Low sodium diet.
- Cardiology follow up in 1 week.
- Daily weight monitoring.
- Return to emergency care if symptoms worsen.
"""

# NLP extraction (same for both language examples)
EXTRACTED_ITEMS_BASE = [
    {"type": "diagnosis", "text": "Type 2 Diabetes", "normalized": "Type 2 diabetes mellitus"},
    {"type": "diagnosis", "text": "Hypertension", "normalized": "Hypertension"},
    {"type": "diagnosis", "text": "Mild congestive heart failure", "normalized": "Congestive heart failure"},
    {"type": "allergy", "text": "Penicillin", "normalized": "Penicillin"},
    {"type": "lab", "text": "HbA1c 8.4 percent", "normalized": "Hemoglobin A1c", "value": "8.4", "unit": "%"},
    {"type": "lab", "text": "Creatinine 1.2 mg/dL", "normalized": "Creatinine", "value": "1.2", "unit": "mg/dL"},
    {"type": "lab", "text": "BNP 210 pg/mL", "normalized": "BNP", "value": "210", "unit": "pg/mL"},
    {"type": "medication", "text": "Metformin 1000 mg", "normalized": "Metformin 1000 mg tablet", "sig": "1000 mg PO BID"},
    {"type": "medication", "text": "Losartan 50 mg", "normalized": "Losartan 50 mg tablet", "sig": "50 mg PO daily"},
    {"type": "medication", "text": "Furosemide 20 mg", "normalized": "Furosemide 20 mg tablet", "sig": "20 mg PO daily"},
    {"type": "medication", "text": "Atorvastatin 20 mg", "normalized": "Atorvastatin 20 mg tablet", "sig": "20 mg PO daily"},
    {"type": "imaging", "text": "LVEF approximately 45 percent", "normalized": "Echocardiogram"},
]

# Coded concepts
CODED_ITEMS_BASE = [
    {"type": "diagnosis", "text": "Type 2 Diabetes", "normalized": "Type 2 diabetes mellitus", "code_system": "SNOMED CT", "code": "44054006"},
    {"type": "diagnosis", "text": "Hypertension", "normalized": "Hypertension", "code_system": "SNOMED CT", "code": "38341003"},
    {"type": "diagnosis", "text": "Mild congestive heart failure", "normalized": "Congestive heart failure", "code_system": "SNOMED CT", "code": "84114007"},
    {"type": "allergy", "text": "Penicillin", "normalized": "Penicillin", "code_system": "RxNorm", "code": "7980"},
    {"type": "lab", "text": "HbA1c 8.4 percent", "normalized": "Hemoglobin A1c", "code_system": "LOINC", "code": "4548-4", "value": "8.4", "unit": "%"},
    {"type": "lab", "text": "Creatinine 1.2 mg/dL", "normalized": "Creatinine", "code_system": "LOINC", "code": "2160-0", "value": "1.2", "unit": "mg/dL"},
    {"type": "lab", "text": "BNP 210 pg/mL", "normalized": "BNP", "code_system": "LOINC", "code": "33762-6", "value": "210", "unit": "pg/mL"},
    {"type": "medication", "text": "Metformin 1000 mg", "normalized": "Metformin 1000 mg tablet", "code_system": "RxNorm", "code": "860975", "sig": "1000 mg PO BID"},
    {"type": "medication", "text": "Losartan 50 mg", "normalized": "Losartan 50 mg tablet", "code_system": "RxNorm", "code": "979487", "sig": "50 mg PO daily"},
    {"type": "medication", "text": "Furosemide 20 mg", "normalized": "Furosemide 20 mg tablet", "code_system": "RxNorm", "code": "312513", "sig": "20 mg PO daily"},
    {"type": "medication", "text": "Atorvastatin 20 mg", "normalized": "Atorvastatin 20 mg tablet", "code_system": "RxNorm", "code": "617314", "sig": "20 mg PO daily"},
    {"type": "imaging", "text": "LVEF approximately 45 percent", "normalized": "Echocardiogram", "code_system": "SNOMED CT", "code": "40701008"},
]

FHIR_BUNDLE_BASE = {
    "resourceType": "Bundle",
    "type": "transaction",
    "original_record_id": "IPHR-DEMO-001",
    "entries": [
        {"resourceType": "Condition", "code_system": "SNOMED CT", "code": "44054006", "text": "Type 2 diabetes mellitus"},
        {"resourceType": "Condition", "code_system": "SNOMED CT", "code": "38341003", "text": "Hypertension"},
        {"resourceType": "Condition", "code_system": "SNOMED CT", "code": "84114007", "text": "Congestive heart failure"},
        {"resourceType": "AllergyIntolerance", "code_system": "RxNorm", "code": "7980", "text": "Penicillin"},
        {"resourceType": "Observation", "code_system": "LOINC", "code": "4548-4", "text": "Hemoglobin A1c", "value": "8.4", "unit": "%"},
        {"resourceType": "Observation", "code_system": "LOINC", "code": "2160-0", "text": "Creatinine", "value": "1.2", "unit": "mg/dL"},
        {"resourceType": "Observation", "code_system": "LOINC", "code": "33762-6", "text": "BNP", "value": "210", "unit": "pg/mL"},
        {"resourceType": "MedicationStatement", "code_system": "RxNorm", "code": "860975", "text": "Metformin 1000 mg tablet"},
        {"resourceType": "MedicationStatement", "code_system": "RxNorm", "code": "979487", "text": "Losartan 50 mg tablet"},
        {"resourceType": "MedicationStatement", "code_system": "RxNorm", "code": "312513", "text": "Furosemide 20 mg tablet"},
        {"resourceType": "MedicationStatement", "code_system": "RxNorm", "code": "617314", "text": "Atorvastatin 20 mg tablet"},
        {"resourceType": "DiagnosticReport", "code_system": "SNOMED CT", "code": "40701008", "text": "Echocardiogram"},
    ],
}

SAMPLE_RECORDS = {
    "Turkey - Turkish discharge summary": {
        "original": ORIGINAL_TR,
        "translation": TRANSLATION_TR_EN,
        "extracted": EXTRACTED_ITEMS_BASE,
        "coded": CODED_ITEMS_BASE,
        "fhir": FHIR_BUNDLE_BASE,
    },
    "Spain - Spanish discharge summary": {
        "original": ORIGINAL_ES,
        "translation": TRANSLATION_ES_EN,
        "extracted": EXTRACTED_ITEMS_BASE,
        "coded": CODED_ITEMS_BASE,
        "fhir": FHIR_BUNDLE_BASE,
    },
}

# ---------------------------------------------------------
# Streamlit layout
# ---------------------------------------------------------

st.title("IPHR Translation and EHR Integration Demo")

st.markdown(
    "This demo shows how the IPHR system turns international health records into "
    "structured, standardized data that can flow into an EHR."
)

st.markdown(
    "1. Translation and NLP engine detects the language and extracts clinical concepts.  \n"
    "2. Concepts are mapped to SNOMED CT, LOINC, and RxNorm and formatted as HL7 FHIR.  \n"
    "3. A clinical reviewer validates the output.  \n"
    "4. A FHIR bundle is sent to the EHR while keeping the original and translated documents linked."
)

# Sidebar controls
st.sidebar.header("Scenario controls")

language_choice = st.sidebar.selectbox(
    "Sample record",
    options=list(SAMPLE_RECORDS.keys()),
    index=0,
)

path_choice = st.sidebar.radio(
    "Record intake path",
    options=[
        "Path A - Patient uploads documents",
        "Path B - External provider sends documents",
    ],
    index=0,
)

st.sidebar.markdown("### Reviewer simulation")
reviewer_action = st.sidebar.radio(
    "Reviewer decision",
    options=["Approve all items", "Approve with notes", "Flag issues"],
    index=0,
)
reviewer_notes = st.sidebar.text_area(
    "Reviewer notes (optional)",
    value="",
    height=80,
)

# Path info box
if "Path A" in path_choice:
    st.info(
        "Current view: Path A. The international patient or family uploads records directly into the IPHR intake portal."
    )
else:
    st.info(
        "Current view: Path B. A sending clinic or hospital transmits foreign records to the IPHR service on behalf of the patient."
    )

# Get sample data
sample = SAMPLE_RECORDS[language_choice]
sample_original = sample["original"]
sample_translation = sample["translation"]
sample_extracted = sample["extracted"]
sample_coded = sample["coded"]
sample_fhir = sample["fhir"]

tabs = st.tabs(["Documents", "Structured data", "FHIR bundle"])

# ---------------------------------------------------------
# Documents tab: synced scroll
# ---------------------------------------------------------
with tabs[0]:
    st.subheader("Original vs translated document")

    mode = st.radio(
        "Document source",
        options=["Use sample record", "Paste your own foreign document"],
        index=0,
    )

    if mode == "Use sample record":
        render_synced_documents(
            left_text=sample_original,
            right_text=sample_translation,
            left_label="Original document (foreign language)",
            right_label="Translated document (English, medically tuned)",
            height=500,
        )
    else:
        user_original = st.text_area(
            "Paste clinical text in any language",
            value="",
            height=200,
            placeholder="Example: discharge summary, clinic note, medication list, lab report...",
        )

        placeholder_translation = (
            "In a full implementation, the translation and NLP engine would detect the language, "
            "produce a medically tuned translation, and highlight extracted clinical concepts here.\n\n"
            "For this demo, the structured data in the next tabs stays linked to the sample case "
            "so you can still see how the pipeline behaves end to end."
        )

        render_synced_documents(
            left_text=user_original or "[No text pasted yet]",
            right_text=placeholder_translation,
            left_label="Original document (pasted foreign text)",
            right_label="Translated document (demo explanation)",
            height=500,
        )

# ---------------------------------------------------------
# Structured data tab
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("Extracted and coded clinical concepts")

    st.markdown(
        "This view shows how the IPHR pipeline turns narrative text into discrete elements "
        "such as diagnoses, medications, labs, allergies, and imaging findings."
    )

    concept_types = sorted(set(item["type"] for item in sample_extracted))
    selected_types = st.multiselect(
        "Filter by concept type",
        options=concept_types,
        default=concept_types,
    )

    extracted_filtered = [item for item in sample_extracted if item["type"] in selected_types]
    coded_filtered = [item for item in sample_coded if item["type"] in selected_types]

    st.markdown("**NLP extracted concepts (before coding)**")
    st.table(extracted_filtered)

    st.markdown("**Mapped and standardized concepts (after coding)**")
    st.table(coded_filtered)

    st.markdown("### Clinical reviewer interaction")

    if reviewer_action == "Approve all items":
        st.success("Reviewer decision: All mapped items approved without changes.")
    elif reviewer_action == "Approve with notes":
        st.warning("Reviewer decision: Approved with comments. See notes below.")
    else:
        st.error("Reviewer decision: Some items flagged for correction or removal.")

    if reviewer_notes.strip():
        st.markdown("**Reviewer notes:**")
        st.markdown(reviewer_notes)

    st.markdown(
        "In a full system, any corrections from the reviewer would be fed back into the translation and "
        "mapping models so that similar records are handled more accurately in the future."
    )

# ---------------------------------------------------------
# FHIR bundle tab
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("FHIR import package")

    st.markdown(
        "This is a simplified HL7 FHIR bundle that the IPHR system would send to the receiving EHR. "
        "Because the data is standardized, the EHR knows where to place each item for medication reconciliation, "
        "allergy review, problem list updates, and documentation."
    )

    st.json(sample_fhir)

    fhir_json_str = json.dumps(sample_fhir, indent=2)

    st.download_button(
        label="Download FHIR bundle as JSON",
        data=fhir_json_str,
        file_name="iphr_fhir_bundle_demo.json",
        mime="application/json",
    )

    st.markdown(
        "The bundle keeps a link back to the original document and its translation so that clinicians can "
        "always trace structured data back to its source if something looks unclear."
    )
