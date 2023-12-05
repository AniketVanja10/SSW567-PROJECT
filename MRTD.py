from mrz.checker.td3 import TD3CodeChecker
from mrz.generator.td3 import TD3CodeGenerator
from string import ascii_uppercase, digits
import iso3166

country_list = iso3166.countries_by_alpha3.keys()


# Function to scan MRZ
def scanMRZ():
    pass


# Function to validate MRZ details
def validateMRZ(encoded_mrz):
    try:
        td3_check = TD3CodeChecker(encoded_mrz)
        if bool(td3_check):
            return True
    except Exception as err:
        pass
        return False


# Function to decode MRZ
def decodeMRZ(encoded_mrz):
    encoded_mrz = encoded_mrz.replace(';', '\n')
    decoded_mrz = TD3CodeChecker(encoded_mrz)
    if bool(decoded_mrz):
        return decoded_mrz.fields().__str__()
    return 'Invalid Field'


# Function to calculate the check digits
def cal_checkdigit(string: str):
    show = digits + ascii_uppercase
    string = string.upper().replace("<", "0")
    sequence = [7, 3, 1]
    total = 0
    for i in range(len(string)):
        c = string[i]
        if c not in show:
            raise ValueError("%s invalid char" % string, c)
        total += show.index(c) * sequence[i % 3]
    return total % 10


# Function to encode the MRZ
def encodeMRZ(document_type, issuing_country, last_name, given_name, passport_number,
              country_code, birth_date, sex, expiration_date, personal_number):
    try:
        encoded_mrz = TD3CodeGenerator(document_type, issuing_country, last_name, given_name, passport_number,
                                       country_code, birth_date, sex, expiration_date, personal_number)
        return encoded_mrz.__str__()
    except Exception as err:
        if (
                err.args.__str__() == "('String was not recognized as a valid country code or country or country name. It should be a valid country code (3 letters) or a valid country name (english)', 'U174793T5')"):
            if issuing_country != country_code:
                return "issuing_country not equal to country_code"
            if issuing_country not in country_list:
                return "illegal issuing_country"
        return err.args.__str__()


# Function to verify the check digits
def verify_checkdigits(mrz_line2, passport_number, birth_date, expiration_date, personal_number):
    passport_checkdigit = str(cal_checkdigit(passport_number))
    birth_checkdigit = str(cal_checkdigit(birth_date))
    expiration_checkdigit = str(cal_checkdigit(expiration_date))
    personal_checkdigit = str(cal_checkdigit(personal_number))

    passport_verify = mrz_line2[9]
    birthdate_verify = mrz_line2[19]
    expirationdate_verify = mrz_line2[27]
    personalnumber_verify = mrz_line2[43]

    if passport_verify != passport_checkdigit:
        return "Incorrect Passport check digit!"
    if birthdate_verify != birth_checkdigit:
        return "Incorrect birth date check digit!"
    if expirationdate_verify != expiration_checkdigit:
        return "Incorrect Passport expiration date check digit!"
    if personalnumber_verify != personal_checkdigit:
        return "Incorrect personal number check digit!"
    return "Check Digits are correct"


if __name__ == "__main__":
    scanMRZ()
    encodeMRZ("P", "REU", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M", "690413", "UK128819I")
    print(decodeMRZ("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n"
                "L898902C36UTO7408122F1204159ZE184226B<<<<<10"))