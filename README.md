# AWS Cost Audit & Cost Optimization Analysis

**Author:** Ozoude Emmanuel Izuchukwu
**Date:** 9/9/2026
**Project Type:** AWS Cost Audit / FinOps / Cloud Cost Optimization
**Audit Period:** June 2026 – August 2026

---

## Project Overview

This project is a practical **AWS Cost Audit and Cost Optimization Analysis** performed against a personal AWS account over a three-month period.

The purpose of the audit was not simply to determine how much money was spent on AWS, but to investigate:

* What services generated the cost
* Which services were the largest cost drivers
* Which AWS region generated the most spending
* What specific usage types generated the charges
* What operations were responsible for the usage
* Which resources were potentially wasteful
* Whether resources were appropriately sized
* What infrastructure could potentially be removed or optimized
* What recommendations could reduce unnecessary future spending

The audit combines **AWS Cost Explorer, AWS resource investigation, Python, Boto3, Pandas, data validation, cost analysis, and audit reporting**.

The project was performed on a personal AWS learning environment, which made it possible to identify how temporary infrastructure created for learning and experimentation can continue generating costs when it is not properly cleaned up.

---

# Author Information

**Name:** Ozoude Emmanuel Izuchukwu
**Date:** 9/9/2026

---

# Audit Objectives

The primary objectives of this audit were to:

1. Analyze three months of AWS spending.
2. Identify the largest AWS cost drivers.
3. Analyze monthly spending trends.
4. Identify unusual cost increases.
5. Analyze spending by AWS service.
6. Analyze spending by AWS region.
7. Investigate Usage Types associated with major costs.
8. Investigate Operations associated with major costs.
9. Investigate EC2 infrastructure and utilization.
10. Identify idle EC2 instances.
11. Identify unattached EBS volumes.
12. Identify potentially oversized EC2 instances.
13. Investigate VPC networking costs.
14. Investigate Transit Gateway usage.
15. Investigate AWS Certificate Manager costs.
16. Identify potential cloud waste.
17. Produce evidence-based recommendations.
18. Build a reusable Python ETL pipeline for AWS cost data.
19. Develop an audit methodology that can later be applied to client AWS environments.

---

# Audit Scope

The audit focused primarily on the following AWS services and infrastructure:

* Amazon EC2
* EC2-Other
* Amazon EBS
* Amazon VPC
* AWS Transit Gateway
* AWS Certificate Manager
* TLS/SSL certificates
* AWS regions
* EC2 instance types
* EC2 operating platform
* Networking infrastructure
* Resource utilization
* AWS Cost Explorer billing data

Other AWS services appearing in the Cost Explorer dataset were also reviewed as part of the overall account analysis.

---

# Audit Period

The audit covered three complete months:

| Month       | Period                  |
| ----------- | ----------------------- |
| June 2026   | 2026-06-01 – 2026-06-30 |
| July 2026   | 2026-07-01 – 2026-07-31 |
| August 2026 | 2026-08-01 – 2026-08-31 |

The Cost Explorer API query used:

```text
Start:       2026-06-01
End:         2026-09-01
Granularity: MONTHLY
Metric:      UnblendedCost
Group By:    SERVICE
```

The September 1 end date is exclusive, allowing the complete month of August to be included.

---

# AWS Environment

The audited AWS account was primarily used as a personal cloud engineering learning environment.

The environment included infrastructure created for:

* AWS learning
* EC2 practice
* Networking practice
* Terraform projects
* Cloud engineering experiments
* Infrastructure testing
* Portfolio development

Because many resources were temporary learning resources, the audit specifically examined whether infrastructure created for previous exercises was still generating charges after the associated learning activity had finished.

This provided a realistic demonstration of a common cloud cost-management problem:

> Temporary resources can become recurring costs when they are not properly managed or removed.

---

# Tools & Technologies

## AWS Services

