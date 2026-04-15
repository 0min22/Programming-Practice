def read_file(filename):
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                data.append(line.strip())
    except FileNotFoundError:
        print("파일이 없습니다.")
    return data


def analyze(data):
    result = {}
    for line in data:
        for ch in line:
            if ch in result:
                result[ch] += 1
            else:
                result[ch] = 1
    return result


def save_result(result, filename):
    with open(filename, "w") as f:
        f.write("=== 분석 결과 ===\n")
        for key in result:
            f.write(f"{key}: {result[key]}\n")


def main():
    data = read_file("log.txt")
    result = analyze(data)
    save_result(result, "result.txt")


if __name__ == "__main__":
    main()