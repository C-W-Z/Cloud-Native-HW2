import sys
import re

def is_valid_task_line(line):
    # 合法 task list 格式（只允許空白、x、X）
    return re.match(r"^\s*[-+*]\s\[( |x|X)\]\s.+", line)

def is_potential_task_line(line):
    # 抓出可能是 task list 的行
    return re.search(r"^\s*[-+*]\s*\[.*\]", line)

def check_markdown(filename):
    issues = []
    with open(filename, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            # 標題格式檢查
            if line.startswith('#') and not re.match(r"#+\s", line):
                issues.append(f"{filename}:{lineno}: 標題後缺空格 `{line.strip()}`")

            # 檢查任務清單格式
            if is_potential_task_line(line) and not is_valid_task_line(line):
                issues.append(f"{filename}:{lineno}: 任務清單格式錯誤 `{line.strip()}`")

    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("請指定 Markdown 檔案")
        sys.exit(1)

    all_issues = []
    for filename in sys.argv[1:]:
        all_issues += check_markdown(filename)

    if all_issues:
        print("格式錯誤")
        for issue in all_issues:
            print(issue)
        sys.exit(1)  # 讓 GitHub Action 判定為失敗
    else:
        print("✅格式正確")
