# DeutschIQ monetisation launch checklist

## Keep disabled now

- [x] Free beta access enabled
- [x] Payments disabled
- [x] Future Pro preview visible at 700 Stars for 30 days
- [x] Interest and restore attempts measurable

## Evidence

- [ ] 10 completed diagnostics
- [ ] 5 completed lessons
- [ ] 3 returning learners
- [ ] 2 genuine Pro-interest signals
- [ ] No serious production errors in the review window
- [ ] Feedback themes reviewed and blocking confusion fixed

## Commercial and legal

- [ ] Seller identity and support contact finalized
- [ ] Privacy, Terms and Impressum reviewed for the paid offer
- [ ] Telegram Stars product wording and refund process finalized
- [ ] Purchase, entitlement, restore and refund reconciliation tested end to end
- [ ] Production database backup and restore procedure verified
- [ ] Always-on hosting decision made for paid customers

## Activation rule

Do not switch `PAYMENTS_ENABLED` to `true` merely because the application builds. Activate only after the evidence and commercial/legal sections are complete, then run the full CI, mobile E2E, production smoke and error-log checks again.
