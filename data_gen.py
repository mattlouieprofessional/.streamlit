import pandas as pd
import random

# Generate 100 fake entries for your Case Study
data = []
for i in range(100):
    reported = random.randint(1, 10)
    # Simulate the "Masking Bias": Someone says they are 9/10 happy, 
    # but their "Spiritual Alignment" is 2/10.
    spiritual = random.randint(1, 10)
    data.append({
        "Employee_ID": f"EMP-{i+100}",
        "Stated_Happiness": reported,
        "Spiritual_Alignment": spiritual,
        "Meeting_Hours_Daily": random.randint(2, 8),
        "Last_Promotion_Months": random.randint(1, 24)
    })

df = pd.DataFrame(data)
df.to_csv("case_study_data.csv", index=False)
print("Success! 'case_study_data.csv' created.")