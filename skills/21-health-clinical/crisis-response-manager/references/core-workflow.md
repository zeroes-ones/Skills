# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~25 min): Adverse Event Detection and Regulatory Reporting
1. Detect potential AEs from all patient-facing channels: community posts, app feedback, support tickets, social media, clinical study data. Implement keyword/phrase detection (drug names + adverse event terminology from MedDRA) with human triage for flagged content.
2. Triage the event: is it a valid AE? Four elements required: (1) identifiable patient, (2) identifiable reporter, (3) a suspect product (drug, device, biologic), (4) an adverse event or fatal outcome. If all four present, it is reportable.
3. Determine seriousness: results in death, life-threatening, requires hospitalization or prolongs existing hospitalization, results in persistent or significant disability/incapacity, is a congenital anomaly/birth defect, or requires intervention to prevent permanent impairment/damage. Serious + unexpected = expedited reporting (15 days, or 7 days for death/life-threatening).
4. Report to the appropriate authority: FDA MedWatch (Form 3500 for voluntary, 3500A for mandatory), EudraVigilance (EU), manufacturer pharmacovigilance system (if involving their product). Use the correct form and timeline for the jurisdiction.
5. Document internally: create an incident record with timeline, reporter details, patient details, product details, event description, seriousness assessment, expectedness assessment, reporting timeline, and confirmation of submission. Retain per regulatory recordkeeping requirements (typically 10 years for FDA).

### Phase 1 Implementation: AE Reporting Code (~30 min)

#### FDA MedWatch eMDR XML Generation (Form 3500A)

```python
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def generate_medwatch_3500a_xml(ae_report: dict) -> str:
    """Generate FDA MedWatch eMDR Form 3500A XML for electronic submission."""
    root = ET.Element("ichicsr", attrib={
        "xmlns": "urn:hl7-org:v3",
        "messagetype": "ichicsr"
    })

    # Safety report header
    header = ET.SubElement(root, "safetyreportheader")
    ET.SubElement(header, "messagenumber").text = ae_report.get("message_id", "")
    ET.SubElement(header, "messagedate").text = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    ET.SubElement(header, "reporttype").text = "1"  # Spontaneous report

    # Patient demographics (de-identified per HIPAA)
    patient = ET.SubElement(root, "patient")
    ET.SubElement(patient, "patientonsetage").text = str(ae_report.get("age", ""))
    ET.SubElement(patient, "patientonsetageunit").text = "801"  # Year
    ET.SubElement(patient, "patientsex").text = str(ae_report.get("sex", "0"))

    # Drug/reaction block
    for drug in ae_report.get("suspect_products", []):
        drug_el = ET.SubElement(root, "patientdrug")
        ET.SubElement(drug_el, "drugcharacterization").text = "1"  # Suspect
        ET.SubElement(drug_el, "medicinalproduct").text = drug.get("name", "")

    for reaction in ae_report.get("reactions", []):
        reaction_el = ET.SubElement(root, "patientreaction")
        ET.SubElement(reaction_el, "reactionmeddrapt").text = reaction.get("meddra_pt", "")

    # Seriousness criteria
    seriousness = ET.SubElement(root, "seriousness")
    for criteria in ae_report.get("seriousness_criteria", []):
        ET.SubElement(seriousness, criteria).text = "1"

    # Reporter info
    reporter = ET.SubElement(root, "reporter")
    ET.SubElement(reporter, "reportertype").text = "1"  # Physician
    ET.SubElement(reporter, "reportergivename").text = ae_report.get("reporter_name", "")

    return ET.tostring(root, encoding="unicode", xml_declaration=True)
```

#### MedDRA Coding: SOC → PT → LLT Hierarchy

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MedDRATerm:
    """MedDRA coding with SOC (System Organ Class), PT (Preferred Term),
    LLT (Lowest Level Term) hierarchy."""
    llt_code: str       # Lowest Level Term code (e.g., "10003922")
    llt_name: str       # LLT name ("Head pain")
    pt_code: str        # Preferred Term code ("10019211")
    pt_name: str        # PT name ("Headache")
    soc_code: str       # System Organ Class code ("10029205")
    soc_name: str       # SOC name ("Nervous system disorders")

def classify_ae_with_meddra(verbatim_term: str, meddra_db: dict) -> Optional[MedDRATerm]:
    """Map a verbatim patient-reported term to the MedDRA hierarchy (LLT → PT → SOC)."""
    # Lookup LLT by exact or normalized match
    llt = meddra_db.get("llt_index", {}).get(verbatim_term.lower())
    if not llt:
        # Fallback: try MedDRA LLT-normalized matching
        llt = meddra_db.get("llt_normalized", {}).get(
            verbatim_term.lower().replace(" ", "_")
        )

    if not llt:
        return None  # Requires manual coding by safety professional

    return MedDRATerm(
        llt_code=llt["llt_code"],
        llt_name=llt["llt_name"],
        pt_code=llt["pt_code"],
        pt_name=llt["pt_name"],
        soc_code=llt["soc_code"],
        soc_name=llt["soc_name"],
    )
