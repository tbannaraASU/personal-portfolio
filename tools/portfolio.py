#!/usr/bin/env python3
"""Portfolio CMS: local SQLite -> static JSON/JS for GitHub Pages.

Existing photography/gallery tables are untouched.  No external services.
"""
from __future__ import annotations
import json
import re
import sqlite3
import sys
from pathlib import Path
from uuid import uuid4

ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/'local'/'gallery.sqlite'
SEED=ROOT/'tools'/'portfolio-seed.json'
KINDS={'hero','about','skills','projects','experience','photography','contact','custom','footer'}
SCHEMA='''
CREATE TABLE IF NOT EXISTS portfolio_sections (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL,
 eyebrow TEXT NOT NULL DEFAULT '', description TEXT NOT NULL DEFAULT '',
 enabled INTEGER NOT NULL DEFAULT 1, position INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS portfolio_items (
 id TEXT PRIMARY KEY, section_id TEXT NOT NULL REFERENCES portfolio_sections(id) ON DELETE CASCADE,
 content TEXT NOT NULL, enabled INTEGER NOT NULL DEFAULT 1, position INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_portfolio_items_section ON portfolio_items(section_id,position);
'''

def connect():
    DB.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(DB,timeout=10)
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript(SCHEMA)
    if con.execute('SELECT COUNT(*) FROM portfolio_sections').fetchone()[0]==0:
        seed=json.loads(SEED.read_text(encoding='utf8'))['sections']
        for pos,sec in enumerate(seed):
            con.execute('INSERT INTO portfolio_sections(id,kind,title,eyebrow,description,enabled,position) VALUES(?,?,?,?,?,?,?)',(
                sec['id'],sec['kind'],sec['title'],sec.get('eyebrow',''),sec.get('description',''),1,pos))
            for idx,item in enumerate(sec['items']):
                con.execute('INSERT INTO portfolio_items(id,section_id,content,enabled,position) VALUES(?,?,?,?,?)',(
                    'item-'+uuid4().hex[:20],sec['id'],json.dumps(item,ensure_ascii=False),1,idx))
        con.commit()
    return con

def dump():
    with connect() as con:
        con.row_factory=sqlite3.Row
        sections=[]
        for row in con.execute('SELECT * FROM portfolio_sections ORDER BY position,id').fetchall():
            sec=dict(row)
            sec['enabled']=bool(sec['enabled'])
            sec['items']=[]
            for item in con.execute('SELECT * FROM portfolio_items WHERE section_id=? ORDER BY position,id',(row['id'],)).fetchall():
                record=json.loads(item['content'])
                record.update({'id':item['id'],'enabled':bool(item['enabled'])})
                sec['items'].append(record)
            sections.append(sec)
    return {'sections':sections}

