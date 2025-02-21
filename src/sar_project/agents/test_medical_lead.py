import unittest
from unittest.mock import patch
from medical_lead_agent import MedicalTeamLeaderAgent, drug_inventory
import json

class TestMedicalTeamLeaderAgent(unittest.TestCase):

    def setUp(self):
        self.agent = MedicalTeamLeaderAgent()

    def test_init(self):
        self.assertEqual(self.agent.patients_treated_wounds, 0)
        self.assertEqual(self.agent.total_response_time, 0)
        self.assertEqual(self.agent.total_injuries, 0)
        self.assertEqual(self.agent.patient_survival_rate, 0)
        self.assertEqual(self.agent.diagnosis_accuracy, 0)
        self.assertIsNotNone(self.agent.medical_inventory)
        self.assertIsNotNone(self.agent.model)
        self.assertEqual(self.agent.drug_inventory, drug_inventory)

    def test_process_patient_treat_wounds_01(self):
        initial_patients = self.agent.patients_treated_wounds
        initial_injuries = self.agent.total_injuries
        initial_bandages = self.agent.medical_inventory['bandages']
        self.agent.process_patient_treat_wounds('minor')

        self.assertEqual(self.agent.total_injuries, initial_injuries + 1)
        self.assertGreater(self.agent.total_response_time, 0)
        self.assertLess(self.agent.medical_inventory['bandages'], initial_bandages)
        self.assertGreaterEqual(self.agent.patients_treated_wounds, initial_patients)


    def test_generate_report(self):
        self.agent.patients_treated_wounds = 5
        self.agent.total_response_time = 50
        self.agent.total_injuries = 10
        self.agent.diagnosis_accuracy = 450

        report = self.agent.generate_report()

        self.assertIsInstance(report, str)
        report_dict = eval(report)
        self.assertIn('patients_treated', report_dict)
        self.assertIn('avg_response_time_minutes', report_dict)
        self.assertIn('survival_rate_percentage', report_dict)
        self.assertIn('avg_diagnosis_accuracy_percentage', report_dict)
        self.assertIn('remaining_medical_inventory', report_dict)
        self.assertIn('remaining_drug_inventory by condition', report_dict)

    def test_generate_report_no_patients(self):
        report = self.agent.generate_report()
        self.assertEqual(report, '{"message": "No patients processed yet"}')

    @patch('random.random', return_value=0.9) 
    def test_process_patient_treat_wounds_minor(self, mock_random):
        initial_treated = self.agent.patients_treated_wounds
        self.agent.process_patient_treat_wounds("minor")
        self.assertEqual(self.agent.patients_treated_wounds, initial_treated + 1)

    def test_process_patient_treat_wounds_moderate(self):
        initial_treated = self.agent.patients_treated_wounds
        self.agent.process_patient_treat_wounds("moderate")
        self.assertLessEqual(self.agent.patients_treated_wounds, initial_treated + 1)

    def test_process_patient_treat_wounds_severe(self):
        initial_treated = self.agent.patients_treated_wounds
        self.agent.process_patient_treat_wounds("severe")
        self.assertLessEqual(self.agent.patients_treated_wounds, initial_treated + 1)

    def test_get_drug_recommendation_valid_condition(self):
        condition = "Hypertension"
        patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
        drug = self.agent.get_drug_recommendation(condition, patient_info)
        self.assertIsNotNone(drug)
        self.assertIn("drug_name", drug)
        self.assertIn("generic_name", drug)
        self.assertIn("side_effects", drug)
        self.assertIn("supply", drug)

    def test_get_drug_recommendation_invalid_condition(self):
        condition = "NonExistentCondition"
        patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
        drug = self.agent.get_drug_recommendation(condition, patient_info)
        self.assertIsNone(drug)

    def test_process_patient_drugs_valid_condition(self):
        condition = "Hypertension"
        patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
        drug_name = self.agent.process_patient_drugs(condition, patient_info)
        self.assertIsNotNone(drug_name)

    def test_process_patient_drugs_invalid_condition(self):
        condition = "NonExistentCondition"
        patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
        drug_name = self.agent.process_patient_drugs(condition, patient_info)
        self.assertIsNone(drug_name)

    def test_query_gemini_for_side_effects(self):
        drug_name = "SomeDrug"
        side_effects = "Nausea, Dizziness"
        patient_info = {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]}
        response = self.agent.query_gemini_for_side_effects(drug_name, side_effects, patient_info)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_query_gemini_for_treatment(self):
        injury_severity = "severe"
        response = self.agent.query_gemini_for_treatment(injury_severity)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_query_gemini_for_hospital_coordination(self):
        patient_info = {"severity": "severe"}
        response = self.agent.query_gemini_for_hospital_coordination(patient_info)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_generate_report_no_patients(self):
        report = self.agent.generate_report()
        self.assertIn("No patients processed yet", report)

    def test_generate_report_with_patients(self):
        self.agent.process_patient_treat_wounds("minor")
        self.agent.process_patient_treat_wounds("moderate")
        report = self.agent.generate_report()
        self.assertIn("patients_treated", report)
        self.assertIn("avg_response_time_minutes", report)
        self.assertIn("survival_rate_percentage", report)
        self.assertIn("avg_diagnosis_accuracy_percentage", report)
        self.assertIn("remaining_medical_inventory", report)
        self.assertIn("remaining_drug_inventory by condition", report)

if __name__ == '__main__':
    unittest.main()
