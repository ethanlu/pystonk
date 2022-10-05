from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.SupportResistanceSearch import SupportResistanceSearch

from datetime import datetime
from unittest import TestCase


class SupportResistanceSearchTest(TestCase):
    def setUp(self):
        pass

    def fixtureNoSupportResistance(self):
        return [
            CandleStick(100.00, 120.00, 80.00, 105.00, 100, int(datetime.strptime('2022-01-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 95.00, 100, int(datetime.strptime('2022-01-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-01-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 93.00, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 91.00, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 110.00, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 98.00, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 90.00, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
        ]

    def fixtureSupport(self):
        return [
            CandleStick(100.00, 110.23, 93.05, 103.67, 100, int(datetime.strptime('2022-01-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(103.67, 115.54, 95.49, 102.59, 100, int(datetime.strptime('2022-01-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.59, 120.11, 99.22, 101.95, 100, int(datetime.strptime('2022-01-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(101.95, 120.50, 99.99, 100.72, 100, int(datetime.strptime('2022-01-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.72, 119.00, 97.38, 101.00, 100, int(datetime.strptime('2022-01-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(101.00, 118.00, 96.95, 102.67, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.67, 117.00, 94.00, 103.12, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(103.12, 115.00, 92.34, 104.00, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.00, 111.00, 89.00, 98.00, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(98.00, 120.00, 88.38, 97.99, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
        ]

    def fixtureResistance(self):
        return [
            CandleStick(98.00, 120.00, 88.38, 97.99, 100, int(datetime.strptime('2022-01-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(97.99, 111.00, 89.00, 98.00, 100, int(datetime.strptime('2022-01-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(98.00, 115.00, 92.34, 100.00, 100, int(datetime.strptime('2022-01-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 117.00, 94.00, 102.12, 100, int(datetime.strptime('2022-01-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.12, 118.00, 96.95, 102.67, 100, int(datetime.strptime('2022-01-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.67, 119.00, 97.38, 105.00, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(105.00, 120.50, 99.99, 106.72, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(106.72, 120.11, 99.22, 104.95, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.95, 115.54, 95.49, 104.59, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.59, 110.23, 93.05, 103.67, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
        ]

    def fixutureMultipleSupportResistance(self):
        return [
            # nothing
            CandleStick(100.00, 120.00, 80.00, 105.00, 100, int(datetime.strptime('2022-01-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 95.00, 100, int(datetime.strptime('2022-01-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-01-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            # support 1
            CandleStick(100.00, 110.23, 93.05, 103.67, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(103.67, 115.54, 95.49, 102.59, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.59, 120.11, 99.22, 101.95, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(101.95, 120.50, 99.99, 100.72, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.72, 119.00, 97.38, 101.00, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(101.00, 118.00, 96.95, 102.67, 100, int(datetime.strptime('2022-03-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.67, 117.00, 94.00, 103.12, 100, int(datetime.strptime('2022-03-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(103.12, 115.00, 92.34, 104.00, 100, int(datetime.strptime('2022-03-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.00, 111.00, 89.00, 98.00, 100, int(datetime.strptime('2022-04-04', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(98.00, 120.00, 88.38, 97.99, 100, int(datetime.strptime('2022-04-11', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            # resistance 2
            CandleStick(97.99, 111.00, 89.00, 98.00, 100, int(datetime.strptime('2022-04-18', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(98.00, 115.00, 92.34, 100.00, 100, int(datetime.strptime('2022-04-25', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 117.00, 94.00, 102.12, 100, int(datetime.strptime('2022-05-02', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.12, 118.00, 96.95, 102.67, 100, int(datetime.strptime('2022-05-09', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.67, 119.00, 97.38, 105.00, 100, int(datetime.strptime('2022-05-16', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(105.00, 120.50, 99.99, 106.72, 100, int(datetime.strptime('2022-05-23', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(106.72, 120.11, 99.22, 104.95, 100, int(datetime.strptime('2022-05-30', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.95, 115.54, 95.49, 104.59, 100, int(datetime.strptime('2022-06-06', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.59, 110.23, 93.05, 103.67, 100, int(datetime.strptime('2022-06-13', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            # nothing
            CandleStick(100.00, 120.00, 80.00, 105.00, 100, int(datetime.strptime('2022-06-20', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 95.00, 100, int(datetime.strptime('2022-06-27', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-07-04', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            # resistance 2
            CandleStick(103.00, 111.00, 89.00, 103.50, 100, int(datetime.strptime('2022-07-11', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(103.50, 115.00, 92.34, 104.30, 100, int(datetime.strptime('2022-07-18', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.30, 117.00, 94.00, 107.72, 100, int(datetime.strptime('2022-07-25', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(107.72, 118.00, 96.95, 110.51, 100, int(datetime.strptime('2022-08-01', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(110.51, 119.00, 97.38, 108.00, 100, int(datetime.strptime('2022-08-08', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(108.00, 120.50, 99.99, 106.72, 100, int(datetime.strptime('2022-08-15', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(106.72, 120.11, 99.22, 104.95, 100, int(datetime.strptime('2022-08-22', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.95, 115.54, 95.49, 104.59, 100, int(datetime.strptime('2022-08-29', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(104.59, 110.23, 93.05, 103.67, 100, int(datetime.strptime('2022-09-05', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            # support 2
            CandleStick(103.67, 115.54, 95.49, 102.59, 100, int(datetime.strptime('2022-09-12', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.59, 120.11, 99.22, 101.95, 100, int(datetime.strptime('2022-09-19', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(101.95, 120.50, 99.99, 100.35, 100, int(datetime.strptime('2022-09-26', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(100.35, 119.00, 97.38, 102.00, 100, int(datetime.strptime('2022-10-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.00, 118.00, 96.95, 102.67, 100, int(datetime.strptime('2022-10-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(102.67, 117.00, 94.00, 105.12, 100, int(datetime.strptime('2022-10-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(105.12, 115.00, 92.34, 106.00, 100, int(datetime.strptime('2022-10-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
            CandleStick(106.00, 111.00, 89.00, 98.00, 100, int(datetime.strptime('2022-10-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),
        ]

    def testNoSupportResistanceIdentification(self):
        o = SupportResistanceSearch(self.fixtureNoSupportResistance())
        self.assertIsInstance(o, SupportResistanceSearch)
        self.assertEqual(o.supports(1.0), {}, "SupportResistanceSearch did not return expected empty supports")
        self.assertEqual(o.resistances(1.0), {}, "SupportResistanceSearch did not return expected empty resistance")

    def testSupportIdentification(self):
        o = SupportResistanceSearch(self.fixtureSupport())
        s = o.supports(2.0)
        r = o.resistances(2.0)

        self.assertEqual(list(s.keys()), ['100.72'], "SupportResistanceSearch did not return expected support keys")
        self.assertEqual(len(s['100.72']), 1, "SupportResistanceSearch did not return expected number of support prices")
        self.assertEqual(s['100.72'][0].close_price, 100.72, "SupportResistanceSearch did not return expected support price")
        self.assertEqual(s['100.72'][0].start_datetime, datetime.strptime('2022-01-24', '%Y-%m-%d'), "SupportResistanceSearch did not return expected support price datetime")
        self.assertEqual(r, {}, "SupportResistanceSearch did not return expected empty resistance")

    def testResistanceIdentification(self):
        o = SupportResistanceSearch(self.fixtureResistance())
        s = o.supports(2.0)
        r = o.resistances(2.0)

        self.assertEqual(s, {}, "SupportResistanceSearch did not return expected empty support")
        self.assertEqual(list(r.keys()), ['106.72'], "SupportResistanceSearch did not return expected resistance keys")
        self.assertEqual(len(r['106.72']), 1, "SupportResistanceSearch did not return expected number of resistance prices")
        self.assertEqual(r['106.72'][0].close_price, 106.72, "SupportResistanceSearch did not return expected resistance price")
        self.assertEqual(r['106.72'][0].start_datetime, datetime.strptime('2022-02-14', '%Y-%m-%d'), "SupportResistanceSearch did not return expected resistance price datetime")

    def testMultipleSupportResistanceIdentification(self):
        o = SupportResistanceSearch(self.fixutureMultipleSupportResistance())

        s = o.supports(2.0)
        self.assertEqual(list(s.keys()), ['100.53'], "SupportResistanceSearch did not return expected support keys")
        self.assertEqual(len(s['100.53']), 2, "SupportResistanceSearch did not return expected number of support prices")
        self.assertEqual(s['100.53'][0].close_price, 100.72, "SupportResistanceSearch did not return expected support price")
        self.assertEqual(s['100.53'][0].start_datetime, datetime.strptime('2022-02-28', '%Y-%m-%d'), "SupportResistanceSearch did not return expected support price datetime")
        self.assertEqual(s['100.53'][1].close_price, 100.35, "SupportResistanceSearch did not return expected support price")
        self.assertEqual(s['100.53'][1].start_datetime, datetime.strptime('2022-09-26', '%Y-%m-%d'), "SupportResistanceSearch did not return expected support price datetime")

        r = o.resistances(2.0)
        self.assertEqual(list(r.keys()), ['106.72', '110.51'], "SupportResistanceSearch did not return expected resistance keys")
        self.assertEqual(len(r['106.72']), 1, "SupportResistanceSearch did not return expected number of resistance prices")
        self.assertEqual(r['106.72'][0].close_price, 106.72, "SupportResistanceSearch did not return expected resistance price")
        self.assertEqual(r['106.72'][0].start_datetime, datetime.strptime('2022-05-23', '%Y-%m-%d'), "SupportResistanceSearch did not return expected resistance price datetime")
        self.assertEqual(len(r['110.51']), 1, "SupportResistanceSearch did not return expected number of resistance prices")
        self.assertEqual(r['110.51'][0].close_price, 110.51, "SupportResistanceSearch did not return expected resistance price")
        self.assertEqual(r['110.51'][0].start_datetime, datetime.strptime('2022-08-01', '%Y-%m-%d'), "SupportResistanceSearch did not return expected resistance price datetime")
