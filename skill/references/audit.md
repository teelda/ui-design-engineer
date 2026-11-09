# Focused UI audit

Start with the user, goal, device, primary journey, and evidence mode. Use **interactive** for exercised behavior, **source-assisted** for implementation evidence, and **snapshot** for supplied screenshots or DOM facts. A screenshot cannot prove accessible names, hidden states, or task completion.

Check only relevant layers: orientation, hierarchy, visual consistency, interaction states, responsive layout, content, accessibility, trust, and implementation. Compare against the actual design system if available. Intentional branding is not a defect without a user impact.

Report a small ranked set of unique findings. For each: type (observed defect, source risk, or recommendation), evidence, impact, concrete fix, and an observable acceptance criterion. Record coverage and untested states. Do not invent pixel measurements, privacy claims, or user counts.

Rank by consequence, reach, frequency, workaround, and recoverability. Use these examples as calibration, not fixed labels:

| Level | Example |
|---|---|
| S0 | A demonstrated irreversible loss or widespread inability to complete the core task, with no practical recovery. |
| S1 | A major path fails for many users or a serious risk is directly evidenced. |
| S2 | Significant confusion or a blocked path with a workable recovery. |
| S3 | A local usability or clarity problem that slows the task. |
| S4 | A polish improvement with limited task impact. |

For AI interfaces, inspect what is generated versus verified, evidence per finding, uncertainty, correction, cancellation, stale results, permissions, and recovery. A ranked list or score helps navigation but does not prove AI accuracy. Test repeat runs before claiming consistency. An audit does not authorize changing the product or publishing it.
