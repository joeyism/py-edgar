import unittest
from edgar import XBRL

class TestXBRL(unittest.TestCase):

  def test_parse_context_ref(self):
    input_output = [
      ("As_Of_2_16_2016_abt_CurrencyExchangeRateAxis_abt_DiproRateMember", {"from": "2016-02-16"}),
      ("Duration_1_1_2018_To_12_31_2018", {"from": "2018-01-01", "to": "2018-12-31"}),
      ("Duration_1_1_2018_To_12_31_2018_xxx_ABC", {"from": "2018-01-01", "to": "2018-12-31"}),
      ("As_Of_12_31_2017", {"from": "2017-12-31"}),
      ("As_Of_12_31_2017_xxx_ABC", {"from": "2017-12-31"}),
      ("FD2019Q4YTD_us-gaap_StatementEquityComponentsAxis_us-gaap_RetainedEarningsMember", {"other": "FD2019Q4YTD"})
    ]

    for inp, output in input_output:
      self.assertEqual(XBRL.parse_context_ref(inp), output)
