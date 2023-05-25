def list_to_console(list_to_print):
    list_str = []
    index = 0
    for element in list_to_print:
        list_str.append(f"{index}: {element}")
        index += 1
    print(" | ".join(list_str))
