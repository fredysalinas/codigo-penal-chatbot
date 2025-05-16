
---

### `utils.py`

```python
import PyPDF2

def cargar_pdf(ruta):
    with open(ruta, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        texto = ""
        for pagina in lector.pages:
            texto += pagina.extract_text()
        return texto