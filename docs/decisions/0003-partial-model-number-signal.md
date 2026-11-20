# 0003: Add a "partly matching model number" signal, and show what it costs

**Status:** accepted, 0.1.0

## Context

Many duplicates the first model missed had model numbers that differ by a prefix or suffix, such as "p-fdu4" and "p-fdu4gbsv-ef" in the validation pairs. I first noticed the pattern while looking at test pairs, which should not drive any choice. I checked that the same pattern appears in the validation pairs before adding the signal.

## Decision

Add two signals: one model number contains the other (both at least 5 characters), and a model number is missing on one side.

## Tradeoff

- The combined model found more duplicates: on Walmart-Amazon from 66% to 78% at its best threshold, and its ranking score rose from 0.728 to 0.747.
- The same signal caused the only wrong merge on Walmart-Amazon: "icusb1284" (6 ft) and "icusb128410" (10 ft). Model number families are a real risk, and the page lists every wrong merge so a reviewer can see it.
