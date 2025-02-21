import unittest
from unittest.mock import patch
from medical_lead_agent import MedicalTeamLeaderAgent, drug_inventory
import json

class TestMedicalTeamLeaderAgent(unittest.TestCase):   

    def setUp(self):
        self.agent = MedicalTeamLeaderAgent()
        self.conditions = ["Hypertension", "Diabetes (Type 2)", "Asthma"]
        self.patient_infos = [
            {"age": 65, "gender": "female", "allergies": ["penicillin"], "other_conditions": ["arthritis"]},
            {"age": 50, "gender": "male", "allergies": [], "other_conditions": ["obesity"]},
            {"age": 30, "gender": "female", "allergies": ["aspirin"], "other_conditions": []}
        ]

    def test_process_patients_and_generate_report(self):
        for condition, patient_info in zip(self.conditions, self.patient_infos):
            self.agent.process_patient_drugs(condition, patient_info)

        report_json = self.agent.generate_report()
        self.assertIsNotNone(report_json, "Report should not be None")
        report = json.loads(report_json)

        self.assertEqual(report["patients_treated"], 0, "No wounds treated")
        self.assertEqual(report["remaining_total_drug_supply_count"], 153, "Should have used 3 drugs")

        self.assertGreaterEqual(report["avg_response_time_minutes"], 5)
        self.assertLessEqual(report["avg_response_time_minutes"], 15)
        self.assertEqual(report["survival_rate_percentage"], 100)

        for condition in self.conditions:
            self.assertIn(condition, report["remaining_drug_inventory by condition"])
            condition_drugs = report["remaining_drug_inventory by condition"][condition]
            self.assertEqual(len(condition_drugs), 2, f"Should have 2 drugs for {condition}")
            used_drug = next(drug for drug in condition_drugs if drug["supply"] == 2)
            unused_drug = next(drug for drug in condition_drugs if drug["supply"] == 3)
            self.assertIsNotNone(used_drug, f"One drug should have been used for {condition}")
            self.assertIsNotNone(unused_drug, f"One drug should be unused for {condition}")

        self.assertEqual(report["remaining_medical_inventory"]["bandages"], 100)
        self.assertEqual(report["remaining_medical_inventory"]["surgical_kits"], 10)
        self.assertEqual(report["remaining_medical_inventory"]["IV_fluids"], 20)


if __name__ == '__main__':
    unittest.main()