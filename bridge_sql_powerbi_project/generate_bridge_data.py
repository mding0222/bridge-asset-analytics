import csv, random, sqlite3, os, math
from datetime import date, timedelta
random.seed(20260629)
out='/mnt/data/bridge_sql_powerbi_project'
os.makedirs(out, exist_ok=True)
provinces=[
 {'province_id':'SC','province_name':'Sichuan','region':'Southwest','terrain':'Mountainous / Basin','climate':'humid subtropical','notes':'More mountain valley crossings in western/southern areas'},
 {'province_id':'HB','province_name':'Hubei','region':'Central','terrain':'River plain / hills','climate':'humid subtropical','notes':'Yangtze/Han River corridor and urban expressway bridges'},
 {'province_id':'SN','province_name':'Shaanxi','region':'Northwest','terrain':'Loess plateau / Qinling mountains','climate':'temperate continental','notes':'Loess gullies and mountain expressways'}]
road_classes=['Expressway','Class I Highway','Class II Highway','Class III Highway']
bridge_types=['Prestressed concrete box girder','Simply supported T-beam','Continuous rigid-frame','Arch bridge','Steel-concrete composite girder','Cable-stayed bridge','Small slab bridge']
material_map={'Prestressed concrete box girder':'PSC','Simply supported T-beam':'RC/PSC','Continuous rigid-frame':'PSC','Arch bridge':'RC/Masonry','Steel-concrete composite girder':'Steel-Concrete','Cable-stayed bridge':'Steel/PSC','Small slab bridge':'RC'}
defect_types=[
 ('Crack','Superstructure','Longitudinal/transverse cracking in girder or slab'),
 ('Spalling','Superstructure','Concrete cover spalling / exposed aggregate'),
 ('Rebar corrosion','Superstructure','Exposed or corroded reinforcement'),
 ('Bearing damage','Bearing','Aging rubber bearing, displacement or shear deformation'),
 ('Expansion joint damage','Deck system','Broken seal, leakage or joint blockage'),
 ('Deck pavement rutting','Deck system','Pavement rutting, pothole, delamination'),
 ('Drainage blockage','Deck system','Blocked scupper, water ponding'),
 ('Abutment settlement','Substructure','Approach settlement or differential movement'),
 ('Pier crack','Substructure','Vertical/inclined cracking at pier or cap beam'),
 ('Scour / erosion','Foundation','Riverbed scour or slope erosion'),
 ('Railing damage','Ancillary','Damaged barrier or guardrail'),
 ('Water leakage / efflorescence','Superstructure','Seepage marks and efflorescence')]
condition_desc={1:'Excellent / new or near-new',2:'Good with minor defects',3:'Fair, moderate defects but serviceable',4:'Poor, major defects affecting function or capacity',5:'Dangerous / urgent restriction or closure'}
# roads
roads=[]
for p in provinces:
 for i in range(1,13):
  cls=random.choices(road_classes,[.35,.25,.28,.12])[0]
  roads.append({'road_id':f"{p['province_id']}-R{i:02d}",'province_id':p['province_id'],'road_name':f"{p['province_id']} {random.choice(['G','S','X'])}{random.randint(10,99)}{random.choice([' Expressway',' Highway',' Ring Road',' Connecting Road'])}",'road_class':cls,'AADT':random.randint(35000,85000) if cls=='Expressway' else random.randint(12000,45000) if cls=='Class I Highway' else random.randint(3000,18000),'heavy_vehicle_pct':round(random.uniform(8,30),1)})
