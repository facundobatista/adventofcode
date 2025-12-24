test_lines = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""
expected_test_result = 4174379265


def _parse_lines(lines):
    (line,) = lines
    idranges = [tuple(map(int, r.split("-"))) for r in line.split(",")]
    return idranges


def run(lines):
    idranges = _parse_lines(lines)
    total = 0
    for rs, re in idranges:
        for nint in range(rs, re + 1):
            nstr = str(nint)
            ls = len(nstr)
            for nparts in range(2, ls + 1):
                step, rest = divmod(ls, nparts)
                if rest:
                    continue
                parts = set()
                for idx in range(nparts):
                    cut = nstr[step * idx:step * (idx + 1)]
                    parts.add(cut)
                if len(parts) == 1:
                    total += nint
                    break
    return total