* AWS Cost Explorer
* AWS Cost Explorer API
* Amazon EC2
* Amazon EBS
* Amazon VPC
* AWS Transit Gateway
* AWS Certificate Manager
* AWS CloudWatch
* AWS IAM
* AWS Billing and Cost Management

## Programming & Data Analysis

* Python
* Boto3
* Pandas
* Matplotlib
* JSON
* CSV
* Python Logging

## Development Tools

* Visual Studio Code
* Python Virtual Environment
* Git
* GitHub

---

# Audit Methodology

The audit followed a structured investigation process:

```text
Cost Collection
      ↓
Data Preparation
      ↓
Cost Analysis
      ↓
Cost Driver Identification
      ↓
Usage Type Investigation
      ↓
Operation Investigation
      ↓
Resource Investigation
      ↓
Waste Detection
      ↓
Evidence Collection
      ↓
Audit Findings
      ↓
Recommendations
```

The key principle used throughout the audit was:

> **A high cost does not automatically mean waste.**

A service must be investigated to determine why the cost exists and whether the underlying resource or usage is actually necessary.

---

# Cost Investigation Hierarchy

The audit used the following investigation model:

```text
Service
   ↓
Usage Type
   ↓
Operation
   ↓
Region
   ↓
Resource / Configuration
   ↓
Utilization
   ↓
Root Cause
   ↓
Potential Waste
```

For example:

```text
EC2-Other
   ↓
EBS
   ↓
EBS-related operation/usage
   ↓
Ireland
   ↓
Unattached EBS volume
   ↓
No workload using the volume
   ↓
Potential waste
```

This approach prevents the audit from making assumptions based only on high-level billing categories.

---

# Phase 1 — Data Collection & Preparation

The first stage was focused on collecting and preparing AWS Cost Explorer data.

The AWS Cost Explorer API was accessed programmatically using Boto3.

The raw response was saved to:

```text
data/raw/
```

The original raw JSON was preserved as the source-of-truth for the analysis.

The processed dataset was stored separately in:

```text
data/processed/
```

This separation ensures that the original AWS billing evidence is not modified during transformation.

---

# Raw Data

The raw AWS Cost Explorer response was stored as JSON.

Example:

```text
data/
└── raw/
    └── cost_explorer_....json
```

The raw response contains the original AWS Cost Explorer results, including:

* Time periods
* Services
* Costs
* Currency
* Estimated status
* Grouped billing information

---

# Processed Data

The raw JSON was transformed into a structured dataset containing fields such as:

```text
start_date
end_date
service
cost
currency
estimated
```

The processed data was exported as CSV.

Example:

```text
data/
└── processed/
    └── clean_cost_data_....csv
```

---

# Data Validation

Before analysis, the data was validated for:

* Missing values
* Duplicate records
* Invalid dates
* Invalid costs
* Negative costs
* Missing service names
* Invalid currency
* Invalid estimated values
* Invalid time periods

Critical financial-data problems were treated as validation errors rather than silently replacing the values.

This is important because incorrectly replacing missing cost information with zero could produce misleading audit conclusions.

---

# Phase 2 — Cost Analysis

Phase 2 focused on understanding what was happening in the AWS account before attempting to classify resources as waste.

The analysis included:

* Monthly spending
* Service-level spending
* Percentage share by service
* Top cost drivers
* Monthly service trends
* Month-over-month changes
* New charges
* Cost spikes
* Regional spending
* Investigation candidates

---

# Three-Month Cost Overview

The account generated approximately:

| Month       |  AWS Spend |
| ----------- | ---------: |
| June 2026   |      $4.44 |
| July 2026   |      $9.38 |
| August 2026 |     $13.84 |
| **Total**   | **$27.66** |

This showed a clear upward trend in monthly AWS spending.

The account moved from approximately **$4.44 in June** to approximately **$13.84 in August**.

Therefore, simply looking at the three-month total would not have been enough.

The monthly trend helped identify when significant changes occurred.

---

# Tax Treatment

The total bill included approximately:

```text
Total AWS charges:  $27.66
Tax:                $1.92
Pre-tax spend:      $25.74
```

