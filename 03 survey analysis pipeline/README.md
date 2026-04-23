# Survey Data Cleaning & Analysis Pipeline

A structured workflow for taking raw survey exports and producing analysis-ready datasets. Focused on the cleaning and validation steps that usually happen informally and invisibly, making them explicit and auditable.

## Why survey data is harder than it looks

Raw survey exports typically contain:
- Responses in the wrong format (free text where a number was expected)
- Inconsistent option labels (legacy surveys with changed wording mid-run)
- Partial completions that should be treated differently from refusals
- Metadata columns mixed with response data
- Timestamps, IDs, or platform artefacts that need stripping before analysis

This pipeline handles each of these systematically before any analysis begins.

## What the pipeline does

### Stage 1: Structural audit
- Identifies column types and flags mismatches
- Separates metadata from response columns
- Reports completion rate per respondent and per question

### Stage 2: Response cleaning
- Standardises option labels against a defined codebook
- Flags open-text responses that are too short to be meaningful (< 3 words)
- Handles partial completions with explicit classification (not silent exclusion)

### Stage 3: Consistency checks
- For questions with logical dependencies (e.g. Q4 only applies if Q3 = "Yes"), checks that skip logic was followed
- Flags internally inconsistent response sets (e.g. "I have never used this product" + detailed product rating)

### Stage 4: Summary tables
- Frequency tables per question
- Cross-tabulations for selected variable pairs
- Structured notes on data quality issues for the analyst's record

## Files

```
03_survey_analysis_pipeline/
├── pipeline.py
├── codebook.yaml           # Expected response options per question
├── sample_data/
│   └── raw_survey_export.csv
├── outputs/
│   ├── clean_responses.csv
│   ├── audit_report.txt
│   └── summary_tables/
│       ├── q1_frequency.csv
│       └── q3_q4_crosstab.csv
└── README.md
```

## Skills demonstrated

- Systematic handling of messy, real-world data
- Codebook-driven cleaning (decisions are explicit, not ad hoc)
- Thinking through edge cases before they cause silent errors downstream
- Producing outputs structured for human review, not just further processing
