from pathlib import Path
import re,html,textwrap,json
from PIL import Image,ImageDraw,ImageFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,Image as RLImage,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
R=Path(__file__).resolve().parents[1]
D=R/'report';D.mkdir(exist_ok=True)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
f=ImageFont.truetype(FONT,36); fb=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',38)
def diagram(file,title,nodes,edges,foot):
 height=1800 if file=='task06-uml.png' else 1350
 im=Image.new('RGB',(1440,height),'white');dr=ImageDraw.Draw(im)
 dr.text((40,25),title,font=fb,fill='#173458')
 for a,b,kind,label in edges:
  x1,y1,w1,h1,_=nodes[a];x2,y2,w2,h2,_=nodes[b]
  # Child points upwards to parent; composition uses side connector.
  if kind=='inherit':
   sx,sy=x1+w1/2,y1;tx,ty=x2+w2/2,y2+h2
   mid=(sy+ty)/2
   dr.line([(sx,sy),(sx,mid),(tx,mid),(tx,ty+26)],fill='#355b83',width=5)
   dr.polygon([(tx,ty),(tx-14,ty+26),(tx+14,ty+26)],outline='#355b83',fill='white',width=4)
   if label:dr.text((sx+10,mid+4),label,font=f,fill='#355b83')
  else:
   sx,sy=x1+w1,y1+h1/2;tx,ty=x2,y2+h2/2
   dr.line([(sx,sy),(tx,ty)],fill='#355b83',width=5)
   dr.polygon([(sx,sy),(sx+16,sy-12),(sx+32,sy),(sx+16,sy+12)],fill='#355b83')
 for x,y,w,h,lines in nodes.values():
  dr.rounded_rectangle((x,y,x+w,y+h),radius=12,fill='#f0f4fa',outline='#355b83',width=4)
  dr.line((x,y+63,x+w,y+63),fill='#355b83',width=3)
  for i,line in enumerate(lines): dr.text((x+18,y+12+i*48),line,font=fb if i==0 else f,fill='#142b47')
 for i,line in enumerate(foot):dr.text((40,height-160+i*47),line,font=f,fill='#27425f')
 im.save(D/file)
diagram('task01-uml.png','Task 1 | Payroll hierarchy',{
 'base':(400,115,640,220,['<<abstract>> Staff','- name; id','+ pay() const = 0','+ virtual destructor']),
 'salary':(80,460,650,220,['<<abstract>> SalariedStaff','- basic; # DA_RATE','# salaryWithDA()','+ constructor']),
 'guest':(820,460,540,220,['GuestFaculty','- hours; rate','+ pay() override']),
 'prof':(40,880,600,220,['Professor','- research','+ pay() override']),
 'lab':(740,880,650,220,['LabAssistant','+ pay() override'])},
 [('salary','base','inherit','public'),('guest','base','inherit','public'),('prof','salary','inherit','public'),('lab','salary','inherit','public')],
 ['Hollow triangles point to the base class.','+ public   # protected   - private'])
diagram('task02-uml.png','Tasks 2 and 3 | Shared identity and members',{
 'person':(60,110,660,270,['Person','- name; id; phone','- Address address','+ identity accessors','+ virtual destructor']),
 'address':(900,130,490,180,['Address','- city','+ constructor']),
 'student':(40,550,650,260,['Student','- programme; cgpa','- Course course','+ constructor']),
 'staff':(800,550,590,210,['Staff','- department; salary','+ constructor']),
 'ta':(650,960,740,180,['TeachingAssistant','+ constructor; destructor']),
 'rs':(40,960,540,180,['ResearchScholar','- fellowship'])},
 [('student','person','inherit','virtual public'),('staff','person','inherit','virtual public'),('ta','student','inherit','public'),('ta','staff','inherit','public'),('rs','student','inherit','public'),('person','address','composition','')],
 ['Filled diamond: composition. Student also owns a Course.','One Person subobject is shared by the TA roles.'])
