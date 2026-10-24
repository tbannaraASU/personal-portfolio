#!/usr/bin/env python3
"""Fill MISSING project case-study fields from documented work.

Preserves every existing user-edited field. Does not invent dates, URLs, or results.
"""
import json
import sqlite3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import portfolio

FACTS={
 'Studio XE — Accessibility & Interface Consistency':{
   'role':'Accessibility engineering contributor',
   'skills':'React, TypeScript, axe-core, eslint-plugin-jsx-a11y, WCAG 2.2 AA, VPAT 2.5',
   'outcomes':'Integrating automated accessibility checks into CI.\nWorking on keyboard and screen-reader accessibility.\nSupporting WCAG 2.2 AA evaluations and VPAT 2.5 documentation.',
 },
 'LLM-Based Data Sharing Research':{
   'role':'Research collaborator in a six-person team',
   'skills':'LLM evaluation, Experimental design, Privacy decisions, Prompting research',
   'outcomes':'Designing experiments on model confidence, consistency, and prompting effects; study ongoing.',
 },
 'Student Discussion Application':{
   'role':'Java developer · Agile team member',
   'skills':'Java, MVC, CRUD, Input validation, Agile development, Testing',
   'outcomes':'Implemented a Java discussion application with MVC architecture and CRUD workflows.\nCollaborated on user-story-based development and iterative testing.',
 },
 'Personal Portfolio Website':{
   'role':'Independent front-end developer',
   'skills':'HTML, CSS, JavaScript, Git, GitHub, SQLite, Responsive design, Accessibility',
   'outcomes':'Created a personal portfolio with editable project details and a photography gallery.\nBuilt a local SQLite-backed content manager and published static data for GitHub Pages.',
   'github_url':'https://github.com/tbannaraASU/personal-portfolio',
   'images':'project-images/portfolio-original-screenshot.webp',
   'image_captions':'Early Portfolio version, captured from my browser during the Git competency exercise',
 },
 'Mustang Emergency Tail Light':{
   'role':'Digital logic designer',
   'skills':'Logisim, Finite-state machines, Boolean logic, Digital circuits',
   'outcomes':'Designed a finite-state-machine counter to simulate Mustang emergency tail light sequences.',
 },
}

def main():
  n=0
  with portfolio.connect() as db:
    sections=db.execute("SELECT id FROM portfolio_sections WHERE kind='projects'").fetchall()
    for (section_id,) in sections:
      for item_id,raw in db.execute('SELECT id,content FROM portfolio_items WHERE section_id=?',(section_id,)).fetchall():
        content=json.loads(raw)
        extra=FACTS.get(content.get('title'))
        if not extra:continue
        changed=False
        for key,value in extra.items():
          if not str(content.get(key,'')).strip():
            content[key]=value;changed=True
        if changed:
          db.execute('UPDATE portfolio_items SET content=? WHERE id=?',(json.dumps(content,ensure_ascii=False),item_id))
          n+=1
    db.commit()
  portfolio.build()
  print(f'Updated {n} project items (only previously empty fields). Review in Admin before publishing.')
if __name__=='__main__':main()
