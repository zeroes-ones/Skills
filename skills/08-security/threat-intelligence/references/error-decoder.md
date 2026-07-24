# Error Decoder

| Error Message | What It Really Means | Fix |
|---|---|---|
| MISP: "Event failed validation" | STIX export contains fields that don't conform to the MISP-STIX mapping | Check for custom STIX properties, simplify to core STIX 2.1 SDOs, validate with `stix2-validator` |
| OpenCTI: "Connector stuck in 'waiting' state" | The connector can't reach the external source or authentication failed | Check connector logs, verify API key hasn't expired, test network connectivity to the external platform |
| `stix2-validator`: "Missing required property 'spec_version'" | STIX bundle missing the spec_version field (must be "2.1") | Add `"spec_version": "2.1"` to every STIX object in the bundle |
| TAXII server: "401 Unauthorized on collection" | TAXII client doesn't have read access to the requested collection | Verify TAXII client certificate, check collection ACLs on the server side |
| MISP: "Warning: no correlations found" | Your event has IOCs but MISP couldn't correlate them with existing data | This is expected for new, unique IOCs; verify that attribute types are correctly set (ip-dst, domain, md5, etc.) |
