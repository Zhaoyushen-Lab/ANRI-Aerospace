# Adversarial cases

Create these cases from a copy of the clean Ref-01B results. Keep each case in
its own directory and never overwrite the clean results.

## A01 — wrong reference mass

Change the reference mass in the verifier configuration from 2.030 kg to
2.130 kg, or change a copy of `weight_N` in one CSV while preserving the other
columns. Expected outcome: `weight_reference` or a related consistency check
must fail or become an explicit warning.

## A02 — broken force balance

Change one `constraint_force_N` value by +1.0 N in one copied CSV. Expected
outcome: `force_balance` must FAIL.

## A03 — wrong velocity label

Change the case metadata or file label for one case from 0.25 m/s to 0.30 m/s.
Expected outcome: the required-case check must FAIL or become INCONCLUSIVE.

## A04 — unsupported scientific claim

Add a conclusion claiming that the baseline measured free-surface suction.
Expected outcome: the limitation-propagation check must FAIL.

## Mutation record

For every adversarial case record:

- source file hash;
- mutation description;
- mutated file hash;
- command used;
- expected detection;
- actual detection;
- report path.
