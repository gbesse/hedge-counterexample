import copy
import itertools
import random
import unittest
from hedge_counterexample.__main__ import example
from hedge_counterexample.engine import analyze,utc_seconds,iso,validate,payoff,evaluate,verify_witness
class HedgeTests(unittest.TestCase):
    def test_same_title_timezones_create_both_losing_legs(self):
        r=analyze(example());self.assertEqual(r['full_fill_worst']['payoff']['settled_net_cents'],-924);self.assertTrue(r['witness_replay']['valid']);self.assertEqual(r['normalized_deadlines'][1]['utc'],'2026-10-21T02:00:00Z')
    def test_matching_rules_full_fill_has_positive_synthetic_net(self):
        r=analyze(example('partial-fill-gap'),False);self.assertEqual(r['worst']['payoff']['settled_net_cents'],76)
    def test_independent_partial_fills_break_full_fill_cover(self):
        r=analyze(example('partial-fill-gap'));self.assertEqual(r['worst']['payoff']['settled_net_cents'],-462);self.assertIn(0,r['worst']['fills']);self.assertEqual(r['full_fill_worst']['payoff']['settled_net_cents'],76)
    def test_zero_fill_has_no_fixed_fee(self):
        c=example();_,contracts=validate(c);world={'fictional_launch':utc_seconds('2026-10-20T21:00:00Z')};self.assertEqual(payoff(contracts,world,[0,0])['cost_cents'],0)
    def test_unresolved_is_interval_not_realized_loss(self):
        c=example()
        for contract in c['contracts']:contract['settlement']='unresolved'
        r=analyze(c);p=r['worst']['payoff'];self.assertIsNone(p['settled_net_cents']);self.assertEqual(p['net_interval_cents'],[-924,1076]);self.assertEqual(p['unresolved_cost_cents'],924)
    def test_dst_ambiguous_time_requires_fold_and_folds_differ(self):
        d={'local':'2026-11-01T01:30:00','zone':'America/New_York'}
        with self.assertRaises(ValueError):utc_seconds(d)
        self.assertEqual(utc_seconds({**d,'fold':1})-utc_seconds({**d,'fold':0}),3600)
    def test_dst_nonexistent_time_rejected(self):
        with self.assertRaises(ValueError):utc_seconds({'local':'2026-03-08T02:30:00','zone':'America/New_York'})
    def test_naive_time_fractional_seconds_and_invalid_fold_rejected(self):
        for d in ('2026-10-20T12:00:00','2026-10-20T12:00:00.1Z',{'local':'2026-11-01T01:30:00','zone':'America/New_York','fold':True}):
            with self.assertRaises(ValueError):utc_seconds(d)
    def test_inclusive_and_exclusive_boundary_are_distinct(self):
        c=example('partial-fill-gap');c['contracts'][1]['rule']['op']='at_or_before';r=analyze(c,False);self.assertEqual(r['worst']['events']['fictional_launch'],'2026-10-20T22:00:00Z');self.assertEqual(r['worst']['payoff']['settled_net_cents'],-924)
    def test_critical_cells_match_full_second_enumeration_on_random_small_cases(self):
        rng=random.Random(11);origin=utc_seconds('2026-10-20T00:00:00Z')
        for _ in range(20):
            c=example('partial-fill-gap');c['events']['fictional_launch']={'start':iso(origin),'end':iso(origin+12),'allow_absent':True}
            for contract in c['contracts']:
                contract['rule']['deadline']=iso(origin+rng.randrange(13));contract['rule']['op']=rng.choice(['before','at_or_before'])
            _,contracts=validate(c);expected=min(payoff(contracts,{'fictional_launch':time},fills)['net_interval_cents'][0] for time in [None,*range(origin,origin+13)] for fills in itertools.product(*[v['fills'] for v in contracts]))
            self.assertEqual(analyze(c)['worst']['payoff']['net_interval_cents'][0],expected)
    def test_witness_replay_rejects_tampered_cost_or_truncated_fills(self):
        c=example();w=analyze(c)['worst'];w['payoff']['cost_cents']=0;self.assertFalse(verify_witness(c,w)['valid']);w=analyze(c)['worst'];w['fills']=[];self.assertFalse(verify_witness(c,w)['valid'])
    def test_nonfictional_negative_fee_bool_quantity_and_unknown_rule_rejected(self):
        for field,value in [('fee_per_unit_cents',-1),('quantity',True),('rule',{'op':'python','code':'anything'})]:
            c=example();c['contracts'][0][field]=value
            with self.assertRaises(ValueError):analyze(c)
        c=example();c['fictional']=False
        with self.assertRaises(ValueError):analyze(c)
    def test_boolean_composition_and_absent_event_semantics(self):
        c=example();rule=c['contracts'][0]['rule'];c['contracts'][0]['rule']={'op':'or','args':[rule,{'op':'not','arg':rule}]};_,contracts=validate(c);self.assertTrue(evaluate(contracts[0]['compiled_rule'],{'fictional_launch':None}))
if __name__=='__main__':unittest.main()
