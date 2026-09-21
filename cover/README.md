# Physics Black Book – Front Cover

Print-ready A4 front cover for the RBSE Class 12 Physics question bank (Science Flux Classes).

- `cover.tex` – full source (XeLaTeX + TikZ; every graphic is drawn in code)
- `cover.pdf` – vector output, A4 full bleed
- `cover_300dpi.png` – raster export for WhatsApp / social previews
- `assets/` – circular logo and author photo

Build (two passes are needed for page-anchored TikZ):

```bash
cd cover
xelatex cover.tex && xelatex cover.tex
```

Fonts used: Inter Display (hero), Inter (UI), Fira Sans Heavy Italic (hook lines).
