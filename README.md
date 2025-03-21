# Medical Team Leader Agent

The Medical Team Leader Agent represents a medical team leader responsible for managing patient treatment, drug administration, and resource allocation in emergency situations.

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

## Data Management

The agent uses a CSV file named "filtered_drug_treatment_data.csv" to manage drug data. This file contains information about various drugs, including names, medical conditions they treat, and side effects. The data from this file is used to populate the agent's drug inventory.

## Key Attributes:

    Tracks treated patients, response times, and survival rates

    Manages medical inventory (bandages, surgical kits, IV fluids)

    Maintains a drug inventory for various medical conditions

    Utilizes Google's Generative AI for decision support

## Main Functions:

### process_patient_treat_wounds(injury_severity)

    Simulates treating a patient's wounds based on injury severity

    Updates medical inventory and patient statistics

### get_drug_recommendation(condition, patient_info)

    Uses AI to recommend a drug for a given medical condition and patient information

    Considers available drugs and their side effects

### process_patient_drugs(condition, patient_info)

    Administers drugs to patients based on their condition

    Updates drug inventory and patient statistics

### query_gemini_for_side_effects(drug_name, side_effects, patient_info)

    Consults AI for guidance on handling potential drug side effects

### query_gemini_for_treatment(injury_severity)

    Requests AI-generated treatment recommendations for injuries

### query_gemini_for_hospital_coordination(patient_info)

    Seeks AI advice on hospital transfer decisions

### generate_report()

    Produces a JSON report summarizing the agent's performance and inventory status

## Example Usage
### Initialize the agent
    from medical_lead_agent import MedicalTeamLeaderAgent
    agent = MedicalTeamLeaderAgent()

### Obtain medication recommendation based on patient's condition
    condition = "Hypertension"
    patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
    drug = self.agent.get_drug_recommendation(condition, patient_info)

### Process some patients and generate a report
    agent.process_patient_treat_wounds('minor')
    agent.process_patient_treat_wounds('severe')
    agent.process_patient_drugs("Hypertension", {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]})
    report = agent.generate_report()
    print("Agent Report:")
    print(report)

### Update medical inventory
    agent.medical_inventory['bandages'] += 10
    print(f"Updated bandages inventory: {agent.medical_inventory['bandages']}")

### Check drug inventory for medications that can treat a specific conditon
    condition = "Asthma"
    if condition in agent.drug_inventory:
        print(f"Drug inventory for {condition}:")
        for drug in agent.drug_inventory[condition]:
            print(f"- {drug['drug_name']}: {drug['supply']} remaining")
    else:
        print(f"No drugs available for {condition}.")

### Coordinate hospital transport
    severe_patient_info = {'severity': 'severe'}
    agent.process_patient_treat_wounds('severe')
    hospital_response = agent.query_gemini_for_hospital_coordination(severe_patient_info)
    print(f"Hospital coordination response: {hospital_response}")

## Insights
As I developed the Medical Team Leader Agent, my goal was to create a system that could efficiently manage medical resources and provide effective treatment recommendations. However, upon receiving feedback, I realized that there were several areas where the system could be improved to better align with these goals.

One of the primary insights was the importance of scalability and reliability. The feedback highlighted issues with API model availability and quota limits, which underscored the need for robust error handling and the use of supported models. This was a crucial lesson because it emphasized that even with a well-designed system, external factors like API limitations can significantly impact performance. To address this, I implemented retry logic and ensured that the system uses models that are compatible with the current API version.

Another key insight was the value of transparency and tracking. The suggestion to assign unique patient IDs and implement low stock alerts for medical supplies resonated with my intention to create a system that could monitor and manage resources effectively. By integrating these features, I enhanced the system's ability to track patient treatments and inventory levels, making it more transparent and easier to manage.

## Modifications
Enhanced Reliability and Scalability: 
Updated the code to use supported models and implemented retry logic to handle transient errors and quota exhaustion. 
This not only improved the system's reliability but also ensured that it could scale more effectively.

Improved Transparency and Tracking: 
Introduced a patient ID system to track treatments more effectively and implemented low stock alerts for medical supplies. 
This enhanced the system's ability to monitor and manage resources, aligning with my original goal of creating an efficient and effective medical resource management system.

