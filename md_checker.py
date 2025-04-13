import sys
import re

def is_valid_task_line(line):
    # 合法 task list 格式（只允許空白、x、X）
    return re.match(r"^\s*[-+*]\s\[( |x|X)\]\s.+", line)

def is_potential_task_line(line):
    # 抓出可能是 task list 的行
    return re.search(r"^\s*[-+*]\s*\[.*\]", line)

def find_invalid_links(line):
    issues = []

    # 合法連結格式：[說明文字](網址)
    link_pattern = r"\[[^\[\]]+\]\([^)]+\)"
    all_matches = re.finditer(r"\[.*?\]\(.*?\)", line)

    for match in all_matches:
        if not re.match(link_pattern, match.group()):
            issues.append(f"可能的連結格式錯誤 `{match.group()}`")

    return issues

def check_markdown(filename):
    issues = []
    with open(filename, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            # 標題格式檢查
            if line.startswith('#') and not re.match(r"#+\s", line):
                issues.append(f"{filename}:{lineno}: Missing space after title `{line.strip()}`")

            # 檢查任務清單格式
            if is_potential_task_line(line) and not is_valid_task_line(line):
                issues.append(f"{filename}:{lineno}: Task list format error `{line.strip()}`")

            # 檢查連結格式
            link_issues = find_invalid_links(line)
            for li in link_issues:
                issues.append(f"{filename}:{lineno}: {li}")

    return issues

if __name__ == "__main__":
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

    if len(sys.argv) < 2:
        print("Please specify a Markdown file")
        sys.exit(1)

    all_issues = []
    for filename in sys.argv[1:]:
        all_issues += check_markdown(filename)

    if all_issues:
        print("Format Error")
        for issue in all_issues:
            print(issue)
        sys.exit(1)  # 讓 GitHub Action 判定為失敗
    else:
        print("✅ Correct")
