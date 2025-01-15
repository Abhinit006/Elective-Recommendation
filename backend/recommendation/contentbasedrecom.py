# -*- coding: utf-8 -*-
"""contentBasedRecom.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WxULDhyrzDPV94GvQFKGLwRGXdcOXigf
"""

# Importing necessary libraries
import pandas as pd

# Read the dataset
data = pd.read_excel('/content/Anon_Data.xlsx')

# Replace roll numbers with unique numeric IDs
roll_number_mapping = {roll: idx + 1 for idx, roll in enumerate(data['RollNumber'].unique())}
data['RollNumber'] = data['RollNumber'].map(roll_number_mapping)

# Calculate the average marks for each course
average_marks_by_course = data.groupby('Course Code')['Marks (200)'].mean().reset_index()
average_marks_by_course.columns = ['Course Code', 'Average Marks']

# Function to recommend courses based on scoring capacity
def recommend_courses(student_avg_marks, course_data):
    tolerance = 5
    recommended_courses = course_data[
        (course_data['Average Marks'] >= student_avg_marks - tolerance) &
        (course_data['Average Marks'] <= student_avg_marks + tolerance)
    ]

    if recommended_courses.empty:
        closest_course = course_data.iloc[
            (course_data['Average Marks'] - student_avg_marks).abs().argmin()
        ]
        return [closest_course['Course Code']]

    return recommended_courses['Course Code'].tolist()

# Input student's average scoring capacity with validation
while True:
    student_avg_marks = float(input("Enter the student's average scoring capacity (1-200): "))
    if 1 <= student_avg_marks <= 200:
        break
    else:
        print("Invalid input. Please enter a value between 1 and 200.")

# Get recommendations
recommended_courses = recommend_courses(student_avg_marks, average_marks_by_course)

# Display recommendations
if recommended_courses:
    print(f"Recommended courses for a student with an average scoring capacity of {student_avg_marks}:")
    for course in recommended_courses:
        print(f"- {course}")
else:
    print(f"No suitable courses found for an average scoring capacity of {student_avg_marks}.")