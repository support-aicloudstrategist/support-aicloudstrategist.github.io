# Channel 1 Research Report: Naukri / Resdex mechanics and senior profile optimization for ₹1.5 Cr target

Date: 2026-05-18  
Scope: Naukri/Naukri Recruiter mechanics only: recruiter search/filter behavior, candidate fields, freshness, resume upload, role/title/skills/salary/notice visibility implications for a 22+ year cloud/platform leader targeting ₹1.5 Cr.

## Executive findings

1. Naukri’s employer product is centered on **Resdex**, a recruiter-facing searchable resume/profile database. Public Naukri copy positions it as giving recruiters “instant access” to a large database across **functional roles, hierarchy and sectors**.
2. Recruiters can search/filter candidate supply; public product copy explicitly mentions searchable resumes, candidates across locations including international locations, fresh resumes daily, and real-time contact via email/SMS.
3. Naukri’s own privacy policy confirms that profile/resume information includes work experience, education, current/past salary/remuneration, resume copy, contact details, etc., and can be shared/forwarded to potential recruiters when Naukri determines a resume matches a job/vacancy.
4. Jobseeker registration/profile code exposes the important structured fields Naukri collects: resume headline, key skills, current employment, work experience, company, designation, salary, notice period, industry, department, role category, role, desired job type/employment type, preferred location, expected CTC, immediate availability/join date, profile summary, projects, IT skills, certifications, education, resume, photo.
5. Naukri’s public job-search UI code exposes job filters such as experience, salary/CTC, location, work-from-home type, job type/employment type, industry, role/function clusters, top companies, education and posting age. Recruiter-side filters are not fully public, but these fields strongly indicate the structured taxonomy Naukri uses to match/search.
6. For a ₹1.5 Cr senior cloud/platform leader, the profile must be optimized both for **keyword retrieval** and **structured filter survival**: current CTC, expected CTC, notice period, experience, role/category, location, industry, and designation can all decide whether he appears in recruiter workflows.

## Evidence URLs

### Naukri/Resdex recruiter product sources

- https://recruit.naukri.com/hiringsuite/naukri-resdex.html  
  Evidence: Naukri describes Resdex as recruiter access to a comprehensive database across functional roles, hierarchy and sectors; lists searchable resumes, location coverage including international, fresh resumes daily, contact via email/SMS, and multiple search tools.
- https://www.naukri.com/recruit/resume-database-access-resdex?isCrawler=1  
  Evidence from title/search snippets and page metadata: “Resume Database Access”, “CV Database”, “Search using filters & contact candidates instantly.”
- https://www.naukri.com/recruit/buy-resume-database-access-packages  
  Evidence from title/search snippets: resume database access packages and employer purchasing path.
- https://resdex.naukri.com/  
  Evidence: public endpoint redirects to recruiter login, confirming Resdex is a gated recruiter product.

### Naukri privacy / data-use source

- https://www.naukri.com/privacypolicy  
  Evidence: Naukri collects resume-like information including name/contact details, work experience, education, current/past remuneration/salary, resume copy; uses data for relevant search results/recommended jobs/candidates; may share/forward resume to potential recruiters when matching a job/vacancy; users can update/correct profile info.

### Naukri jobseeker/profile implementation sources

- https://www.naukri.com/registration/createAccount  
  Evidence: registration entry point and metadata (“Create your Profile Now, Free”).
- https://static.naukimg.com/s/7/104/j/main.d03f3164.min.js  
  Evidence from public JS: registration/profile completion fields include `resumeHeadline`, `keySkills`, `workExp`, `company`, `designation`, `currency`, `salary`, `noticePeriod`, `lastWorkingDay`, `industry`, `department`, `roleCategory`, `role`, `desiredJobType`, `desiredEmploymentType`, `preferredSalary`, `newLocationPrefId`; text says recruiters prefer/give first preference to candidates who have a resume.
- https://www.naukri.com/nlogin/authIntro  
  Evidence: jobseeker login metadata mentions access to non-public jobs, search/apply, and follow recruiters.
- https://static.naukimg.com/s/5/105/j/app_v447.min.js  
  Evidence from public JS: profile sections include My Profile, Employment Details, Education Details, Resume Headline, Profile Summary, Key Skills, Project Details, IT Skills, Other Details, Career Profile, Resume, Photo Upload, Jobs from Recruiters, Jobs For You; desired profile fields include preferred location, expected CTC, immediate availability/join date.

