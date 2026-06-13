import pathlib

f = pathlib.Path('d:/project/mq/comp_8420_final/final/frontend/src/pages/Home.jsx')
lines = f.read_text('utf-8').splitlines()

code_to_insert = """
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = async () => {
      setImageSearchLoading(true);
      try {
        const res = await fetch(`${API_BASE}/search/image`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_data_url: reader.result })
        });
        if (res.ok) {
          const data = await res.json();
          setProducts(data.results);
          if (data.query_used) {
            setQuery(data.query_used);
          }
        }
      } catch (err) {
        console.error(err);
      } finally {
        setImageSearchLoading(false);
        productsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }
    };
    reader.readAsDataURL(file);
  };
"""

for i, line in enumerate(lines):
    if "productsRef.current?.scrollIntoView({ behavior: 'smooth' });" in line:
        idx = i + 3
        lines.insert(idx, code_to_insert)
        break

f.write_text('\n'.join(lines), 'utf-8')
