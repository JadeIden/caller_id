def validate_number(number: str):
    if not number:
        return # instead of throwing an error, say 'Unknown caller'
    if not number.isdigit() or len(number) not in (10, 11):
        return 'URL field number must be a 10- or 11-digit number'


def phone_num_prettify(number: str):
    if not number:
        return ''
    if len(number) == 10:
        chunks = number[:3], number[3:6], number[6:10]
    elif len(number) == 11:
        chunks = number[0:1], number[1:4], number[4:7], number[7:11]
    return '-'.join(chunks)


def name_to_audio(name, number):
    error = validate_number(number)
    if error:
        raise ValueError(error)
    pretty_num = phone_num_prettify(number)
    if not name or name.lower() == "unknown":
        name_num = f"Unknown caller {pretty_num}"
    elif name.lower() == "blocked":
        name_num = f"Blocked number {pretty_num}"
    else:
        name_num = name
    to_audio = name_num
    return to_audio
