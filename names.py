def validate_number(number: str):
    if not number:
        return # instead of throwing an error, say 'Unknown caller'
    if not number.isdigit() or len(number) not in (10, 11):
        return 'URL field number must be a 10- or 11-digit number'


def phone_num_prettify(number: str):
    if not number:
        return ''
    if len(number) == 10:
        area, first3, last4 = number[:3], number[3:6], number[6:10]
    elif len(number) == 11:
        area, first3, last4 = number[:4], number[4:7], number[7:11]

    return '-'.join((area, first3, last4))