Tax was excluded from the optimization analysis because tax is not an AWS infrastructure resource that can be rightsized, stopped, or deleted.

Therefore, optimization analysis focused on approximately:

> **$25.74 of pre-tax AWS service spending**

---

# Top Cost Drivers

The largest cost categories identified were:

| Service                 |  Cost |  Share |
| ----------------------- | ----: | -----: |
| EC2 - Other             | $8.64 | 31.24% |
| AWS Certificate Manager | $7.00 | 25.31% |
| Amazon VPC              | $4.84 | 17.50% |
| Amazon EC2 - Compute    | $4.82 | 17.43% |
| Tax                     | $1.92 |  6.94% |

The top four non-tax services represented approximately:

> **91.48% of the total AWS bill**

This concentration allowed the audit to focus investigation efforts on the areas with the greatest financial impact.

---

# EC2-Other Investigation

## Cost

```text
EC2-Other:
$8.64
```

EC2-Other was the largest cost category in the account.

However, EC2-Other is a broad billing category and does not represent a single resource.

Therefore, the audit investigated the underlying billing dimensions.

### Usage Type

The largest Usage Type identified under EC2-Other was:

> **EBS**

This was significant because it connected the high-level EC2-Other cost to storage-related infrastructure.

### Investigation

The EBS-related cost was investigated against the actual EC2/EBS environment.

The investigation identified:

* Unattached EBS volumes
* Storage associated with previous learning activities
* EBS resources that were no longer actively associated with workloads

### Audit Conclusion

The EC2-Other category should not be treated as a single waste item.

The investigation demonstrated the importance of breaking down:

```text
EC2-Other
     ↓
Usage Type
     ↓
EBS
     ↓
EBS Resources
     ↓
Attachment Status
     ↓
Potential Waste
```

---

# AWS Certificate Manager Investigation

## Cost

```text
AWS Certificate Manager:
$7.00
```

ACM represented approximately:

```text
25.31% of total spending
```

The charge appeared as a new significant cost in August.

Monthly pattern:

| Month  | ACM Cost |
| ------ | -------: |
| June   |    $0.00 |
| July   |    $0.00 |
| August |    $7.00 |

### Usage Type

The identified usage type was:

> **Exportable public SSL/TLS certificates**

### Operation

The associated operation was:

> **Request Certificate**

This provided a much more specific explanation of the charge than simply saying:

> "ACM cost $7."

The audit was able to trace the cost to the certificate usage type and certificate-request operation.

### Audit Investigation

The certificate usage was reviewed to determine:

* Whether the certificate was still required
* Whether it belonged to a temporary project
* Whether it was associated with an active workload
* Whether it was unnecessarily created for learning purposes
* Whether unused certificates existed

### Recommendation

Review all exportable public SSL/TLS certificates and remove certificates that are no longer required.

Before deletion, confirm that the certificate is not required by an active workload.

---

# Amazon VPC Investigation

## Cost

```text
Amazon VPC:
$4.84
```

Monthly spending:

| Month  |  Cost |
| ------ | ----: |
| June   | $0.77 |
| July   | $3.65 |
| August | $0.42 |

The major increase occurred in July.

The increase from June to July was:

```text
$3.65 - $0.77 = $2.88
```

This represented a significant networking-cost spike.

---

# VPC Usage Type Investigation

The investigation identified:

> **Transit Gateway**

as the relevant VPC usage type.

The associated operation was also:

> **Transit Gateway**

This connected the VPC-level cost to Transit Gateway infrastructure rather than treating the entire VPC category as a generic networking charge.

---

# Transit Gateway Finding

Transit Gateway infrastructure was present in the learning environment.

For a small personal learning environment, Transit Gateway may provide more networking infrastructure than is actually required.

The audit therefore investigated whether the Transit Gateway was providing meaningful architectural value.

### Investigation Areas

* Transit Gateway existence
* VPC attachments
* Routing configuration
* Network connectivity requirements
* Data processing
* Purpose of the Transit Gateway
* Whether it was created for learning
* Whether it was still required

