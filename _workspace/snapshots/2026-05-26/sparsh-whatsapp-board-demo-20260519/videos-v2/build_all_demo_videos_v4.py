from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, textwrap, json, os, shutil, math

ROOT=Path('/home/OpenClaw/.openclaw/workspace/reports/sparsh-whatsapp-board-demo-20260519/videos-v4')
ROOT.mkdir(parents=True, exist_ok=True)
EDGE='/home/OpenClaw/.openclaw/workspace/aics-lead-engine-v1/calling-agent/vobiz-livekit-india-pilot-v1/.venv-tts/bin/edge-tts'
FF='/home/OpenClaw/.openclaw/workspace/.local-ffmpeg/usr/bin/ffmpeg'
FP='/home/OpenClaw/.openclaw/workspace/.local-ffmpeg/usr/bin/ffprobe'
ENV=os.environ.copy(); ENV['LD_LIBRARY_PATH']='/home/OpenClaw/.openclaw/workspace/.local-ffmpeg/usr/lib/x86_64-linux-gnu'
W,H=1280,720
fd=Path('/usr/share/fonts/truetype/dejavu')
FONT={
 'brand': ImageFont.truetype(str(fd/'DejaVuSans-Bold.ttf'), 28),
 'h1': ImageFont.truetype(str(fd/'DejaVuSans-Bold.ttf'), 42),
 'h2': ImageFont.truetype(str(fd/'DejaVuSans-Bold.ttf'), 29),
 'body': ImageFont.truetype(str(fd/'DejaVuSans.ttf'), 25),
 'bodyb': ImageFont.truetype(str(fd/'DejaVuSans-Bold.ttf'), 25),
 'small': ImageFont.truetype(str(fd/'DejaVuSans.ttf'), 18),
 'smallb': ImageFont.truetype(str(fd/'DejaVuSans-Bold.ttf'), 18),
 'tiny': ImageFont.truetype(str(fd/'DejaVuSans.ttf'), 14),
 'micro': ImageFont.truetype(str(fd/'DejaVuSans.ttf'), 13),
}
NAVY=(7,16,31); BLUE=(31,98,255); LBLUE=(237,243,255); GREEN=(199,255,77); TEXT=(16,38,83); MUTED=(87,101,126); WHITE=(255,255,255); PALE=(248,251,255); BORDER=(218,231,251); ORANGE=(255,247,237); RED=(255,241,242)
CONTACT='Website: aicloudstrategist.com  |  WhatsApp: +91 87963 02608  |  Voice line: +91 80654 80898  |  Email: contact@aicloudstrategist.com  |  Support: support@aicloudstrategist.com'

def run(cmd, **kw):
    print('+', ' '.join(map(str,cmd)))
    return subprocess.run(cmd, check=True, env=ENV, **kw)