```

#### Causality Assessment: Naranjo Scale + WHO-UMC Criteria

```python
from enum import Enum

class CausalityCategory(Enum):
    CERTAIN = "Certain"
    PROBABLE = "Probable"
    POSSIBLE = "Possible"
    UNLIKELY = "Unlikely"

# Naranjo Adverse Drug Reaction Probability Scale (10 questions, scored -1/0/+1)
NARANJO_QUESTIONS = [
    "Are there previous conclusive reports on this reaction?",
    "Did the adverse event appear after the suspected drug was administered?",
    "Did the adverse reaction improve when the drug was discontinued?",
    "Did the adverse reaction reappear when the drug was re-administered?",
    "Are there alternative causes that could have caused the reaction?",
    "Did the reaction reappear when a placebo was given?",
    "Was the drug detected in blood/fluids in concentrations known to be toxic?",
    "Was the reaction more severe when the dose was increased or less severe when decreased?",
    "Did the patient have a similar reaction to the same or similar drugs previously?",
    "Was the adverse event confirmed by any objective evidence?"
]

def naranjo_score(answers: list[int]) -> tuple[int, CausalityCategory]:
    """
    Calculate Naranjo ADR probability score.
    answers: list of 10 integers (0=No, 1=Do not know/NA, 2=Yes).
    Question 5 (alternative causes) is reverse-scored: 0=Yes, 2=No.
    Returns (total_score, category).
    """
    if len(answers) != 10:
        raise ValueError("Exactly 10 Naranjo answers required")

    total = sum(answers)
    if total >= 9:
        return total, CausalityCategory.CERTAIN
    elif total >= 5:
        return total, CausalityCategory.PROBABLE
    elif total >= 1:
        return total, CausalityCategory.POSSIBLE
    else:
        return total, CausalityCategory.UNLIKELY

# WHO-UMC Causality Categories (structured clinical assessment)
def who_umc_assess(
    temporal_plausible: bool,
    dechallenge_positive: bool,
    rechallenge_positive: bool,
    alternative_causes_excluded: bool,
    previous_known: bool,
) -> CausalityCategory:
    """WHO-UMC causality assessment with structured clinical reasoning."""
    if all([temporal_plausible, dechallenge_positive, rechallenge_positive,
            alternative_causes_excluded, previous_known]):
        return CausalityCategory.CERTAIN
    elif temporal_plausible and dechallenge_positive and alternative_causes_excluded:
        return CausalityCategory.PROBABLE
    elif temporal_plausible and not dechallenge_positive and not alternative_causes_excluded:
        return CausalityCategory.POSSIBLE
    else:
        return CausalityCategory.UNLIKELY
```

#### EudraVigilance ICSR XML Format

```python
def generate_eudravigilance_icsr_xml(ae_report: dict, qppv_name: str) -> str:
    """Generate EudraVigilance ICSR XML per ICH E2B(R3) for EU reporting."""
    root = ET.Element("ichicsr", attrib={
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "messagetype": "ichicsr",
        "messagemode": "1"  # 1 = new, 2 = follow-up
    })

    # EU-specific: QPPV sign-off metadata
    qppv = ET.SubElement(root, "qppv")
    ET.SubElement(qppv, "qppvname").text = qppv_name
    ET.SubElement(qppv, "reportnullification").text = "0"

    # Primary source qualification (EU requires HCP or consumer designation)
    source = ET.SubElement(root, "primarysource")
    ET.SubElement(source, "reportercountry").text = ae_report.get("country", "US")
    ET.SubElement(source, "qualification").text = ae_report.get("reporter_qualification", "1")

    # Reaction with MedDRA coding (E2B R3 format)
    for reaction in ae_report.get("reactions", []):
        reaction_el = ET.SubElement(root, "reaction")
        ET.SubElement(reaction_el, "primarysourcereaction").text = reaction.get("verbatim", "")
        ET.SubElement(reaction_el, "reactionmeddrapt").text = reaction.get("meddra_pt", "")
        ET.SubElement(reaction_el, "reactionmeddraversion").text = ae_report.get(
            "meddra_version", "27.1"
        )

    # Seriousness — EU GVP Module VI criteria
    seriousness = ET.SubElement(root, "seriousness")
    criteria_map = {
        "death": "1", "life_threatening": "2", "hospitalization": "3",
        "disability": "4", "congenital_anomaly": "5",
        "other_medically_important": "6"
    }
    for criteria, code in criteria_map.items():
        if ae_report.get(criteria):
            ET.SubElement(seriousness, criteria).text = code

    return ET.tostring(root, encoding="unicode", xml_declaration=True)
```

#### Automated Timeline Detection for 7-Day / 15-Day / 30-Day Rules

```python
from datetime import datetime, timedelta
from enum import Enum

