def num_to_thai(n:float):
    split_number = str(n).split('.')
    # check for input being 0
    zero = False
    for n in split_number:
        if n == "0":
            zero = True
    if zero:
        return "ศูนย์"
    
    ones = {"1": "หนึ่ง", "2":"สอง", "3":"สาม", "4":"สี่", "5":"ห้า", "6":"หก", "7":"เจ็ด", "8":"แปด", "9":"เก้า"}
    tens = {"1": "สิบ"}
    # degits

    # decimal
    decimal = ""

    return "bruh"