def wrap_text(text, font, max_width):
    words=text.split(); lines=[]; cur=''
    dummy=Image.new('RGB',(10,10)); d=ImageDraw.Draw(dummy)
    for w in words:
        cand=(cur+' '+w).strip()
        if d.textbbox((0,0), cand, font=font)[2] <= max_width or not cur:
            cur=cand
        else:
            lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def draw_multiline(d, text, xy, font, fill, max_width, line_gap=8):
    x,y=xy
    for line in wrap_text(text,font,max_width):
        d.text((x,y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y

def bg():
    im=Image.new('RGB',(W,H),LBUE if False else LBLUE)
    d=ImageDraw.Draw(im)
    for y in range(H):
        col=(237+int(18*y/H),243+int(9*y/H),255)
        d.line((0,y,W,y), fill=col)
    # subtle circles
    d.ellipse((960,-120,1430,350), fill=(225,235,255))
    d.ellipse((-180,450,280,900), fill=(229,239,255))
    return im

def rounded(d,box,fill,r=24,outline=BORDER,width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def header_footer(d, package):
    # Premium brand header: no cramped box, clean mark + wordmark
    d.rounded_rectangle((46,28,92,74), radius=14, fill=NAVY)
    d.text((59,39),'AI',font=FONT['smallb'],fill=GREEN)
    d.text((108,31),'AICloudStrategist',font=FONT['brand'],fill=TEXT)
    d.text((110,61),'Cloud, automation and AI workflows for growing businesses',font=FONT['micro'],fill=MUTED)

    # Package badge with ample width
    d.rounded_rectangle((940,30,1234,76), radius=23, fill=GREEN)
    tw=d.textbbox((0,0),package,font=FONT['smallb'])[2]
    d.text((940+(294-tw)//2,44),package,font=FONT['smallb'],fill=NAVY)

    # Clean contact footer: full-width two-line strip, no label crowding
    d.line((46,636,1234,636), fill=BORDER, width=2)
    d.rounded_rectangle((46,648,1234,696), radius=18, fill=(255,255,255), outline=BORDER, width=1)
    row1='Website: aicloudstrategist.com     •     WhatsApp: +91 87963 02608     •     Voice line: +91 80654 80898'
    row2='Email: contact@aicloudstrategist.com     •     Support: support@aicloudstrategist.com'
    d.text((72,656),row1,font=FONT['micro'],fill=TEXT)
    d.text((72,676),row2,font=FONT['micro'],fill=MUTED)

def title_slide(package, title, subtitle):
    im=bg(); d=ImageDraw.Draw(im); header_footer(d, package)
    d.text((70,150), title, font=FONT['h1'], fill=TEXT)
    draw_multiline(d, subtitle, (72,220), FONT['body'], (51,65,95), 860, 10)
    rounded(d,(72,380,1180,520),WHITE,26)
    d.text((105,410),'Welcome',font=FONT['h2'],fill=BLUE)
    draw_multiline(d,'This short demo explains the clinic problem, the solution we build, what components are included, and the benefit for the customer.',(105,456),FONT['body'],TEXT,1000,8)
    return im

def section_slide(package, tag, title, bullets, accent=BLUE):
    im=bg(); d=ImageDraw.Draw(im); header_footer(d, package)
    d.rounded_rectangle((70,112,70+len(tag)*13+60,152), radius=20, fill=GREEN)
    d.text((96,121), tag, font=FONT['smallb'], fill=NAVY)
    d.text((70,178), title, font=FONT['h1'], fill=TEXT)
    y=260
    for b in bullets:
        rounded(d,(76,y,1204,y+78),WHITE,18)
        d.rounded_rectangle((100,y+22,128,y+50), radius=14, fill=accent)
        d.text((108,y+21),'✓',font=FONT['smallb'],fill=WHITE)
        draw_multiline(d,b,(148,y+18),FONT['body'],(51,65,95),990,6)
        y+=94
        if y>610: break
    return im

def columns_slide(package, tag, title, cols):
    im=bg(); d=ImageDraw.Draw(im); header_footer(d, package)
    d.rounded_rectangle((70,106,70+len(tag)*13+60,146), radius=20, fill=GREEN)
    d.text((96,115), tag, font=FONT['smallb'], fill=NAVY)
    d.text((70,170), title, font=FONT['h1'], fill=TEXT)
    n=len(cols); gap=18; x0=70; y0=260; h=330; w=(1140-gap*(n-1))//n
    for i,(head,body,color) in enumerate(cols):
        x=x0+i*(w+gap)
        rounded(d,(x,y0,x+w,y0+h),WHITE,24)
        d.rounded_rectangle((x+18,y0+18,x+w-18,y0+62), radius=18, fill=color)
        d.text((x+35,y0+28),head,font=FONT['smallb'],fill=WHITE if color!=GREEN else NAVY)
        draw_multiline(d,body,(x+24,y0+86),FONT['body'],TEXT,w-48,8)
    return im

def board_slide(package, title, subtitle, advanced=False):
    im=bg(); d=ImageDraw.Draw(im); header_footer(d, package)
    d.text((70,112), title, font=FONT['h1'], fill=TEXT)
    draw_multiline(d,subtitle,(72,170),FONT['body'],(51,65,95),1050,8)
    labels=['New enquiries','Appointment requests','Staff follow-up','Closed / summary'] if not advanced else ['API enquiry','Workflow engine','Staff action','Owner report']
    cards=[['Hair fall timing','Acne consult','Missed call'],['Slot request','Doctor timing','Location'],['Callback due','No response','Reminder'],['Booked','Opt-out','Daily summary']]
    x0=58; y0=280; gap=14; w=(1164-gap*3)//4
    for i,l in enumerate(labels):
        x=x0+i*(w+gap)
        rounded(d,(x,y0,x+w,620),PALE,20)
        d.text((x+18,y0+18),l,font=FONT['smallb'],fill=TEXT)
        y=y0+58
        for c in cards[i]:
            rounded(d,(x+16,y,x+w-16,y+58),WHITE,14)
            d.text((x+30,y+17),c,font=FONT['small'],fill=TEXT)
            y+=72
    return im

def closing_slide(package, title, body):
    im=bg(); d=ImageDraw.Draw(im); header_footer(d, package)
    d.text((70,140),title,font=FONT['h1'],fill=TEXT)
    draw_multiline(d,body,(75,215),FONT['body'],(51,65,95),1050,10)
    rounded(d,(110,430,1170,575),NAVY,26,outline=NAVY)
    d.text((150,458),'Thank you',font=FONT['h2'],fill=GREEN)
    draw_multiline(d,'AICloudStrategist can show the demo first, understand the clinic process, and then suggest the smallest practical pilot. No patient medical records are needed for the demo.',(150,505),FONT['body'],WHITE,940,8)
    return im

def package_data():
    return {
 'starter': {
  'label':'Starter Package',
  'title':'Starter Clinic Follow-up Board',
  'subtitle':'For clinics that want to stop missed WhatsApp, call, and website enquiries without starting with heavy software.',
  'slides': [
   ('problem','Customer problem',['Clinic enquiries arrive on WhatsApp, calls, Google, Instagram, and website forms.','Staff may be busy, so callbacks and appointment confirmations can get delayed.','The owner has no simple daily view of what is pending, booked, or missed.']),
   ('requirement','What the clinic needs',['One simple place to see new enquiries, appointment requests, callbacks, and closed items.','A practical staff handover board that can start small and improve follow-up discipline.','A daily owner summary without checking every staff phone manually.']),
   ('solution','Solution we build',[('New enquiries','Fresh WhatsApp, missed-call, and form requests appear as cards.',BLUE),('Appointment requests','Staff confirms timing, doctor availability, and next step.',(15,138,71)),('Staff follow-up','Callbacks and no-response reminders stay visible.',(194,65,12)),('Daily summary','Owner sees booked, pending, and missed follow-ups.',NAVY)]),
   ('board','Starter board','Every enquiry stays visible until it is handled. The clinic can start with sample data and then move to a live pilot.'),
   ('components','Components included',['Clinic enquiry board with simple status columns.','WhatsApp click-to-chat or enquiry form capture.','Basic reply templates for timing, location, and appointment confirmation.','Daily owner summary: new, pending, booked, and missed follow-ups.','Privacy-safe setup: no diagnosis, treatment advice, or patient records in demo.']),
   ('benefits','Customer benefits',['Warm leads do not disappear inside WhatsApp chat history.','Reception knows exactly what needs action today.','Owner gets visibility without micromanaging staff.','Patients receive faster replies for timing, location, and appointment requests.','Clinic can later upgrade to Growth or Advanced only if needed.'])
  ],
  'closing':'For Sparsh Clinic, the Starter demo is the safest first step: show the board, understand their real enquiry process, and suggest a small pilot only after the walkthrough.'
 },
 'growth': {
  'label':'Growth Package',
  'title':'Growth Clinic Automation Dashboard',
  'subtitle':'For clinics that already get regular enquiries and want reminders, source tracking, staff assignment, and owner insights.',
  'slides': [
   ('problem','Customer problem',['The clinic may receive leads from WhatsApp, calls, Instagram, Google, and website forms.','The owner does not know which channel brings useful enquiries.','Follow-ups depend on staff memory, so good enquiries can go cold.']),
   ('requirement','What the clinic needs',['A clearer view of enquiry source, service type, staff owner, and next action.','Reminder rules for callbacks, no-response cases, and appointment confirmations.','Daily and weekly owner insights to improve clinic operations.']),
   ('solution','Solution we build',[('Source tracking','Shows whether enquiry came from WhatsApp, call, Instagram, Google, or website.',BLUE),('Service routing','Hair, skin, acne, laser, or consultation enquiries go to the right queue.',(15,138,71)),('Reminders','Callback and no-response reminders keep staff moving.',(194,65,12)),('Owner insights','Simple reports show pending, booked, source split, and response time.',NAVY)]),
   ('board','Growth dashboard','The Growth view adds automation and insight on top of the Starter board, while still keeping the process easy for clinic staff.'),
   ('components','Components included',['Starter board plus source tracking and service categories.','Staff assignment rules for reception, manager, or owner review.','Follow-up reminders for callbacks and no-response leads.','Website or form connection where needed.','Owner dashboard with daily and weekly improvement summary.']),
   ('benefits','Customer benefits',['Clinic understands where enquiries are coming from.','Staff receives a clear priority list instead of scattered messages.','Owner can identify response delays and missed opportunities.','Follow-up consistency improves without replacing existing clinic software.','Creates a base for later official WhatsApp API automation.'])
  ],
  'closing':'Growth is useful after the clinic likes the Starter board and wants better reporting, reminders, and staff accountability.'
 },
 'advanced': {
  'label':'Advanced Package',
  'title':'Advanced WhatsApp API Workflow',
  'subtitle':'For clinics that need scale, official WhatsApp templates, integrations, staff roles, audit trail, and deeper automation.',
  'slides': [
   ('problem','Customer problem',['Manual WhatsApp becomes difficult when enquiry volume increases.','The clinic may need official appointment reminders, follow-up templates, and multi-staff access.','The owner needs better reporting, audit trail, and integrations with forms, calls, or CRM.']),
   ('requirement','What the clinic needs',['Official WhatsApp Business API workflow for approved templates and scalable messaging.','Role-based staff access, opt-out handling, and clear audit trail.','Integration with website forms, call events, sheets, CRM, or appointment systems.']),
   ('solution','Solution we build',[('WhatsApp API','Official template-based customer communication where required.',BLUE),('Workflow engine','Enquiries move through rules, reminders, escalation, and status updates.',(15,138,71)),('Integrations','Website, forms, calls, sheets, CRM, or appointment tools can connect.',(194,65,12)),('Audit reports','Owner sees delivery status, pending work, staff action, and outcomes.',NAVY)]),
   ('board','Advanced workflow view','The Advanced view is for scale. It connects WhatsApp API, webhooks, staff workflow, owner dashboard, and audit reporting.'),
   ('components','Components included',['Growth dashboard plus official WhatsApp API setup support.','Message template design for appointment, reminder, follow-up, and review request.','Webhook-based intake from website forms, calls, and other sources.','Multi-staff roles, escalation rules, opt-out handling, and audit logs.','Advanced reporting for response time, source quality, and unresolved queue.']),
   ('benefits','Customer benefits',['Clinic can handle higher enquiry volume with more control.','Official templates make repeated reminders and confirmations cleaner.','Owner gets stronger visibility, compliance hygiene, and reporting.','Less dependency on one staff phone or one WhatsApp chat.','Foundation for future appointment, CRM, and call automation integration.'])
  ],
  'closing':'Advanced should be proposed only when volume and process maturity justify it. For Sparsh, we should first show the demo, then recommend the smallest practical step.'
 }
}

def make_slides(pkg_key, data):
    ddir=ROOT/pkg_key; ddir.mkdir(exist_ok=True)
    images=[]; scripts=[]
    welcome=f"Welcome to this AICloudStrategist demo. In this video, we will explain the {data['title']} in simple business language: the clinic problem, the solution we build, the components included, and the benefits for the customer."
    im=title_slide(data['label'],data['title'],data['subtitle']); p=ddir/'slide_01.png'; im.save(p); images.append(p); scripts.append(welcome)
    idx=2
    for typ,title,*rest in data['slides']:
        if typ in ('problem','requirement','components','benefits'):
            bullets=rest[0]
            im=section_slide(data['label'], typ.upper(), title, bullets)
            script= title + '. ' + ' '.join(bullets)
        elif typ=='solution':
            cols=rest[0]
            im=columns_slide(data['label'], 'SOLUTION', title, cols)
            script= title + '. ' + ' '.join([h + ': ' + b for h,b,c in cols])
        elif typ=='board':
            subtitle=rest[0]
            im=board_slide(data['label'], title, subtitle, advanced=(pkg_key=='advanced'))
            script= title + '. ' + subtitle
        p=ddir/f'slide_{idx:02d}.png'; im.save(p); images.append(p); scripts.append(script); idx+=1
    closing_text=f"Thank you for watching. {data['closing']} For the next step, AICloudStrategist can show the demo, understand the clinic's current enquiry flow, and prepare a practical pilot plan. You can reach us at aicloudstrategist.com, WhatsApp +91 87963 02608, voice line +91 80654 80898, or contact@aicloudstrategist.com."
    im=closing_slide(data['label'],'Thank you and next step',data['closing']); p=ddir/f'slide_{idx:02d}.png'; im.save(p); images.append(p); scripts.append(closing_text)
    return ddir, images, scripts

def tts_segments(ddir, scripts):
    audios=[]; durs=[]
    for i,txt in enumerate(scripts,1):
        txtfile=ddir/f'script_{i:02d}.txt'; txtfile.write_text(txt)
        mp3=ddir/f'audio_{i:02d}.mp3'
        run([EDGE,'--voice','en-IN-NeerjaExpressiveNeural','--rate','+2%','--file',str(txtfile),'--write-media',str(mp3)], stdout=subprocess.DEVNULL)
        dur=float(subprocess.check_output([FP,'-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(mp3)], env=ENV).decode().strip())
        audios.append(mp3); durs.append(dur+0.7)  # hold slide just after speech ends
    return audios,durs

def render_video(pkg_key, ddir, images, audios, durs):
    concat=ddir/'slides.txt'
    lines=[]
    for img,dur in zip(images,durs):
        lines += [f"file '{img.name}'\n", f"duration {dur:.3f}\n"]
    lines.append(f"file '{images[-1].name}'\n")
    concat.write_text(''.join(lines))
    audio_list=ddir/'audio.txt'
    audio_list.write_text(''.join([f"file '{a.name}'\n" for a in audios]))
    joined=ddir/'voice_joined.mp3'
    run([FF,'-y','-f','concat','-safe','0','-i',str(audio_list.name),'-c','copy',str(joined.name)], cwd=ddir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out=ddir/f'aics-{pkg_key}-clinic-demo-v4.mp4'
    run([FF,'-y','-f','concat','-safe','0','-i',str(concat.name),'-i',str(joined.name),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','medium','-crf','20','-c:a','aac','-b:a','160k','-shortest',str(out.name)], cwd=ddir)
    return out

manifest={}
for key,data in package_data().items():
    ddir, imgs, scripts = make_slides(key,data)
    audios,durs=tts_segments(ddir,scripts)
    out=render_video(key,ddir,imgs,audios,durs)
    manifest[key]={'video':str(out),'slides':len(imgs),'duration_sum':sum(durs)}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
