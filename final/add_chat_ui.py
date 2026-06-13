import json

with open('d:/project/mq/comp_8420_final/final/Final_Notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find cell index containing "Evaluation: RAG vs Baseline"
target_idx = -1
for i, cell in enumerate(nb['cells']):
    if cell.get('source'):
        text = ''.join(cell['source'])
        if "Evaluation: RAG vs Baseline" in text:
            target_idx = i
            break

if target_idx != -1:
    chat_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import ipywidgets as widgets\n",
            "from IPython.display import display, clear_output\n",
            "\n",
            "output = widgets.Output()\n",
            "\n",
            "text_input = widgets.Text(\n",
            "    value='',\n",
            "    placeholder='Ask something about the products...', \n",
            "    description='Query:',\n",
            "    layout=widgets.Layout(width='80%')\n",
            ")\n",
            "button = widgets.Button(description='Ask RAG', button_style='primary')\n",
            "\n",
            "def on_button_click(b):\n",
            "    with output:\n",
            "        clear_output()\n",
            "        query = text_input.value\n",
            "        if not query:\n",
            "            return\n",
            "        print(f\"User: {query}\")\n",
            "        \n",
            "        # Retrieval\n",
            "        retrieved_docs = retrieve(query, top_k=5)\n",
            "        context = \"\\n\".join(retrieved_docs)\n",
            "        \n",
            "        # Generation\n",
            "        prompt = f\"Context:\\n{context}\\n\\nQuestion: {query}\\nAnswer:\"\n",
            "        \n",
            "        try:\n",
            "            res = llm_client.chat.completions.create(\n",
            "                model=\"llama-3.1-8b-instant\",\n",
            "                messages=[{\"role\": \"user\", \"content\": prompt}],\n",
            "                max_tokens=300,\n",
            "                temperature=0.2\n",
            "            )\n",
            "            answer = res.choices[0].message.content\n",
            "        except Exception as e:\n",
            "            answer = f\"Error: {e}\"\n",
            "            \n",
            "        print(f\"RAG: {answer}\\n\" + \"-\"*50)\n",
            "        text_input.value = ''\n",
            "\n",
            "button.on_click(on_button_click)\n",
            "display(widgets.HBox([text_input, button]), output)\n"
        ]
    }
    
    # insert after the RAG eval and the markdown cell following it if there is one
    nb['cells'].insert(target_idx + 2, chat_cell)
    
    with open('d:/project/mq/comp_8420_final/final/Final_Notebook.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Successfully inserted chat cell.")
else:
    print("Could not find target cell.")