### Recommendation

If the Transit Gateway was created solely for learning and is no longer required:

1. Confirm that no active workloads depend on it.
2. Review Transit Gateway attachments.
3. Remove unnecessary attachments.
4. Remove unnecessary routing configuration.
5. Delete the Transit Gateway when it is confirmed to be unused.

The recommendation is therefore based on **actual usage and architectural necessity**, not simply because Transit Gateway generates cost.

---

# Amazon EC2 Compute Investigation

## Cost

Amazon EC2 Compute generated approximately:

```text
$4.82
```

representing approximately:

```text
17.43%
```

of the total bill.

Monthly spending was:

| Month  |  Cost |
| ------ | ----: |
| June   | $2.03 |
| July   | $1.11 |
| August | $1.68 |

---

# EC2 Instance Investigation

The EC2 environment was investigated at the instance level.

### Instance Type

The identified EC2 instance type was:

> **t3.micro**

### Platform

The instance platform was:

> **Linux/Unix**

The instance type and operating platform were considered when evaluating whether the compute resources were appropriately sized for the learning workload.

---

# Finding — Oversized EC2 Instance for Learning Workloads

The audit identified an EC2 instance configuration that was larger than necessary for the workload it was supporting.

Because the instance was primarily being used for learning and experimentation, the workload requirements were relatively modest.

### Recommendation

Review CloudWatch utilization before changing the instance.

Relevant metrics include:

* CPU utilization
* Memory utilization where available
* Network utilization
* Runtime
* Workload patterns

If utilization remains consistently low, consider moving to a smaller and more appropriate instance type.

The change should be validated against actual workload requirements before implementation.

---

# Finding — Idle EC2 Instances

The audit identified EC2 instances that were idle or no longer actively required.

These resources were associated primarily with learning and experimentation.

### Potential Waste

A running EC2 instance can continue generating compute charges even when it is not actively being used.

The common lifecycle observed was:

```text
Create EC2
     ↓
Use for learning
     ↓
Finish project
     ↓
Instance remains running
     ↓
Recurring cost
```

### Recommendation

For completed learning projects:

* Stop instances that may be required later.
* Terminate instances that are no longer required.
* Preserve important data before termination.
* Review associated EBS volumes.
* Review Elastic IPs and networking resources.

---

# Finding — Unattached EBS Volumes

The investigation identified unattached EBS volumes.

These volumes were particularly relevant because **EBS was the largest Usage Type under EC2-Other**.

### Potential Waste

An EBS volume may continue generating storage charges even when it is no longer attached to an active EC2 instance.

### Recommendation

For every unattached EBS volume:

```text
Identify volume
      ↓
Identify previous project
      ↓
Determine whether data is required
      ↓
Snapshot if necessary
      ↓
Delete if unnecessary
```

This should be included in the cleanup process after every learning project.

---

# Key Audit Findings Summary

| # | Finding            | Evidence / Detail                                                      | Recommendation                                |
| - | ------------------ | ---------------------------------------------------------------------- | --------------------------------------------- |
| 1 | Idle EC2 instances | EC2 resources were no longer actively required                         | Stop or terminate unused instances            |
| 2 | Unattached EBS     | EBS was the largest EC2-Other Usage Type                               | Remove unused volumes after data verification |
| 3 | EC2 rightsizing    | EC2 workload did not require excessive capacity                        | Review CloudWatch and rightsize               |
| 4 | Transit Gateway    | VPC cost associated with Transit Gateway usage                         | Remove if no longer architecturally required  |
| 5 | ACM certificates   | Exportable public SSL/TLS certificates; operation: Request Certificate | Review and remove unnecessary certificates    |
| 6 | EC2-Other          | Largest cost category at $8.64                                         | Continue usage-type-level investigation       |
| 7 | Learning resources | Temporary infrastructure remained after projects                       | Implement resource cleanup process            |

---

# Recommendations