bridges=[]; inspections=[]; defects=[]; maint=[]
for idx in range(1,361):
 p=random.choice(provinces); pr=p['province_id']
 road=random.choice([r for r in roads if r['province_id']==pr])
 btype=random.choices(bridge_types,[.25,.24,.14,.10,.10,.04,.13])[0]
 length=round(random.lognormvariate(math.log(85),0.8),1)
 if btype=='Cable-stayed bridge': length=round(random.uniform(450,1350),1)
 elif btype=='Continuous rigid-frame': length=round(random.uniform(160,760),1)
 elif btype=='Arch bridge': length=round(random.uniform(60,420),1)
 elif 'Small' in btype: length=round(random.uniform(8,60),1)
 spans=max(1,int(length/random.choice([16,20,25,30,40,50,60])))
 width=round(random.choice([8.5,10.5,12,16,24,32]) + random.uniform(-.4,.4),1)
 year=random.randint(1988,2022)
 age=2026-year
 # condition probability depends age, traffic, terrain
 risk=age/35 + road['heavy_vehicle_pct']/45 + (0.25 if p['terrain'].startswith('Mountain') else 0) + (0.15 if length>300 else 0)
 if risk<0.9: cond=random.choices([1,2,3],[.25,.6,.15])[0]
 elif risk<1.35: cond=random.choices([1,2,3,4],[.08,.45,.38,.09])[0]
 elif risk<1.8: cond=random.choices([2,3,4,5],[.25,.5,.22,.03])[0]
 else: cond=random.choices([2,3,4,5],[.12,.45,.35,.08])[0]
 bcid={1:random.uniform(91,99),2:random.uniform(76,90),3:random.uniform(61,75),4:random.uniform(42,60),5:random.uniform(15,40)}[cond]
 bridge_id=f"BR{idx:04d}"
 bridges.append({'bridge_id':bridge_id,'bridge_name':f"{random.choice(['Longhe','Qingxi','Dongshan','Hanjiang','Jialing','Weihe','Nanhu','Qinling','Minjiang'])} Bridge {idx:03d}",'province_id':pr,'road_id':road['road_id'],'route_code':road['road_name'].split()[1],'road_class':road['road_class'],'bridge_type':btype,'main_material':material_map[btype],'length_m':length,'width_m':width,'span_count':spans,'completion_year':year,'age_years':age,'design_load':'Highway-I' if road['road_class'] in ['Expressway','Class I Highway'] else 'Highway-II','management_unit':random.choice(['Provincial Highway Centre','Municipal Transport Bureau','Expressway Maintenance Co.','County Road Office']),'latitude':round({'SC':30.6,'HB':30.5,'SN':34.3}[pr]+random.uniform(-2.5,2.5),6),'longitude':round({'SC':104.1,'HB':112.3,'SN':108.9}[pr]+random.uniform(-2.8,2.8),6),'latest_condition_class':cond,'latest_BCI':round(bcid,1),'risk_level': 'High' if cond>=4 or bcid<60 else 'Medium' if cond==3 or bcid<75 else 'Low'})
 # inspections 2-4 per bridge
 start_year=max(year+1,2021)
 n=random.randint(2,4)
 years=sorted(random.sample(range(start_year,2027), min(n, max(1,2027-start_year))))
 prev=min(2,cond+random.choice([0,1]))
 for y in years:
  if y==years[-1]: c=cond; score=bcid
  else:
   c=max(1,min(5,cond-random.choice([0,0,1])))
   score={1:random.uniform(91,99),2:random.uniform(76,90),3:random.uniform(61,75),4:random.uniform(42,60),5:random.uniform(15,40)}[c]
  ins_id=f"INSP-{bridge_id}-{y}"
  insp_date=date(y, random.randint(3,11), random.randint(1,25)).isoformat()
  inspections.append({'inspection_id':ins_id,'bridge_id':bridge_id,'inspection_date':insp_date,'inspection_type':random.choices(['Regular inspection','Frequent inspection','Special inspection'],[.7,.2,.1])[0],'condition_class':c,'BCI_score':round(score,1),'deck_score':round(max(20,min(100,score+random.uniform(-12,8))),1),'superstructure_score':round(max(20,min(100,score+random.uniform(-10,10))),1),'substructure_score':round(max(20,min(100,score+random.uniform(-9,12))),1),'inspector_team':random.choice(['Team A','Team B','Team C','External consultant']),'recommended_action': 'Routine maintenance' if c<=2 else 'Repair planning' if c==3 else 'Major repair / load assessment' if c==4 else 'Traffic restriction / emergency action'})
 # defects latest mostly
 defect_count=random.choices([0,1,2,3,4,5],[.12,.25,.28,.2,.1,.05])[0] if cond<=2 else random.choices([1,2,3,4,5,6],[.08,.18,.28,.25,.14,.07])[0]
 for d in range(defect_count):
  dt=random.choice(defect_types)
  severity=random.choices(['Minor','Moderate','Severe','Critical'], [0.55,0.32,0.10,0.03] if cond<=3 else [0.2,0.45,0.28,0.07])[0]
  defects.append({'defect_id':f"DEF-{bridge_id}-{d+1}",'bridge_id':bridge_id,'inspection_id':f"INSP-{bridge_id}-{years[-1]}",'defect_type':dt[0],'component':dt[1],'severity':severity,'description':dt[2],'quantity':round(random.uniform(0.5,60),1),'unit':random.choice(['m','m2','point','location']),'estimated_repair_cost_cny':round(random.uniform(5000,200000)*(1 if severity=='Minor' else 2 if severity=='Moderate' else 4 if severity=='Severe' else 8),0),'requires_special_inspection': severity in ['Severe','Critical']})
 if cond>=3 or random.random()<.3:
  priority='Urgent' if cond>=5 else 'High' if cond==4 else 'Medium' if cond==3 else 'Low'
  maint.append({'maintenance_id':f"MT-{bridge_id}",'bridge_id':bridge_id,'planned_year':random.choice([2026,2027,2028]),'maintenance_type':random.choice(['Crack sealing','Bearing replacement','Expansion joint replacement','Deck resurfacing','Drainage cleaning','Concrete patch repair','Load rating / special inspection','Scour protection']),'priority':priority,'estimated_budget_cny':round(random.uniform(30000,1200000)*(1.8 if cond>=4 else 1),0),'status':random.choice(['Planned','In design','Approved','Completed'] if priority!='Urgent' else ['Planned','Approved'])})