def build():
    complete=dump()
    obj={'sections':[]}
    for section in complete['sections']:
        if not section['enabled']:continue
        row={**section,'items':[item for item in section['items'] if item['enabled']]}
        obj['sections'].append(row)
    data=ROOT/'data'; data.mkdir(exist_ok=True)
    wire=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
    (data/'portfolio.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (data/'portfolio-data.js').write_text('window.PORTFOLIO_CONTENT='+wire+';\n',encoding='utf8')
    return obj

def small(value,limit):
    v=str(value or '').strip()
    if len(v)>limit:raise ValueError(f'Text exceeds {limit} characters.')
    return v

def check_slug(val):
    if not re.fullmatch(r'[a-z][a-z0-9-]{1,47}',str(val or '')):
        raise ValueError('ID must be 2–48 lowercase letters, numbers, or hyphens (starting with a letter).')
    return val

def save_section(obj, *, new=False):
    if not isinstance(obj,dict):raise ValueError('Invalid section.')
    ident=check_slug(obj.get('id'))
    kind=small(obj.get('kind'),30)
    if kind not in KINDS:raise ValueError('Unrecognized section kind.')
    title=small(obj.get('title'),110)
    if not title:raise ValueError('Section title is required.')
    eyebrow=small(obj.get('eyebrow'),100)
    description=small(obj.get('description'),500)
    enabled=1 if obj.get('enabled',True) else 0
    with connect() as con:
        if new:
            if kind!='custom':raise ValueError('New sections must use Custom section type.')
            pos=con.execute('SELECT COALESCE(MAX(position),-1)+1 FROM portfolio_sections').fetchone()[0]
            con.execute('INSERT INTO portfolio_sections(id,kind,title,eyebrow,description,enabled,position) VALUES(?,?,?,?,?,?,?)',
                        (ident,kind,title,eyebrow,description,enabled,pos))
        else:
            cur=con.execute('UPDATE portfolio_sections SET title=?,eyebrow=?,description=?,enabled=? WHERE id=? AND kind=?',
                        (title,eyebrow,description,enabled,ident,kind))
            if not cur.rowcount:raise ValueError('Section not found or type mismatch.')
    build()
    return ident

def delete_section(ident):
    with connect() as con:
        cur=con.execute('DELETE FROM portfolio_sections WHERE id=?',(str(ident),))
        if not cur.rowcount:raise ValueError('Section not found.')
    build()

def move(table,ident,direction):
    if table not in {'portfolio_sections','portfolio_items'}:raise ValueError('Invalid list.')
    direction=int(direction)
    if direction not in {-1,1}:raise ValueError('Direction must be -1 or 1.')
    with connect() as con:
        row=con.execute(f'SELECT * FROM {table} WHERE id=?',(ident,)).fetchone()
        if row is None:raise ValueError('Item not found.')
        if table=='portfolio_sections':
            ids=[x[0] for x in con.execute('SELECT id FROM portfolio_sections ORDER BY position,id')]
        else:
            section=con.execute('SELECT section_id FROM portfolio_items WHERE id=?',(ident,)).fetchone()[0]
            ids=[x[0] for x in con.execute('SELECT id FROM portfolio_items WHERE section_id=? ORDER BY position,id',(section,))]
        old=ids.index(ident)
        new=max(0,min(len(ids)-1,old+direction))
        ids.insert(new,ids.pop(old))
        for pos,item_id in enumerate(ids):
            con.execute(f'UPDATE {table} SET position=? WHERE id=?',(pos,item_id))
    build()

def save_item(obj, *, new=False):
    if not isinstance(obj,dict):raise ValueError('Invalid item.')
    section_id=small(obj.get('section_id'),48)
    if not section_id:raise ValueError('Select a section.')
    with connect() as con:
        if not con.execute('SELECT 1 FROM portfolio_sections WHERE id=?',(section_id,)).fetchone():
            raise ValueError('Section does not exist.')
        content=obj.get('content')
        if not isinstance(content,dict):raise ValueError('Invalid item content.')
        if len(content)>35:raise ValueError('Too many fields.')
        clean={small(k,64):small(v,6500) for k,v in content.items()}
        if not any(v for v in clean.values()):raise ValueError('Enter at least one detail.')
        serialized=json.dumps(clean,ensure_ascii=False)
        if len(serialized)>16000:raise ValueError('Item too large.')
        enabled=1 if obj.get('enabled',True) else 0
        if new:
            ident='item-'+uuid4().hex[:20]
            pos=con.execute('SELECT COALESCE(MAX(position),-1)+1 FROM portfolio_items WHERE section_id=?',(section_id,)).fetchone()[0]
            con.execute('INSERT INTO portfolio_items(id,section_id,content,enabled,position) VALUES(?,?,?,?,?)',
                        (ident,section_id,serialized,enabled,pos))
        else:
            ident=small(obj.get('id'),60)
            cur=con.execute('UPDATE portfolio_items SET content=?,enabled=? WHERE id=? AND section_id=?',
                            (serialized,enabled,ident,section_id))
            if not cur.rowcount:raise ValueError('Content item not found.')
    build()
    return ident

def delete_item(ident):
    with connect() as con:
        cur=con.execute('DELETE FROM portfolio_items WHERE id=?',(str(ident),))
        if not cur.rowcount:raise ValueError('Content item not found.')
    build()

if __name__=='__main__':
    command=sys.argv[1] if len(sys.argv)>1 else 'build'
    if command not in {'build','init','status'}:raise SystemExit('Usage: python tools/portfolio.py build')
    data=build()
    print(f'Portfolio ready: {len(data["sections"])} sections, '+str(sum(len(x['items']) for x in data['sections']))+' content items')
