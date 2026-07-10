#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
PUBLIC_SKIP={'.git','node_modules','.workspace-snapshots','preview'}
CATEGORIES={
 'Cloud bill / cost problem':['my AWS bill is too high','why is my AWS bill so high','how to reduce AWS bill','how to reduce cloud bill','how to reduce cloud costs','how to optimize AWS cloud bill','AWS bill too high','Azure bill too high','Google Cloud billing too high','how to limit AWS billing','cloud cost optimization consultant','FinOps consultant India'],
 'Manual work / staff time waste':['too much manual work in my business','how to reduce manual work in office','how to reduce workload of employees','how to automate repetitive tasks','manual data entry taking too much time','same work repeated every day','staff wasting time on follow up','reduce office workload','automate Excel work','automate WhatsApp follow up','business process automation for small business','how to save staff time without hiring more people'],
 'Clinic patients / leads':['my clinic is not getting patients','how to get more patients in clinic','how to increase patients in clinic','how to increase patient footfall','how to increase OPD footfall','patients not coming to clinic','dental clinic not getting calls','IVF clinic leads not converting','how to improve clinic bookings','clinic enquiries not converting','reception not following up patients','WhatsApp follow up for clinic patients'],
 'Compliance / privacy fear':['what compliance does my business need','data privacy law India','customer data protection India','privacy policy for website India','is privacy policy mandatory in India','DPDP rules for small business','how to protect customer data','can I store customer WhatsApp data','is WhatsApp marketing legal in India','website form consent India','data leak what should business do','customer consent for clinic WhatsApp'],

 'Shop / retailer / local business':['small shop customer increase India','how to get more customers for small shop','how to increase local business customers','how to increase sales in retail shop','my shop is not getting customers','customers are not coming to my shop','how to attract customers to retail store India','WhatsApp customer follow up small business','how to follow up customers on WhatsApp','customer follow up message for small business','local business digital marketing India','small business marketing India'],
 'Small factory / manufacturing':['factory manual work reduce India','small manufacturing automation India','how to reduce labour cost in factory India','how to reduce manual work in factory','factory work tracking software India','factory production follow up Excel','factory owner dashboard India','manufacturing automation for small business','reduce manpower in manufacturing India','factory daily report automation','factory order tracking WhatsApp','factory staff follow up system'],
 'School / coaching / education':['coaching admission increase India','how to increase admission in coaching classes','how to get more admissions for coaching institute India','school admission enquiry follow up software','school admission CRM India','coaching leads not converting','parents enquiry follow up school','student admission follow up WhatsApp','coaching institute digital marketing India','admission enquiry tracking software','how to improve school admissions India','education institute lead management India'],
 'Hotel / restaurant / service business':['restaurant customers increase India','how to increase restaurant sales in India','how to get more customers for restaurant','restaurant marketing ideas India','hotel bookings not increasing India','service business customers increase India','local business digital marketing agency India','how to improve Google reviews restaurant','repeat customer WhatsApp follow up restaurant','restaurant offer WhatsApp campaign','cafe customers increase India','salon customers increase India'],
 'Vendor selection / consultant search':['best cloud consultant India','AWS cost optimization consultant India','cloud cost consultant','business automation consultant India','small business automation consultant','healthcare digital marketing agency India','clinic growth consultant India','clinic marketing agency India','DPDP compliance consultant India','website and automation company India','AI consultant for small business India','best consultant for reducing business cost']
}
REQUIRED_PAGES={
 'Cloud bill / cost problem':'resources/customer-problem-search/aws-cloud-bill-too-high/index.html',
 'Manual work / staff time waste':'resources/customer-problem-search/manual-work-wasting-staff-time/index.html',
 'Clinic patients / leads':'resources/customer-problem-search/clinic-not-getting-patients/index.html',
 'Compliance / privacy fear':'resources/customer-problem-search/business-compliance-privacy-confusion/index.html',

 'Shop / retailer / local business':'resources/customer-problem-search/small-shop-customer-increase/index.html',
 'Small factory / manufacturing':'resources/customer-problem-search/factory-manual-work-reduce/index.html',
 'School / coaching / education':'resources/customer-problem-search/coaching-school-admission-increase/index.html',
 'Hotel / restaurant / service business':'resources/customer-problem-search/restaurant-local-service-customers-increase/index.html',
 'Vendor selection / consultant search':'resources/customer-problem-search/find-right-consultant-vendor/index.html',
}
def public_files():
    for p in ROOT.rglob('*.html'):
        parts=set(p.relative_to(ROOT).parts)
        if parts & PUBLIC_SKIP: continue
        yield p
site='\n'.join(p.read_text(encoding='utf-8',errors='ignore').lower() for p in public_files())
sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8',errors='ignore').lower() if (ROOT/'sitemap.xml').exists() else ''
llms=(ROOT/'llms.txt').read_text(encoding='utf-8',errors='ignore').lower() if (ROOT/'llms.txt').exists() else ''
results=[]
for cat, phrases in CATEGORIES.items():
    exact=sum(1 for ph in phrases if ph.lower() in site)
    page_exists=(ROOT/REQUIRED_PAGES[cat]).exists()
    slug=REQUIRED_PAGES[cat].replace('index.html','').lower()
    in_sitemap=slug in sitemap
    in_llms=slug in llms
    page_text=(ROOT/REQUIRED_PAGES[cat]).read_text(encoding='utf-8',errors='ignore').lower() if page_exists else ''
    has_faq='application/ld+json' in page_text and 'faqpage' in page_text
    has_cta='free-business-review' in page_text and 'wa.me/918796302608' in page_text
    # 60 exact phrase coverage + 10 page + 10 sitemap + 10 llms + 5 FAQ + 5 CTA
    score=min(60, round(60*exact/len(phrases))) + (10 if page_exists else 0) + (10 if in_sitemap else 0) + (10 if in_llms else 0) + (5 if has_faq else 0) + (5 if has_cta else 0)
    results.append({'category':cat,'score':score,'exact_phrase_hits':exact,'required_phrases':len(phrases),'page_exists':page_exists,'in_sitemap':in_sitemap,'in_llms':in_llms,'faq_schema':has_faq,'cta':has_cta})
overall=round(sum(r['score'] for r in results)/len(results),1)
report={'overall':overall,'categories':results}
print(json.dumps(report,indent=2))
sys.exit(0 if all(r['score']==100 for r in results) else 1)
