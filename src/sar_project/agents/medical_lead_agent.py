import random
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

    def process_patient(self, injury_severity):
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

            report = {
                "patients_treated": self.patients_treated,
                "avg_response_time_minutes": avg_response_time,
                "survival_rate_percentage": survival_rate,
                "avg_diagnosis_accuracy_percentage": avg_diagnosis_accuracy,
                "remaining_medical_inventory": self.medical_inventory
            }
            return json.dumps(report, indent=4)  
        else:
            return json.dumps({"message": "No injuries processed yet"})


if __name__ == "__main__":
    agent = MedicalTeamLeaderAgent()
    
    
    injuries = ['minor', 'moderate', 'severe', 'moderate', 'minor']
    for injury in injuries:
        agent.process_patient(injury)
        
        treatment_response = agent.query_gemini_for_treatment(injury)
        print(f"Treatment recommendation for {injury} injury: {treatment_response}")
    
    severe_patient_info = {'severity': 'severe'}
    hospital_response = agent.query_gemini_for_hospital_coordination(severe_patient_info)
    print(f"Hospital coordination response: {hospital_response}")
    
    report = agent.generate_report()
    print("Agent Report:")
    print(report)