def write_csv(name, rows):
 with open(os.path.join(out,name),'w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
  w.writeheader(); w.writerows(rows)
for name,rows in [('dim_province.csv',provinces),('dim_road.csv',roads),('dim_bridge.csv',bridges),('fact_inspection.csv',inspections),('fact_defect.csv',defects),('fact_maintenance.csv',maint)]: write_csv(name,rows)
# data dictionary
with open(os.path.join(out,'data_dictionary.csv'),'w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f); w.writerow(['table','field','description'])
 for t, rows in [('dim_province',provinces),('dim_road',roads),('dim_bridge',bridges),('fact_inspection',inspections),('fact_defect',defects),('fact_maintenance',maint)]:
  for k in rows[0].keys(): w.writerow([t,k,'Synthetic bridge asset database field for SQL/Power BI portfolio project'])
# sqlite
conn=sqlite3.connect(os.path.join(out,'china_bridge_asset_demo.sqlite'))
for table, rows in [('dim_province',provinces),('dim_road',roads),('dim_bridge',bridges),('fact_inspection',inspections),('fact_defect',defects),('fact_maintenance',maint)]:
 cols=list(rows[0].keys())
 conn.execute(f"DROP TABLE IF EXISTS {table}")
 conn.execute(f"CREATE TABLE {table} ({', '.join([c+' TEXT' for c in cols])})")
 conn.executemany(f"INSERT INTO {table} VALUES ({','.join(['?']*len(cols))})", [[str(r[c]) for c in cols] for r in rows])
conn.commit(); conn.close()
# sql schema + sample queries
schema='''-- China Bridge Asset Demo Database (synthetic data)
-- Use this with SQLite / DB Browser for SQLite. All records are simulated for portfolio practice.

.mode csv
.import dim_province.csv dim_province
.import dim_road.csv dim_road
.import dim_bridge.csv dim_bridge
.import fact_inspection.csv fact_inspection
.import fact_defect.csv fact_defect
.import fact_maintenance.csv fact_maintenance

-- 1. Bridge count and average BCI by province
SELECT p.province_name, COUNT(*) AS bridge_count, ROUND(AVG(CAST(b.latest_BCI AS REAL)),1) AS avg_bci,
       SUM(CASE WHEN CAST(b.latest_condition_class AS INTEGER) >= 4 THEN 1 ELSE 0 END) AS class_4_5_count
FROM dim_bridge b
JOIN dim_province p ON b.province_id = p.province_id
GROUP BY p.province_name
ORDER BY class_4_5_count DESC;

-- 2. Top 10 high-risk bridges by estimated defect cost
SELECT b.bridge_id, b.bridge_name, p.province_name, b.road_class, b.bridge_type,
       b.latest_condition_class, b.latest_BCI,
       ROUND(SUM(CAST(d.estimated_repair_cost_cny AS REAL)),0) AS total_defect_cost_cny
FROM dim_bridge b
JOIN dim_province p ON b.province_id = p.province_id
LEFT JOIN fact_defect d ON b.bridge_id = d.bridge_id
GROUP BY b.bridge_id, b.bridge_name, p.province_name, b.road_class, b.bridge_type, b.latest_condition_class, b.latest_BCI
ORDER BY total_defect_cost_cny DESC
LIMIT 10;

-- 3. Defect distribution by component and severity
SELECT component, severity, COUNT(*) AS defect_count,
       ROUND(SUM(CAST(estimated_repair_cost_cny AS REAL)),0) AS estimated_cost_cny
FROM fact_defect
GROUP BY component, severity
ORDER BY estimated_cost_cny DESC;

-- 4. Maintenance budget by planned year and priority
SELECT planned_year, priority, COUNT(*) AS work_items,
       ROUND(SUM(CAST(estimated_budget_cny AS REAL)),0) AS budget_cny
FROM fact_maintenance
GROUP BY planned_year, priority
ORDER BY planned_year, budget_cny DESC;

-- 5. Bridges needing special inspection
SELECT b.bridge_id, b.bridge_name, p.province_name, b.latest_condition_class, b.latest_BCI,
       COUNT(d.defect_id) AS severe_or_critical_defects
FROM dim_bridge b
JOIN dim_province p ON b.province_id=p.province_id
JOIN fact_defect d ON b.bridge_id=d.bridge_id
WHERE d.requires_special_inspection='True'
GROUP BY b.bridge_id, b.bridge_name, p.province_name, b.latest_condition_class, b.latest_BCI
ORDER BY severe_or_critical_defects DESC, CAST(b.latest_BCI AS REAL) ASC;
'''
with open(os.path.join(out,'schema_and_sample_queries.sql'),'w',encoding='utf-8') as f: f.write(schema)
print(len(bridges),len(inspections),len(defects),len(maint))
