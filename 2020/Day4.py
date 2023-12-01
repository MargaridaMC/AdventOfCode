from aocd import get_data
import re

lines = get_data(day=4, year=2020)
#with open("../test_input.txt") as f:
#    lines = f.read()

mandatory_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} #  "cid"
passports = [{k_v_pair.split(":")[0]: k_v_pair.split(":")[1] for k_v_pair in line.replace("\n", " ").split(" ")} for line in lines.split("\n\n")]

valid_passport_count = 0
for p in passports:
    valid_passport_count += set(p.keys()).issuperset(mandatory_fields)

print("Part 1 number of valid passports", valid_passport_count)

valid_passport_count = 0
for p in passports:
    if set(p.keys()).issuperset(mandatory_fields):
        if int(p["byr"]) not in range(1920, 2003): continue
        if int(p["iyr"]) not in range(2010, 2021): continue
        if int(p["eyr"]) not in range(2020, 2031): continue
        hgt = p["hgt"]
        height_value = int(hgt[:-2])
        if ("cm" not in hgt and "in" not in hgt) or (hgt.endswith("cm") and height_value not in range(150, 194)) or (hgt.endswith("in") and height_value not in range(59, 77)): continue
        hcl_match = re.match("#[0-9a-f]{6}", p["hcl"])
        if hcl_match is None: continue
        if p["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]: continue
        if not (len(p["pid"]) == 9 and p["pid"].isdigit()): continue

        valid_passport_count += 1

print("Part 2 number of valid passports", valid_passport_count)