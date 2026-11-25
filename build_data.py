import json, zipfile, xml.etree.ElementTree as ET, re, unicodedata, math, os
from collections import defaultdict, Counter
from decimal import Decimal, ROUND_HALF_UP

XLSX_PATH = "/Users/jaredruiz/INNOVACON/Copia de 04NOV2026 - SIT Consolidado Historico Boletines 2014-2026 v2.xlsx"
INE_PATH = "/Users/jaredruiz/INNOVACON/BrechaDigitalConectividadDigitalEnHogaresMunicipio.xlsx"
TRAZ_PATH = "/Users/jaredruiz/INNOVACON/trazabilidad_brecha_digital.xlsx"
EDU_ECO_PATH = "/Users/jaredruiz/INNOVACON/DatosEstadisticos_tecnologia_educacion_economico.xlsx"
KMZ_MUNIS = "/Users/jaredruiz/INNOVACON/Copia de Municipios.kmz"
KMZ_LP = "/Users/jaredruiz/INNOVACON/Copia de Lugares Poblados 2026.kmz"
MUNIS_TOPO = "/Users/jaredruiz/.gemini/antigravity/brain/ab0ec326-df20-4463-a2f7-8b69783b005d/scratch/munis.json"
DEPTOS_TOPO = "/Users/jaredruiz/.gemini/antigravity/brain/ab0ec326-df20-4463-a2f7-8b69783b005d/scratch/deptos.json"
OUT_DIR = "/Users/jaredruiz/.gemini/antigravity/scratch/innovacon-mapa-sit"
NS = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

os.makedirs(OUT_DIR, exist_ok=True)

def norm(s):
    if s is None:
        return ''
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def col_to_idx(col_str):
    idx = 0
    for c in col_str:
        idx = idx * 26 + (ord(c.upper()) - ord('A') + 1)
    return idx - 1

def parse_desc_table(html):
    pairs = re.findall(r'<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', html, re.S | re.I)
    out = {}
    for k, v in pairs:
        k2 = re.sub(r'<[^>]+>', '', k).strip()
        v2 = re.sub(r'<[^>]+>', '', v).strip()
        if k2:
            out[k2] = v2
    return out

def load_all_sheets(xlsx_path):
    with zipfile.ZipFile(xlsx_path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            ss_root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in ss_root.findall('main:si', NS):
                shared_strings.append(''.join(t.text or '' for t in si.findall('.//main:t', NS)))
        rels_root = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rid_to_target = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels_root}
        wb_root = ET.fromstring(z.read('xl/workbook.xml'))
        out = {}
        for s in wb_root.findall('.//main:sheet', NS):
            name = s.attrib['name']
            rid = s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = rid_to_target[rid].lstrip('/')
            if not target.startswith('xl/'):
                target = 'xl/' + target
            ws_root = ET.fromstring(z.read(target))
            rows = []
            for row_el in ws_root.findall('.//main:sheetData/main:row', NS):
                row_vals = {}
                max_c = -1
                for c in row_el.findall('main:c', NS):
                    ref = c.attrib.get('r', '')
                    m = re.match(r'^([A-Z]+)', ref)
                    c_idx = col_to_idx(m.group(1)) if m else max_c + 1
                    if c_idx > max_c:
                        max_c = c_idx
                    t = c.attrib.get('t')
                    v_el = c.find('main:v', NS)
                    is_el = c.find('main:is', NS)
                    val = None
                    if t == 's' and v_el is not None and v_el.text is not None:
                        val = shared_strings[int(v_el.text)]
                    elif t == 'inlineStr' and is_el is not None:
                        val = ''.join(x.text or '' for x in is_el.findall('.//main:t', NS))
                    elif v_el is not None and v_el.text is not None:
                        val = v_el.text
                    row_vals[c_idx] = val
                if max_c >= 0:
                    rows.append([row_vals.get(i) for i in range(max_c + 1)])
            out[name] = rows
        return out

TOPO_ALIASES = {
    ('alta verapaz', 'san agustin lanquin'): ('alta verapaz', 'lanquin'),
    ('alta verapaz', 'san miguel tucuru'): ('alta verapaz', 'tucuru'),
    ('alta verapaz', 'santa maria cahabon'): ('alta verapaz', 'cahabon'),
    ('baja verapaz', 'santa cruz el chol'): ('baja verapaz', 'el chol'),
    ('chimaltenango', 'san juan comalapa'): ('chimaltenango', 'comalapa'),
    ('chimaltenango', 'san miguel pochuta'): ('chimaltenango', 'pochuta'),
    ('chimaltenango', 'san pedro yepocapa'): ('chimaltenango', 'yepocapa'),
    ('chimaltenango', 'san andres iztapa'): ('chimaltenango', 'san andres itzapa'),
    ('guatemala', 'san miguel petapa'): ('guatemala', 'petapa'),
    ('guatemala', 'san raimundo'): ('guatemala', 'san raymundo'),
    ('huehuetenango', 'san pedro soloma'): ('huehuetenango', 'soloma'),
    ('huehuetenango', 'santa cruz barillas'): ('huehuetenango', 'barillas'),
    ('huehuetenango', 'san idelfonso ixtahuacan'): ('huehuetenango', 'san ildefonso ixtahuacan'),
    ('huehuetenango', 'san rafel la independencia'): ('huehuetenango', 'san rafael la independencia'),
    ('jalapa', 'mataquiescuintla'): ('jalapa', 'mataquescuintla'),
    ('quetzaltenango', 'colomba costa cuca'): ('quetzaltenango', 'colomba'),
    ('quetzaltenango', 'san juan olintepeque'): ('quetzaltenango', 'olintepeque'),
    ('quiche', 'playa grande ixcan'): ('quiche', 'ixcan'),
    ('quiche', 'san miguel uspantan'): ('quiche', 'uspantan'),
    ('quiche', 'santa maria nebaj'): ('quiche', 'nebaj'),
    ('quiche', 'santo tomas chichicastenango'): ('quiche', 'chichicastenango'),
    ('quiche', 'cotzal'): ('quiche', 'san juan cotzal'),
    ('retalhuleu', 'san felipe realhuleu'): ('retalhuleu', 'san felipe'),
    ('sacatepequez', 'san juan alotenango'): ('sacatepequez', 'alotenango'),
    ('san marcos', 'san jose el rodeo'): ('san marcos', 'el rodeo'),
    ('santa rosa', 'santa cruz el naranjo'): ('santa rosa', 'santa cruz naranjo'),
}