diagram('task06-uml.png','Task 6 | Extensible rental fleet',{
 'v':(300,90,840,180,['<<abstract>> Vehicle','+ charge() = 0; kind() = 0','+ rent(); returnVehicle(); virtual destructor']),
 'b':(40,440,480,155,['Bicycle','+ charge() override']),
 'm':(680,440,710,180,['<<abstract>> MotorVehicle','- level; ServiceRecord service']),
 't':(40,760,550,155,['TwoWheeler','- perLitre']),
 'c':(800,760,590,155,['Car','- seats; perLitre']),
 'e':(650,1050,740,155,['ElectricCar','- batteryKWh; perKWh']),
 'bus':(650,1370,740,155,['ElectricBus','+ charge() override'])},
 [('b','v','inherit',''),('m','v','inherit',''),('t','m','inherit',''),('c','m','inherit',''),('e','c','inherit',''),('bus','e','inherit','')],
 ['All inheritance is public. Triangle points to base.','ElectricBus adds a daily fee; generic fleet loops stay unchanged.'])
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body11',fontName='Helvetica',fontSize=11,leading=15,spaceAfter=8))
styles.add(ParagraphStyle(name='Code11',fontName='Courier',fontSize=11,leading=14,spaceAfter=10))
styles.add(ParagraphStyle(name='Title28',fontName='Helvetica-Bold',fontSize=28,leading=34,spaceAfter=20))
styles.add(ParagraphStyle(name='Sub16',fontName='Helvetica-Bold',fontSize=16,leading=21,spaceAfter=12,spaceBefore=14))
styles.add(ParagraphStyle(name='Head13',fontName='Helvetica-Bold',fontSize=13,leading=18,spaceBefore=12,spaceAfter=8))
styles.add(ParagraphStyle(name='Cell11',fontName='Helvetica',fontSize=11,leading=14))
S=[]
def p(t,style='Body11'):
 # Markdown inline markers; escaped source is still readable in PDF.
 t=html.escape(t);t=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',t)
 S.append(Paragraph(t,styles[style]))
def code(t):
 lines=[]
 for l in t.splitlines():lines+=textwrap.wrap(l,width=70,replace_whitespace=False,drop_whitespace=False) or ['']
 S.append(KeepTogether([Preformatted('\n'.join(lines),styles['Code11'])]))
def table(rows):
 cols=len(rows[0]); widths=[480/cols]*cols
 data=[[Paragraph(html.escape(c.strip()),styles['Cell11']) for c in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf7')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#a4b3c8')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 S.append(t);S.append(Spacer(1,12))
def md(text):
 ls=text.splitlines();i=0
 while i<len(ls):
  l=ls[i].strip()
  if not l:i+=1;continue
  if l.startswith('```'):
   chunk=[];i+=1
   while i<len(ls) and not ls[i].startswith('```'):chunk.append(ls[i]);i+=1
   code('\n'.join(chunk));i+=1;continue
  if l.startswith('|'):
   rows=[]
   while i<len(ls) and ls[i].strip().startswith('|'):
    row=ls[i].strip().strip('|').split('|')
    if not all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in row):rows.append(row)
    i+=1
   table(rows);continue
  if l.startswith('#'):
   level=len(l)-len(l.lstrip('#'));p(l.lstrip('# '),'Sub16' if level==1 else 'Head13');i+=1;continue
  chunk=[l];i+=1
  while i<len(ls) and ls[i].strip() and not ls[i].lstrip().startswith(('#','|','```')):chunk.append(ls[i].strip());i+=1
  p(' '.join(chunk))
