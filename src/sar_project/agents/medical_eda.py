import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

drug_treatment_data = pd.read_csv('medication_treatments.csv')

# data types
print("Basic Info about the dataset:")
print(drug_treatment_data.info()) 

print("\nFirst few rows of the dataset:")
print(drug_treatment_data.head())

print("\nMissing values in each column:")
print(drug_treatment_data.isnull().sum())

# distribution of medical conditions/ no.drug treatments for each condition
print("\nDistribution of medical conditions:")
plt.figure(figsize=(10, 6))
sns.countplot(data=drug_treatment_data, y='medical_condition', order=drug_treatment_data['medical_condition'].value_counts().index)
plt.title('Distribution of Medical Conditions')
plt.show()


condition_drug_relationship = drug_treatment_data[['medical_condition', 'brand_names']].dropna()
print("\nExample of Medical Condition and Brand Names relationship:")
print(condition_drug_relationship.head())

# drug counts
condition_drug_count = condition_drug_relationship.groupby('medical_condition').size()
print("\nNumber of medications available for each medical condition:")
print(condition_drug_count.sort_values(ascending=False))

# check common side effects
print("\nChecking common side effects for certain conditions:")
side_effects_info = drug_treatment_data[['medical_condition', 'side_effects']].dropna()
print(side_effects_info.head())

print("\nAvailable medications count:")
print(drug_treatment_data['brand_names'].str.split(','))

relevant_conditions = [
    "Pain", "Hypertension", "Osteoarthritis", "Eczema", "Hayfever", "Diabetes (Type 2)", 
    "AIDS/HIV", "GERD (Heartburn)", "Constipation", "Psoriasis", "Insomnia", "Osteoporosis", 
    "Asthma", "Anxiety", "Depression", "Seizures", "Rheumatoid Arthritis", 
    "Cancer", "Covid 19", "Colds & Flu", "Migraine", "Hypothyroidism", "Stroke", "Incontinence", "Diarrhea", "UTI"
]

filter_df = drug_treatment_data[drug_treatment_data["medical_condition"].isin(relevant_conditions)]
filter_df_new = filter_df[['drug_name', 'medical_condition', 'generic_name','side_effects']]
#filter_df_new.head()

filter_df_new.to_csv("filtered_drug_treatment_data.csv", index=False)

print("File saved at:", os.path.abspath("filtered_drug_treatment_data.csv"))
