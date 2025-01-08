import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import csv

# Classify Agreement Types
def classify_agreement_types(business_info):
    keywords = {
        "online": "Internet Agreement",
        "renovation": ["Direct Agreement", "Future Performance Agreement"],
        "remote": "Remote Agreement",
    }
    identified_types = set()
    for keyword, types in keywords.items():
        if keyword.lower() in business_info.get("category", "").lower():
            if isinstance(types, list):
                identified_types.update(types)
            else:
                identified_types.add(types)
    return list(identified_types) if identified_types else ["General Consumer Agreement"]

# Generate Checklist
def generate_combined_checklist(agreement_types):
    checklist_templates = {
        "Direct Agreement": [
            "Is the agreement in writing?",
            "Are all payment terms clear and included?",
            "Does the agreement include the consumer's right to cancel?"
        ],
        "Remote Agreement": [
            "Is the remote agreement properly disclosed to the consumer?",
            "Does the consumer have an express opportunity to accept or decline?",
            "Are additional charges clearly stated?"
        ],
        "Internet Agreement": [
            "Are all terms and conditions displayed prominently?",
            "Is the consumer provided with a copy of the agreement within 15 days?",
            "Are payment methods secure and disclosed?"
        ],
        "Future Performance Agreement": [
            "Is a clear timeline for service completion provided?",
            "Are cancellation terms clearly stated?",
            "Is a refund policy included for non-performance?"
        ]
    }

    combined_checklist = []
    for agreement in agreement_types:
        combined_checklist.extend(checklist_templates.get(agreement, []))
    return combined_checklist

# Generate Inspection Report
def generate_combined_report(business_info, checklist_results, filename="combined_inspection_report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"Inspection Report - {business_info['name']}", styles['Title']))
    content.append(Spacer(1, 20))
    content.append(Paragraph("Business Information:", styles['Heading2']))
    content.append(Paragraph(f"Category: {business_info['category']}", styles['BodyText']))
    content.append(Paragraph(f"Description: {business_info['description']}", styles['BodyText']))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Checklist Results:", styles['Heading2']))
    for i, (item, status) in enumerate(checklist_results.items(), 1):
        content.append(Paragraph(f"{i}. {item}: {status}", styles['BodyText']))
    
    doc.build(content)

# Save Results to ICPS (Simulated CSV)
def save_to_icps(business_info, checklist_results):
    filename = "icps_inspection_results.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Business Name", "Checklist Item", "Compliance Status"])
        for item, status in checklist_results.items():
            writer.writerow([business_info['name'], item, status])
    print(f"Inspection results saved to {filename}")

# Streamlit Interface
def inspection_interface():
    # Example Business Information
    business_info = {
        "name": "Castlebury Contracting",
        "category": "Renovation Services",
        "description": "Providing renovation and remodeling services.",
    }

    # Classify Agreement Types
    agreement_types = classify_agreement_types(business_info)
    st.title(f"Inspection Checklist - {business_info['name']}")
    st.write("Identified Agreement Types:")
    st.write(", ".join(agreement_types))

    # Generate Checklist
    checklist = generate_combined_checklist(agreement_types)
    st.write("Please review each checklist item and mark compliance status.")

    # Interactive Form
    responses = {}
    for i, item in enumerate(checklist, 1):
        responses[item] = st.radio(f"{i}. {item}", ["Compliant", "Non-Compliant", "N/A"])

    if st.button("Submit Checklist"):
        st.success("Checklist submitted successfully!")
        st.write("Generating Inspection Report...")
        generate_combined_report(business_info, responses)
        save_to_icps(business_info, responses)
        st.success("Inspection report generated and results saved to ICPS!")
        st.write("You can find the generated PDF and ICPS file in the working directory.")

# Run Streamlit App
if __name__ == "__main__":
    inspection_interface()
