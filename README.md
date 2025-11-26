IPHR Translation and EHR Integration Demo

This project is an interactive Streamlit application demonstrating how the International Patient Health Record (IPHR) System processes foreign medical documents. The demo simulates the complete workflow from translation to EHR integration using fully fictional patient data.

The system allows users to:

View foreign medical documents alongside English translations

See synced scrolling between the original and translated documents

Review extracted clinical concepts using a simulated NLP engine

Explore standardized medical coding (SNOMED CT, LOINC, RxNorm)

Interact with a mock clinical reviewer workflow

Download a FHIR bundle that would be sent to a receiving EHR

All medical information used in this demo is entirely synthetic and not based on any real patients.

🚀 Live Demo

You can access and interact with the full application online (no installation required):

👉 Live Streamlit App

https://iphr-demo-zuv37tnu5gnvbhsrsxsmyd.streamlit.app/

🧠 System Overview

The demo simulates the following steps of the IPHR pipeline:

Translation and Document Processing
The system accepts foreign-language medical documents (sample or user text) and displays an English translation. Both panes scroll in sync to support clinical review.

NLP Extraction
Clinical concepts such as diagnoses, medications, allergies, labs, and imaging findings are extracted from the text.

Standardization & Coding
Extracted items are mapped to standardized vocabularies:

SNOMED CT

LOINC

RxNorm

Clinical Reviewer Validation
A simulated reviewer can approve, comment, or flag items.

FHIR Packaging
A simplified HL7 FHIR transaction bundle is generated and available for download.
