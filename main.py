from load_data import load_all
from report import make_report

def main():
    students, performance, attendance, homework, comm = load_all()

    text, table = make_report(students, performance, attendance, top_n=10)

    print(text)

    # сохраним в файл, чтобы удобно сдавать
    with open('report.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    # сохраняем общую табличку
    table.to_csv('students_summary.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()
