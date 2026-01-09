# analysis_attendance.py
# Всё про посещаемость: % посещений и самые/наименее посещаемые занятия.

import pandas as pd
from clean_utils import is_present

def student_attendance(attendance):
    """Считаем долю посещений (Present/Late) по каждому студенту."""
    df = attendance.copy()

    df['present_flag'] = df['Attendance_Status'].apply(is_present).astype(int)

    out = df.groupby('Student_ID', as_index=False).agg(
        lessons_total=('present_flag', 'count'),
        lessons_present=('present_flag', 'sum')
    )
    out['attendance_rate'] = (out['lessons_present'] / out['lessons_total']) * 100
    out['attendance_rate'] = out['attendance_rate'].round(2)

    return out

def subject_attendance(attendance):
    """Считаем посещаемость по предметам (это и есть 'занятия' в простом виде)."""
    df = attendance.copy()
    df['present_flag'] = df['Attendance_Status'].apply(is_present).astype(int)

    out = df.groupby('Subject', as_index=False).agg(
        lessons_total=('present_flag', 'count'),
        lessons_present=('present_flag', 'sum')
    )
    out['attendance_rate'] = (out['lessons_present'] / out['lessons_total']) * 100
    out['attendance_rate'] = out['attendance_rate'].round(2)

    return out

def most_and_least_subjects(subject_df, n=3):
    d = subject_df.dropna(subset=['attendance_rate']).copy()
    most = d.sort_values('attendance_rate', ascending=False).head(n)
    least = d.sort_values('attendance_rate', ascending=True).head(n)
    return most, least
