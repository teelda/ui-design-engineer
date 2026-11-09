# Illustrative before and after

These examples show the decision boundary. They are **not** results from a model benchmark.

## Existing brand

**Request:** “Improve the signup page's hierarchy. Keep our coral gradient, typography, and video.”

**Poor response:** Replaces the gradient with a flat purple button, swaps the typeface, removes the video, and calls the result cleaner. It follows a generic minimal style instead of the brief.

**Better response:** Inspects the existing tokens and page, keeps the gradient and video, adjusts heading/supporting-copy scale and spacing, verifies text contrast across the gradient, and tests narrow layout plus loading/error states. It reports any unavailable viewport or interaction test.

## Screenshot-only audit

**Poor finding:** “The form has no accessible labels and the submit button does not work.” Neither claim follows from a screenshot.

**Better observation:** “The screenshot shows an in-field prompt. Whether a persistent label or accessible name exists is unverified; inspect the DOM and the populated state. Submit behavior and keyboard focus were not tested.” The visible fact and verification question stay separate from a confirmed defect.