def decode_topo_arcs(topo):
    scale = topo['transform']['scale']
    trans = topo['transform']['translate']
    decoded = []
    for arc in topo['arcs']:
        x, y = 0, 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * scale[0] + trans[0], y * scale[1] + trans[1]))
        decoded.append(pts)
    return decoded

def simplify_dp(pts, tol):
    if len(pts) <= 2:
        return pts
    stack = [(0, len(pts) - 1)]
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    tol2 = tol * tol
    while stack:
        s, e = stack.pop()
        if e <= s + 1:
            continue
        x1, y1 = pts[s]
        x2, y2 = pts[e]
        dx, dy = x2 - x1, y2 - y1
        len2 = dx * dx + dy * dy
        max_d2 = -1.0
        idx = -1
        for i in range(s + 1, e):
            px, py = pts[i]
            if len2 == 0:
                d2 = (px - x1)**2 + (py - y1)**2
            else:
                t = max(0.0, min(1.0, ((px - x1)*dx + (py - y1)*dy) / len2))
                d2 = (px - (x1 + t * dx))**2 + (py - (y1 + t * dy))**2
            if d2 > max_d2:
                max_d2 = d2
                idx = i
        if max_d2 > tol2:
            keep[idx] = True
            stack.append((s, idx))
            stack.append((idx, e))
    return [pts[i] for i in range(len(pts)) if keep[i]]

def build_projection(munis_topo):
    arcs = decode_topo_arcs(munis_topo)
    used_arcs = set()
    for g in munis_topo['objects']['municipios_gtm']['geometries']:
        if g['properties']['id'] == 4000:
            continue
        def collect(a):
            for item in a:
                if isinstance(item, list): collect(item)
                else: used_arcs.add(item if item >= 0 else ~item)
        collect(g['arcs'])
    lons, lats = [], []
    for idx in used_arcs:
        for lon, lat in arcs[idx]:
            lons.append(lon); lats.append(lat)
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    mid_lat = (min_lat + max_lat) / 2.0
    cos_lat = math.cos(math.radians(mid_lat))
    w_geo = (max_lon - min_lon) * cos_lat
    h_geo = (max_lat - min_lat)
    pad = 24.0
    target_w = 840.0
    scale = (target_w - 2 * pad) / w_geo
    target_h = h_geo * scale + 2 * pad

    def proj(lon, lat):
        return (pad + (lon - min_lon) * cos_lat * scale, pad + (max_lat - lat) * scale)

    proj_params = {
        'min_lon': round(min_lon, 6),
        'max_lat': round(max_lat, 6),
        'cos_lat': round(cos_lat, 6),
        'scale': round(scale, 6),
        'pad': pad,
    }
    return proj, round(target_w, 1), round(target_h, 1), proj_params

def point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi):
            inside = not inside
        j = i
    return inside

def point_in_geom_rings(lon, lat, poly_rings):
    for outer, holes in poly_rings:
        if point_in_ring(lon, lat, outer):
            if not any(point_in_ring(lon, lat, h) for h in holes):
                return True
    return False

def geom_to_svg_and_geo(geom, proj_arcs, raw_arcs):
    poly_list = [geom['arcs']] if geom['type'] == 'Polygon' else (geom['arcs'] if geom['type'] == 'MultiPolygon' else [])
    minx, miny, maxx, maxy = 1e9, 1e9, -1e9, -1e9
    gminx, gminy, gmaxx, gmaxy = 1e9, 1e9, -1e9, -1e9
    best_ring_area = -1.0
    best_ring_centroid = (0.0, 0.0)
    best_geo_centroid = (0.0, 0.0)
    geo_polys = []
    parts = []

    for poly in poly_list:
        outer_geo = None
        holes_geo = []
        for r_idx, ring in enumerate(poly):
            pts = []
            gpts = []
            for a in ring:
                ap = proj_arcs[a] if a >= 0 else list(reversed(proj_arcs[~a]))
                gp = raw_arcs[a] if a >= 0 else list(reversed(raw_arcs[~a]))
                pts.extend(ap[1:] if pts else ap)
                gpts.extend(gp[1:] if gpts else gp)
            if len(pts) < 3:
                continue
            if r_idx == 0: outer_geo = gpts
            else: holes_geo.append(gpts)

            for x, y in pts:
                if x < minx: minx = x
                if y < miny: miny = y
                if x > maxx: maxx = x
                if y > maxy: maxy = y
            for gx, gy in gpts:
                if gx < gminx: gminx = gx
                if gy < gminy: gminy = gy
                if gx > gmaxx: gmaxx = gx
                if gy > gmaxy: gmaxy = gy

            if r_idx == 0:
                a2 = cx = cy = 0.0
                ga2 = gcx = gcy = 0.0
                for i in range(len(pts)):
                    x0, y0 = pts[i]; x1, y1 = pts[(i+1)%len(pts)]
                    c = x0*y1 - x1*y0
                    a2 += c; cx += (x0+x1)*c; cy += (y0+y1)*c
                for i in range(len(gpts)):
                    x0, y0 = gpts[i]; x1, y1 = gpts[(i+1)%len(gpts)]
                    c = x0*y1 - x1*y0
                    ga2 += c; gcx += (x0+x1)*c; gcy += (y0+y1)*c
                area = abs(a2) / 2.0
                if area > best_ring_area and abs(a2) > 1e-6:
                    best_ring_area = area
                    best_ring_centroid = (cx/(3.0*a2), cy/(3.0*a2))
                    if abs(ga2) > 1e-12:
                        best_geo_centroid = (gcx/(3.0*ga2), gcy/(3.0*ga2))

            cmd = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
            lx, ly = round(pts[0][0], 1), round(pts[0][1], 1)
            for x, y in pts[1:]:
                rx, ry = round(x, 1), round(y, 1)
                if rx != lx or ry != ly:
                    cmd.append(f"L{rx:.1f},{ry:.1f}")
                    lx, ly = rx, ry
            cmd.append("Z")
            parts.append("".join(cmd))
        if outer_geo:
            geo_polys.append((outer_geo, holes_geo))

    cx, cy = best_ring_centroid if best_ring_area > 0 else ((minx+maxx)/2, (miny+maxy)/2)
    gcx, gcy = best_geo_centroid if best_ring_area > 0 else ((gminx+gmaxx)/2, (gminy+gmaxy)/2)
    return "".join(parts), [round(minx,1), round(miny,1), round(maxx,1), round(maxy,1)], [round(cx,1), round(cy,1)], [round(gcx,5), round(gcy,5)], (gminx, gminy, gmaxx, gmaxy), geo_polys