## 1. Stop or Terminate Idle EC2 Instances

Review every running instance.

For each instance:

* Identify purpose
* Check utilization
* Confirm project status
* Stop temporary resources
* Terminate completed resources

**Priority: High**

---

## 2. Remove Unattached EBS Volumes

Because EBS was the largest Usage Type contributing to EC2-Other, EBS cleanup should be prioritized.

**Priority: High**

---

## 3. Rightsize EC2

Review actual resource utilization and select an instance size appropriate for the workload.

**Priority: Medium–High**

---

## 4. Review Transit Gateway

Determine whether Transit Gateway is necessary for the current environment.

If it was created for experimentation and is no longer required, remove it.

**Priority: High**

---

## 5. Review Exportable Public SSL/TLS Certificates

Inventory certificates and identify those that are no longer required.

The audit specifically identified:

```text
Usage Type:
Exportable public SSL/TLS certificates

Operation:
Request Certificate
```

**Priority: High**

---

## 6. Investigate EC2-Other Continuously

EC2-Other was the largest cost category.

Future investigations should always break this category down into its underlying usage types.

The current audit identified EBS as the largest Usage Type.

**Priority: High**

---

# Cost Governance Recommendations

The audit also identified opportunities to prevent similar waste in the future.

## Resource Tagging

Recommended tags:

```text
Project
Environment
Owner
Purpose
ManagedBy
CreatedDate
ExpirationDate
```

Example:

```text
Project = AWS-Learning
Environment = Development
Purpose = Terraform-Lab
Owner = Ozoude Emmanuel
ExpirationDate = 2026-09-30
```

---

# AWS Budgets

An AWS Budget should be configured to provide early warning when spending reaches predefined thresholds.

Example:

```text
Monthly Budget
      ↓
50% Alert
      ↓
80% Alert
      ↓
100% Alert
```

This would help prevent unexpected spending from accumulating unnoticed.

---

# Resource Cleanup Policy

For future learning projects, resources should have an explicit lifecycle.

```text
Create
  ↓
Learn
  ↓
Test
  ↓
Complete Project
  ↓
Review Resources
  ↓
Delete Unnecessary Resources
```

A final cleanup checklist should include:

```text
[ ] EC2 instances
[ ] EBS volumes
[ ] EBS snapshots
[ ] Elastic IPs
[ ] NAT Gateways
[ ] Transit Gateway
[ ] Load Balancers
[ ] SSL/TLS certificates
[ ] CloudWatch resources
[ ] S3 resources
[ ] Other networking resources
```

---

# Potential Savings Approach

The audit does not present savings as guaranteed.

Instead, potential savings should be calculated from the actual cost associated with resources confirmed to be unnecessary.

The methodology is:

```text
Current Cost
      -
Cost After Optimization
      =
Potential Monthly Savings
```

Annualized:

```text
Potential Monthly Savings × 12
=
Potential Annual Savings
```

This prevents the audit from overstating its financial impact.

---

# Audit Report Structure

The findings from this project can be converted into a formal client-facing audit report.

Each finding should contain:

### Finding

What was identified?

### Evidence

What AWS data or resource information supports the finding?

### Root Cause

Why is the cost occurring?

### Impact

What is the financial or operational impact?

### Recommendation

What should be changed?

### Priority

How urgent or important is the recommendation?

### Potential Savings

How much could potentially be saved?

### Risk

What risks should be considered before implementing the recommendation?

---

# Evidence Collection

Evidence was collected from multiple levels of the AWS environment.

Examples include:

* AWS Cost Explorer
* Cost Explorer service breakdown
* Usage Type analysis
* Operation analysis
* Regional analysis
* EC2 instance information
* EC2 instance type
* EC2 platform
* EBS attachment status
* VPC configuration
* Transit Gateway configuration
* ACM certificate information
* CloudWatch utilization metrics
* Raw Cost Explorer JSON
* Processed CSV
* Python analysis output

This allowed findings to be supported by actual AWS information rather than assumptions.

---

