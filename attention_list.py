import pandas as pd

from load_data import load_all
from analysis_scores import student_scores
from analysis_attendance import student_attendance


def build_summary(students, performance, attendance):
    # собираем одну таблицу, как в report.py, чтобы дальше было удобно фильтровать
    scores = student_scores(performance)
    att = student_attendance(attendance)

    base = students[["Student_ID", "Full_Name", "Grade_Level"]].copy()
    res = base.merge(scores, on="Student_ID", how="left").merge(att, on="Student_ID", how="left")
    return res


def read_float(prompt, default_value):
    # простой ввод числа, если enter то берется значение по умолчанию
    s = input(prompt).strip()
    if s == "":
        return float(default_value)

    s = s.replace(",", ".")
    try:
        return float(s)
    except:
        print("не похоже на число, беру значение по умолчанию")
        return float(default_value)


def df_to_lines(df, cols, limit=15):
    if df is None or len(df) == 0:
        return ["(нет данных)"]
    return [df[cols].head(limit).to_string(index=False)]


def main():
    students, performance, attendance, homework, comm = load_all()
    res = build_summary(students, performance, attendance)

    # базовые значения для порогов берем из средних по всем студентам
    avg_score = res["avg_exam_score"].mean()
    avg_att = res["attendance_rate"].mean()

    print("мини отчет: кому нужно внимание")
    print("")
    print(f"средний балл по всем студентам: {avg_score:.2f}")
    print(f"средняя посещаемость по всем студентам: {avg_att:.2f}%")
    print("")

    score_cut = read_float(f"порог по баллу (enter = {avg_score:.2f}): ", avg_score)
    att_cut = read_float(f"порог по посещаемости (enter = {avg_att:.2f}): ", avg_att)

    # три простые группы
    # 1) низкий балл и низкая посещаемость
    # 2) низкий балл, но посещаемость нормальная
    # 3) балл нормальный, но посещаемость низкая
    low_score = res["avg_exam_score"] < score_cut
    low_att = res["attendance_rate"] < att_cut

    g1 = res[low_score & low_att].copy()
    g2 = res[low_score & (~low_att)].copy()
    g3 = res[(~low_score) & low_att].copy()

    # сортировки чтобы сверху были самые проблемные примеры
    g1 = g1.sort_values(["avg_exam_score", "attendance_rate"], ascending=[True, True])
    g2 = g2.sort_values(["avg_exam_score", "attendance_rate"], ascending=[True, False])
    g3 = g3.sort_values(["attendance_rate", "avg_exam_score"], ascending=[True, False])

    cols = ["Student_ID", "Full_Name", "Grade_Level", "avg_exam_score", "attendance_rate"]

    lines = []
    lines.append("мини отчет: кому нужно внимание")
    lines.append("")
    lines.append(f"порог по баллу: {score_cut:.2f}")
    lines.append(f"порог по посещаемости: {att_cut:.2f}%")
    lines.append("")

    print("")
    print("группа 1: низкий балл и низкая посещаемость")
    print(f"студентов: {len(g1)}")
    for x in df_to_lines(g1, cols):
        print(x)
    lines.append("группа 1: низкий балл и низкая посещаемость")
    lines.append(f"студентов: {len(g1)}")
    lines += df_to_lines(g1, cols)
    lines.append("")

    print("")
    print("группа 2: низкий балл, но посещаемость нормальная")
    print(f"студентов: {len(g2)}")
    for x in df_to_lines(g2, cols):
        print(x)
    lines.append("группа 2: низкий балл, но посещаемость нормальная")
    lines.append(f"студентов: {len(g2)}")
    lines += df_to_lines(g2, cols)
    lines.append("")

    print("")
    print("группа 3: балл нормальный, но посещаемость низкая")
    print(f"студентов: {len(g3)}")
    for x in df_to_lines(g3, cols):
        print(x)
    lines.append("группа 3: балл нормальный, но посещаемость низкая")
    lines.append(f"студентов: {len(g3)}")
    lines += df_to_lines(g3, cols)
    lines.append("")

    ans = input("сохранить в файл attention_report.txt (y/n): ").strip().lower()
    if ans == "y":
        with open("attention_report.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("сохранил: attention_report.txt")


if __name__ == "__main__":
    main()