def main():
    with open(MUNIS_TOPO) as f: m_topo = json.load(f)
    with open(DEPTOS_TOPO) as f: d_topo = json.load(f)

    proj, svg_w, svg_h, proj_params = build_projection(m_topo)
    m_arcs_raw = decode_topo_arcs(m_topo)
    m_arcs_proj = [simplify_dp([proj(lon, lat) for lon, lat in arc], 0.35) for arc in m_arcs_raw]
    d_arcs_raw = decode_topo_arcs(d_topo)
    d_arcs_proj = [simplify_dp([proj(lon, lat) for lon, lat in arc], 0.45) for arc in d_arcs_raw]

    muni_geoms = {}
    topo_lookup = {}
    geo_spatial = {}  # gid -> (bbox_geo, geo_polys)
    lakes = []
    for g in m_topo['objects']['municipios_gtm']['geometries']:
        p = g['properties']
        gid = p['id']
        if gid == 4000: continue
        path_d, bbox, centroid, geo_c, gbb, gpolys = geom_to_svg_and_geo(g, m_arcs_proj, m_arcs_raw)
        if gid == 0:
            lakes.append({'name': p['Municipio'], 'd': path_d, 'c': centroid})
            continue
        muni_geoms[gid] = {
            'id': gid, 'ine_depto': p['id_depto'], 'depto_topo': p['Departamento'],
            'muni_topo': p['Municipio'], 'd': path_d, 'bb': bbox, 'c': centroid, 'gc': geo_c
        }
        topo_lookup[(norm(p['Departamento']), norm(p['Municipio']))] = gid
        geo_spatial[gid] = (gbb, gpolys)

    depto_geoms = {}
    depto_lookup = {}
    for g in d_topo['objects']['departamentos_gtm']['geometries']:
        p = g['properties']
        did = p['id']
        path_d, bbox, centroid, _, _, _ = geom_to_svg_and_geo(g, d_arcs_proj, d_arcs_raw)
        depto_geoms[did] = {'id': did, 'name': p['Departamento'], 'd': path_d, 'bb': bbox, 'c': centroid}
        depto_lookup[norm(p['Departamento'])] = did

    # === Parse Copia de Municipios.kmz for AreaKm2 (excluding the 7 parents whose borders split later) ===
    # Municipalities that were later split to create Sipacate(514), San José La Máquina(1021), La Blanca(1230),
    # Petatán(1333), Las Cruces(1713), El Chal(1714), San Jorge(1911):
    SPLIT_PARENTS = {507, 1002, 1218, 1317, 1705, 1708, 1901}  # La Gomera, Cuyotenango, Ocós, Concepción Huista, La Libertad, Dolores, Zacapa
    kmz_area = {}
    with zipfile.ZipFile(KMZ_MUNIS) as z:
        root_m = ET.fromstring(z.read('doc.kml'))
    ns_m = {'k': root_m.tag.split('}')[0].strip('{')}
    for pm in root_m.findall('.//k:Placemark', ns_m):
        desc = pm.find('k:description', ns_m)
        tbl = parse_desc_table(desc.text) if desc is not None and desc.text else {}
        cod = tbl.get('Codigo', '')
        area_s = tbl.get('AreaKm2', '')
        if cod.isdigit() and int(cod) in muni_geoms and area_s:
            cid = int(cod)
            if cid not in SPLIT_PARENTS:
                kmz_area[cid] = round(float(area_s), 2)
    print(f"Loaded verified AreaKm2 from Municipios.kmz for {len(kmz_area)} municipalities (excluded {len(SPLIT_PARENTS)} pre-split parents).")

    # === Parse Copia de Lugares Poblados 2026.kmz (27,352 geolocated sites!) ===
    print("Parsing Copia de Lugares Poblados 2026.kmz...")
    with zipfile.ZipFile(KMZ_LP) as z:
        root_lp = ET.fromstring(z.read('doc.kml'))
    ns_lp = {'k': root_lp.tag.split('}')[0].strip('{')}

    # Category normalization & ordering
    CAT_GROUPS = ['CABECERA/URBANO', 'ALDEA', 'CASERIO', 'COLONIA/LOTIF.', 'FINCA/HACIENDA', 'OTRO']
    def cat_group_idx(raw_cat):
        c = norm(raw_cat)
        if c in ('ciudad', 'villa', 'pueblo'): return 0
        if c == 'aldea': return 1
        if c == 'caserio': return 2
        if c in ('colonia', 'asentamiento', 'lotificacion', 'condominio', 'residenciales', 'barrio', 'canton'): return 3
        if c in ('finca', 'hacienda', 'granja', 'labor', 'parcelamiento'): return 4
        return 5

    lp_by_muni = defaultdict(list)  # gid -> list of [lon4, lat4, name, raw_cat_idx, group_idx]
    raw_cats = []
    raw_cat_idx = {}
    def get_cat_idx(rc):
        rc2 = (rc or 'SIN CATEGORÍA').strip().upper()
        if rc2 not in raw_cat_idx:
            raw_cat_idx[rc2] = len(raw_cats)
            raw_cats.append(rc2)
        return raw_cat_idx[rc2]

    def resolve_muni_by_name(depto, muni):
        k = (norm(depto), norm(muni))
        if k in topo_lookup: return topo_lookup[k]
        if k in TOPO_ALIASES and TOPO_ALIASES[k] in topo_lookup: return topo_lookup[TOPO_ALIASES[k]]
        return None

    # Build quick bbox index for PIP
    gids_list = list(muni_geoms.keys())
    pip_matched = 0
    text_fallback = 0
    nearest_fallback = 0

    for pm in root_lp.findall('.//k:Placemark', ns_lp):
        pt = pm.find('.//k:Point/k:coordinates', ns_lp)
        if pt is None or not pt.text: continue
        parts = pt.text.strip().split(',')
        if len(parts) < 2: continue
        lon, lat = float(parts[0]), float(parts[1])
        desc = pm.find('k:description', ns_lp)
        tbl = parse_desc_table(desc.text) if desc is not None and desc.text else {}
        lp_name = tbl.get('lugar_pobl', '').strip() or 'Sin nombre'
        raw_cat = tbl.get('categoria', '').strip() or 'OTRA'
        dep_txt = tbl.get('departamen', '').strip()
        muni_txt = tbl.get('municipio', '').strip()

        # 1. Exact spatial Point-in-Polygon against our 340 official polygons!
        assigned_gid = None
        for gid in gids_list:
            (x1, y1, x2, y2), gpolys = geo_spatial[gid]
            if x1 <= lon <= x2 and y1 <= lat <= y2:
                if point_in_geom_rings(lon, lat, gpolys):
                    assigned_gid = gid
                    pip_matched += 1
                    break
        # 2. Fallback to text match if point fell slightly outside coastline/border
        if assigned_gid is None:
            assigned_gid = resolve_muni_by_name(dep_txt, muni_txt)
            if assigned_gid is not None:
                text_fallback += 1
        # 3. Nearest centroid fallback (should be near-zero)
        if assigned_gid is None:
            best_d = 1e9
            for gid in gids_list:
                cx, cy = muni_geoms[gid]['gc']
                d2 = (lon - cx)**2 + (lat - cy)**2
                if d2 < best_d:
                    best_d = d2; assigned_gid = gid
            nearest_fallback += 1

        lp_by_muni[assigned_gid].append([
            round(lon, 4), round(lat, 4), lp_name, get_cat_idx(raw_cat), cat_group_idx(raw_cat)
        ])

    total_lp = sum(len(v) for v in lp_by_muni.values())
    print(f"Geolocated {total_lp} populated places across {len(lp_by_muni)}/340 munis! (PIP={pip_matched}, text_fallback={text_fallback}, nearest={nearest_fallback})")

    # Pick official Cabecera Municipal GPS coordinate for each of the 340 municipalities
    cabecera_gps = {}
    lp_summary = {}
    for gid in gids_list:
        pts = lp_by_muni[gid]
        # Count by 6 category groups
        gcounts = [0]*6
        for pt in pts:
            gcounts[pt[4]] += 1
        lp_summary[gid] = {'tot': len(pts), 'grp': gcounts}

        # Find best cabecera point (CIUDAD/VILLA/PUEBLO matching muni name, else any CIUDAD/VILLA/PUEBLO, else centroid)
        m_norm = norm(muni_geoms[gid]['muni_topo'])
        best_pt = None
        for pt in pts:
            if pt[4] == 0 and (norm(pt[2]) == m_norm or m_norm in norm(pt[2])):
                best_pt = pt; break
        if not best_pt:
            for pt in pts:
                if pt[4] == 0:
                    best_pt = pt; break
        if best_pt:
            cabecera_gps[gid] = {'lon': best_pt[0], 'lat': best_pt[1], 'nm': best_pt[2], 'src': 'kmz'}
        else:
            gc = muni_geoms[gid]['gc']
            cabecera_gps[gid] = {'lon': round(gc[0], 4), 'lat': round(gc[1], 4), 'nm': muni_geoms[gid]['muni_topo'], 'src': 'centroid'}

        # Sort points inside each municipality: Cabeceras first, then Aldeas, then Caserios, etc., then alphabetical
        pts.sort(key=lambda x: (x[4], x[2]))

    kmz_cab_count = sum(1 for v in cabecera_gps.values() if v['src'] == 'kmz')
    print(f"Official Cabecera GPS from Lugares Poblados 2026.kmz: {kmz_cab_count} / 340 (rest use exact polygon centroid)")

    # === Load ALL Excel sheets ===
    sheets = load_all_sheets(XLSX_PATH)

    def resolve_muni_id(depto, muni):
        k = (norm(depto), norm(muni))
        if k in topo_lookup: return topo_lookup[k]
        if k in TOPO_ALIASES and TOPO_ALIASES[k] in topo_lookup: return topo_lookup[TOPO_ALIASES[k]]
        return None

    op_names = ['Cablenet', 'COMCEL', 'A-Tel', 'TELGUA', 'Teléfonos del Norte', 'Claro', 'GUATEL', 'Columbus Networks', 'Liberty Networks']
    periods_08 = []
    muni_fixed = defaultdict(dict)
    depto_fixed = defaultdict(dict)
    sit_canonical_name = {}
    pdf_files = []
    pdf_index = {}
    def get_pdf_idx(path_str):
        if not path_str: return -1
        short = path_str.split('/')[-1]
        if short not in pdf_index:
            pdf_index[short] = len(pdf_files)
            pdf_files.append(short)
        return pdf_index[short]

    for r in sheets['08 Líneas municipales'][3:]:
        period = r[2]
        if period not in periods_08: periods_08.append(period)
        lvl, depto, name = r[3], r[4], r[5]
        vals = []; total = 0
        for i in range(6, 15):
            v = r[i] if i < len(r) else None
            if v is None or str(v).strip() == '': vals.append(None)
            else:
                iv = int(float(v)); vals.append(iv); total += iv
        page = int(float(r[15])) if len(r) > 15 and r[15] is not None else None
        pidx = get_pdf_idx(r[16] if len(r) > 16 else None)
        xrow = int(float(r[17])) if len(r) > 17 and r[17] is not None else None
        entry = {'v': vals, 't': total, 'pg': page, 'pdf': pidx, 'r': xrow}
        if lvl == 'Municipio':
            gid = resolve_muni_id(depto, name)
            assert gid is not None, f"Unresolved muni in 08: {depto} / {name}"
            sit_canonical_name[gid] = (depto, name)
            muni_fixed[gid][period] = entry
        elif lvl == 'Departamento':
            depto_fixed[depto_lookup[norm(depto)]][period] = entry

    assert len(sit_canonical_name) == 340

    periods_09 = []
    muni_rb = defaultdict(dict)
    depto_rb = defaultdict(dict)
    special_localities = defaultdict(list)

    for r in sheets['09 Radiobases territoriales'][3:]:
        period = r[2]
        if period not in periods_09: periods_09.append(period)
        lvl, depto, name = r[3], r[4], r[5]
        val = int(float(r[6]))
        page = int(float(r[7])) if len(r) > 7 and r[7] is not None else None
        pidx = get_pdf_idx(r[8] if len(r) > 8 else None)
        xrow = int(float(r[9])) if len(r) > 9 and r[9] is not None else None
        if lvl == 'Departamento':
            depto_rb[depto_lookup[norm(depto)]][period] = {'v': val, 'pg': page, 'pdf': pidx, 'r': xrow}
        elif lvl == 'Municipio':
            gid = resolve_muni_id(depto, name)
            if gid is None:
                special_localities[depto_lookup[norm(depto)]].append({'name': name, 'p': period, 'v': val, 'pg': page, 'pdf': pidx, 'r': xrow})
            else:
                rec = {'v': val, 'pg': page, 'pdf': pidx, 'r': xrow}
                if name != sit_canonical_name[gid][1]: rec['on'] = name
                muni_rb[gid][period] = rec

    # Verify Sheet 15 exact arithmetic reconciliation!
    control_territorial = []
    for r in sheets['15 Control territorial'][3:]:
        rec = {
            'p': r[0], 'mag': r[1],
            'ndept': int(float(r[2])) if r[2] is not None else None,
            'nmuni': int(float(r[3])) if r[3] is not None else None,
            'sdept': int(float(r[4])) if r[4] is not None else None,
            'smuni': int(float(r[5])) if r[5] is not None else None,
            'dloc': int(float(r[6])) if len(r) > 6 and r[6] is not None else None,
            'tnac': int(float(r[7])) if len(r) > 7 and r[7] is not None else None,
            'dnac': int(float(r[8])) if len(r) > 8 and r[8] is not None else None,
        }
        control_territorial.append(rec)
        if rec['mag'] == 'Líneas fijas':
            calc = sum(muni_fixed[gid][rec['p']]['t'] for gid in muni_fixed if rec['p'] in muni_fixed[gid])
            assert calc == rec['smuni']
        elif rec['mag'] == 'Radiobases':
            calc_m = sum(muni_rb[gid][rec['p']]['v'] for gid in muni_rb if rec['p'] in muni_rb[gid])
            calc_sp = sum(x['v'] for items in special_localities.values() for x in items if x['p'] == rec['p'])
            assert (calc_m + calc_sp) == rec['smuni']

    print("100% ARITHMETIC RECONCILIATION PASSED AGAINST SHEET 15!")

    # National sheets
    serie_hist = []
    for r in sheets['01 Serie histórica'][3:]:
        def num(i):
            if i >= len(r) or r[i] is None or str(r[i]).strip() == '': return None
            f = float(r[i])
            return int(f) if f.is_integer() else round(f, 6)
        serie_hist.append({
            'p': r[2], 'fijas': num(3), 'moviles': num(4), 'pospago': num(5), 'prepago': num(6),
            'total_fm': num(7), 'pct_f': num(8), 'pct_m': num(9), 'baf': num(10), 'etm': num(11),
            'tnac_f': num(12), 'tnac_m': num(13), 'tint_f': num(14), 'tint_m': num(15),
            'tbaf_eb': num(16), 'tbam_nac_eb': num(17), 'tbam_roam_eb': num(18), 'rb': num(19),
            'pdf': get_pdf_idx(r[20] if len(r) > 20 else None), 'pg': num(21)
        })

    fixed_ops = defaultdict(list)
    for r in sheets['03 Telefonía fija'][3:]:
        fixed_ops[r[2]].append({'op': r[3], 'v': int(float(r[4])), 'pct': round(float(r[5]), 2)})

    mobile_ops = defaultdict(lambda: defaultdict(list))
    for r in sheets['04 Telefonía móvil'][3:]:
        mobile_ops[r[2]][r[3]].append({'op': r[4], 'v': int(float(r[5])), 'pct': round(float(r[6]), 2)})

    internet_etm = defaultdict(lambda: defaultdict(list))
    for r in sheets['07 Internet y ETM'][3:]:
        val = float(r[5])
        internet_etm[r[2]][r[3]].append({
            'op': r[4], 'v': int(val) if val.is_integer() else round(val, 6),
            'pct': round(float(r[6]), 4) if r[6] is not None else None,
            'roam': round(float(r[7]), 6) if len(r) > 7 and r[7] is not None else None,
            'u': r[9] if len(r) > 9 else ''
        })

    tarifas_latest = []
    for r in sheets['12 Tarifas puntuales'][3:]:
        if r[2] == '2025-S2':
            tarifas_latest.append({'p': r[2], 'op': r[3], 'c': r[4], 'q': round(float(r[5]), 4), 'pg': int(float(r[6])) if r[6] is not None else None})

    control_num = [{'tab': r[0], 'regs': int(float(r[1])), 'nper': int(float(r[2])), 'from': r[3], 'to': r[4]} for r in sheets['13 Control numérico'][3:]]
    conciliacion = [{'p': r[0], 'chk': r[1], 'c1': int(float(r[2])), 'c2': int(float(r[3])), 'tot': int(float(r[4])), 'dif': int(float(r[5]))} for r in sheets['14 Conciliación'][3:]]

    # === Load Official INE XII Censo Digital Divide in Households (340/340 exact INE codes) ===
    ine_sheets = load_all_sheets(INE_PATH)
    ine_rows = list(ine_sheets.values())[0]
    ine_by_gid = {}
    ine_by_did = defaultdict(lambda: {'h': 0, 'con': 0, 'sin': 0})
    tot_h_nac = tot_con_nac = tot_sin_nac = 0
    for r in ine_rows:
        if len(r) < 7 or r[1] is None or not str(r[1]).strip().isdigit():
            continue
        cid = int(str(r[1]).strip())
        h = int(float(r[3]))
        con = int(float(r[4]))
        sin = int(float(r[5]))
        assert h == con + sin, f"INE arithmetic mismatch for {cid}: {h} != {con}+{sin}"
        brecha = round(float(r[6]) * 100.0, 2)
        pct_con = round(100.0 - brecha, 2)
        ine_by_gid[cid] = {'h': h, 'con': con, 'sin': sin, 'br': brecha, 'pc': pct_con}
        did = muni_geoms[cid]['ine_depto']
        ine_by_did[did]['h'] += h
        ine_by_did[did]['con'] += con
        ine_by_did[did]['sin'] += sin
        tot_h_nac += h; tot_con_nac += con; tot_sin_nac += sin
    assert len(ine_by_gid) == 340, f"Expected 340 INE rows, got {len(ine_by_gid)}"
    for did, drec in ine_by_did.items():
        drec['br'] = round((drec['sin'] / drec['h']) * 100.0, 2) if drec['h'] > 0 else 0.0
        drec['pc'] = round(100.0 - drec['br'], 2)
    print(f"Loaded INE XII Censo Digital Divide for 340/340 munis! National: {tot_h_nac:,} hogares, {tot_sin_nac:,} sin internet ({tot_sin_nac/tot_h_nac*100:.2f}% brecha).")

    # === Load Official 2018->2023 Traceability Workbook (trazabilidad_brecha_digital.xlsx) ===
    # Verifies 340/340 municipal 2018 reconciliation (0 diffs) + loads SEGEPLAN 2023 municipal poverty/consumption
    # + loads official INE ENCOVI 2023 departmental digital divide (22/22 departments, expanded values)
    traz_sheets = load_all_sheets(TRAZ_PATH)
    traz_muni_rows = traz_sheets['Datos municipios']
    traz_depto_rows = traz_sheets['Datos departamentos']

    depto_u18 = defaultdict(lambda: {'p7': 0, 'pint': 0, 'pcel': 0})
    muni_traz_cnt = 0
    tot18_p7 = tot18_pint = 0
    for r in traz_muni_rows[2:]:
        if len(r) < 17 or r[2] is None or not str(r[2]).strip().replace('.0', '').isdigit():
            continue
        cid = int(float(r[2]))
        hog = int(round(float(r[7])))
        hint = int(round(float(r[8])))
        assert ine_by_gid[cid]['h'] == hog and ine_by_gid[cid]['con'] == hint, f"2018 mismatch in trazabilidad for {cid}"
        p7 = int(round(float(r[4])))
        pcel = int(round(float(r[5])))
        pint = int(round(float(r[6])))
        uso18 = round((pint / p7) * 100.0, 2) if p7 > 0 else 0.0
        cel18 = round((pcel / p7) * 100.0, 2) if p7 > 0 else 0.0
        pobr23 = round(float(r[14]), 1) if r[14] is not None and str(r[14]).strip() != '' else None
        cons23 = round(float(r[16]), 2) if r[16] is not None and str(r[16]).strip() != '' else None
        ine_by_gid[cid].update({
            'p7': p7, 'pint': pint, 'pcel': pcel, 'uso': uso18, 'cel': cel18,
            'pobr23': pobr23, 'cons23': cons23,
        })
        did = muni_geoms[cid]['ine_depto']
        depto_u18[did]['p7'] += p7
        depto_u18[did]['pint'] += pint
        depto_u18[did]['pcel'] += pcel
        tot18_p7 += p7; tot18_pint += pint
        muni_traz_cnt += 1
    assert muni_traz_cnt == 340, f"Expected 340 munis in trazabilidad, got {muni_traz_cnt}"
    for did, urec in depto_u18.items():
        ine_by_did[did]['p7'] = urec['p7']
        ine_by_did[did]['pint'] = urec['pint']
        ine_by_did[did]['uso'] = round((urec['pint'] / urec['p7']) * 100.0, 2) if urec['p7'] > 0 else 0.0
        ine_by_did[did]['cel'] = round((urec['pcel'] / urec['p7']) * 100.0, 2) if urec['p7'] > 0 else 0.0

    ine23_by_did = {}
    tot23_h = tot23_con = tot23_sin = tot23_p7 = tot23_pint = 0
    for r in traz_depto_rows[2:]:
        if len(r) < 17 or r[0] is None or not str(r[0]).strip().replace('.0', '').isdigit():
            continue
        did = int(float(r[0])) * 100
        assert did in depto_geoms, f"Unknown depto code in ENCOVI 2023: {did}"
        pob23 = int(round(float(r[2])))
        h23 = int(round(float(r[3])))
        p7_23 = int(round(float(r[4])))
        pint_23 = int(round(float(r[5])))
        pcel_23 = int(round(float(r[6])))
        con23 = int(round(float(r[7])))
        sin23 = h23 - con23
        assert sin23 >= 0, f"ENCOVI 2023 negative sin for {did}"
        br23 = round((sin23 / h23) * 100.0, 2) if h23 > 0 else 0.0
        pc23 = round(100.0 - br23, 2)
        uso23 = round((pint_23 / p7_23) * 100.0, 2) if p7_23 > 0 else 0.0
        cel23 = round((pcel_23 / p7_23) * 100.0, 2) if p7_23 > 0 else 0.0
        pobr23 = round(float(r[10]), 1)
        q_cel = round(float(r[11]), 2)
        pct_g_cel = round(float(r[12]), 2)
        q_int = round(float(r[13]), 2)
        gasto = round(float(r[15]), 2)
        peso150 = round(float(r[16]), 2)
        dbr = round(br23 - ine_by_did[did]['br'], 2)
        duso = round(uso23 - ine_by_did[did]['uso'], 2)
        ine23_by_did[did] = {
            'pob': pob23, 'h': h23, 'con': con23, 'sin': sin23,
            'br': br23, 'pc': pc23, 'dbr': dbr,
            'p7': p7_23, 'pint': pint_23, 'uso': uso23, 'duso': duso, 'cel': cel23,
            'pobr': pobr23, 'q_cel': q_cel, 'pct_g_cel': pct_g_cel,
            'q_int': q_int, 'gasto': gasto, 'peso150': peso150,
        }
        tot23_h += h23; tot23_con += con23; tot23_sin += sin23
        tot23_p7 += p7_23; tot23_pint += pint_23
    assert len(ine23_by_did) == 22, f"Expected 22 deptos in ENCOVI 2023, got {len(ine23_by_did)}"
    nat_br18 = round(tot_sin_nac / tot_h_nac * 100.0, 2)
    nat_br23 = round(tot23_sin / tot23_h * 100.0, 2)
    nat_uso18 = round(tot18_pint / tot18_p7 * 100.0, 2)
    nat_uso23 = round(tot23_pint / tot23_p7 * 100.0, 2)
    print(f"Loaded ENCOVI 2023 (22/22 deptos) + SEGEPLAN 2023 (340/340 munis)! National 2018->2023: Hogares sin internet {nat_br18:.2f}% -> {nat_br23:.2f}% ({nat_br23-nat_br18:+.2f} pp) | Uso 7+ {nat_uso18:.2f}% -> {nat_uso23:.2f}% ({nat_uso23-nat_uso18:+.2f} pp).")

    # === Load Official INE Technology, Education & Economy Table (DatosEstadisticos_tecnologia_educacion_economico.xlsx) ===
    edu_sheets = load_all_sheets(EDU_ECO_PATH)
    edu_rows = list(edu_sheets.values())[0]
    soc_by_gid = {}
    soc_by_did = defaultdict(lambda: {'pob': 0, 'alf': 0, 'ana': 0, 'ocu': 0})
    tot_soc_pob = tot_soc_alf = tot_soc_ana = tot_soc_ocu = 0
    for r in edu_rows:
        if len(r) < 16 or r[1] is None or not str(r[1]).strip().isdigit():
            continue
        cid = int(str(r[1]).strip())
        if cid not in muni_geoms:
            continue
        pob = int(round(float(r[3])))
        hog = int(round(float(r[4])))
        hi = int(round(float(r[6])))
        hsin = int(round(float(r[7])))
        alf = int(round(float(r[10])))
        ana = int(round(float(r[11])))
        ocu = int(round(float(r[14])))
        assert ine_by_gid[cid]['h'] == hog and ine_by_gid[cid]['con'] == hi and ine_by_gid[cid]['sin'] == hsin, f"EDU_ECO hog mismatch {cid}"
        assert ine_by_gid[cid]['p7'] == (alf + ana), f"EDU_ECO alf+ana != p7 for {cid}"
        pct_ana = round(float(r[12]) * 100.0, 2)
        pct_alf7 = round((alf / (alf + ana)) * 100.0, 2) if (alf + ana) > 0 else 0.0
        pct_ocu = round(float(r[15]) * 100.0, 2)
        soc_by_gid[cid] = {
            'pob': pob, 'alf': alf, 'ana': ana,
            'pct_ana': pct_ana, 'pct_alf7': pct_alf7,
            'ocu': ocu, 'pct_ocu': pct_ocu,
        }
        did = muni_geoms[cid]['ine_depto']
        soc_by_did[did]['pob'] += pob
        soc_by_did[did]['alf'] += alf
        soc_by_did[did]['ana'] += ana
        soc_by_did[did]['ocu'] += ocu
        tot_soc_pob += pob; tot_soc_alf += alf; tot_soc_ana += ana; tot_soc_ocu += ocu
    assert len(soc_by_gid) == 340, f"Expected 340 EDU_ECO rows, got {len(soc_by_gid)}"
    for did, drec in soc_by_did.items():
        drec['pct_ana'] = round((drec['ana'] / drec['pob']) * 100.0, 2) if drec['pob'] > 0 else 0.0
        drec['pct_alf7'] = round((drec['alf'] / (drec['alf'] + drec['ana'])) * 100.0, 2) if (drec['alf'] + drec['ana']) > 0 else 0.0
        drec['pct_ocu'] = round((drec['ocu'] / drec['pob']) * 100.0, 2) if drec['pob'] > 0 else 0.0
    soc_totals = {
        'pob': tot_soc_pob, 'alf': tot_soc_alf, 'ana': tot_soc_ana,
        'pct_ana': round((tot_soc_ana / tot_soc_pob) * 100.0, 2),
        'pct_alf7': round((tot_soc_alf / (tot_soc_alf + tot_soc_ana)) * 100.0, 2),
        'ocu': tot_soc_ocu,
        'pct_ocu': round((tot_soc_ocu / tot_soc_pob) * 100.0, 2),
    }
    print(f"Loaded INE Tecnologia/Educacion/Economia for 340/340 munis! Pob={tot_soc_pob:,} | Analfabeta={tot_soc_ana:,} ({soc_totals['pct_ana']}%) | Ocupada={tot_soc_ocu:,} ({soc_totals['pct_ocu']}%).")

    # === Exact 5-Step Puntaje de Brecha Digital (0 a 100) — Matches trazabilidad_brecha_digital.xlsx sheet 'Brecha digital' ===
    # Paso 1: % uso internet 7+ (INE Censo 2018) redondeado a 1 decimal
    # Paso 2: Posicion 1..340 de menor a mayor (empates comparten promedio, RANK.AVG ascendente)
    # Paso 3: Antenas por cada 10,000 habitantes (SIT 2026-S1 / Poblacion Censo 2018) -> posicion 1..340 de menor a mayor
    # Paso 4: Promedio de las dos posiciones
    # Paso 5: 100 * RANK.AVG(promedio, descendente) / 340 -> 100 = atender primero, cerca de 0 = menor brecha
    def excel_round1(x):
        return float(Decimal(str(x)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    def rank_avg_1based(vals, ascending=True):
        n = len(vals)
        indexed = sorted(enumerate(vals), key=lambda kv: kv[1], reverse=not ascending)
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and indexed[j+1][1] == indexed[i][1]:
                j += 1
            avg_r = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = avg_r
            i = j + 1
        return ranks

    sorted_gids = sorted(muni_geoms.keys())
    bd_uso_r = []
    bd_ant10k = []
    for gid in sorted_gids:
        uso_exact = 100.0 * ine_by_gid[gid]['pint'] / ine_by_gid[gid]['p7']
        bd_uso_r.append(excel_round1(uso_exact))
        ant26 = muni_rb[gid]['2026-S1']['v']
        pob18 = soc_by_gid[gid]['pob']
        bd_ant10k.append(10000.0 * ant26 / pob18)

    r_uso_bd = rank_avg_1based(bd_uso_r, ascending=True)
    r_ant_bd = rank_avg_1based(bd_ant10k, ascending=True)
    avg_pos_bd = [(r_uso_bd[i] + r_ant_bd[i]) / 2.0 for i in range(len(sorted_gids))]
    r_score_bd = rank_avg_1based(avg_pos_bd, ascending=False)

    bd_by_gid = {}
    bd_by_did = defaultdict(list)
    for idx, gid in enumerate(sorted_gids):
        sc = round(100.0 * r_score_bd[idx] / len(sorted_gids), 2)
        bd_by_gid[gid] = {
            'sc': sc,
            'uso': bd_uso_r[idx],
            'ru': round(r_uso_bd[idx], 1),
            'ant': round(bd_ant10k[idx], 2),
            'ra': round(r_ant_bd[idx], 1),
            'avg': round(avg_pos_bd[idx], 2),
        }
        bd_by_did[muni_geoms[gid]['ine_depto']].append(sc)
    # Assign 1..340 priority rank (1 = highest score)
    for rk, gid in enumerate(sorted(sorted_gids, key=lambda g: (-bd_by_gid[g]['sc'], g)), 1):
        bd_by_gid[gid]['rk'] = rk
    assert bd_by_gid[1608]['sc'] == 100.0 and bd_by_gid[102]['sc'] == 0.29, "Puntaje Brecha Digital calibration mismatch!"
    print(f"Computed exact 5-step Puntaje de Brecha Digital (0-100) for 340/340 munis! #1 Senahu={bd_by_gid[1608]['sc']} | #340 Sta. Catarina Pinula={bd_by_gid[102]['sc']}.")

    # === Compute Economic Saturation & Opportunity Index (ISI 0-100) + HHI + 3y Growth ===
    # Methodology: OECD Composite Indicators (percentile-rank normalization across 340 munis)
    # combining SIT 2026-S1 + KMZ 2026 + INE XII Censo Hogares + DOJ/FTC HHI
    def pct_ranks(values):
        n = len(values)
        indexed = sorted(enumerate(values), key=lambda x: x[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and indexed[j+1][1] == indexed[i][1]:
                j += 1
            avg_r = (i + j) / 2.0
            pct = (avg_r / (n - 1)) * 100.0 if n > 1 else 50.0
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = pct
            i = j + 1
        return ranks

    sorted_gids = sorted(muni_geoms.keys())
    raw_p1, raw_p2, raw_p3, raw_p4, raw_p5 = [], [], [], [], []
    eco_raw = {}
    for gid in sorted_gids:
        rb26 = muni_rb[gid]['2026-S1']['v']
        rb23 = muni_rb[gid]['2023-S1']['v']
        fx26 = muni_fixed[gid]['2026-S1']['t']
        lp_tot = max(1, lp_summary[gid]['tot'])
        ine_rec = ine_by_gid[gid]
        vals = [v for v in muni_fixed[gid]['2026-S1']['v'] if v is not None]
        n_ops = sum(1 for v in vals if v > 0)
        hhi = round(sum(((v / fx26) * 100.0) ** 2 for v in vals if v > 0), 1) if fx26 > 0 else None
        comp = (10000.0 - hhi) if hhi is not None else -1.0
        g3y = round(((rb26 - rb23) / rb23) * 100.0, 1) if rb23 > 0 else None
        raw_p1.append(rb26 / lp_tot)                    # 25% Cobertura móvil por comunidad
        raw_p2.append(ine_rec['pc'])                    # 25% Conectividad real en hogares (% con internet INE)
        raw_p3.append(fx26 / max(1, ine_rec['h']))      # 20% Penetración fija por hogar (SIT / INE)
        raw_p4.append(rb26)                             # 15% Escala absoluta de radiobases
        raw_p5.append(comp)                             # 15% Diversidad competitiva fija (10000 - HHI)
        eco_raw[gid] = {'hhi': hhi, 'n_ops': n_ops, 'g3y': g3y, 'rb_lp': round(rb26 / lp_tot, 3), 'lp_rb': round(lp_tot / rb26, 2) if rb26 > 0 else None}

    r_p1, r_p2, r_p3, r_p4, r_p5 = pct_ranks(raw_p1), pct_ranks(raw_p2), pct_ranks(raw_p3), pct_ranks(raw_p4), pct_ranks(raw_p5)
    eco_by_gid = {}
    for idx, gid in enumerate(sorted_gids):
        isi = round(0.25 * r_p1[idx] + 0.25 * r_p2[idx] + 0.20 * r_p3[idx] + 0.15 * r_p4[idx] + 0.15 * r_p5[idx], 1)
        tier = 2 if isi >= 75 else (1 if isi >= 45 else 0)
        er = eco_raw[gid]
        eco_by_gid[gid] = {
            'isi': isi, 'tier': tier,
            'p1': round(r_p1[idx], 1), 'p2': round(r_p2[idx], 1),
            'p3': round(r_p3[idx], 1), 'p4': round(r_p4[idx], 1), 'p5': round(r_p5[idx], 1),
            'hhi': er['hhi'], 'n_ops': er['n_ops'], 'g3y': er['g3y'],
            'rb_lp': er['rb_lp'], 'lp_rb': er['lp_rb']
        }

    munis_list = []
    for gid in sorted_gids:
        g = muni_geoms[gid]
        sit_d, sit_m = sit_canonical_name[gid]
        cab = cabecera_gps[gid]
        munis_list.append({
            'id': gid, 'did': g['ine_depto'], 'dep': sit_d, 'nom': sit_m,
            'd': g['d'], 'bb': g['bb'], 'c': g['c'],
            'gps': [cab['lon'], cab['lat'], cab['src']],
            'area': kmz_area.get(gid),
            'lp_sum': lp_summary[gid],
            'ine': ine_by_gid[gid],
            'soc': soc_by_gid[gid],
            'bd': bd_by_gid[gid],
            'eco': eco_by_gid[gid],
            'fx': muni_fixed[gid], 'rb': muni_rb[gid],
        })

    deptos_list = []
    for did in sorted(depto_geoms.keys()):
        g = depto_geoms[did]
        deptos_list.append({
            'id': did, 'nom': g['name'], 'd': g['d'], 'bb': g['bb'], 'c': g['c'],
            'ine': dict(ine_by_did[did]),
            'ine23': ine23_by_did[did],
            'soc': dict(soc_by_did[did]),
            'bd_avg': round(sum(bd_by_did[did]) / len(bd_by_did[did]), 1),
            'fx': depto_fixed[did], 'rb': depto_rb[did], 'sp': special_localities.get(did, []),
        })

    payload = {
        'meta': {
            'source_file': 'Consolidado Histórico de Boletines Estadísticos de Telecomunicaciones 2014-2026',
            'ine_file': 'BrechaDigitalConectividadDigitalEnHogaresMunicipio.xlsx',
            'traz_file': 'trazabilidad_brecha_digital.xlsx',
            'edu_eco_file': 'DatosEstadisticos_tecnologia_educacion_economico.xlsx',
            'ine_totals': {'h': tot_h_nac, 'con': tot_con_nac, 'sin': tot_sin_nac, 'br': nat_br18, 'pc': round(100.0 - nat_br18, 2), 'uso': nat_uso18},
            'ine23_totals': {'h': tot23_h, 'con': tot23_con, 'sin': tot23_sin, 'br': nat_br23, 'pc': round(100.0 - nat_br23, 2), 'dbr': round(nat_br23 - nat_br18, 2), 'uso': nat_uso23, 'duso': round(nat_uso23 - nat_uso18, 2)},
            'soc_totals': soc_totals,
            'periods_ine': ['2018', '2023'],
            'kmz_munis': 'Copia de Municipios.kmz',
            'kmz_lp': 'Copia de Lugares Poblados 2026.kmz',
            'total_lp': total_lp,
            'svg_w': svg_w, 'svg_h': svg_h,
            'proj': proj_params,
            'op_names': op_names,
            'periods_fx': periods_08, 'periods_rb': periods_09,
            'pdfs': pdf_files,
            'lp_cats': raw_cats,
            'lp_groups': CAT_GROUPS,
        },
        'lakes': lakes,
        'deptos': deptos_list,
        'munis': munis_list,
        'lp': {str(gid): lp_by_muni[gid] for gid in sorted(muni_geoms.keys())},
        'national': {
            'serie': serie_hist,
            'fixed_ops': dict(fixed_ops),
            'mobile_ops': {k: dict(v) for k, v in mobile_ops.items()},
            'internet_etm': {k: dict(v) for k, v in internet_etm.items()},
            'tarifas_latest': tarifas_latest,
            'control_num': control_num,
            'conciliacion': conciliacion,
            'control_terr': control_territorial,
        }
    }

    out_json = os.path.join(OUT_DIR, 'sit_data_bundle.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Wrote {out_json} ({os.path.getsize(out_json)/1024:.1f} KB)")

if __name__ == '__main__':
    main()
