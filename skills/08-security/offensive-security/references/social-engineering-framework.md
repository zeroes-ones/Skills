# Social Engineering Framework

## Overview

Social engineering exploits human psychology rather than technical vulnerabilities. It is consistently the most effective attack vector -- 74% of breaches involve a human element (Verizon DBIR 2024). This framework covers pretext design, phishing campaign execution, physical social engineering methodology, and awareness training measurement.

## Pretext Design Matrix

A successful pretext answers three questions: (1) Who am I? (2) Why am I contacting you? (3) Why do I need what I am asking for? The pretext must be internally consistent, reference verifiable details about the organization, and create appropriate urgency without triggering suspicion.

### Authority-Based Pretexts
- **IT/Help Desk:** "Password policy update," "Email migration," "VPN certificate renewal." Leverages compliance with authority.
- **Executive:** "CFO needs this processed urgently," "CEO requested this report." Leverages deference to hierarchy.
- **External Authority:** "IRS audit notification," "Law enforcement inquiry," "Regulatory compliance check." Leverages fear of consequences.
- **Success factors:** Correct internal terminology, knowledge of current projects, real employee names as references.

### Urgency-Based Pretexts
- **Time pressure:** "Must be completed by 5 PM or access is revoked," "Invoice payment overdue -- late fees apply."
- **Scarcity:** "Limited slots for this security training -- register now," "Only 10 accounts will be migrated today."
- **Fear:** "Your account was compromised -- verify credentials immediately," "Unusual login from foreign country."
- **Warning:** Urgency that is too extreme triggers skepticism. "Your account will be deleted in 10 minutes" is less believable than "Password expires Friday."

## Phishing Campaign Design

### Email Crafting
- **From address:** Spoofed display name (real employee name), domain typo-squatting (compamy.com vs company.com), lookalike domains (rnicrosoft.com), legitimate compromised third-party. SPF/DKIM/DMARC bypass assessment is part of the test.
- **Subject lines:** Test multiple approaches: urgency ("Password Expiration Notice"), curiosity ("Q3 Budget Draft -- Please Review"), utility ("Updated VPN Client Download"), social proof ("Re: Meeting Follow-up").
- **Body:** Professional formatting matching company templates. Real employee signatures. Internal jargon. Current projects or events as context.
- **Attachments:** HTML attachment (credential capture form), macro-enabled Office documents (test macro security), PDF with embedded link, ISO/IMG files (bypass Mark-of-the-Web).

### Landing Page Design
- Clone actual company login portal (Microsoft 365, Okta, VPN portal, custom SSO).
- Capture email and password fields. NEVER store plaintext credentials -- hash or count entries.
- After credential entry: redirect to legitimate page or display "training moment" page explaining the test.