### Naukri job-search/filter implementation sources

- https://www.naukri.com/vp-engineering-jobs  
  Evidence: senior-role search page; public Next.js payload references search state, filters, selected filters, sort, location and keyword.
- https://static.naukimg.com/s/9/121/_next/static/chunks/app/srp/page-8edba2c6b42c2dd9.js  
  Evidence from public JS: filters/analytics names include experience slider 0–30 years, salary/CTC filter, location, WFH type, job type, employment type, industry, top companies, education, posting age; sort-by UI exists.
- https://static.naukimg.com/s/9/121/_next/static/chunks/6845-e0a91a42826dd875.js  
  Evidence from public JS: user profile/event attributes include experience years/months, current salary lacs/thousands, functional area; profile fields include notice period, desired employment type, work permit country; filter key list includes `jobAge`, `wfhType`, `cityTypeGid`, `ctcFilter`, `experience`, `jobTypeFilter`, `industryTypeIdGid`, `functionAreaIdGid`, `roleTypeFilterGid`, etc.

## How recruiters appear to search/filter on Naukri/Resdex

Public sources do not expose the full logged-in recruiter UI. However, Naukri’s own product and implementation evidence support the following model:

- Recruiters search the Resdex resume/profile database, not just inbound applications.
- Search likely combines free-text/keyword matching with structured filters/taxonomies.
- Candidate visibility depends on Naukri profile data and uploaded resume data.
- Structured fields matter because Naukri collects and normalizes them separately: current company, designation, experience, salary, notice period, industry, department, role, role category, desired role, desired employment type, expected CTC, preferred location.
- Freshness matters because Naukri sells “fresh resumes every day” to recruiters and candidate activity/profile updates are a likely ranking/filter dimension. Exact ranking formula is not public.
- Resume upload matters because Naukri’s registration JS says recruiters prefer/first prefer candidates with a resume on profile.
- Contactability matters: Resdex is sold with email/SMS candidate contact, so mobile/email verification, visibility and accurate contact data likely improve recruiter conversion.

## 25 practical rules for Rajiv’s Naukri profile

1. **Upload a current ATS-readable resume**; do not rely only on typed profile fields.
2. **Keep the same target identity everywhere:** Cloud/Platform Engineering Leader, not a generic “IT Head.”
3. **Use the headline as a search result hook:** include role level + domain + scale + compensation band signal if appropriate.
4. **Put exact recruiter keywords in Key Skills**, not only narrative prose.
5. **Mirror key skills in the resume, headline, profile summary and employment bullets** so both parser and keyword search catch them.
6. **Use senior title variants:** VP Engineering, Director Engineering, Head of Platform, Head Cloud, Cloud Infrastructure Leader, Platform Engineering, SRE, DevOps, Enterprise Architecture.
7. **Avoid over-indexing on one title**; senior recruiters search using multiple variants.
8. **Set total experience accurately at 22+ years**; misstatement can fail experience filters.
9. **Use current designation strategically**; if current formal title is obscure, add parenthetical business-readable title in headline/summary/resume.
10. **Fill current CTC carefully**; recruiters often use salary filters. For a ₹1.5 Cr target, a too-low CTC may route him to lower-band mandates; a too-high CTC may filter him out of mid/senior roles.
11. **Set expected CTC as negotiable but not vague**; use a range aligned to target, e.g., ₹1.4–1.6 Cr or ₹1.5 Cr+ depending on current CTC and willingness.
12. **Notice period must be recruiter-friendly**; if possible, select the shortest accurate option and state buyout/early joining availability.
13. **Preferred locations should match senior demand pools:** Bengaluru, Hyderabad, Pune, NCR/Gurgaon/Noida, Mumbai, Chennai, plus Remote/Hybrid if available.
14. **Do not leave industry/department/role-category blank**; these are likely filter dimensions.
15. **Choose functional area/department around Engineering/IT/Technology/Cloud/Infrastructure**, not generic management unless forced.
16. **Role category should map to senior technology leadership**: Engineering Manager/Director, Technology Head, Enterprise/Cloud Architecture, Infrastructure/Platform leadership depending on taxonomy options.
17. **Current employment section should show scope:** team size, platform scale, cloud spend, uptime/SRE metrics, migration scale, security/compliance, cost optimization.
18. **Profile summary should be concise and searchable:** first 3 lines must carry 22+ yrs, cloud/platform/SRE/DevOps, leadership scale, target role type.
19. **Use “Jobs from Recruiters” and recruiter follow features** to create activity signals and contact paths.
20. **Refresh profile regularly** by making meaningful updates: resume upload, headline tweaks, skill updates, role updates. Avoid spammy daily micro-edits if they degrade quality.
21. **Apply selectively to ₹1 Cr+ relevant senior roles** to reinforce recommendation/matching signals; avoid applying to misaligned low-salary roles.
22. **Keep mobile/email verified and visible** because recruiter product emphasizes real-time email/SMS contact.
23. **Use public resume file name professionally:** `Rajiv_Gupta_Cloud_Platform_Engineering_Leader_Resume.pdf`.
24. **Avoid keyword stuffing that creates false matches**; recruiters may reject if profile looks inflated.
25. **Check profile completeness until all core sections are complete:** employment, education, resume headline, profile summary, key skills, resume, desired career profile, salary/notice/location.

