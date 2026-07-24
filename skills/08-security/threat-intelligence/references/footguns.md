# Footguns

- **Feeding raw OSINT directly into SIEM without curation** floods analysts with false positives. Twitter-scraped IPs have ~60% false positive rate — every uncurated IOC degrades detection fidelity.
- **Mapping every alert to an APT without evidence** creates attribution bias. "APT29" is not the default answer for every Russian-language phishing email. Attribution requires TTP matching, infrastructure overlap, and targeting alignment — not just language or geo-IP.
- **Setting IOC expiration to "never"** accumulates dead indicators that consume analyst time and SIEM performance. IPs churn within hours; domains within days. Expire IOCs on a decay curve based on indicator type and threat actor TTP cadence.
- **Using TAXII collections without authentication** on an internet-facing server. TAXII without mutual TLS or API key auth exposes your entire intelligence database to anyone who discovers the endpoint.
- **Publishing intelligence without classification markings** (TLP, dissemination controls). A TLP:RED report shared via unencrypted email to a distribution list that includes vendors is an intelligence compromise with regulatory and reputational consequences.
- **Trusting Pastebin/dark web scrapes without sanitization** can expose analysts to malicious content — weaponized PDFs, browser exploits, and C2 beacons embedded in "intelligence" sources. All raw collection must be analyzed in isolated environments.
