import pandas as pd

print("🚀 Career Twin is starting...")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("../data/candidate_job_role_dataset.csv")
print("📊 Dataset loaded successfully!")

courses_df = pd.read_csv("../data/Courses_and_Learning_Material.csv")
print("📚 Courses dataset loaded successfully!")
# 🔑 Skill → Keyword mapping for smarter course matching
skill_keyword_map = {
    "tensorflow": ["deep learning", "neural network", "ai", "tensorflow"],
    "machine learning": ["machine learning", "ml", "data science"],
    "communication": ["soft skills", "communication", "presentation"],
    "sql": ["database", "sql", "data"]
}




# ---------------- FUNCTIONS ----------------
def recommend_job(skills_input):
    skills_input = skills_input.lower()

    for index, row in df.iterrows():
        job_skills = row['skills'].lower()
        match_count = 0

        for skill in skills_input.split(','):
            if skill.strip() in job_skills:
                match_count += 1

        if match_count >= 2:
            return row['job_role']

    return "No suitable job role found"


def skill_gap_analysis(skills_input, job_role):
    skills_input = set([s.strip().lower() for s in skills_input.split(',')])

    job_row = df[df['job_role'] == job_role]

    if job_row.empty:
        return []

    required_skills = set(
    s.strip().lower() for s in job_row.iloc[0]['skills'].split(',')
)


    missing_skills = required_skills - skills_input
    return list(missing_skills)


def recommend_courses(missing_skills):
    recommendations = []

    for skill in missing_skills:
        skill = skill.strip().lower()
        keywords = skill_keyword_map.get(skill, [skill])

        for keyword in keywords:
            matched = courses_df[
                courses_df['Course_Learning_Material']
                .str.lower()
                .str.contains(keyword, na=False)
            ]

            for _, row in matched.iterrows():
                recommendations.append({
                    "missing_skill": skill,
                    "module": row['Module_Code'],
                    "material": row['Course_Learning_Material'],
                    "link": row['Course_Learning_Material_Link'],
                    "level": row['Course_Level'],
                    "type": row['Type_Free_Paid']
                })

    return recommendations




# ---------------- TEST / RUN ----------------
test_skills = "python, sql, machine learning"

result = recommend_job(test_skills)
print("✅ Recommended Job Role:", result)

missing = skill_gap_analysis(test_skills, result)
print("❌ Missing Skills:", missing)

courses = recommend_courses(missing)
print("📚 Recommended Courses:")
for c in courses:
    print(c)

print("\n📄 Dataset Preview:")
print(df.head())
