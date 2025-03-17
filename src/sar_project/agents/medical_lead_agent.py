import random
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load drug data from CSV
def load_drug_data(file_path):
    """Loads drug data from a CSV file."""
    return pd.read_csv(file_path)

# Function to create drug inventory
def create_drug_inventory(drug_data, max_drugs_per_condition):
    """Creates a drug inventory based on the drug data."""
    drug_inventory = {}
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

    return drug_inventory

# Load drug data and create inventory
drug_data = load_drug_data("filtered_drug_treatment_data.csv")
max_drugs_per_condition = 2
drug_inventory = create_drug_inventory(drug_data, max_drugs_per_condition)

# Class for Medical Team Leader Agent
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
        self.model = genai.GenerativeModel("gemini-2.0-flash")  
        self.drug_inventory = drug_inventory
        self.total_drug_supply = 156
        self.patient_ids = {}
        self.patient_id_counter = 0

    # Function to process patient wounds
    def process_patient_treat_wounds(self, injury_severity):
        """Processes a patient with wounds."""
        self.total_injuries += 1
        response_time = random.randint(5, 15)  
        self.total_response_time += response_time
        
        survival_chance = {'minor': 0.95, 'moderate': 0.85, 'severe': 0.65}
        treatment_outcome = random.random() < survival_chance.get(injury_severity, 0.7)
        
        # If patient survives after being treated
        if treatment_outcome:
            self.patients_treated_wounds += 1

        self.medical_inventory['bandages'] -= 1
        self.medical_inventory['surgical_kits'] -= 1
        self.medical_inventory['IV_fluids'] -= 1

        # Assign a patient ID
        self.patient_id_counter += 1
        self.patient_ids[self.patient_id_counter] = {
            "injury_severity": injury_severity,
            "treatment_outcome": treatment_outcome
        }

    # Function to get drug recommendation
    def get_drug_recommendation(self, condition, patient_info):
        """Gets a drug recommendation for a patient."""
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

    # Function to process patient drugs
    def process_patient_drugs(self, condition, patient_info):
        """Processes a patient with drugs."""
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
            
            # Assign a patient ID
            self.patient_id_counter += 1
            self.patient_ids[self.patient_id_counter] = {
                "condition": condition,
                "drug": drug['drug_name']
            }
            
            return drug["drug_name"]
        else:
            print(f"No available drug for {condition}. Consult a specialist.")
            return None

    # Function to query Gemini for side effects
    def query_gemini_for_side_effects(self, drug_name, side_effects, patient_info):
        """Queries Gemini for handling side effects."""
        prompt = f"A patient with characteristics {patient_info} is prescribed {drug_name} but has potential side effects: {side_effects}. How should we proceed considering the patient's specific situation?"
        response = self.model.generate_content(prompt)
        return response.text

    # Function to query Gemini for treatment
    def query_gemini_for_treatment(self, injury_severity):
        """Queries Gemini for treatment recommendations."""
        prompt = f"Provide treatment recommendations for a {injury_severity} injury."
        response = self.model.generate_content(prompt)  
        return response.text  

    # Function to query Gemini for hospital coordination
    def query_gemini_for_hospital_coordination(self, patient_info):
        """Queries Gemini for hospital coordination."""
        prompt = f"Should a patient with {patient_info['severity']} injury be sent to the hospital? What transport method should be used?"
        response = self.model.generate_content(prompt) 
        return response.text  
    

    ### new methods
    def process_patient_drugs_new(self, condition):
        """Processes a patient with drugs."""
        response_time = random.randint(5, 15)
        self.total_response_time += response_time
        
        drug = self.get_drug_recommendation_new(condition)
        self.diagnosis_accuracy += random.randint(80, 100)  
        
        if drug:
            self.total_medicated_patients += 1
            self.total_drug_supply -= 1
            drug["supply"] -= 1
            print(f"Administering {drug['drug_name']} for {condition}.")
            
            if drug["side_effects"]:
                print(f"Warning: Side effects - {drug['side_effects']}")
                # You might want to remove or modify this line since patient_info is no longer passed
                # gemini_response = self.query_gemini_for_side_effects(drug["drug_name"], drug["side_effects"], patient_info)
            
            # Assign a patient ID
            self.patient_id_counter += 1
            self.patient_ids[self.patient_id_counter] = {
                "condition": condition,
                "drug": drug['drug_name']
            }
            
            return drug["drug_name"]
        else:
            print(f"No available drug for {condition}. Consult a specialist.")
            return None
    def get_drug_recommendation_new(self, condition):
        """Gets a drug recommendation for a condition."""
        if condition in self.drug_inventory and self.drug_inventory[condition]:
            drugs = self.drug_inventory[condition]
            # Modify the prompt to not include patient_info
            prompt = f"Recommend a drug for {condition}. Available drugs: {[drug['drug_name'] for drug in drugs]}. Each drug has these side effects: {[{drug['drug_name']: drug['side_effects']} for drug in drugs]}."
            response = self.model.generate_content(prompt)
            recommendation = response.text
            
            recommended_drug_name = next((drug['drug_name'] for drug in drugs if drug['drug_name'] in recommendation), None)
            
            if recommended_drug_name:
                return next(drug for drug in drugs if drug['drug_name'] == recommended_drug_name)
            else:
                return random.choice(drugs)  
        return None


    # Function to generate a report
    def generate_report(self):
        """Generates a report on the agent's performance."""
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
                "patients_treated": self.patients_treated_wounds + self.total_medicated_patients,
                "avg_response_time_minutes": avg_response_time,
                "survival_rate_percentage": survival_rate,
                "avg_diagnosis_accuracy_percentage": avg_diagnosis_accuracy,
                "remaining_medical_inventory": self.medical_inventory,
                "remaining_total_drug_supply_count": self.total_drug_supply,
                "remaining_drug_inventory by condition": drug_inventory_summary,
                "patient_ids": self.patient_ids
            }
            
            # Check for low stock and restock if necessary
            for item, quantity in self.medical_inventory.items():
                if quantity < 10:
                    print(f"Low stock alert: {item} is running low.")
                    # Restock logic can be added here
            
            for condition, drugs in self.drug_inventory.items():
                for drug in drugs:
                    if drug["supply"] < 1:
                        print(f"Low stock alert: {drug['drug_name']} is running low.")
                        # Restock logic can be added here
            
            return json.dumps(report, indent=4)
        else:
            return json.dumps({"message": "No patients processed yet"})

if __name__ == "__main__":
    agent = MedicalTeamLeaderAgent()

    # Process patients with wounds
    # agent.process_patient_treat_wounds('severe')

    # # Hospital coordination
    # severe_patient_info = {'severity': 'severe'}
    # hospital_response = agent.query_gemini_for_hospital_coordination(severe_patient_info)
    # print(f"Hospital coordination response: {hospital_response}")

    # Process patients with drugs
    conditions = ["Hypertension", "Diabetes (Type 2)", "Asthma"]
    patient_infos = [
        {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]},
        {"age": 50, "gender": "male", "allergies": [], "other_conditions": ["obesity"]},
        # {"age": 30, "gender": "female", "allergies": ["aspirin"], "other_conditions": []}
    ]
    for condition, patient_info in zip(conditions, patient_infos):
        drug_response = agent.process_patient_drugs(condition, patient_info)
    # for condition in conditions:
    #     drug_response = agent.process_patient_drugs_new(condition)


    # Generate report
    report = agent.generate_report()
    print("Agent Report:")
    print(report)
