import json

with open('d:/project/mq/comp_8420_final/final/Final_Notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

source = nb['cells'][-1]['source']
new_source = []
for line in source:
    if "db.reviews.update_many" in line and "{\"\":" in line.replace("'", "\""):
        line = line.replace("{'':", "{'$set':")
    new_source.append(line)
nb['cells'][-1]['source'] = new_source

with open('d:/project/mq/comp_8420_final/final/Final_Notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
