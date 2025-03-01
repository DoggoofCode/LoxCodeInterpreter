def panic(msg: str, line: int | None = None, extra_info: list = []):
    print(extra_info)
    if line:
        print(f"\x1b[1;31m Interpreter Error: {msg}, at line {line}")
    else:
        print(f"\x1b[1;31m Interpreter Error: {msg}")

    exit(1)
