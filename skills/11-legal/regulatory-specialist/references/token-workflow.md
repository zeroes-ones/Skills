# Token-Efficient Workflow

```
# Step 1: Classification decision tree (scripted)
python3 scripts/classify_samd.py \
  --intended-use "Software that analyzes retinal images to detect diabetic retinopathy" \
  --clinician-review false --output json
# Returns: {"is_samd": true, "fda_class": "Class II", "pathway": "510(k)", "confidence": "high"}

# Step 2: Decision tree → action per classification
# Class I → Document determination. Ship with general controls.
# Class II → Identify predicate devices. Prepare 510(k). Build QMS.
# Class III → PMA pathway. This is a multi-year commitment. Plan accordingly.

# Step 3: Checklist execution with exit codes
# Verify design controls are in place
python3 scripts/check_design_controls.py --repo . --output json
# Returns: {"design_inputs": true, "design_outputs": true, "traceability": false,
#           "dhf_complete": false, "missing": ["traceability_matrix", "design_review_003"]}
# Exit code 0 = all controls present, 1 = gaps

# Step 4: QMS document status
python3 scripts/qms_status.py --qms-dir docs/qms --output json
# Returns: {"documents": 45, "overdue_review": 3, "next_audit_days": 120}
```

**Principle:** `classify_samd.py` outputs JSON with classification + pathway. Agent follows decision tree to exactly one next action. Document checks verify completeness via exit codes. Never reads regulation text into agent context.
