import unittest
from edgar import Edgar

class TestEdgar(unittest.TestCase):

  def test_split_raw_string_to_cik_name(self):
    input_output = [
      ("591 BEVERAGE, INC.:0001602820:", ("591 BEVERAGE, INC.", "0001602820")),
      ("5:15 FUND, LTD.:0001464817:", ("5:15 FUND, LTD.", "0001464817")),
      ("!J INC:0001438823:", ("!J INC", "0001438823"))
    ]
    for inp, output in input_output:
      self.assertEqual(Edgar.split_raw_string_to_cik_name(inp), output)
