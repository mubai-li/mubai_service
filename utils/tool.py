def get_int_choices_enum_choices(choices_enums) -> tuple:
    choices = []
    for choices_enum in choices_enums._member_map_.values():
        choices.append((choices_enum.intvalue, choices_enum.value))

    return tuple(choices)
