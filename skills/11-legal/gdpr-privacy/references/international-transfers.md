# 8. International Transfers

The GDPR restricts transfers of personal data to third countries (non-EEA) unless specific safeguards are in place. This became significantly more complex after the CJEU Schrems II ruling (July 2020), which invalidated the Privacy Shield and raised the bar for transfer assessments.

For a comprehensive international transfer compliance guide covering adequacy decisions, SCC module selection, Transfer Impact Assessments, BCRs, UK-specific requirements, and the Data Privacy Framework, see `references/international-transfer-guide.md`.

### 8.1 Transfer Identification

A transfer occurs when personal data is sent from the EEA to a third country or international organization (Art. 44). **Remote access from a third country constitutes a transfer** -- if an engineer in India accesses an EU-hosted database, that is a transfer. This makes transfers pervasive for any organization with global operations or remote workforce.

### 8.2 Transfer Safeguards Hierarchy

In order of preference:

1. **Adequacy decision** (Art. 45): The European Commission has determined the country provides an adequate level of protection. Current list includes: Andorra, Argentina, Canada (commercial), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, UK, Uruguay. **Note:** The US is NOT on the general adequacy list but has the Data Privacy Framework (see below).

2. **Appropriate safeguards** (Art. 46):
   - Standard Contractual Clauses (SCCs) -- 2021 version, the most common mechanism
   - Binding Corporate Rules (BCRs) -- for intra-group transfers
   - Approved codes of conduct (Art. 40) with binding commitments
   - Approved certification mechanisms (Art. 42) with binding commitments
   - Ad hoc contractual clauses authorized by DPA

3. **Data Privacy Framework (DPF):** For transfers to the US, organizations that self-certify under the EU-US DPF, UK Extension, or Swiss-US DPF provide adequate protection. Check the DPF list before relying on this.

4. **Derogations** (Art. 49): Narrow, exceptional situations -- consent (explicit), contract necessity, public interest, legal claims, vital interests, public register. These are NOT suitable for routine, repetitive transfers.

### 8.3 Standard Contractual Clauses (SCCs 2021)

The 2021 SCCs are modular. Choose the correct module(s):
- **Module 1:** Controller to Controller
- **Module 2:** Controller to Processor (most common for SaaS)
- **Module 3:** Processor to Sub-Processor
- **Module 4:** Processor to Controller

**Key obligations:**
- Complete Annex I (parties, description of transfer), Annex II (security measures), Annex III (sub-processors)
- Include the docking clause to allow additional parties to accede
- Conduct a Transfer Impact Assessment (TIA) before executing
- Implement supplementary measures if TIA identifies gaps

### 8.4 Transfer Impact Assessment (TIA)

Per EDPB Recommendations 01/2020, before transferring data under SCCs, you must assess:

1. The laws and practices of the destination country regarding government access to data
2. Whether those laws impinge on the effectiveness of the SCCs
3. Whether supplementary measures can address any gaps

**Specific risk factors for US transfers:**
- FISA Section 702 (surveillance of non-US persons)
- Executive Order 12333 (foreign intelligence gathering)
- Cloud Act (US law enforcement access to data held by US companies)
- Assess whether your data is of the type that might be subject to these authorities

**If gaps exist:** Implement supplementary measures -- encryption with keys held outside the destination country, pseudonymization with no re-identification capability in the destination country, or (if gaps cannot be closed) suspend transfers.

---
