import unittest
from unittest import mock
import MRTD

class TestMRTDModule(unittest.TestCase):

    @mock.patch('MRTD.scanMRZ')
    def test_successful_MRZ_decoding(self, mock_scanMRZ):
        mock_scanMRZ.return_value = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<;L898902C36UTO7408122F1204159ZE184226B<<<<<10"
        result = MRTD.scanMRZ()
        self.assertEqual(MRTD.decodeMRZ(result),
                         "fields(surname='ERIKSSON', name='ANNA MARIA', country='UTO', nationality='UTO', "
                         "birth_date='740812', expiry_date='120415', sex='F', document_type='P', "
                         "document_number='L898902C3', optional_data='ZE184226B', birth_date_hash='2', "
                         "expiry_date_hash='9', document_number_hash='6', optional_data_hash='1', final_hash='0')")

    @mock.patch('MRTD.scanMRZ')
    def test_wrong_document_type_decoding(self, mock_scanMRZ):
        mock_scanMRZ.return_value = "Z<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<;L898902C36UTO7408122F1204159ZE184226B<<<<<10"
        result = MRTD.scanMRZ()
        self.assertEqual(MRTD.decodeMRZ(result), "Invalid Field")

    # ... (similar paraphrasing for other test cases)

    def test_successful_MRZ_encoding(self):
        self.assertEqual(
            MRTD.encodeMRZ("P", "REU", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M", "690413",
                           "UK128819I"),
            "P<REUMCFARLAND<<TRINITY<AMITY<<<<<<<<<<<<<<<\nQ683170H11REU6403131M6904133UK128819I<<<<<94")

    def test_wrong_country_code_encoding(self):
        self.assertEqual(
            MRTD.encodeMRZ("P", "ABC", "MCFARLAND", "TRINITY AMITY", "Q683170H1", "REU", "640313", "M", "690413",
                           "UK128819I"),
            "('String was not recognized as a valid country code or country or country name. "
            "It should be a valid country code (3 letters) or a valid country name ("
            "english)', 'ABC')")

    # ... (similar paraphrasing for other test cases)

    def test_successful_MRZ_validation(self):
        self.assertEqual(MRTD.validateMRZ("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n"
                                          "L898902C36UTO7408122F1204159ZE184226B<<<<<10"), True)

    def test_invalid_input_MRZ_validation(self):
        self.assertEqual(MRTD.validateMRZ("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n"
                                          "L898902C36UTO7408122F1204159Z<<<<<10"), False)

    # ... (similar paraphrasing for other test cases)

    def test_incorrect_personal_number_check_digit(self):
        self.assertEqual(MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<10", "L898902C3", "740812",
                                                  "120415", "ZE184226B"), 'Incorrect personal number check digit!')

    def test_correct_check_digits(self):
        self.assertEqual(MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<<1", "L898902C3", "740812",
                                                  "120415", "ZE184226B"), "Check Digits are correct")

    def test_incorrect_birth_date_check_digit(self):
        self.assertEqual(MRTD.verify_checkdigits("L898902C36UTO7408122F1204159ZE184226B<<<<<<10", "L898902C3", "74081",
                                                  "120415", "ZE184226B"), "Incorrect birth date check digit!")

if __name__ == '__main__':
    unittest.main()