# Python ETL Pipeline

A reusable Python ETL pipeline was developed to support the cost audit.

The pipeline follows:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
   ↓
Analyze
```

---

# Extract

Boto3 was used to communicate with the AWS Cost Explorer API.

The extraction process retrieves the AWS billing data and saves the original API response as JSON.

The raw response remains unchanged so it can be used as audit evidence.

---

# Transform

The transformation stage converts the Cost Explorer response into structured records.

The process includes:

* Flattening nested JSON
* Extracting service names
* Extracting dates
* Converting cost values
* Converting dates
* Validating currency
* Validating estimated status
* Sorting records

---

# Load

The validated dataset is exported into:

```text
data/processed/
```

as a timestamped CSV file.

This creates a clean dataset that can be reused for:

* Analysis
* Visualization
* Reporting
* Future automation

---

# Main Pipeline Control

`main.py` acts as the control room for the ETL pipeline.

The workflow is:

```text
main.py
   │
   ├── extract_data()
   │
   ├── save_raw_data()
   │
   ├── transform_data()
   │
   └── load_data()
```

The individual modules remain responsible for their own tasks while `main.py` controls the complete workflow.

---

# Production-Quality Practices

The Python pipeline follows several practices that make it more suitable for real audit work:

* Reusable functions
* Clear separation of responsibilities
* Logging instead of print statements
* Exception handling
* Data validation
* Reusable configuration
* Environment-based AWS configuration
* Preservation of raw source data
* Timestamped processed files
* Clear error messages
* Modular design

AWS credentials and sensitive authentication information are not hardcoded into the Python source code.

---

# Project Structure

aws-cost-audit-finops-analysis/
│
├── .venv/
│
├── data/
│   ├── raw/
│   │   └── cost_explorer_....json
│   │
│   └── processed/
│       └── clean_cost_data_....csv
│
│
├── screenshots/
│   ├── cost_explorer_3_months.png
│   ├── cost_by_service.png
│   ├── ec2_other_usage_type.png
│   ├── virtual_private_cloud_usage_type.png
│   ├── virtual_private_cloud_api_operation.png
│   ├── certificate_manager_usage_type.png
│   ├── certificate_manager_api_operation.png
│   ├── cost_by_region.png
│   └── etl_pipeline_success.png
│
├── src/
│   ├── analysis.ipynb
│   ├── extract.py
│   ├── load.py
│   ├── main.py
│   ├── settings.py
│   └── transform.py
│
├── .gitignore
│
├── README.md
│
└── requirements.txt

---

# Audit Principles

## Understand Before Optimizing

The audit first established what was happening before investigating waste.

```text
Understand
   ↓
Investigate
   ↓
Validate
   ↓
Recommend
```

---

## Follow the Cost

Instead of stopping at:

```text
VPC = $4.84
```

the investigation went deeper:

```text
VPC
 ↓
Transit Gateway
 ↓
Transit Gateway operation
 ↓
Resource investigation
```

Similarly:

```text
EC2-Other
 ↓
EBS
 ↓
EBS resources
 ↓
Unattached volumes
```

And:

```text
ACM
 ↓
Exportable public SSL/TLS certificates
 ↓
Request Certificate
 ↓
Certificate investigation
```

This is the core of the audit methodology.

---

# Key Lessons Learned

## 1. A Cloud Bill Is Only the Starting Point

The bill tells you where money was spent.

A proper audit must determine why.

---

## 2. Usage Type Is Extremely Important

Service-level information can hide the real source of spending.

For example:

```text
EC2-Other
```

became more meaningful when investigated as:

```text
EC2-Other
     ↓
EBS
```

---

## 3. Operations Provide More Context

The operation can help identify what action or AWS activity is associated with the charge.

For example:

```text
AWS Certificate Manager
     ↓
Exportable public SSL/TLS certificates
     ↓
