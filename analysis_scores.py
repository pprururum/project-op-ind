import pandas as pd
from clean_utils import to_percent

def student_scores(performance):
    """Считаем средний Exam_Score по каждому студенту."""
    df = performance.copy()

    # делаем проценты по ДЗ числом (если столбец есть)
    if 'Homework_Completion_%' in df.columns:
        df['Homework_Completion_%'] = df['Homework_Completion_%'].apply(to_percent)

    out = df.groupby('Student_ID', as_index=False).agg(
        avg_exam_score=('Exam_Score', 'mean'),
        subjects_count=('Subject', 'nunique')
    )

    # если есть проценты по ДЗ — добавим
    if 'Homework_Completion_%' in df.columns:
        hw = df.groupby('Student_ID', as_index=False)['Homework_Completion_%'].mean()
        hw = hw.rename(columns={'Homework_Completion_%': 'avg_homework_completion'})
        out = out.merge(hw, on='Student_ID', how='left')

    # округлим для красоты
    out['avg_exam_score'] = out['avg_exam_score'].round(2)
    if 'avg_homework_completion' in out.columns:
        out['avg_homework_completion'] = out['avg_homework_completion'].round(2)

    return out

def top_and_bottom(df, col, n=10):
    """Берем топ и анти-топ по столбцу."""
    d = df.dropna(subset=[col]).copy()
    top = d.sort_values(col, ascending=False).head(n)
    bottom = d.sort_values(col, ascending=True).head(n)
    return top, bottom
