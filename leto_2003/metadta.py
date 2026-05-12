import os


pot = '03_ang_opisi'
dokumenti = [f for f in os.listdir(pot) if f.endswith('.txt')]

st_doc = len(dokumenti)

print(st_doc)