Request Certificate
```

This provides a significantly more useful audit trail than simply reporting:

> "ACM cost $7."

---

## 4. Networking Costs Can Be Easy to Miss

VPC-related costs can come from networking infrastructure rather than the VPC itself.

In this audit, Transit Gateway was identified as a relevant VPC cost driver.

---

## 5. Learning Environments Need Cost Controls

Cloud engineering labs are excellent for learning, but temporary infrastructure can become recurring spending.

Resources should therefore be reviewed after every project.

---

## 6. Resource Rightsizing Requires Utilization Data

Instance type alone is not enough to declare an EC2 instance oversized.

Utilization and workload requirements should be considered before making a rightsizing recommendation.

---

# Limitations

This was a personal AWS learning environment rather than a production enterprise environment.

Therefore:

* Total spending was relatively small.
* Some resources were intentionally created for learning.
* Workloads were not production workloads.
* Availability requirements were limited.
* Traffic patterns were limited.
* Savings estimates were not treated as guaranteed.
* Some cost categories require additional investigation before exact resource-level savings can be calculated.

The project should therefore be viewed as a **practical portfolio demonstration of AWS cost auditing and FinOps methodology**.

---

# Future Improvements

Future versions of this project can include:

### Automated Resource Inventory

Use Boto3 to automatically discover:

* EC2 instances
* EBS volumes
* Elastic IPs
* NAT Gateways
* Transit Gateways
* Load Balancers
* RDS
* S3
* ACM certificates

### Automated Utilization Analysis

Combine:

```text
EC2 Cost
+
Instance Type
+
CloudWatch Utilization
+
Runtime
```

to identify potential rightsizing opportunities.

### Automated Cost Anomaly Detection

Detect unusual increases in AWS spending automatically.

### Automated Savings Estimation

Calculate potential monthly and annual savings for confirmed waste.

### Automated Audit Reports

Generate standardized audit reports containing:

* Executive summary
* Cost overview
* Cost drivers
* Findings
* Evidence
* Potential savings
* Recommendations
* Priority
* Action plan

---

# Conclusion

This project performed a three-month AWS Cost Audit covering **June, July, and August 2026**.

The account generated approximately **$27.66 in total charges**, including approximately **$1.92 in tax**, resulting in approximately **$25.74 of pre-tax AWS spending** considered for optimization analysis.

The largest cost categories were:

1. **EC2-Other — $8.64**
2. **AWS Certificate Manager — $7.00**
3. **Amazon VPC — $4.84**
4. **Amazon EC2 Compute — $4.82**

The audit then moved beyond service-level analysis.

The major cost drivers were investigated through their underlying billing dimensions:

```text
EC2-Other
   ↓
EBS
```

```text
VPC
   ↓
Transit Gateway
   ↓
Transit Gateway operation
```

```text
AWS Certificate Manager
   ↓
Exportable public SSL/TLS certificates
   ↓
Request Certificate
```

```text
EC2
   ↓
t3.micro
   ↓
Linux/Unix
   ↓
Utilization / workload investigation
```

The resource investigation identified several potential optimization opportunities, including:

* Idle EC2 instances
* Unattached EBS volumes
* Potential EC2 overprovisioning
* Transit Gateway infrastructure
* Exportable public SSL/TLS certificates
* EC2-Other cost drivers
* Temporary learning resources remaining after project completion

The project demonstrates that effective cloud cost optimization is not simply about finding the most expensive AWS service.

It is about following the cost from:

```text
AWS Bill
    ↓
Service
    ↓
Usage Type
    ↓
Operation
    ↓
Region
    ↓
Resource
    ↓
Configuration
    ↓
Utilization
    ↓
Root Cause
    ↓
Waste
    ↓
Evidence
    ↓
Recommendation
    ↓
Potential Savings
```

This project therefore serves as a practical demonstration of **AWS Cost Auditing, FinOps analysis, cloud waste detection, infrastructure investigation, and evidence-based cloud cost optimization**.

---

**Author:** Ozoude Emmanuel Izuchukwu
**Date:** 9/9/2026
**Project:** AWS Cost Audit & Cost Optimization Analysis
