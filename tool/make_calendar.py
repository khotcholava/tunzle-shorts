import csv, datetime as dt, sys, collections
sys.path.insert(0,'.')
from melodies import M
TIMES=["16:00","18:00","21:00","00:00","03:00"]; LEVELS=["Easy","Easy","Medium","Medium","Hard"]
THEME={0:("Classical Hits",["classical"]),1:("Folk Songs Around the World",["folk"]),2:("Movie & Cartoon Classics",["movie","classical"]),
       3:("Opera & Ballet",["opera","classical"]),4:("Kids Songs",["kids"]),5:("Party & Celebration",["party","folk","kids"]),
       6:("HARD MODE Sunday",["classical","movie","opera","folk","kids","party"])}
last_used={}; uses={}
for k,d in [("nokia",3),("tetris",3),("fur_elise",3),("ode_to_joy",3),("mountain_king",3),("william_tell",4),("can_can",4),("zarathustra",4),("funeral_march",4),("valkyries",4)]:
    last_used[k]=d; uses[k]=1
def pick(cats, day, level=None, hard_fmt=False, mix=False):
    cands=[k for k,m in M.items() if m["cat"] in cats and not (m.get("only_hard") and not hard_fmt)]
    def score(k):
        gap=day-last_used.get(k,-99)
        ci=0 if mix else cats.index(M[k]["cat"])
        return (gap<7, uses.get(k,0), bool(M[k].get("check")), ci, 0 if (level is None or M[k]["level"]==level) else 1, -gap)
    k=min(cands,key=score); last_used[k]=day; uses[k]=uses.get(k,0)+1; return k
rows=[]
for day in range(5,31):
    d=dt.date(2026,11,day); theme,cats=THEME[d.weekday()]
    nx= 0 if day<20 else (2 if day<27 else 3)
    for s in range(5):
        lvl=LEVELS[s]; fmt="normal"; th=theme
        if s>=5-nx:
            k=pick(["xmas"],day); th="Christmas Countdown"; lvl=M[k]["level"] if s<4 else "Hard"
            if s==4 and M[k]["level"]!="Hard": fmt="three_notes"
        elif d.weekday()==6:
            fmt=["three_notes","backwards","double_speed","three_notes","backwards"][s]; lvl="Hard"
            k=pick(cats,day,hard_fmt=fmt=="three_notes",mix=True)
        else:
            k=pick(cats,day,lvl)
            if s==4 and M[k]["level"]!="Hard": fmt="three_notes"
        pd=d if s<3 else d+dt.timedelta(days=1)
        rows.append(dict(batch_date=d.isoformat(),slot=s+1,post_date=pd.isoformat(),time=TIMES[s],theme=th,format=fmt,melody=k,level=lvl))
with open('calendar.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), collections.Counter(r['melody'] for r in rows).most_common(4))
for r in rows:
    if r['batch_date'] in ('2026-11-05','2026-11-08','2026-11-27'): print(r['batch_date'],r['time'],r['theme'],r['format'],r['melody'],r['level'])
