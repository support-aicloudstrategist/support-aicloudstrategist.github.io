(function(){
  var form=document.getElementById('lostLeadAuditForm'); if(!form)return;
  var ok=document.getElementById('auditSuccess'),err=document.getElementById('auditError'),button=document.getElementById('auditSubmitButton');
  var params=new URLSearchParams(location.search),attr=window.aicsAttribution||{};
  form.elements.form_loaded_at.value=String(Date.now());
  form.elements.package_context.value=params.get('offer')||''; form.elements.service_context.value=params.get('service')||'';
  ['landing_page','referrer','utm_source','utm_medium','utm_campaign'].forEach(function(k){if(form.elements[k])form.elements[k].value=attr[k]||params.get(k)||'';});
  form.addEventListener('submit',async function(e){e.preventDefault();ok.hidden=true;err.hidden=true;if(!form.checkValidity()){form.reportValidity();return;}
    var payload=Object.fromEntries(new FormData(form).entries());try{payload.business_name=new URL(payload.website).hostname.replace(/^www\./,'');}catch(_){payload.business_name=payload.website;}
    payload.notes=[payload.primary_issue,payload.specific_notes].filter(Boolean).join(' · ');button.disabled=true;button.textContent='Submitting securely…';
    try{var response=await fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}),result=await response.json().catch(function(){return{};});if(!response.ok||!result.ok)throw new Error(result.error||'Submission failed');ok.textContent='Request received. Reference: '+result.lead_id+'. We will reply by email.';ok.hidden=false;form.reset();if(window.aicsAnalytics)window.aicsAnalytics.track('form_submit_success',{props:{form:'focused_fit_review',offer:payload.package_context||payload.primary_issue||''}});}catch(ex){err.textContent='The request could not be delivered. Retry or email contact@aicloudstrategist.com.';err.hidden=false;if(window.aicsAnalytics)window.aicsAnalytics.track('form_submit_error',{props:{form:'focused_fit_review'}});}finally{button.disabled=false;button.textContent='Request fit review';}
  });
})();