## Exact Naukri field implications for a 22+ year cloud/platform leader targeting ₹1.5 Cr

### Resume Headline

Recommended pattern:

> Cloud & Platform Engineering Leader | 22+ yrs | VP/Director/Head Engineering | AWS/Azure/GCP, SRE, DevOps, Kubernetes | Large-scale SaaS/Enterprise Platforms | Target ₹1.5 Cr

If explicitly showing target salary feels risky, omit salary from headline and keep it in expected CTC. Alternative:

> VP/Director Engineering – Cloud Platform, SRE & DevOps | 22+ yrs | Enterprise SaaS / Infrastructure Modernization | Kubernetes, AWS/Azure/GCP

Implication: headline is likely visible in recruiter search results and profile previews; it must carry the exact senior keywords recruiters type.

### Profile Summary

Include:

- 22+ years total technology leadership.
- Cloud/platform/SRE/DevOps/infra modernization identity.
- Scale indicators: teams led, users/transactions, uptime, migration, cost optimization, security/compliance.
- Target roles: VP Engineering, Director Engineering, Head of Platform Engineering, Head Cloud Infrastructure, CTO-1/Technology Head.

Avoid:

- Long autobiography.
- Generic “seeking challenging role.”
- Too many unrelated industries/functions.

### Key Skills

Prioritized skills list:

- Cloud Platform Engineering
- Platform Engineering
- Site Reliability Engineering / SRE
- DevOps Transformation
- AWS, Azure, GCP (only truthful)
- Kubernetes, Docker, Containers
- Microservices Architecture
- Infrastructure as Code / Terraform / Ansible
- CI/CD, GitOps
- Observability / Monitoring / APM
- Cloud Migration
- Cloud Cost Optimization / FinOps
- Enterprise Architecture
- Distributed Systems
- API Platforms
- Security / DevSecOps
- IT Infrastructure
- Data Center Migration (if relevant)
- Engineering Leadership
- Program Delivery / Transformation
- Vendor Management
- Agile / Scrum / SAFe (if relevant)
- Budget Ownership / P&L (if relevant)

Implication: key skills are a likely high-weight retrieval field. Use exact words, abbreviations and variants.

### Employment Details

For each recent role, structure bullets around:

- Title and business-readable equivalent.
- Team size and reporting line.
- Cloud/platform scope.
- Measurable outcomes: uptime, latency, deployment frequency, migration volume, cost savings, security/compliance, revenue/product impact.
- Technologies and leadership keywords.

Implication: employment fields include company, designation, industry, department, role category and role. These should match senior technology filters and not hide leadership under vague titles.

### Designation / Current Role

If Naukri allows only the formal company title, keep formal title. In headline/summary/resume add equivalent titles:

- VP Engineering
- Director Engineering
- Head Platform Engineering
- Head Cloud Infrastructure
- Technology Head
- Enterprise Architect / Principal Architect only if aiming for IC/architecture roles too

Implication: recruiters often search titles directly; include multiple truthful variants in searchable text.

### Current CTC

For ₹1.5 Cr target:

- Enter accurate current CTC as required.
- If current CTC is below target, compensate with profile proof: scale, leadership, cloud cost ownership, revenue/platform impact.
- If current CTC is close to target, expected CTC can be more direct.

