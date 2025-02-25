# Medical Team Leader Agent

The Medical Team Leader Agent represents a medical team leader responsible for managing patient treatment, drug administration, and resource allocation in emergency situations.
## Key Attributes:

    Tracks treated patients, response times, and survival rates

    Manages medical inventory (bandages, surgical kits, IV fluids)

    Maintains a drug inventory for various medical conditions

    Utilizes Google's Generative AI for decision support

## Main Functions:

process_patient_treat_wounds(injury_severity)

    Simulates treating a patient's wounds based on injury severity

    Updates medical inventory and patient statistics

get_drug_recommendation(condition, patient_info)

    Uses AI to recommend a drug for a given medical condition and patient information

    Considers available drugs and their side effects

process_patient_drugs(condition, patient_info)

    Administers drugs to patients based on their condition

    Updates drug inventory and patient statistics

query_gemini_for_side_effects(drug_name, side_effects, patient_info)

    Consults AI for guidance on handling potential drug side effects

query_gemini_for_treatment(injury_severity)

    Requests AI-generated treatment recommendations for injuries

query_gemini_for_hospital_coordination(patient_info)

    Seeks AI advice on hospital transfer decisions

generate_report()

    Produces a JSON report summarizing the agent's performance and inventory status

## Data Management

The agent uses a CSV file named "filtered_drug_treatment_data.csv" to manage drug data. This file contains information about various drugs, including names, medical conditions they treat, and side effects. The data from this file is used to populate the agent's drug inventory.

## Requirements

    Python 3.x

    Google Generative AI library

    pandas
    
    dotenv

## Installation

    Clone the repository

    Install required packages: pip install google-generativeai pandas python-dotenv

    Set up your Google API key in a .env file

    Ensure the "filtered_drug_treatment_data.csv" file is present in the project directory

## Example Usage
### Initialize the agent
    from medical_lead_agent import MedicalTeamLeaderAgent
    agent = MedicalTeamLeaderAgent()

### Obtain medication recommendation based on patient's condition
    condition = "Hypertension"
    patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
    drug = self.agent.get_drug_recommendation(condition, patient_info)

