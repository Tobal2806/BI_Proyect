"""Extract a column subset from FONASA's GRD_PUBLICO_<year> file without cleaning any values.
Usage: python3 01_extraer_grd.py <path_to_txt_or_zip> <year> <output.csv>   (then gzip the output)
- Reads in chunks (chunksize) so it fits in limited memory.
- Keeps original values as text; only adds EDAD_ANIOS (age in years), N_DIAG (number of diagnoses),
  N_PROC (number of procedures) and ANIO_BASE (file year). No rows are filtered.
- Drops the encrypted patient identifier and FECHA_NACIMIENTO (date of birth) from the extract
  (personal-data minimisation). Original FONASA column names are kept for traceability.
"""
import sys, zipfile, io
import pandas as pd

src, year, out = sys.argv[1], sys.argv[2], sys.argv[3]
KEEP = ["COD_HOSPITAL","SEXO","FECHA_NACIMIENTO","PROVINCIA","COMUNA","PREVISION","SERVICIO_SALUD",
        "TIPO_PROCEDENCIA","TIPO_INGRESO","ESPECIALIDAD_MEDICA","TIPO_ACTIVIDAD","FECHA_INGRESO",
        "SERVICIOINGRESO","FECHAALTA","SERVICIOALTA","TIPOALTA","DIAGNOSTICO1","USOSPABELLON",
        "IR_29301_COD_GRD","IR_29301_PESO","IR_29301_SEVERIDAD","IR_29301_MORTALIDAD","HOSPPROCEDENCIA"]

def opener():
    if src.endswith(".zip"):
        z = zipfile.ZipFile(src); name = z.namelist()[0]; raw = z.open(name)
    else:
        raw = open(src, "rb")
    head = raw.read(4); raw.close()
    enc = "utf-16" if head[:2] in (b"\xff\xfe", b"\xfe\xff") else "latin-1"
    if src.endswith(".zip"):
        z = zipfile.ZipFile(src); raw = z.open(z.namelist()[0])
    else:
        raw = open(src, "rb")
    return io.TextIOWrapper(raw, encoding=enc, newline=""), enc

fh, enc = opener()
print("detected encoding:", enc)
reader = pd.read_csv(fh, sep="|", dtype=str, chunksize=200_000, keep_default_na=False)
first = True; n = 0
for ch in reader:
    cols = list(ch.columns)
    dx = [c for c in cols if c.startswith("DIAGNOSTICO")]
    px = [c for c in cols if c.startswith("PROCEDIMIENTO")]
    sub = ch[[c for c in KEEP if c in cols]].copy()
    sub["N_DIAG"] = (ch[dx] != "").sum(axis=1)
    sub["N_PROC"] = (ch[px] != "").sum(axis=1)
    def parse_date(col):
        # Each date column is parsed with its own format: in GRD 2023 the birth date is YYYY-MM-DD
        # while admission/discharge dates are DD-MM-YYYY; in GRD 2024 all dates are YYYY-MM-DD.
        v = sub[col].str[:10]
        if v.str.match(r"^\d{2}/\d{2}/\d{4}$").any():
            fmt = "%d/%m/%Y"
        elif v.str.match(r"^\d{2}-\d{2}-\d{4}$").any():
            fmt = "%d-%m-%Y"
        else:
            fmt = "%Y-%m-%d"
        return pd.to_datetime(v, errors="coerce", format=fmt)
    birth = parse_date("FECHA_NACIMIENTO")
    admission = parse_date("FECHA_INGRESO")
    sub["EDAD_ANIOS"] = ((admission - birth).dt.days // 365.25).astype("Int64")
    sub = sub.drop(columns=["FECHA_NACIMIENTO"])
    sub["ANIO_BASE"] = year
    sub.to_csv(out, mode="w" if first else "a", header=first, index=False, encoding="utf-8")
    first = False; n += len(sub)
    print("rows:", n, flush=True)
if first is False:
    print("original columns:", len(cols))
