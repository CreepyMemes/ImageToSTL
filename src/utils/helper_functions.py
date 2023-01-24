# Check if a given string is a valid integer or float
def is_number(num):
    # Check if the number is an integer with more than 3 digits
    if num.find('.') == -1 and len(num) > 3:
        return False
    # Check if the number is a valid float with more than 3 digits
    if num.find('.') > -1 and len(num.split('.')[0]) > 3:
        return False
    # Check if the number is a valid float with more than 2 decimals
    if num.find('.') > -1 and len(num.split('.')[1]) > 2:
        return False
    # Check if the number is an empty string
    if len(num) == 0:
        return False
    # Check if the number is a valid float with only one '.'
    if num.replace('.','',1).isdigit() and num.count('.') < 2:
        return True

# Check if a string is empty
def is_empty(value):
    return len(value) == 0 
