import random
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

drug_data = pd.read_csv("filtered_drug_treatment_data.csv")


drug_inventory = {}
max_drugs_per_condition = 3

for _, row in drug_data.iterrows():
    condition = row["medical_condition"]
    drug_info = {
        "drug_name": row["drug_name"],
        "generic_name": row["generic_name"],
        "side_effects": row["side_effects"],
        "supply": 10  
    }

    if condition not in drug_inventory:
        drug_inventory[condition] = []

    if len(drug_inventory[condition]) < max_drugs_per_condition:
        if not any(drug['drug_name'] == drug_info['drug_name'] for drug in drug_inventory[condition]):
            drug_inventory[condition].append(drug_info)

print("Medical Conditions:", list(drug_inventory.keys()))
print(len(drug_inventory))
class MedicalTeamLeaderAgent:
    def __init__(self):
        self.patients_treated = 0
        self.total_response_time = 0
        self.total_injuries = 0
        self.patient_survival_rate = 0
        self.diagnosis_accuracy = 0
        self.medical_inventory = {
            'bandages': 100,
            'medications': 50,
            'surgical_kits': 10,
            'IV_fluids': 20
        }
        self.model = genai.GenerativeModel("gemini-pro")  
        self.drug_inventory = drug_inventory

    def process_patient_treat_wounds(self, injury_severity):
        self.total_injuries += 1
        response_time = random.randint(5, 15)  
        self.total_response_time += response_time
        
        survival_chance = {'minor': 0.95, 'moderate': 0.85, 'severe': 0.65}
        treatment_outcome = random.random() < survival_chance.get(injury_severity, 0.7)
        if treatment_outcome:
            self.patients_treated += 1
        
        self.diagnosis_accuracy += random.randint(80, 100)  

        self.medical_inventory['bandages'] -= 1
        self.medical_inventory['medications'] -= 1

    def get_drug_recommendation(self, condition):
        if condition in self.drug_inventory and self.drug_inventory[condition]:
            drug = self.drug_inventory[condition][0]  
            return drug
        return None
    
    def process_patient_drugs(self, condition):
        self.total_injuries += 1
        response_time = random.randint(5, 15)
        self.total_response_time += response_time
        
        drug = self.get_drug_recommendation(condition)
        
        if drug:
            drug["supply"] -= 1
            print(f"Administering {drug['drug_name']} for {condition}.")
            
            if drug["side_effects"]:
                print(f"Warning: Side effects - {drug['side_effects']}")
                gemini_response = self.query_gemini_for_side_effects(drug["drug_name"], drug["side_effects"])
                print(f"Gemini AI Suggestion: {gemini_response}")
        else:
            print(f"No available drug for {condition}. Consult a specialist.")

    def query_gemini_for_side_effects(self, drug_name, side_effects):
        prompt = f"A patient is prescribed {drug_name} but has potential side effects: {side_effects}. How should I proceed?"
        response = self.model.generate_content(prompt)
        return response.text
    

    def query_gemini_for_treatment(self, injury_severity):
        """
        Use Google Gemini to get treatment suggestions based on the patient's injury severity.
        """
        prompt = f"Provide treatment recommendations for a {injury_severity} injury."
        response = self.model.generate_content(prompt)  
        return response.text  

    def query_gemini_for_hospital_coordination(self, patient_info):
        """
        Use Google Gemini to assist in hospital coordination for a severe patient.
        """
        prompt = f"Should a patient with {patient_info['severity']} injury be sent to the hospital? What transport method should be used?"
        response = self.model.generate_content(prompt) 
        return response.text  

    def generate_report(self):
        if self.total_injuries > 0:
            avg_response_time = self.total_response_time / self.total_injuries
            survival_rate = (self.patients_treated / self.total_injuries) * 100
            avg_diagnosis_accuracy = self.diagnosis_accuracy / self.total_injuries

            drug_inventory_summary = {}
            for condition, drugs in self.drug_inventory.items():
                drug_inventory_summary[condition] = drugs[0]["supply"]  # Supply left of the first drug

            report = {
                "patients_treated": self.patients_treated,
                "avg_response_time_minutes": avg_response_time,
                "survival_rate_percentage": survival_rate,
                "avg_diagnosis_accuracy_percentage": avg_diagnosis_accuracy,
                "remaining_medical_inventory": self.medical_inventory,
                "remaining_drug_inventory": drug_inventory_summary
            }
            
            return json.dumps(report, indent=4)
        else:
            return json.dumps({"message": "No patients processed yet"})


if __name__ == "__main__":
    agent = MedicalTeamLeaderAgent()
    
    
    injuriesSeverity = ['minor', 'moderate', 'severe', 'moderate', 'minor']
    for injury in injuriesSeverity:
        agent.process_patient_treat_wounds(injury)
        
        treatment_response = agent.query_gemini_for_treatment(injury)
        print(f"Treatment recommendation for {injury} injury: {treatment_response}")
    
    severe_patient_info = {'severity': 'severe'}
    hospital_response = agent.query_gemini_for_hospital_coordination(severe_patient_info)
    print(f"Hospital coordination response: {hospital_response}")

    conditions = ["Hypertension", "Diabetes (Type 2)", "Asthma"]
    for condition in conditions:
        agent.process_patient_drugs(condition)

    report = agent.generate_report()
    print("Agent Report:")
    print(report)