class ReportingDeadline(Enum):
    SEVEN_DAY = 7       # Death or life-threatening
    FIFTEEN_DAY = 15    # Serious, unexpected, non-life-threatening
    THIRTY_DAY = 30     # Medical device death/serious injury

def determine_reporting_deadline(ae_report: dict) -> tuple[ReportingDeadline, datetime]:
    """
    Determine regulatory reporting deadline and calculate due date.
    Clock starts at first employee awareness — not when investigation concludes.
    """
    awareness_date = ae_report.get("awareness_date", datetime.utcnow())
    is_serious = ae_report.get("is_serious", False)
    is_unexpected = ae_report.get("is_unexpected", True)
    outcome = ae_report.get("outcome", "").lower()
    is_device = ae_report.get("is_device", False)

    if is_device and ("death" in outcome or "serious injury" in outcome):
        deadline = ReportingDeadline.THIRTY_DAY
    elif is_serious and is_unexpected and ("death" in outcome or "life-threatening" in outcome):
        deadline = ReportingDeadline.SEVEN_DAY
    elif is_serious and is_unexpected:
        deadline = ReportingDeadline.FIFTEEN_DAY
    else:
        return None, None  # Not expedited — standard reporting timeline

    due_date = awareness_date + timedelta(days=deadline.value)
    return deadline, due_date

def check_ae_timeline_compliance(submissions: list[dict]) -> list[dict]:
    """Audit AE reports for regulatory timeline compliance. Flag violations."""
    violations = []
    for sub in submissions:
        deadline, due_date = determine_reporting_deadline(sub)
        if deadline and sub.get("submission_date") > due_date:
            violations.append({
                "message_id": sub.get("message_id"),
                "deadline_type": deadline.name,
                "days_late": (sub["submission_date"] - due_date).days,
                "regulatory_risk": "FDA 483 / Warning Letter exposure"
            })
    return violations
```

### Phase 2 (~20 min): Public Health Emergency Response
1. Detect the emergency signal: disease outbreak in patient community, product recall notification from manufacturer or FDA, safety alert from CDC/WHO/health authority, or data suggesting a cluster of serious AEs.
2. Activate the crisis team: Crisis Response Manager (lead), Health Compliance, Legal Advisor, Clinical Lead, CEO/designee (for S1-S2), Community Operations Manager (if patient-facing comms), Communications/PR (if media potential).
3. Verify the facts: confirm the source (manufacturer, regulator, clinical data), assess the scope (which patients, products, geographies are affected), determine the urgency (ongoing exposure vs retrospective concern).
4. Issue patient notification: what happened, what products/geographies are affected, what patients should do (stop use, contact HCP, seek medical attention), where to get more information (hotline, website), and what the company is doing about it. Legal/Regulatory review required before release.
5. Monitor and update: track patient inquiries, media coverage, social media sentiment. Issue updates as new information becomes available. Do not go silent — even "we are still investigating" updates maintain trust.

### Phase 3 (~20 min): Crisis Communication Templates
1. **Patient Notification Template:** (a) What happened — clear, factual, no speculation. (b) Who is affected — specific products, lot numbers, date ranges. (c) What patients should do — actionable instructions. (d) What we are doing — investigation status, corrective actions. (e) Contact information — hotline, website, HCP resources. Health literacy checked: ≤8th grade reading level.
2. **Regulatory Disclosure Template:** (a) Event description with date/time of first awareness. (b) Product identification (name, lot, NDC/UDI). (c) Patient impact summary (number affected, outcomes). (d) Root cause analysis status. (e) Corrective and preventive actions (CAPA). (f) Regulatory timeline compliance confirmation. Submit through formal regulatory channels, not email.
3. **Internal Communications Template:** (a) Situation summary (one paragraph). (b) What we know and what we do not know. (c) Current response status. (d) What employees should do if contacted by patients, media, or regulators (refer to designated spokesperson). (e) Next update expected.
4. All communications must: be approved by Legal and Regulatory, be consistent across channels, include a date/time stamp, and be archived for regulatory recordkeeping.

### Phase 4 (~25 min): Pharmacovigilance Signal Detection
1. Define the data sources: patient community posts, social media listening, app feedback, support tickets, clinical study data, published literature, regulatory databases (FAERS, EudraVigilance).
2. Implement automated detection: NLP-based keyword/phrase matching (drug names, product names + MedDRA Preferred Terms), sentiment analysis for negative health outcomes, anomaly detection for AE reporting rate spikes. Human triage validates all flagged content.
3. Triage detected signals: is this a new signal (not in the product label/Investigator Brochure), a change in frequency or severity of a known signal, or a known reaction at expected frequency? New signals require expedited assessment.
4. Validate the signal: clinical review by safety physician, causality assessment (Naranjo scale, WHO-UMC criteria), expectedness check against reference safety information, literature and database search for corroborating evidence.
5. Act on validated signals: update product labeling, issue Dear Healthcare Professional letter, update risk management plan (RMP/REMS), report to regulators, and communicate to patients and HCPs as appropriate.