Implication: salary/remuneration is collected by Naukri and salary/CTC filters exist in job-search UI; recruiter-side compensation screening is highly likely.

### Expected CTC / Preferred Salary

Recommended range depends on current CTC:

- If current CTC ≥ ₹1.1–1.3 Cr: expected ₹1.5 Cr or ₹1.4–1.6 Cr.
- If current CTC lower: expected ₹1.2–1.5 Cr / negotiable may keep more funnels open, while resume positioning handles premium roles.
- If only one number allowed: choose a strategic anchor, e.g., ₹1.5 Cr, but monitor response volume.

Implication: too rigid a number can reduce reach; too low can anchor recruiters below target.

### Notice Period

Recommended:

- Select actual notice period.
- If available, add “can join earlier via buyout / negotiable / transition support.”
- If serving notice, update last working day immediately.

Implication: `noticePeriod` and `lastWorkingDay` are explicit Naukri fields; recruiters commonly prioritize immediate/30/60-day candidates.

### Preferred Location

Recommended:

- Bengaluru, Hyderabad, Pune, NCR/Gurgaon/Noida, Mumbai, Chennai.
- Add “Remote/Hybrid” if taxonomy supports it.
- For ₹1.5 Cr, keep flexibility for GCCs, SaaS firms, fintech, enterprise tech and consulting leadership roles.

Implication: location filters are explicit in search UI and likely recruiter workflows.

### Industry / Department / Role Category / Role

Recommended taxonomy choices if available:

- Industry: IT Services, Software Product, SaaS, Cloud, Internet, FinTech, Enterprise Technology, Telecom if relevant.
- Department: Engineering - Software / IT & Information Security / Technology / Infrastructure & Cloud depending on options.
- Role Category: Engineering Management, Technology Leadership, Enterprise/Cloud Architecture, DevOps/SRE, Infrastructure Services.
- Role: VP Engineering, Director Engineering, Head Engineering, Head Platform, Cloud Architect/Leader, CTO-1/Technology Head.

Implication: Naukri code shows these fields are separate normalized objects. Blank or wrong choices can make the profile invisible to filtered searches.

### Resume Upload

Recommended:

- PDF or DOCX with text, not image/scanned.
- First page should include title, phone/email, location, target role, 10–15 high-value keywords.
- File name should contain name + target identity.
- Re-upload after meaningful updates.

Implication: Naukri registration copy says recruiters prefer/first prefer candidates with a resume on profile.

### Profile Completeness

Complete all high-signal sections:

- Resume Headline
- Profile Summary
- Key Skills
- Employment Details
- Education
- IT Skills / Tools
- Projects / Transformation Programs
- Desired Career Profile
- Current/Expected CTC
- Notice Period
- Preferred Locations
- Resume
- Photo, if professional and comfortable

Implication: Naukri has a profile completion flow; incomplete profiles likely lose recruiter confidence and possibly ranking.

## Risks and unknowns

1. **Exact Resdex ranking formula is not public.** We can infer from product/fields but cannot prove weighting.
2. **Logged-in recruiter filters are gated.** Public sources reveal candidate fields and job-search filters, not the full Resdex UI.
3. **Salary strategy is sensitive.** A ₹1.5 Cr expected CTC can improve fit for premium mandates but may reduce volume if recruiters filter below that.
4. **Freshness mechanics are not explicitly documented.** Public product copy emphasizes fresh resumes; profile update frequency likely matters, but cadence/weight are unknown.
5. **Keyword stuffing risk.** Adding too many title variants can help retrieval but may reduce credibility if not backed by experience.
6. **Naukri taxonomies change.** Field labels/options may differ by UI version and account status.
7. **Paid services are not evaluated here.** This report focuses on public mechanics and organic recruiter discovery, not Naukri FastForward/Premium ROI.

## Recommended Naukri positioning for Rajiv Gupta

Position Rajiv as:

> A 22+ year Cloud & Platform Engineering leader for VP/Director/Head roles, with credible scale in cloud infrastructure, SRE/DevOps transformation, enterprise platforms, Kubernetes/microservices, cost optimization, reliability and engineering leadership; compensation target around ₹1.5 Cr for premium GCC/SaaS/enterprise technology mandates.

Primary profile objective: pass senior recruiter filters for **experience + salary + notice + location + role category**, then rank/retrieve for **cloud/platform/SRE/DevOps/engineering leadership keywords**.
