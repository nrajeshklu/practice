import pandas as pd

# Load data
df = pd.read_csv("Y23SRC.csv")  # Replace with your actual file name

# Drop full duplicate rows
df = df.drop_duplicates()

# Select columns to include in the course grouping
course_columns = ['CourseCode', 'LTPS', 'CourseDesc', 'Bucket Group',
                  'Course Nature', 'AcademicYear', 'Semester', 'Study Year',
                  'Section', 'RegisterDate', 'course ref id', 'Offered To', 'Offered By']

# Remove duplicates *within* University ID for same course
df = df.drop_duplicates(subset=['University ID'] + course_columns)

# Add course sequence number per University ID
df['CourseNum'] = df.groupby('University ID').cumcount() + 1

# Reshape to wide format
wide_df = df.pivot(index='University ID', columns='CourseNum', values=course_columns)

# Flatten the multi-level column names
wide_df.columns = [f"{col}_{num}" for col, num in wide_df.columns]

# Reset index so University ID is a column
wide_df = wide_df.reset_index()

# Save to CSV
wide_df.to_csv("UniversityID_Wide.csv", index=False)

print("✅ Cleaned and wide-format file saved as 'UniversityID_UniqueCourses_Wide.csv'")
