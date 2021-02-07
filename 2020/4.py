#!/usr/bin/env python3


import operator
import functools

import re

required_fields = """
byr
iyr
eyr
hgt
hcl
ecl
pid
""".strip().split()
#cid


def validate_height(value):
    unit = value[-2:]
    number = int(value[:-2])
    #print("unit:", unit, "number:", number)
    if 'cm' == unit:
        return 150 <= number <= 193
    elif 'in' == unit:
        return 59 <= number <= 76
    else:
        raise Exception("invalid unit:", unit)

VALID_ECL = set("amb blu brn gry grn hzl oth".split())
validator_by_field_name = {
        'byr': lambda v: 1920 <= int(v) <= 2002,
        'iyr': lambda v: 2010 <= int(v) <= 2020,
        'eyr': lambda v: 2020 <= int(v) <= 2030,
        'hgt': validate_height,
        'hcl': lambda v: re.match(r'#([0-9]|[a-f]){6}', v),
        'ecl': lambda v: v in VALID_ECL,
        'pid': lambda v: re.match(r'[0-9]{9}', v),
}
def is_valid_complex(passport):
    for field_name, validator in validator_by_field_name.items():
        validator = validator_by_field_name.get(
            field_name,
            lambda v: False
        )
        try:
            if not validator(passport[field_name]):
                return False
        except:
            return False

    return True


def is_valid_simple(passport):
    for field_name in required_fields:
        if field_name not in passport:
            #print(f"missing {field_name} from {passport}")
            return False
    return True


def count_valid_passports(lines, is_valid=is_valid_simple):
    passport = {}
    valid_passports = []
    for line in lines:
        line = line.strip()
        if not line:
            if is_valid(passport):
                valid_passports.append(passport)

            passport = {}
        else:
            # parse new fields
            new_fields = [term.split(':') for term in line.split()]
            passport.update(new_fields)

    # check last passport
    if is_valid(passport):
        valid_passports.append(passport)
    return len(valid_passports)


uut = count_valid_passports
if __name__ == "__main__":
    with open('input04.txt', 'rt') as f:
        print('part1:', uut(f))
        f.seek(0)
        print("part2:", uut(f, is_valid=is_valid_complex))
        pass


import io
import pytest # for decorator

sample = io.StringIO("""
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""".strip())
def test_uut_part1():
    assert 2 == uut(sample)


def test_uut_complex_invalid():
    assert 0 == uut(io.StringIO("""
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007
    """.strip()), is_valid=is_valid_complex)


def test_uut_complex_valid():
    assert 4 == uut(io.StringIO("""
    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    """.strip()), is_valid=is_valid_complex)


@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
