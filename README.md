# Variable Elimination
This repository contains an implementation of the variable elimination algorithm, a method for efficiently computing marginal probabilities in Bayesian networks. The algorithm works by iteratively eliminating variables from the network until only the desired variables remain. The implementation can read any network from a `.bif` file. Also see the accompanying [paper](docs/paper.pdf). An example output is shown below.

```
-----------------------------------------------------
Running VE on the following setup
-----------------------------------------------------

Query: Leaving, Smoke
Evidence: Alarm = False
Barren: Report

-----------------------------------------------------
Elimination order
-----------------------------------------------------

No elimination order instructions are given
An arbitrary elimination order is chosen

Order: [Fire, Tampering]

-----------------------------------------------------
Reduced factors of nonbarren nodes based on evidence
Evidence: Alarm = False
-----------------------------------------------------

f06(Fire, Tampering)(Alarm)
f01(Fire)()
f07(Leaving)(Alarm)
f04(Fire, Smoke)()
f05(Tampering)()

-----------------------------------------------------
Main loop of VE, going over all the variables
Order: [Fire, Tampering]
-----------------------------------------------------

f06(Fire, Tampering)(Alarm)
f01(Fire)()
f07(Leaving)(Alarm)
f04(Fire, Smoke)()
f05(Tampering)()

-----------------------------------------------------
Processing variable Fire
-----------------------------------------------------

Multiplying the following factors:

f01(Fire)()
f06(Fire, Tampering)(Alarm)
f04(Fire, Smoke)()

Resulting in:

f09(Fire, Smoke, Tampering)(Alarm)

Marginalizing over Fire gives:

f10(Smoke, Tampering)(Alarm)

The new factors are:

f07(Leaving)(Alarm)
f05(Tampering)()
f10(Smoke, Tampering)(Alarm)

-----------------------------------------------------
Processing variable Tampering
-----------------------------------------------------

Multiplying the following factors:

f05(Tampering)()
f10(Smoke, Tampering)(Alarm)

Resulting in:

f11(Smoke, Tampering)(Alarm)

Marginalizing over Tampering gives:

f12(Smoke)(Alarm)

The new factors are:

f07(Leaving)(Alarm)
f12(Smoke)(Alarm)

-----------------------------------------------------
Multiply the final factors
-----------------------------------------------------

Multiplying the following factors:

f07(Leaving)(Alarm)
f12(Smoke)(Alarm)

Resulting in:

f13(Leaving, Smoke)(Alarm)

-----------------------------------------------------
Normalization and final factor
-----------------------------------------------------

f14, variables: [Leaving, Smoke], reduced: [Alarm]
  Leaving  Smoke      prob
0   False  False  0.988829
1   False   True  0.010171
2    True  False  0.000990
3    True   True  0.000010
```
