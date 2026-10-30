from pathlib import Path
root = Path(__file__).resolve().parents[1]
# Produce reproducible descriptive charts from the local raw reference CSV.
# Standalone dependency-light EDA rebuilds CSV and SVG charts using pandas only.
import pandas as pd, csv, json
src=root/'data'/'dataset_original.csv'; out=root/'data'; charts=root/'analysis'
df=pd.read_csv(src)
for c in ['doc_id','doc_type','chunk_id','query_type']: df[c]=df[c].astype('string').str.strip()
for c in ['word_count','retrieval_score','answer_quality_score']: df[c]=pd.to_numeric(df[c],errors='coerce')
df=df.drop_duplicates().dropna().copy(); df['doc_type']=df.doc_type.str.title(); df['query_type']=df.query_type.str.lower(); df.word_count=df.word_count.astype(int); df.retrieval_score=df.retrieval_score.clip(0,1).round(4); df.answer_quality_score=df.answer_quality_score.clip(0,1).round(3); df.to_csv(out/'dataset.csv',index=False)
metrics={'rows':len(df),'columns':len(df.columns),'duplicates_removed':int(pd.read_csv(src).duplicated().sum()),'missing_cells':int(df.isna().sum().sum()),'mean_retrieval_score':round(float(df.retrieval_score.mean()),4),'mean_synthetic_quality_score':round(float(df.answer_quality_score.mean()),4),'quality_range':[round(float(df.answer_quality_score.min()),3),round(float(df.answer_quality_score.max()),3)],'query_type_counts':{str(k):int(v) for k,v in df.query_type.value_counts().sort_index().items()},'interpretation':'Synthetic descriptive metadata only; these are not generator accuracy metrics.'}
(charts/'eda_summary.json').write_text(json.dumps(metrics,indent=2),encoding='utf8')
colors=['#2459d3','#0f766e','#d97706','#7c3aed','#dc2626']
def svg(title,body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="520"><rect width="100%" height="100%" fill="white"/><text x="50" y="52" font-family="Arial" font-size="27" font-weight="bold" fill="#10233f">{title}</text><text x="50" y="82" font-family="Arial" font-size="15" fill="#52627a">Synthetic reference dataset • descriptive, not predictive</text>{body}</svg>'
bins=[0]*10
for x in df.retrieval_score: bins[min(9,int(float(x)*10))]+=1
m=max(bins); body=''
for i,n in enumerate(bins):
 x=100+i*72; h=300*n/m; y=410-h; body+=f'<rect x="{x}" y="{y:.1f}" width="48" height="{h:.1f}" rx="5" fill="{colors[0]}"/><text x="{x+24}" y="{y-9:.1f}" text-anchor="middle" font-family="Arial" font-size="13" fill="#334155">{n}</text><text x="{x+24}" y="435" text-anchor="middle" font-family="Arial" font-size="12" fill="#52627a">{i/10:.1f}</text>'
body+='<text x="460" y="475" text-anchor="middle" font-family="Arial" font-size="14">Retrieval score (bin starts)</text>'; (charts/'retrieval_score_distribution.svg').write_text(svg('Retrieval Score Distribution',body),encoding='utf8')
body=''; counts=df.query_type.value_counts().sort_values(ascending=True)
for i,(label,n) in enumerate(counts.items()):
 y=135+i*62; w=560*n/counts.max(); body+=f'<text x="70" y="{y+23}" font-family="Arial" font-size="16" fill="#334155">{label}</text><rect x="230" y="{y}" width="{w:.1f}" height="34" rx="5" fill="{colors[i%len(colors)]}"/><text x="{245+w:.1f}" y="{y+23}" font-family="Arial" font-size="15" fill="#334155">{n}</text>'
(charts/'query_type_counts.svg').write_text(svg('Query Type Counts',body),encoding='utf8')
body=''
for _,r in df.iterrows():
 x=100+float(r.word_count)/500*700; y=430-float(r.answer_quality_score)*330; body+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.7" fill="{colors[2]}" fill-opacity=".58"/>'
body+='<text x="450" y="475" text-anchor="middle" font-family="Arial" font-size="14">Chunk word count</text><text x="30" y="250" transform="rotate(-90 30,250)" text-anchor="middle" font-family="Arial" font-size="14">Synthetic quality score</text>'; (charts/'word_count_vs_quality.svg').write_text(svg('Word Count and Quality Score',body),encoding='utf8')
fields=[('doc_id','string','DOC002','DOC034','DOC013','No','Synthetic identifier for the source document represented by this chunk.'),('doc_type','category','TXT','TXT','HTML','No','Source format label; categories include TXT, HTML, Markdown, and Word.'),('chunk_id','string','CHK00001','CHK00002','CHK00003','No','Unique identifier for a text chunk in the synthetic retrieval dataset.'),('word_count','integer','457','302','52','No','Number of words associated with the source chunk; observed range 50–499.'),('retrieval_score','float','0.5962','0.7397','0.7735','No','Synthetic relevance score for retrieval, bounded from 0 to 1.'),('query_type','category','analytical','factual','comparative','No','Intent category: analytical, factual, comparative, procedural, or summarization.'),('answer_quality_score','float','0.942','0.976','0.660','No','Synthetic answer-quality score from 0 to 1; not a human-validated benchmark.')]
with open(out/'data_dictionary.csv','w',newline='',encoding='utf8') as f: w=csv.writer(f); w.writerow(['column_name','data_type','sample_value_1','sample_value_2','sample_value_3','nullable','description']); w.writerows(fields)
print(json.dumps(metrics,indent=2))