def image(name):S.append(RLImage(str(D/name),width=480,height=(600 if name=='task06-uml.png' else 450)));S.append(Spacer(1,14))
p('ASSIGNMENT 4 - CO4','Title28');p('Designing Reusable Class Hierarchies','Sub16');S.append(Spacer(1,35));p('S Vinoth Kumar','Sub16');p('Register number: 192471006');p('Object Oriented Programming with C++ (DSA01)');p('Course outcome CO4: inheritance, composition, constructors, pointers and polymorphism.');S.append(Spacer(1,30));p('GitHub repository','Head13');p('https://github.com/vinoththecool7-netizen/DSA01-192471006-Assignment4');p('Six tasks | Executed C++17 programs | Design and analysis report');S.append(PageBreak())
p('Execution method and evidence','Sub16')
p('Compiler: Apple Clang 21.0.0 (clang-2100.4.1.1), arm64 Apple Darwin, invoked as g++. This is the installed Apple compiler alias, not GNU GCC. Every program uses -std=c++17 -Wall -Wextra; sanitizer variants additionally use -fsanitize=address -g. Exact relative commands, source SHA-256 digests, process statuses and consumed inputs are recorded alongside each output.')
p('The required predictions were saved before the first execution in this workflow. prediction_record.json records the actual sequence and hashes; it does not assert prior personal student activity. All supplied prediction outputs and the two completed TODO-program outputs matched byte for byte, including significant trailing spaces and final newlines.')
p('Embedded data is identified for Tasks 1-5; Task 6 reads Task06/input.txt. Output screenshots are genuine browser captures of the archived execution-record viewer, labelled as such. They are not imitation terminal images. Text logs remain the authoritative complete evidence. The only expected ordinary compiler warning is the deliberately reordered initializer-list fixture; the ambiguous-member fixture is an expected compile failure.')
p('ASan limitations','Head13');p('The Mac supports AddressSanitizer but rejects detect_leaks=1. The broken account program exits 0 under the ordinary ASan run, while the explicit leak-support probe terminates with an unsupported-platform message. The report does not interpret that zero exit as evidence of leak freedom. The repaired programs and ownership tests finish with empty ASan stderr.')
table([['Task','Main result'],['1','Payroll: 76000, 28400, 16000'],['2','One virtual Person; two nonvirtual Persons'],['3','Constructor/destructor order and initializer warning verified'],['4','3.5/3.5 defect; 3.5/4.0 repair; slicing confirmed'],['5','Required total 324.00; pointer search and bounds checked'],['6','All five return bills and five errors checked']])
for n in range(1,7):
 S.append(PageBreak())
 md((R/f'Task{n:02}/analysis.md').read_text())
 if n in (1,2,6):
  S.append(PageBreak());p('UML class diagram','Sub16');image(f'task{n:02}-uml.png')
  p('The diagram summarizes the executable declarations. The corresponding .cpp files contain complete class definitions, constructors, access specifiers and method bodies.')
 S.append(Spacer(1,10));p('Selected observed output','Head13')
 files={1:['payroll'],2:['predict_virtual','predict_nonvirtual'],3:['complete','predict','hierarchy','hierarchy_nonvirtual'],4:['predict','broken_asan','repaired_asan'],5:['complete','cart_demo'],6:['fleet','tagged']}[n]
 for stem in files:
  p('Task%02d/evidence/%s.stdout.txt'%(n,stem))
  text=(R/f'Task{n:02}/evidence/{stem}.stdout.txt').read_text();code(text.rstrip('\n'))
S.append(PageBreak());p('Implementation index and verification discussion','Sub16')
table([['Task','Source files'],['1','Task01/payroll.cpp'],['2','Task02/relationships.cpp; predict_virtual.cpp; predict_nonvirtual.cpp; diagnostics/ambiguous.cpp.txt'],['3','Task03/hierarchy.cpp; complete.cpp; predict.cpp; address_pointer.cpp; diagnostics/reordered.cpp.txt'],['4','Task04/broken.cpp; repaired.cpp; predict.cpp'],['5','Task05/complete.cpp; cart_demo.cpp'],['6','Task06/fleet.cpp; tagged.cpp; input.txt']])
p('The supplied TODO skeletons preserve their surrounding behavior. Only intended line breaks lost in the pasted comment formatting were restored. Expanded tests are separate executables. The deliberate unsafe and diagnostic programs are isolated in the runner and are not examples of valid production ownership.')
p('For viva preparation: explain why TA initializes Person directly; trace Address and Course lifetimes; distinguish static binding from dynamic dispatch; explain why a unique_ptr still needs a virtual base destructor; trace reference-return chaining; and add one new vehicle subclass by implementing the charge and kind contract.')
p('Complexity assumes a fixed set of types and fixed-size numeric data unless string length or item count is stated. sizeof measurements are specific to this ABI and exclude separately allocated string payloads, allocator metadata and collection capacity. No timing ranking is inferred solely from Big-O or object sizes.')
p('Specification basis: the supplied Assignment 4 - CO4 brief. All outputs and sizes quoted here come from the accompanying programs and logs. Pricing policies not given in the brief are explicitly identified as demonstration assumptions.')
def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#b9c5d5'));canvas.line(55,44,540,44)
 canvas.setFont('Helvetica',11);canvas.drawString(55,28,'S Vinoth Kumar | 192471006 | Assignment 4');canvas.drawRightString(540,28,str(doc.page))
out=D/'Assignment4_Report.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=55,leftMargin=55,topMargin=50,bottomMargin=62,title='Assignment 4 - Designing Reusable Class Hierarchies',author='S Vinoth Kumar').build(S,onFirstPage=footer,onLaterPages=footer)
# Markdown report is editable and uses the same maintained analysis sources.
mdout='# Assignment 4 - CO4\n\nS Vinoth Kumar | 192471006\n\nRepository: https://github.com/vinoththecool7-netizen/DSA01-192471006-Assignment4\n\n'
for n in range(1,7):mdout+='\n'+(R/f'Task{n:02}/analysis.md').read_text()+'\n'
(D/'Assignment4_Report.md').write_text(mdout)
print(out.name)
