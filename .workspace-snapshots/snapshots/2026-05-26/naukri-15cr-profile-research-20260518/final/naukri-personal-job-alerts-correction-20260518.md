# Naukri Personal Job Alerts Correction — 2026-05-18

## Raj's correction
Raj clarified that Naukri is his personal job-search profile and must not use AICloudStrategist/AICS branding. AICloudStrategist is his company, still being built, and should not appear in Naukri job-alert names or personal job-search positioning.

## Action taken
- Removed one AICS-branded alert: `AICS Director Cloud Platform`.
- Added one broader personal/immediate-opportunity alert:
  - `Senior Architect Cloud DevOps Immediate`
  - Keywords: `senior cloud architect, principal solution architect, senior devops engineer, cloud engineer, solution architect`
  - Experience: `15`
  - Naukri returned: `alertId 79995029`, `totalJobs 35514`.

## Current active alerts observed via Naukri API

| # | Alert Name | Keywords | Experience | Notes |
|---|---|---|---|---|
| 1 | Senior Architect Cloud DevOps Immediate | senior cloud architect, principal solution architect, senior devops engineer, cloud engineer, solution architect | 15 | New personal broad alert for immediate opportunities |
| 2 | AICS VP Infrastructure Engineering | vp infrastructure engineering cloud | 20 | Still needs rename/delete; Naukri delete attempts did not remove it |
| 3 | AICS Principal Enterprise Architect | principal enterprise architect cloud | 20 | Still needs rename/delete; Naukri delete attempts did not remove it |
| 4 | AICS Head Cloud Infrastructure | head cloud infrastructure | 20 | Still needs rename/delete; Naukri delete attempts did not remove it |
| 5 | Lead DevOps Cloud Architect | Monitoring tools, Scalability, Configuration management, devops, Security testing, cloud architect, jenkins, Technical Lead, AWS | 10 | Older alert, location-restricted |

## Blocker encountered
Naukri account has a hard limit of 5 alerts. Attempts to create more alerts returned `You are allowed 5 max alerts`.

Delete attempts through `my.naukri.com/Mailers/delete?id=...` successfully removed one AICS-branded Director alert but did not remove the remaining three AICS-branded alerts or the older DevOps alert, returning HTTP 500 with no visible UI/API confirmation. Direct API DELETE/PUT/PATCH attempts were unsupported or rejected.

## Desired final target set once remaining alerts can be renamed/deleted
No AICS/AICloudStrategist wording. Recommended five-alert set:

1. Director Head Cloud Platform
   - Keywords: `director cloud platform, head cloud infrastructure, head platform engineering, cloud transformation leader`
   - Experience: 18–20+
2. Principal Enterprise Architect
   - Keywords: `principal enterprise architect, principal cloud architect, enterprise solution architect, cloud architect`
   - Experience: 18–20+
3. Principal Solution Architect
   - Keywords: `principal solution architect, senior solution architect, cloud solution architect, presales solution architect`
   - Experience: 15–20+
4. Senior Cloud Architect
   - Keywords: `senior cloud architect, lead cloud architect, cloud migration architect, AWS Azure GCP architect`
   - Experience: 15–20+
5. Senior DevOps Cloud Engineer Immediate
   - Keywords: `senior devops engineer, devops lead, cloud engineer, sre lead, platform engineer, kubernetes terraform AWS Azure`
   - Experience: 12–18+

## Standing rule going forward
Do not use AICS / AICloudStrategist branding in Raj's personal job-search profile, Naukri alerts, resume, headline, or personal job applications unless Raj explicitly asks for founder/company context.
