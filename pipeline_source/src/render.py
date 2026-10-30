import cairosvg,os
from style import STYLE as S
W,H=1920,1080
def head(title,sub=""):
    return f'<rect width="{W}" height="{H}" fill="{S["bg"]}"/><text x="100" y="130" font-family="{S["font"]}" font-size="64" font-weight="bold" fill="{S["ink"]}">{title}</text><rect x="100" y="152" width="180" height="8" fill="{S["accent"]}"/><text x="100" y="215" font-family="{S["font"]}" font-size="34" fill="{S["muted"]}">{sub}</text>'
def t(x,y,s,size=34,fill=None,anchor="start",bold=False):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{S["font"]}" font-size="{size}" fill="{fill or S["ink"]}" {"font-weight=\"bold\"" if bold else ""}>{s}</text>'
def callout(x1,y1,x2,y2,label,anchor="start"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{S["muted"]}" stroke-width="3"/><circle cx="{x1}" cy="{y1}" r="7" fill="{S["accent"]}"/>'+t(x2+(14 if anchor=="start" else -14),y2+10,label,32,anchor=anchor)
def title_card(l):return head("Cell: The Unit of Life","Class 11 Biology · Chapter 8")+f'<circle cx="1300" cy="620" r="260" fill="{S["cyto"]}" stroke="{S["membrane"]}" stroke-width="14"/><circle cx="1260" cy="600" r="90" fill="{S["nucleus"]}"/>'+t(960,880,l[1],56,anchor="middle",fill=S["accent"],bold=True)
def timeline(l):
    o=head("Development of Cell Theory","Learner-paced timeline")+f'<line x1="200" y1="560" x2="1720" y2="560" stroke="{S["muted"]}" stroke-width="6"/>'
    for i,s in enumerate(l):
        x=360+i*600;yr,rest=s.split(" ",1)
        o+=f'<circle cx="{x}" cy="560" r="30" fill="{S["accent"]}"/>'+t(x,470,yr,64,anchor="middle",bold=True)+t(x,680,rest,36,anchor="middle")
    return o
def two_points(l):
    o=head("Cell Theory Today","Two statements")
    for i,s in enumerate(l):
        y=330+i*330;o+=f'<rect x="200" y="{y}" width="1520" height="250" rx="28" fill="{S["panel"]}" stroke="{S["accent"]}" stroke-width="4"/>'+t(260,y+150,s,64,bold=True)
    return o
def prok_vs_euk(l):
    o=head("Prokaryotic vs Eukaryotic","Look at the nucleus")
    o+=t(480,300,l[0],44,anchor="middle",bold=True)+t(1440,300,l[1],44,anchor="middle",bold=True)
    o+=f'<rect x="230" y="380" width="500" height="320" rx="160" fill="{S["cyto"]}" stroke="{S["membrane"]}" stroke-width="10"/><path d="M330 520 q40 -80 90 0 t90 0 t90 0" fill="none" stroke="{S["dna"]}" stroke-width="8"/>'
    for x,y in((300,450),(640,460),(620,620),(340,640)):o+=f'<circle cx="{x}" cy="{y}" r="12" fill="{S["ribo"]}"/>'
    o+=callout(420,520,330,800,l[3],"end")
    o+=f'<ellipse cx="1440" cy="540" rx="320" ry="220" fill="{S["cyto"]}" stroke="{S["membrane"]}" stroke-width="10"/><circle cx="1440" cy="540" r="95" fill="{S["nucleus"]}" stroke="{S["ink"]}" stroke-width="6"/>'
    for x,y in((1260,470),(1600,450),(1580,640),(1290,650)):o+=f'<circle cx="{x}" cy="{y}" r="12" fill="{S["ribo"]}"/>'
    o+=callout(1440,540,1620,830,l[2])+callout(1290,650,1000,860,l[5],"end")+callout(1500,420,1620,320,l[4])
    return o
def compare_table(l):
    o=head("Organelles: What is Shared?","Membrane bound vs ribosomes")
    rows=[("Feature","Prokaryotic","Eukaryotic"),(l[0],"Absent","Present"),(l[1],"Present","Present")]
    for i,r in enumerate(rows):
        y=330+i*210
        for j,c in enumerate(r):
            x=200+j*540;f=S["accent"] if i==0 else S["panel"];ink=S["bg"] if i==0 else S["ink"]
            o+=f'<rect x="{x}" y="{y}" width="520" height="180" rx="18" fill="{f}"/>'+t(x+260,y+108,c,36,fill=ink,anchor="middle",bold=(i==0))
    return o
def plant_vs_animal(l):
    o=head("Plant vs Animal Cell","Features unique to plant cells")
    o+=f'<rect x="640" y="360" width="600" height="520" rx="40" fill="{S["cyto"]}" stroke="{S["wall"]}" stroke-width="26"/><rect x="760" y="470" width="230" height="300" rx="50" fill="{S["vac"]}" opacity="0.7"/><ellipse cx="1100" cy="500" rx="70" ry="38" fill="{S["plast"]}"/><circle cx="1090" cy="720" r="55" fill="{S["nucleus"]}"/>'
    o+=t(940,330,"Plant cell",40,anchor="middle",bold=True)+callout(640,600,520,330,l[0],"end")+callout(1100,500,1290,330,l[1])+callout(860,620,520,620,l[2],"end")
    o+=f'<ellipse cx="1620" cy="640" rx="260" ry="230" fill="{S["cyto"]}" stroke="{S["membrane"]}" stroke-width="10"/><circle cx="1620" cy="640" r="85" fill="{S["nucleus"]}"/>'+t(1620,380,"Animal cell",40,anchor="middle",bold=True)
    return o
T={"title_card":title_card,"timeline":timeline,"two_points":two_points,"prok_vs_euk":prok_vs_euk,"compare_table":compare_table,"plant_vs_animal":plant_vs_animal}
def render(scene,out):
    v=scene["visual"];svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{T[v["template"]](v["labels"])}</svg>'
    open(out.replace(".png",".svg"),"w").write(svg);cairosvg.svg2png(bytestring=svg.encode(),write_to=out,output_width=W,output_height=H)
