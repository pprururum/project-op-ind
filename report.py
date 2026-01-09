import pandas as pd
from analysis_scores import student_scores, top_and_bottom
from analysis_attendance import student_attendance, subject_attendance, most_and_least_subjects

def make_report(students, performance, attendance, top_n=10):
    # 1) средний балл по каждому студенту
    scores = student_scores(performance)

    # 2) посещаемость по каждому студенту
    att = student_attendance(attendance)

    # 3) соединяем с таблицей students, чтобы были имена
    base = students[['Student_ID', 'Full_Name', 'Grade_Level']].copy()
    res = base.merge(scores, on='Student_ID', how='left').merge(att, on='Student_ID', how='left')

    # 4) топ/анти-топ по оценкам
    top_score, bot_score = top_and_bottom(res, 'avg_exam_score', n=top_n)

    # 5) топ/анти-топ по посещаемости
    top_att, bot_att = top_and_bottom(res, 'attendance_rate', n=top_n)

    # 6) самые и наименее посещаемые занятия (по предметам)
    subj = subject_attendance(attendance)
    most_subj, least_subj = most_and_least_subjects(subj, n=3)

    # ---- делаем текст ----
    lines = []
    lines.append("ОТЧЁТ ОБ УСПЕВАЕМОСТИ И ПОСЕЩАЕМОСТИ")
    lines.append("")
    lines.append(f"Всего студентов: {len(students)}")
    lines.append(f"Записей по успеваемости: {len(performance)}")
    lines.append(f"Записей по посещаемости: {len(attendance)}")
    lines.append("")

    # helper для маленьких таблиц
    def small_table(df, cols):
        if df is None or len(df) == 0:
            return ["(нет данных)"]
        return [df[cols].to_string(index=False)]

    lines.append(f"ТОП-{top_n} студентов по среднему баллу:")
    lines += small_table(top_score, ['Student_ID', 'Full_Name', 'Grade_Level', 'avg_exam_score'])
    lines.append("")

    lines.append(f"АНТИ-ТОП-{top_n} студентов по среднему баллу:")
    lines += small_table(bot_score, ['Student_ID', 'Full_Name', 'Grade_Level', 'avg_exam_score'])
    lines.append("")

    lines.append(f"ТОП-{top_n} студентов по посещаемости (%):")
    lines += small_table(top_att, ['Student_ID', 'Full_Name', 'Grade_Level', 'attendance_rate'])
    lines.append("")

    lines.append(f"АНТИ-ТОП-{top_n} студентов по посещаемости (%):")
    lines += small_table(bot_att, ['Student_ID', 'Full_Name', 'Grade_Level', 'attendance_rate'])
    lines.append("")

    lines.append("Наиболее посещаемые занятия (предметы):")
    lines += small_table(most_subj, ['Subject', 'attendance_rate', 'lessons_total'])
    lines.append("")

    lines.append("Наименее посещаемые занятия (предметы):")
    lines += small_table(least_subj, ['Subject', 'attendance_rate', 'lessons_total'])
    lines.append("")

    # немного общей статистики
    lines.append("Короткая статистика по среднему баллу и посещаемости:")
    lines.append(f"Средний балл (по студентам): {res['avg_exam_score'].mean():.2f}")
    lines.append(f"Средняя посещаемость (по студентам): {res['attendance_rate'].mean():.2f}%")
    lines.append("")

    return "\n".join(lines), res
