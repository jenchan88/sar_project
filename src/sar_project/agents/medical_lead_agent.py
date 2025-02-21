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
max_drugs_per_condition = 2

for _, row in drug_data.iterrows():
    condition = row["medical_condition"]
    drug_info = {
        "drug_name": row["drug_name"],
        "generic_name": row["generic_name"],
        "side_effects": row["side_effects"],
        "supply": 3  
    }

    if condition not in drug_inventory:
        drug_inventory[condition] = []

    if len(drug_inventory[condition]) < max_drugs_per_condition:
        if not any(drug['drug_name'] == drug_info['drug_name'] for drug in drug_inventory[condition]):
            drug_inventory[condition].append(drug_info)

print("Medical Conditions:", list(drug_inventory.keys()))
#print(len(drug_inventory))
class MedicalTeamLeaderAgent:
    def __init__(self):
        self.patients_treated_wounds = 0
        self.total_response_time = 0
        self.total_injuries = 0
        self.patient_survival_rate = 0
        self.diagnosis_accuracy = 0
        self.total_medicated_patients = 0
        self.medical_inventory = {
            'bandages': 100,
            'surgical_kits': 10,
            'IV_fluids': 20
        }
        self.model = genai.GenerativeModel("gemini-pro")  
        self.drug_inventory = drug_inventory
        self.total_drug_supply = 156

    def process_patient_treat_wounds(self, injury_severity):
        self.total_injuries += 1
        response_time = random.randint(5, 15)  
        self.total_response_time += response_time
        
        survival_chance = {'minor': 0.95, 'moderate': 0.85, 'severe': 0.65}
        treatment_outcome = random.random() < survival_chance.get(injury_severity, 0.7)
        
        #if patient survives after being treated
        if treatment_outcome:
            self.patients_treated_wounds += 1

        self.medical_inventory['bandages'] -= 1
        self.medical_inventory['surgical_kits'] -= 1
        self.medical_inventory['IV_fluids'] -= 1

    def get_drug_recommendation(self, condition, patient_info):
        if condition in self.drug_inventory and self.drug_inventory[condition]:
            drugs = self.drug_inventory[condition]
            prompt = f"Patient with {condition} and the following characteristics: {patient_info}. Available drugs: {[drug['drug_name'] for drug in drugs]}. Each drug has these side effects: {[{drug['drug_name']: drug['side_effects']} for drug in drugs]}. Which drug would you recommend and why?"
            response = self.model.generate_content(prompt)
            recommendation = response.text
            
            recommended_drug_name = next((drug['drug_name'] for drug in drugs if drug['drug_name'] in recommendation), None)
            
            if recommended_drug_name:
                return next(drug for drug in drugs if drug['drug_name'] == recommended_drug_name)
            else:
                return random.choice(drugs)  
        return None


    def process_patient_drugs(self, condition, patient_info):
        response_time = random.randint(5, 15)
        self.total_response_time += response_time
        
        drug = self.get_drug_recommendation(condition, patient_info)
        self.diagnosis_accuracy += random.randint(80, 100)  
        
        if drug:
            self.total_medicated_patients += 1
            self.total_drug_supply -= 1
            drug["supply"] -= 1
            print(f"Administering {drug['drug_name']} for {condition}.")
            
            if drug["side_effects"]:
                print(f"Warning: Side effects - {drug['side_effects']}")
                gemini_response = self.query_gemini_for_side_effects(drug["drug_name"], drug["side_effects"], patient_info)
                #print(f"Gemini AI Suggestion: {gemini_response}")
            
            return drug["drug_name"]
        else:
            print(f"No available drug for {condition}. Consult a specialist.")
            return None

    def query_gemini_for_side_effects(self, drug_name, side_effects, patient_info):
        prompt = f"A patient with characteristics {patient_info} is prescribed {drug_name} but has potential side effects: {side_effects}. How should we proceed considering the patient's specific situation?"
        response = self.model.generate_content(prompt)
        return response.text

    def query_gemini_for_treatment(self, injury_severity):
        prompt = f"Provide treatment recommendations for a {injury_severity} injury."
        response = self.model.generate_content(prompt)  
        return response.text  

    def query_gemini_for_hospital_coordination(self, patient_info):
        prompt = f"Should a patient with {patient_info['severity']} injury be sent to the hospital? What transport method should be used?"
        response = self.model.generate_content(prompt) 
        return response.text  

    def generate_report(self):
        # 0 patients medicated
        avg_diagnosis_accuracy = -1
        if (self.total_medicated_patients > 0): 
            avg_diagnosis_accuracy = self.diagnosis_accuracy / self.total_medicated_patients

        if (self.total_injuries > 0) or (self.total_medicated_patients > 0):
            avg_response_time = self.total_response_time / (self.total_injuries + self.total_medicated_patients)
            survival_rate = ((self.patients_treated_wounds + self.total_medicated_patients) / (self.total_injuries+self.total_medicated_patients)) * 100
            
            drug_inventory_summary = {}
            for condition, drugs in self.drug_inventory.items():
                drug_inventory_summary[condition] = [
                    {"drug_name": drug["drug_name"], "supply": drug["supply"]}
                    for drug in drugs
                ]

            report = {
                "patients_treated": self.patients_treated_wounds,
                "avg_response_time_minutes": avg_response_time,
                "survival_rate_percentage": survival_rate,
                "avg_diagnosis_accuracy_percentage": avg_diagnosis_accuracy,
                "remaining_medical_inventory": self.medical_inventory,
                "remaining_total_drug_supply_count": self.total_drug_supply,
                "remaining_drug_inventory by condition": drug_inventory_summary
            }
            
            return json.dumps(report, indent=4)
        else:
            return json.dumps({"message": "No patients processed yet"})


if __name__ == "__main__":
    agent = MedicalTeamLeaderAgent()

    # injuriesSeverity = ['minor', 'moderate', 'severe', 'moderate', 'minor']
    # for injury in injuriesSeverity:
    #     agent.process_patient_treat_wounds(injury)
    #     treatment_response = agent.query_gemini_for_treatment(injury)
    #     #print(f"Treatment recommendation for {injury} injury: {treatment_response}")

    severe_patient_info = {'severity': 'severe'}
    agent.process_patient_treat_wounds('severere')
    hospital_response = agent.query_gemini_for_hospital_coordination(severe_patient_info)
    print(f"Hospital coordination response: {hospital_response}")

    conditions = ["Hypertension", "Diabetes (Type 2)", "Asthma"]
    patient_infos = [
        {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]},
        {"age": 50, "gender": "male", "allergies": [], "other_conditions": ["obesity"]},
        {"age": 30, "gender": "female", "allergies": ["aspirin"], "other_conditions": []}
    ]
    for condition, patient_info in zip(conditions, patient_infos):
        drug_response = agent.process_patient_drugs(condition, patient_info)
        #print(f"Drug recommendation for {condition}: {drug_response}")

    report = agent.generate_report()
    print("Agent Report:")
    print(report)