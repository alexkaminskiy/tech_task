import pytest

from utils.normalize_code import normalize_code


class TestValidInputs:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("1234567890", "1234567890"),  # exactly 10, unchanged
            ("6623331", "0006623331"),  # padded to 10
            ("N12345", "0000012345"),  # N prefix stripped, then padded
            (" 6623331 ", "0006623331"),  # whitespace trimmed
            ("n12345", "0000012345"),  # lowercase n prefix
            ("0", "0000000000"),  # single digit
            ("0000000000", "0000000000"),  # already all zeros
            ("N0000000000", "0000000000"),  # N prefix + all zeros
            (" N6623331 ", "0006623331"),  # whitespace around N-prefixed code
        ],
    )
    def test_valid(self, raw, expected):
        assert normalize_code(raw) == expected


class TestInvalidInputs:
    @pytest.mark.parametrize(
        "raw",
        [
            "ABC123",  # non-numeric
            "null",  # string literal, non-numeric
            "",  # empty
            "112233445566",  # more than 10 digits
            "p6623331",  # leading letter that is not N/n
            "N",  # prefix with nothing left after stripping
            "n",  # same, lowercase
            "   ",  # whitespace only
            "12 34",  # embedded whitespace
            "123-456",  # non-digit punctuation
            "Nn123",  # only a single leading N/n is allowed
            "12345678901",  # 11 digits, over the limit
            "-1234567",  # sign character not allowed
            "1234567.0",  # decimal point not allowed
        ],
    )
    def test_invalid_raises(self, raw):
        with pytest.raises(ValueError):
            normalize_code(raw)

    def test_none_raises(self):
        with pytest.raises(ValueError):
            normalize_code(None)

    def test_error_message_mentions_reason(self):
        # Spot-check that messages are actually informative, not just present.
        with pytest.raises(ValueError, match="digits"):
            normalize_code("123ABC")  # non-letter first char, non-digit body
        with pytest.raises(ValueError, match="letter"):
            normalize_code("ABC123")  # invalid leading letter
        with pytest.raises(ValueError, match="None"):
            normalize_code(None)
        with pytest.raises(ValueError, match="10"):
            normalize_code("112233445566")


class TestEdgeCases:
    def test_ten_digit_code_with_n_prefix_and_leading_zero_body(self):
        # Body is exactly 10 digits after stripping N -> already max length.
        assert normalize_code("N1234567890") == "1234567890"

    def test_max_length_boundary_exactly_ten(self):
        assert normalize_code("9999999999") == "9999999999"

    def test_over_boundary_by_one_digit(self):
        with pytest.raises(ValueError):
            normalize_code("99999999999")  # 11 digits

    def test_unicode_digits_are_rejected(self):
        # Arabic-indic / fullwidth digits look numeric but aren't ASCII 0-9.
        with pytest.raises(ValueError):
            normalize_code("١٢٣٤٥٦٧")

    def test_tab_and_newline_whitespace_trimmed(self):
        assert normalize_code("\t6623331\n") == "0006623331"

    def test_internal_case_n_only_as_first_char(self):
        # 'n' appearing after the first character is just an invalid digit char.
        with pytest.raises(ValueError):
            normalize_code("123n456")