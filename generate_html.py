import json, os

OUT_DIR = "/Users/jaredruiz/.gemini/antigravity/scratch/innovacon-mapa-sit"
DATA_PATH = os.path.join(OUT_DIR, "sit_data_bundle.json")
HTML_PATH = os.path.join(OUT_DIR, "mapa_sit_guatemala.html")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data_json = f.read()

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<meta name="theme-color" content="#0f172a" />
<meta name="description" content="Mapa interactivo oficial de los 340 municipios de Guatemala con datos SIT (2014–2026), 27,352 lugares poblados GPS e Índice de Saturación Económica (ISI)." />
<title>Observatorio Geoespacial SIT Guatemala · Mapa Interactivo y Decisión Económica</title>
<style>
  :root {
    --bg: #f1f5f9;
    --surface: #ffffff;
    --surface-2: #f8fafc;
    --border: #e2e8f0;
    --border-strong: #cbd5e1;
    --ink: #0f172a;
    --ink-2: #334155;
    --muted: #64748b;
    --accent: #0284c7;
    --accent-dark: #0369a1;
    --accent-soft: #e0f2fe;
    --teal: #0d9488;
    --teal-soft: #ccfbf1;
    --emerald: #059669;
    --emerald-soft: #d1fae5;
    --amber: #d97706;
    --amber-soft: #fef3c7;
    --red: #dc2626;
    --red-soft: #fee2e2;
    --purple: #6d28d9;
    --purple-soft: #ede9fe;
    --shadow-sm: 0 1px 2px rgba(15,23,42,.06);
    --shadow: 0 4px 14px rgba(15,23,42,.08);
    --shadow-lg: 0 14px 36px rgba(15,23,42,.18);
    --radius: 12px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--ink);
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }
  .num { font-variant-numeric: tabular-nums; }
  .app { display: flex; flex-direction: column; height: 100vh; width: 100%; max-width: 100vw; overflow-x: hidden; }

  /* ===== HEADER ===== */
  header.topbar {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0c4a6e 100%);
    color: #fff;
    height: 54px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    flex-shrink: 0;
    box-shadow: 0 2px 10px rgba(15,23,42,.18);
    z-index: 30;
  }
  .brand { display: flex; align-items: center; gap: 10px; min-width: 0; flex-shrink: 1; }
  .brand-mark {
    width: 34px; height: 34px; border-radius: 9px;
    background: linear-gradient(135deg, #38bdf8, #0284c7);
    display: grid; place-items: center;
    font-weight: 800; font-size: 13.5px; letter-spacing: -0.5px; flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(56,189,248,.35);
  }
  .brand-text { min-width: 0; }
  .brand-text h1 { font-size: 14.5px; font-weight: 700; letter-spacing: -0.01em; line-height: 1.15; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .brand-text p { font-size: 10.5px; color: #94a3b8; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  .nav-tabs { display: flex; background: rgba(255,255,255,.1); padding: 3px; border-radius: 9px; gap: 3px; flex-shrink: 0; }
  .nav-tab {
    border: none; background: transparent; color: #cbd5e1;
    font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 7px;
    cursor: pointer; transition: all .14s ease; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap;
  }
  .nav-tab svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  .nav-tab:hover { background: rgba(255,255,255,.12); color: #fff; }
  .nav-tab.active { background: #ffffff; color: #0f172a; box-shadow: var(--shadow-sm); }

  .header-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
  .btn-excel-hero {
    border: none; background: #10b981; color: #fff;
    font-size: 12px; font-weight: 700; padding: 7px 13px; border-radius: 8px;
    cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
    box-shadow: 0 2px 8px rgba(16,185,129,.35); transition: background .15s; white-space: nowrap;
  }
  .btn-excel-hero:hover { background: #059669; }
  .btn-excel-hero svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2.2; }

  .verified-chip {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 10.5px; font-weight: 600;
    background: rgba(16,185,129,.15); border: 1px solid rgba(52,211,153,.35);
    color: #a7f3d0; padding: 4px 9px; border-radius: 999px; white-space: nowrap;
  }
  .verified-dot { width: 6px; height: 6px; border-radius: 50%; background: #34d399; }

  /* ===== VIEWS ===== */
  .view-container { flex: 1; min-height: 0; display: none; overflow: hidden; }
  .view-container.active { display: flex; }

  /* ===== MAP VIEW ===== */
  #view-map { flex-direction: row; }
  .map-column {
    flex: 1; min-width: 0; display: flex; flex-direction: column;
    background: #eef4f9;
  }

  /* KPI Strip (clean, spacious, non-truncating) */
  .kpi-strip {
    display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px;
    padding: 8px 12px; background: #ffffff; border-bottom: 1px solid var(--border); flex-shrink: 0;
  }
  .kpi-mini {
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 9px;
    padding: 7px 10px; display: flex; flex-direction: column; gap: 1px;
  }
  .kpi-mini .lbl { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .03em; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .kpi-mini .val { font-size: 17px; font-weight: 800; color: var(--ink); letter-spacing: -0.02em; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .kpi-mini .sub { font-size: 10.5px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .kpi-mini.clickable { cursor: pointer; transition: border-color .14s, background .14s; }
  .kpi-mini.clickable:hover { border-color: var(--accent); background: #f0f9ff; }

  /* Dedicated Control Bar ABOVE the map (NEVER overlaps Guatemala!) */
  .map-toolbar {
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
    gap: 8px; padding: 8px 12px; background: #f8fafc; border-bottom: 1px solid var(--border);
    flex-shrink: 0; z-index: 18;
  }
  .tb-group { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
  .search-wrap { position: relative; width: 225px; }
  .search-input {
    width: 100%; height: 32px; padding: 0 26px 0 30px; border-radius: 8px;
    border: 1px solid var(--border-strong); background: #ffffff;
    font-size: 12.5px; color: var(--ink); outline: none; transition: border-color .14s;
  }
  .search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(2,132,199,.14); }
  .search-icon { position: absolute; left: 9px; top: 50%; transform: translateY(-50%); color: var(--muted); pointer-events: none; display: flex; }
  .search-icon svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2; }
  .search-clear { position: absolute; right: 7px; top: 50%; transform: translateY(-50%); border: none; background: none; color: var(--muted); cursor: pointer; font-size: 13px; display: none; }
  .search-results {
    position: absolute; top: 36px; left: 0; right: 0; background: #fff;
    border: 1px solid var(--border-strong); border-radius: 9px; box-shadow: var(--shadow-lg);
    max-height: 280px; overflow-y: auto; display: none; z-index: 60;
  }
  .search-results.open { display: block; }
  .search-item { padding: 7px 10px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 8px; border-bottom: 1px solid #f1f5f9; font-size: 12px; }
  .search-item:last-child { border-bottom: none; }
  .search-item:hover { background: var(--accent-soft); }
  .search-item .si-sub { font-size: 10.5px; color: var(--muted); }
  .search-item .si-tag { font-size: 9.5px; font-weight: 700; padding: 2px 6px; border-radius: 5px; background: #f1f5f9; color: var(--ink-2); flex-shrink: 0; }
  .search-item .si-tag.dept { background: var(--teal-soft); color: #0f766e; }

  .ctrl-select {
    height: 32px; padding: 0 8px; border-radius: 8px;
    border: 1px solid var(--border-strong); background: #ffffff;
    font-size: 12px; font-weight: 600; color: var(--ink); cursor: pointer; outline: none;
    max-width: 245px;
  }
  .ctrl-select:focus { border-color: var(--accent); }

  .timeline-inline {
    display: flex; align-items: center; gap: 6px;
    background: #ffffff; border: 1px solid var(--border-strong); border-radius: 8px;
    padding: 2px 6px; height: 32px;
  }
  .play-btn {
    height: 24px; padding: 0 8px; border-radius: 6px; border: none;
    background: var(--accent); color: #fff; font-size: 11px; font-weight: 700;
    cursor: pointer; display: inline-flex; align-items: center; gap: 4px;
  }
  .play-btn:hover { background: var(--accent-dark); }
  .play-btn.playing { background: var(--red); }
  .play-btn:disabled, .step-btn:disabled { opacity: 0.35; cursor: not-allowed; }
  .step-btn { width: 22px; height: 22px; border-radius: 5px; border: 1px solid var(--border); background: var(--surface-2); color: var(--ink); font-size: 10px; font-weight: 700; cursor: pointer; }
  .step-btn:hover { background: #e2e8f0; }
  input[type=range].period-slider { width: 92px; accent-color: var(--accent); cursor: pointer; }
  .period-pill { font-size: 11.5px; font-weight: 800; color: var(--accent-dark); background: var(--accent-soft); padding: 2px 8px; border-radius: 5px; min-width: 64px; text-align: center; }

  /* Pure Unobstructed Map Stage */
  .map-stage {
    flex: 1; min-height: 0; position: relative; overflow: hidden; user-select: none; cursor: grab;
    background: radial-gradient(circle at 46% 48%, #ffffff 0%, #eef5fb 65%, #e2edf6 100%);
  }
  .map-stage.dragging { cursor: grabbing; }
  .map-stage svg#gt-map { width: 100%; height: 100%; display: block; }

  /* SVG Map Layers */
  .muni-path { stroke: #ffffff; stroke-width: 0.45; stroke-linejoin: round; cursor: pointer; transition: opacity .15s, fill .22s; }
  .muni-path:hover { stroke: #0f172a; stroke-width: 1.4; }
  .muni-path.dimmed { opacity: 0.2; }
  .muni-path.selected { stroke: #f59e0b; stroke-width: 2.3; filter: drop-shadow(0 0 4px rgba(245,158,11,.55)); }
  .muni-path.compare-selected { stroke: #7c3aed; stroke-width: 2.3; filter: drop-shadow(0 0 4px rgba(124,58,237,.5)); }
  .depto-outline { fill: none; stroke: #1e293b; stroke-width: 1.05; stroke-opacity: 0.58; pointer-events: none; stroke-linejoin: round; }
  .depto-outline.focused { stroke: #0284c7; stroke-width: 2.1; stroke-opacity: 0.95; }
  svg#gt-map.depto-level-mode .muni-path { stroke-opacity: 0.28; stroke-width: 0.35; }
  svg#gt-map.depto-level-mode .depto-outline { stroke: #0f172a; stroke-width: 1.45; stroke-opacity: 0.85; }
  .granularity-pill { display: inline-flex; align-items: center; gap: 5px; padding: 2px 8px; border-radius: 999px; font-size: 10.5px; font-weight: 700; background: #fff1f2; color: #9f1239; border: 1px solid #fecdd3; }
  .granularity-pill.muni-lvl { background: #f0fdfa; color: #0f766e; border-color: #99f6e4; }
  .lake-path { fill: #7dd3fc; stroke: #0284c7; stroke-width: 0.6; opacity: 0.85; pointer-events: none; }
  .depto-label {
    font-size: 8px; font-weight: 700; fill: #1e293b; text-anchor: middle; pointer-events: none;
    paint-order: stroke; stroke: rgba(255,255,255,0.92); stroke-width: 2.6px; stroke-linejoin: round;
    letter-spacing: 0.03em; text-transform: uppercase;
  }

  .cab-pin { fill: #0f172a; stroke: #ffffff; stroke-width: 0.7; opacity: 0.8; cursor: pointer; }
  .cab-pin:hover { fill: #f59e0b; opacity: 1; }
  .lp-dot { stroke: #ffffff; stroke-width: 0.45; cursor: pointer; opacity: 0.94; }
  .lp-dot:hover { stroke: #0f172a; stroke-width: 1.1; opacity: 1; }
  .lp-pulse { fill: none; stroke: #e11d48; stroke-width: 1.8; pointer-events: none; animation: lpPulse 1.3s ease-out infinite; }
  @keyframes lpPulse { 0% { opacity: 1; transform: scale(1); } 100% { opacity: 0; transform: scale(3.2); } }

  /* Minimal corner controls inside empty map margins */
  .map-tools { position: absolute; top: 12px; right: 12px; display: flex; flex-direction: column; gap: 6px; z-index: 12; }
  .tool-group {
    background: rgba(255,255,255,.94); border: 1px solid var(--border-strong); border-radius: 8px;
    box-shadow: var(--shadow-sm); display: flex; flex-direction: column; overflow: hidden;
  }
  .tool-btn {
    width: 32px; height: 32px; border: none; background: transparent; color: var(--ink-2);
    font-size: 13px; font-weight: 700; cursor: pointer; display: grid; place-items: center;
    border-bottom: 1px solid var(--border); transition: background .12s;
  }
  .tool-btn:last-child { border-bottom: none; }
  .tool-btn:hover { background: var(--accent-soft); color: var(--accent-dark); }
  .tool-btn.active { background: var(--accent); color: #fff; }
  .tool-btn svg { width: 15px; height: 15px; stroke: currentColor; fill: none; stroke-width: 2; }

  .compare-banner {
    position: absolute; top: 12px; left: 12px; background: #5b21b6; color: #fff;
    padding: 7px 12px; border-radius: 8px; font-size: 12px; font-weight: 600;
    display: none; align-items: center; gap: 10px; box-shadow: var(--shadow); z-index: 15;
  }
  .compare-banner.open { display: flex; }
  .compare-banner button { border: none; background: rgba(255,255,255,.22); color: #fff; padding: 3px 8px; border-radius: 5px; cursor: pointer; font-weight: 700; font-size: 11px; }

  /* Clean Bottom Status & Legend Bar BELOW Map (zero overlap!) */
  .map-footer {
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    padding: 6px 14px; background: #ffffff; border-top: 1px solid var(--border);
    flex-shrink: 0; flex-wrap: wrap;
  }
  .legend-inline { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .legend-lbl { font-size: 11px; font-weight: 700; color: var(--ink-2); }
  .legend-bar-wrap { display: flex; align-items: center; gap: 6px; }
  .legend-swatches { display: flex; gap: 2px; width: 136px; height: 10px; border-radius: 3px; overflow: hidden; }
  .legend-swatches span { flex: 1; }
  .legend-end { font-size: 10.5px; color: var(--muted); font-variant-numeric: tabular-nums; font-weight: 600; }
  .legend-nodata { display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px; color: var(--muted); padding-left: 8px; border-left: 1px solid var(--border); }
  .nodata-box { width: 12px; height: 9px; border-radius: 2px; background: repeating-linear-gradient(45deg, #e2e8f0, #e2e8f0 2.5px, #cbd5e1 2.5px, #cbd5e1 5px); border: 1px solid #94a3b8; }
  .gps-pill { font-size: 11px; font-weight: 600; color: var(--muted); font-variant-numeric: tabular-nums; display: inline-flex; align-items: center; gap: 5px; }

  /* Tooltip */
  #map-tooltip {
    position: fixed; pointer-events: none; z-index: 100;
    background: rgba(15, 23, 42, 0.96); color: #fff; padding: 9px 12px; border-radius: 9px;
    font-size: 12px; box-shadow: var(--shadow-lg); min-width: 205px; max-width: 290px;
    display: none; border: 1px solid rgba(255,255,255,.12);
  }
  #map-tooltip .tt-title { font-weight: 700; font-size: 13px; line-height: 1.2; }
  #map-tooltip .tt-dept { font-size: 10.5px; color: #94a3b8; margin-top: 2px; }
  #map-tooltip .tt-val { margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,.12); display: flex; justify-content: space-between; align-items: baseline; gap: 10px; }
  #map-tooltip .tt-num { font-size: 14.5px; font-weight: 800; color: #38bdf8; }

  /* ===== RIGHT INSPECTOR ===== */
  aside.inspector {
    width: 435px; max-width: 42vw; background: var(--surface); border-left: 1px solid var(--border);
    display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0; z-index: 20;
    box-shadow: -4px 0 18px rgba(15,23,42,.04);
  }
  .inspector-scroll { flex: 1; overflow-y: auto; padding: 14px 16px 24px; display: flex; flex-direction: column; gap: 12px; }
  .ins-header { display: flex; flex-direction: column; gap: 6px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
  .ins-crumbs { display: flex; align-items: center; justify-content: space-between; gap: 6px; flex-wrap: wrap; }
  .pill { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 999px; font-size: 10.5px; font-weight: 700; background: var(--accent-soft); color: var(--accent-dark); border: none; }
  .pill.clickable { cursor: pointer; }
  .pill.clickable:hover { background: #bae6fd; }
  .pill.ine { background: #f1f5f9; color: var(--muted); }
  .pill.ok { background: var(--emerald-soft); color: #065f46; }
  .pill.warn { background: var(--amber-soft); color: #92400e; }
  .pill.danger { background: var(--red-soft); color: #991b1b; }
  .ins-title { font-size: 20px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.15; color: var(--ink); }
  .ins-actions { display: flex; gap: 5px; flex-wrap: wrap; margin-top: 2px; }
  .btn-sm {
    border: 1px solid var(--border-strong); background: #fff; color: var(--ink-2);
    font-size: 11px; font-weight: 600; padding: 5px 8px; border-radius: 7px;
    cursor: pointer; display: inline-flex; align-items: center; gap: 4px; transition: all .12s; text-decoration: none;
  }
  .btn-sm:hover { border-color: var(--accent); color: var(--accent-dark); background: var(--accent-soft); }
  .btn-sm.green { border-color: #10b981; background: #ecfdf5; color: #047857; }
  .btn-sm.green:hover { background: #10b981; color: #fff; }
  .btn-sm.purple:hover { border-color: var(--purple); background: var(--purple); color: #fff; }

  /* Sub-tabs inside Municipal Dossier */
  .sub-tabs { display: flex; background: #f1f5f9; padding: 3px; border-radius: 8px; gap: 3px; }
  .sub-tab {
    flex: 1; border: none; background: transparent; color: var(--muted);
    font-size: 11.5px; font-weight: 700; padding: 6px 6px; border-radius: 6px; cursor: pointer; transition: all .12s;
  }
  .sub-tab.active { background: #ffffff; color: var(--ink); box-shadow: var(--shadow-sm); }

  /* Economic Saturation & Recommendation Hero Card */
  .eco-card {
    border-radius: 11px; padding: 12px 13px; border: 1px solid var(--border);
    display: flex; flex-direction: column; gap: 9px;
  }
  .eco-card.tier-2 { background: linear-gradient(135deg, #fff5f5 0%, #ffffff 65%); border-color: #fecaca; }
  .eco-card.tier-1 { background: linear-gradient(135deg, #fffbeb 0%, #ffffff 65%); border-color: #fde68a; }
  .eco-card.tier-0 { background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 65%); border-color: #a7f3d0; }
  .eco-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
  .eco-score-wrap { display: flex; align-items: baseline; gap: 6px; }
  .eco-score { font-size: 26px; font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
  .eco-card.tier-2 .eco-score { color: #b91c1c; }
  .eco-card.tier-1 .eco-score { color: #b45309; }
  .eco-card.tier-0 .eco-score { color: #047857; }
  .eco-gauge-track {
    position: relative; height: 9px; border-radius: 99px;
    background: linear-gradient(90deg, #10b981 0%, #10b981 44%, #f59e0b 45%, #f59e0b 74%, #ef4444 75%, #b91c1c 100%);
  }
  .eco-needle {
    position: absolute; top: -3px; width: 6px; height: 15px; border-radius: 3px;
    background: #0f172a; border: 1.5px solid #ffffff; transform: translateX(-50%);
    box-shadow: 0 1px 4px rgba(0,0,0,.35);
  }
  .eco-scale-lbls { display: flex; justify-content: space-between; font-size: 9.5px; color: var(--muted); font-weight: 600; margin-top: 3px; }
  .eco-summary { font-size: 12px; color: var(--ink-2); line-height: 1.45; }
  .eco-recs { display: flex; flex-direction: column; gap: 6px; }
  .eco-rec-box {
    background: rgba(255,255,255,.85); border: 1px solid rgba(15,23,42,.08);
    border-radius: 8px; padding: 7px 9px; font-size: 11.5px; line-height: 1.4; color: var(--ink-2);
  }
  .eco-rec-box strong { color: var(--ink); }
  .eco-pillars-mini { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; padding-top: 4px; }
  .eco-p-item { background: rgba(255,255,255,.75); border: 1px solid rgba(15,23,42,.06); border-radius: 7px; padding: 5px 8px; }
  .eco-p-item .pl { font-size: 9.5px; color: var(--muted); font-weight: 700; text-transform: uppercase; }
  .eco-p-item .pv { font-size: 12px; font-weight: 800; color: var(--ink); margin-top: 1px; }

  .stat-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }
  .stat-box { background: var(--surface-2); border: 1px solid var(--border); border-radius: 10px; padding: 9px 11px; }
  .stat-box .s-lbl { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); display: flex; justify-content: space-between; gap: 4px; }
  .stat-box .s-val { font-size: 20px; font-weight: 800; color: var(--ink); margin: 3px 0 2px; letter-spacing: -0.02em; }
  .stat-box .s-meta { font-size: 10.5px; color: var(--muted); line-height: 1.35; }
  .delta-up { color: #059669; font-weight: 700; }
  .delta-down { color: #dc2626; font-weight: 700; }
  .delta-flat { color: var(--muted); font-weight: 600; }

  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 11px 13px; }
  .card-hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; gap: 8px; }
  .card-hd h3 { font-size: 12px; font-weight: 800; color: var(--ink); }
  .card-hd span { font-size: 10.5px; color: var(--muted); font-weight: 600; }

  .op-list { display: flex; flex-direction: column; gap: 7px; }
  .op-row { display: flex; flex-direction: column; gap: 3px; }
  .op-top { display: flex; justify-content: space-between; font-size: 11.5px; gap: 8px; }
  .op-name { font-weight: 600; color: var(--ink-2); }
  .op-nums { font-weight: 700; color: var(--ink); white-space: nowrap; }
  .op-nums small { font-weight: 500; color: var(--muted); margin-left: 3px; }
  .bar-track { height: 7px; background: #eef2f6; border-radius: 99px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 99px; }
  .op-zero-note { margin-top: 7px; font-size: 10.5px; color: var(--muted); line-height: 1.4; }

  .geo-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 9px; padding: 8px 9px; }
  .geo-cell .gl { font-size: 9.5px; font-weight: 700; text-transform: uppercase; color: #0369a1; }
  .geo-cell .gv { font-size: 12px; font-weight: 800; color: var(--ink); margin-top: 2px; }
  .geo-cell .gs { font-size: 10px; color: var(--muted); }

  .lp-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 7px; }
  .lp-chip { border: 1px solid var(--border-strong); background: #fff; color: var(--ink-2); font-size: 10px; font-weight: 700; padding: 3px 7px; border-radius: 999px; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; }
  .lp-chip.active { background: #0f172a; color: #fff; border-color: #0f172a; }
  .lp-dot-swatch { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
  .lp-list { max-height: 250px; overflow-y: auto; border: 1px solid var(--border); border-radius: 8px; background: var(--surface-2); }
  .lp-row { padding: 6px 9px; border-bottom: 1px solid #eef2f6; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 8px; font-size: 11.5px; }
  .lp-row:last-child { border-bottom: none; }
  .lp-row:hover { background: var(--accent-soft); }
  .lp-row-name { font-weight: 600; color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .lp-row-meta { font-size: 10px; color: var(--muted); white-space: nowrap; }

  .chart-svg { width: 100%; height: auto; display: block; overflow: visible; }
  .chart-note { font-size: 10.5px; color: var(--muted); margin-top: 5px; line-height: 1.4; }
  .audit-box { background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 9px; padding: 10px 12px; font-size: 11px; color: var(--ink-2); line-height: 1.5; }
  .audit-box strong { color: var(--ink); }
  .audit-row { margin-top: 4px; }
  .audit-note { margin-top: 7px; padding: 7px 9px; border-radius: 7px; background: var(--amber-soft); color: #78350f; font-size: 11px; line-height: 1.4; }
  .formula-box { background: #0f172a; color: #e2e8f0; border-radius: 8px; padding: 9px 11px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; line-height: 1.5; margin: 7px 0; overflow-x: auto; }

  .rank-list { display: flex; flex-direction: column; gap: 5px; }
  .rank-item { display: flex; align-items: center; justify-content: space-between; padding: 6.5px 9px; border-radius: 8px; background: var(--surface-2); border: 1px solid transparent; cursor: pointer; gap: 8px; font-size: 11.5px; transition: all .12s; }
  .rank-item:hover { background: var(--accent-soft); border-color: #7dd3fc; }
  .rank-left { display: flex; align-items: center; gap: 8px; min-width: 0; }
  .rank-num { width: 21px; height: 21px; border-radius: 6px; background: #e2e8f0; color: var(--ink-2); font-size: 10.5px; font-weight: 800; display: grid; place-items: center; flex-shrink: 0; }
  .rank-item:nth-child(1) .rank-num { background: #fef08a; color: #854d0e; }
  .rank-item:nth-child(2) .rank-num { background: #e2e8f0; color: #334155; }
  .rank-item:nth-child(3) .rank-num { background: #fed7aa; color: #9a3412; }
  .rank-name { font-weight: 700; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .rank-sub { font-size: 10px; color: var(--muted); }
  .rank-val { font-weight: 800; color: var(--accent-dark); white-space: nowrap; }

  .cmp-table { width: 100%; border-collapse: collapse; font-size: 11px; }
  .cmp-table th, .cmp-table td { padding: 5.5px 5px; border-bottom: 1px solid var(--border); text-align: right; }
  .cmp-table th:first-child, .cmp-table td:first-child { text-align: left; }
  .cmp-table th { font-size: 10px; text-transform: uppercase; color: var(--muted); font-weight: 700; }

  /* ===== TABLE & NATIONAL VIEWS ===== */
  #view-table, #view-national { flex-direction: column; overflow-y: auto; padding: 16px 20px 30px; gap: 14px; background: var(--bg); }
  .panel-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; box-shadow: var(--shadow-sm); }
  .toolbar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; margin-bottom: 10px; }
  .toolbar-left { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .table-scroll { overflow: auto; max-height: calc(100vh - 210px); border: 1px solid var(--border); border-radius: 9px; }
  table.data-table { width: 100%; border-collapse: collapse; font-size: 12px; }
  table.data-table thead th {
    position: sticky; top: 0; background: #f8fafc; border-bottom: 2px solid var(--border-strong);
    padding: 8px 9px; text-align: right; font-size: 10.5px; font-weight: 700; text-transform: uppercase;
    color: var(--ink-2); cursor: pointer; white-space: nowrap; user-select: none;
  }
  table.data-table thead th:nth-child(1),
  table.data-table thead th:nth-child(2),
  table.data-table thead th:nth-child(3) { text-align: left; }
  table.data-table thead th:hover { background: #e2e8f0; }
  table.data-table tbody td { padding: 7px 9px; border-bottom: 1px solid #f1f5f9; text-align: right; white-space: nowrap; }
  table.data-table tbody td:nth-child(1),
  table.data-table tbody td:nth-child(2),
  table.data-table tbody td:nth-child(3) { text-align: left; }
  table.data-table tbody tr:hover { background: #f0f9ff; }
  .jump-btn { border: 1px solid var(--accent); background: var(--accent-soft); color: var(--accent-dark); font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 6px; cursor: pointer; }
  .jump-btn:hover { background: var(--accent); color: #fff; }

  .nat-banner { background: linear-gradient(90deg, #eff6ff, #f0fdfa); border: 1px solid #bae6fd; border-radius: 10px; padding: 11px 14px; font-size: 12px; color: #0c4a6e; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
  .nat-kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(185px, 1fr)); gap: 10px; }
  .nat-grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 14px; }

  /* ===== EXCEL EXPORT MODAL ===== */
  .modal-backdrop {
    position: fixed; inset: 0; background: rgba(15,23,42,.55); backdrop-filter: blur(3px);
    display: none; place-items: center; z-index: 200; padding: 16px;
  }
  .modal-backdrop.open { display: grid; }
  .modal {
    background: #ffffff; border-radius: 14px; width: 560px; max-width: 100%; max-height: 90vh;
    overflow: hidden; display: flex; flex-direction: column; box-shadow: var(--shadow-lg);
    border: 1px solid var(--border);
  }
  .modal-hd {
    padding: 14px 18px; background: #0f172a; color: #fff;
    display: flex; justify-content: space-between; align-items: center;
  }
  .modal-hd h2 { font-size: 15px; font-weight: 800; }
  .modal-close { border: none; background: rgba(255,255,255,.15); color: #fff; width: 28px; height: 28px; border-radius: 7px; cursor: pointer; font-weight: 700; }
  .modal-body { padding: 16px 18px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; }
  .exp-modes { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .exp-mode-btn {
    border: 1.5px solid var(--border-strong); background: var(--surface-2); border-radius: 10px;
    padding: 10px 12px; text-align: left; cursor: pointer; transition: all .14s;
  }
  .exp-mode-btn:hover { border-color: var(--accent); background: #f0f9ff; }
  .exp-mode-btn.active { border-color: var(--emerald); background: #ecfdf5; box-shadow: 0 0 0 2px rgba(16,185,129,.2); }
  .exp-mode-btn .em-t { font-size: 12.5px; font-weight: 800; color: var(--ink); }
  .exp-mode-btn .em-s { font-size: 10.5px; color: var(--muted); margin-top: 2px; line-height: 1.3; }
  .exp-config { background: var(--surface-2); border: 1px solid var(--border); border-radius: 10px; padding: 12px; display: flex; flex-direction: column; gap: 10px; }
  .exp-field label { display: block; font-size: 11px; font-weight: 700; color: var(--ink-2); margin-bottom: 4px; }
  .exp-field select, .exp-field input { width: 100%; height: 34px; padding: 0 10px; border-radius: 7px; border: 1px solid var(--border-strong); background: #fff; font-size: 12.5px; }
  .cmp-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
  .cmp-chip { display: inline-flex; align-items: center; gap: 6px; background: var(--purple-soft); color: var(--purple); font-size: 11.5px; font-weight: 700; padding: 4px 9px; border-radius: 999px; }
  .cmp-chip button { border: none; background: none; color: var(--purple); cursor: pointer; font-weight: 800; }
  .exp-sheets-preview { font-size: 11px; color: var(--muted); line-height: 1.5; background: #ffffff; border: 1px dashed var(--border-strong); border-radius: 8px; padding: 8px 10px; }
  .modal-ft { padding: 12px 18px; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; gap: 8px; background: var(--surface-2); }
  .btn-primary-green {
    border: none; background: var(--emerald); color: #fff; font-size: 13px; font-weight: 700;
    padding: 9px 18px; border-radius: 8px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
  }
  .btn-primary-green:hover { background: #047857; }

  .nav-tab.guide-tab { color: #7dd3fc; }
  .nav-tab.guide-tab:hover { color: #ffffff; background: rgba(56,189,248,.22); }
  .nav-tab.guide-tab.active { background: #ffffff !important; color: #0f172a !important; }

  /* Plain-language narrative & guide styles */
  .story-box {
    background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
    border: 1px solid #bae6fd; border-left: 4px solid #0284c7;
    border-radius: 9px; padding: 10px 12px; font-size: 12px; color: var(--ink-2); line-height: 1.5;
  }
  .story-box .st-hd {
    font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em;
    color: #0369a1; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;
  }
  .story-box strong { color: var(--ink); }
  .help-q {
    display: inline-grid; place-items: center; width: 15px; height: 15px; border-radius: 50%;
    background: #e2e8f0; color: #334155; font-size: 10px; font-weight: 800; cursor: help;
    margin-left: 4px; vertical-align: middle; line-height: 1;
  }
  .help-q:hover { background: var(--accent); color: #fff; }
  .guide-link-inline {
    border: none; background: none; color: var(--accent-dark); font-size: 10.5px; font-weight: 700;
    cursor: pointer; text-decoration: underline; padding: 0;
  }

  /* VIEW 4: GUÍA / MANUAL NARRATIVO */
  #view-guide {
    flex-direction: column; overflow-y: auto; padding: 18px 22px 36px; gap: 16px; background: var(--bg);
  }
  .guide-shell { max-width: 1180px; width: 100%; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; }
  .guide-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #0369a1 100%);
    color: #fff; border-radius: 14px; padding: 22px 24px;
    display: flex; justify-content: space-between; align-items: center; gap: 18px; flex-wrap: wrap;
    box-shadow: var(--shadow);
  }
  .guide-hero h2 { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 6px; }
  .guide-hero p { font-size: 13.5px; color: #dbeafe; max-width: 720px; line-height: 1.5; }
  .guide-sec-title { font-size: 16px; font-weight: 800; color: var(--ink); margin-bottom: 4px; letter-spacing: -0.01em; }
  .guide-sec-sub { font-size: 12.5px; color: var(--muted); margin-bottom: 12px; }
  .persona-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
  .persona-card {
    background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 15px 16px;
    display: flex; flex-direction: column; gap: 9px; box-shadow: var(--shadow-sm);
  }
  .persona-tag {
    display: inline-flex; align-items: center; gap: 6px; width: fit-content;
    font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em;
    padding: 3px 9px; border-radius: 999px;
  }
  .persona-card h3 { font-size: 15px; font-weight: 800; color: var(--ink); }
  .persona-card p { font-size: 12.5px; color: var(--ink-2); line-height: 1.5; }
  .persona-steps { padding-left: 16px; font-size: 12px; color: var(--ink-2); line-height: 1.55; display: flex; flex-direction: column; gap: 3px; }
  .persona-actions { display: flex; flex-wrap: wrap; gap: 6px; margin-top: auto; padding-top: 6px; }

  .glossary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 11px; }
  .gloss-card {
    background: #fff; border: 1px solid var(--border); border-radius: 11px; padding: 13px 14px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .gloss-card .gc-term { font-size: 13.5px; font-weight: 800; color: var(--ink); display: flex; justify-content: space-between; align-items: center; gap: 6px; }
  .gloss-card .gc-plain { font-size: 12px; color: var(--ink-2); line-height: 1.5; }
  .gloss-card .gc-ex { font-size: 11px; color: var(--muted); background: var(--surface-2); border-radius: 7px; padding: 6px 8px; border: 1px solid var(--border); line-height: 1.4; }

  .steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 11px; }
  .step-card {
    background: #fff; border: 1px solid var(--border); border-radius: 11px; padding: 13px 14px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .step-badge {
    width: 26px; height: 26px; border-radius: 8px; background: var(--accent); color: #fff;
    font-size: 12.5px; font-weight: 800; display: grid; place-items: center;
  }
  .step-card h4 { font-size: 13px; font-weight: 800; color: var(--ink); }
  .step-card p { font-size: 12px; color: var(--ink-2); line-height: 1.45; }

  /* ===== ACCESSIBILITY & VOICE INCLUSION ===== */
  body.a11y-large { font-size: 112%; }
  body.a11y-large .story-box, body.a11y-large .eco-summary, body.a11y-large .eco-rec-box,
  body.a11y-large .gloss-card .gc-plain, body.a11y-large .persona-card p { font-size: 14px; line-height: 1.6; }
  body.a11y-contrast { --bg: #ffffff; --surface-2: #f8fafc; --border: #94a3b8; --border-strong: #475569; --muted: #334155; }

  .voice-btn {
    border: 1px solid rgba(255,255,255,.24); background: rgba(255,255,255,.1); color: #fff;
    height: 32px; padding: 0 9px; border-radius: 8px; cursor: pointer;
    display: inline-flex; align-items: center; gap: 5px; font-size: 11.5px; font-weight: 700;
    transition: all .15s; white-space: nowrap;
  }
  .voice-btn:hover { background: rgba(255,255,255,.22); }
  .voice-btn.active { background: #ef4444; border-color: #fca5a5; animation: micPulse 1.2s ease-in-out infinite; }
  .voice-btn.speaking { background: #0284c7; border-color: #7dd3fc; }
  .voice-btn svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  @keyframes micPulse { 0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,.55); } 50% { box-shadow: 0 0 0 7px rgba(239,68,68,0); } }

  .mic-inline-btn {
    position: absolute; right: 26px; top: 50%; transform: translateY(-50%);
    border: none; background: transparent; color: var(--accent-dark); cursor: pointer;
    width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center;
  }
  .mic-inline-btn:hover { background: var(--accent-soft); }
  .mic-inline-btn.listening { background: #ef4444; color: #fff; animation: micPulse 1.2s ease-in-out infinite; }
  .mic-inline-btn svg { width: 13px; height: 13px; stroke: currentColor; fill: none; stroke-width: 2.2; }

  .btn-speak-sm {
    border: 1px solid #0284c7; background: #e0f2fe; color: #0369a1;
    font-size: 11px; font-weight: 700; padding: 4px 9px; border-radius: 7px;
    cursor: pointer; display: inline-flex; align-items: center; gap: 5px;
  }
  .btn-speak-sm:hover { background: #0284c7; color: #fff; }
  .btn-speak-sm.speaking { background: #dc2626; border-color: #dc2626; color: #fff; }
  .btn-speak-sm svg { width: 13px; height: 13px; stroke: currentColor; fill: none; stroke-width: 2.1; }

  /* Live Visual Closed-Caption Bar (Accessible for Deaf / Hard-of-Hearing & Voice Dictation) */
  #a11y-caption-bar {
    position: fixed; left: 50%; bottom: 16px; transform: translateX(-50%);
    width: min(740px, calc(100vw - 24px));
    background: rgba(15, 23, 42, 0.96); color: #ffffff;
    border: 2px solid #38bdf8; border-radius: 12px;
    padding: 11px 14px; box-shadow: var(--shadow-lg);
    display: none; align-items: center; justify-content: space-between; gap: 12px;
    z-index: 250;
  }
  #a11y-caption-bar.open { display: flex; }
  .cap-left { display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; }
  .cap-tag { font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: #7dd3fc; display: flex; align-items: center; gap: 6px; }
  .cap-dot { width: 8px; height: 8px; border-radius: 50%; background: #38bdf8; }
  .cap-dot.mic { background: #ef4444; }
  .cap-text { font-size: 13px; line-height: 1.4; color: #f8fafc; font-weight: 500; }
  .cap-stop {
    border: 1px solid rgba(255,255,255,.3); background: rgba(255,255,255,.12); color: #fff;
    font-size: 11.5px; font-weight: 700; padding: 6px 11px; border-radius: 7px; cursor: pointer; flex-shrink: 0;
  }
  .cap-stop:hover { background: #ef4444; border-color: #ef4444; }

  .a11y-panel-guide {
    background: linear-gradient(135deg, #ecfeff 0%, #f0f9ff 100%);
    border: 1.5px solid #7dd3fc; border-radius: 12px; padding: 16px 18px;
    display: flex; flex-direction: column; gap: 10px;
  }
  .a11y-controls-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }

  /* Click-to-speak individual bubbles/cards */
  .speak-bubble {
    position: relative;
    cursor: pointer;
    transition: border-color .15s ease, box-shadow .15s ease, transform .12s ease;
  }
  .speak-bubble:hover {
    border-color: #38bdf8 !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.14);
  }
  .speak-bubble.is-speaking {
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25) !important;
    background: #f0f9ff !important;
  }
  .speak-badge-hint {
    position: absolute; top: 8px; right: 8px;
    width: 22px; height: 22px; border-radius: 999px;
    background: rgba(224, 242, 254, 0.9); color: #0369a1;
    border: 1px solid #bae6fd;
    display: grid; place-items: center; font-size: 11px;
    pointer-events: none; transition: all .15s;
  }
  .speak-bubble:hover .speak-badge-hint { background: #0284c7; color: #ffffff; border-color: #0284c7; }
  .speak-bubble.is-speaking .speak-badge-hint { background: #dc2626; color: #ffffff; border-color: #dc2626; }
  .eco-rec-box.speak-bubble, .eco-p-item.speak-bubble { padding-right: 32px; }
  .gloss-card.speak-bubble, .step-card.speak-bubble, .persona-card.speak-bubble { padding-right: 34px; }
  .stat-box.speak-bubble .s-lbl { padding-right: 22px; }

  @media (max-width: 1160px) {
    .verified-chip { display: none; }
    .brand-text p { display: none; }
  }
  @media (max-width: 980px) {
    html, body { overflow-y: auto; overflow-x: hidden; height: auto; width: 100%; }
    .app { height: auto; min-height: 100vh; width: 100%; }
    header.topbar { height: auto; padding: 9px 10px; flex-wrap: wrap; gap: 7px; width: 100%; }
    .brand { flex: 1 1 0; min-width: 0; }
    .nav-tabs { order: 3; width: 100%; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .nav-tab { justify-content: center; padding: 7px 3px; font-size: 10.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .nav-tab svg { display: none; }
    .nav-tab span.tab-long { display: none; }
    .nav-tab span.tab-short { display: inline !important; }
    .btn-excel-hero { padding: 6px 9px; font-size: 11px; flex-shrink: 0; }
    .btn-excel-hero span.xl-long { display: none; }
    #view-map { flex-direction: column; overflow: visible; width: 100%; }
    .map-column { width: 100%; max-width: 100%; }
    .map-toolbar { padding: 8px 10px; gap: 6px; width: 100%; }
    .tb-group { width: 100%; min-width: 0; }
    .search-wrap { flex: 1 1 140px; min-width: 0; width: auto; }
    .ctrl-select { flex: 1 1 130px; max-width: 100%; min-width: 0; width: 100%; }
    .timeline-inline { width: 100%; justify-content: space-between; min-width: 0; }
    input[type=range].period-slider { flex: 1; width: 60px; min-width: 60px; }
    .map-stage { height: 54vh; min-height: 350px; max-height: 480px; width: 100%; touch-action: pan-y; }
    .map-footer { padding: 7px 10px; font-size: 10.5px; }
    .gps-pill { display: none; }
    aside.inspector { width: 100%; max-width: 100%; border-left: none; border-top: 2px solid var(--border-strong); overflow: visible; }
    .inspector-scroll { overflow: visible; padding: 14px 10px 28px; }
    .kpi-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 8px 10px; gap: 6px; width: 100%; }
    .kpi-mini { min-width: 0; }
    .kpi-mini .val { font-size: 15px; }
    .exp-modes { grid-template-columns: 1fr; }
    .nat-grid-2 { grid-template-columns: 1fr; }
    #view-table, #view-national, #view-guide { padding: 12px 10px 28px; overflow: visible; width: 100%; }
    .table-scroll { max-height: 62vh; }
  }
  @media (max-width: 480px) {
    .brand-text h1 { font-size: 12.5px; }
    .brand-mark { width: 28px; height: 28px; font-size: 11px; }
  }
</style>
</head>
<body>
<div class="app">
  <!-- HEADER -->
  <header class="topbar">
    <div class="brand">
      <div class="brand-mark">SIT</div>
      <div class="brand-text">
        <h1>Observatorio Geoespacial SIT Guatemala</h1>
        <p>340 municipios · 27,352 lugares poblados (KMZ 2026) · Boletines 2014–2026</p>
      </div>
    </div>

    <nav class="nav-tabs" role="tablist">
      <button class="nav-tab active" data-view="map">
        <svg viewBox="0 0 24 24"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
        <span>Mapa<span class="tab-long"> Municipal</span></span>
      </button>
      <button class="nav-tab" data-view="table">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
        <span>Ranking<span class="tab-long"> &amp; Tabla</span></span>
      </button>
      <button class="nav-tab" data-view="national">
        <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <span>Nacional<span class="tab-long"> (SIT)</span></span>
      </button>
      <button class="nav-tab guide-tab" data-view="guide" title="Manual paso a paso y significado sencillo de cada dato">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span><span class="tab-long">Cómo interpretar</span><span class="tab-short" style="display:none">Guía</span></span>
      </button>
    </nav>

    <div class="header-right">
      <button class="voice-btn" id="btn-voice-mic" title="Dictado por voz: di un municipio o comando (ej. 'Cobán' o 'comparar Guatemala con Jalapa')">
        <svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
        <span class="xl-long">Dictar</span>
      </button>
      <button class="voice-btn" id="btn-voice-read" title="Leer en voz alta la vista actual con subtítulos visibles en pantalla">
        <svg viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
        <span class="xl-long">Escuchar</span>
      </button>
      <button class="btn-excel-hero" id="btn-open-excel-modal">
        <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        <span><span class="xl-long">Descargar </span>Excel (.xlsx)</span>
      </button>
    </div>
  </header>

  <!-- VIEW 1: MAPA MUNICIPAL -->
  <section id="view-map" class="view-container active">
    <div class="map-column">
      <!-- KPI Strip -->
      <div class="kpi-strip">
        <div class="kpi-mini">
          <span class="lbl" id="kpi-1-lbl">Radiobases · 2026-S1</span>
          <span class="val num" id="kpi-1-val">—</span>
          <span class="sub" id="kpi-1-sub">—</span>
        </div>
        <div class="kpi-mini">
          <span class="lbl" id="kpi-2-lbl">Cobertura territorial</span>
          <span class="val num" id="kpi-2-val">—</span>
          <span class="sub" id="kpi-2-sub">—</span>
        </div>
        <div class="kpi-mini clickable" id="kpi-3-card" title="Clic para enfocar municipio">
          <span class="lbl" id="kpi-3-lbl">Municipio líder (#1)</span>
          <span class="val num" id="kpi-3-val">—</span>
          <span class="sub" id="kpi-3-sub">—</span>
        </div>
        <div class="kpi-mini">
          <span class="lbl" id="kpi-4-lbl">Semáforo ISI (340 munis)</span>
          <span class="val num" id="kpi-4-val">—</span>
          <span class="sub" id="kpi-4-sub">—</span>
        </div>
      </div>

      <!-- Dedicated Control Bar ABOVE Map (Zero overlap with map!) -->
      <div class="map-toolbar">
        <div class="tb-group">
          <div class="search-wrap">
            <span class="search-icon"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
            <input id="map-search" class="search-input" style="padding-right:52px;" type="text" autocomplete="off" placeholder="Buscar o dictar municipio..." />
            <button id="search-mic" class="mic-inline-btn" title="Buscar por dictado de voz"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg></button>
            <button id="search-clear" class="search-clear" title="Limpiar">✕</button>
            <div id="search-results" class="search-results"></div>
          </div>
          <select id="depto-filter" class="ctrl-select" title="Filtrar departamento">
            <option value="">Todos los deptos (22)</option>
          </select>
        </div>

        <div class="tb-group">
          <select id="metric-select" class="ctrl-select" title="Seleccionar indicador del mapa">
            <option value="bd_score">Puntaje de Brecha Digital (0–100 · Uso INE + Antenas SIT)</option>
            <option value="ine_brecha">Brecha Digital en Hogares (% sin internet · INE 2018–2023)</option>
            <option value="ine_sin">Hogares sin Internet (cantidad · INE 2018–2023)</option>
            <option value="edu_ana">Educación: % Población Analfabeta (INE · ITU)</option>
            <option value="eco_ocu">Economía: % Población Ocupada (INE · ITU)</option>
            <option value="isi">Índice de Saturación Económica (ISI 0–100)</option>
            <option value="rb" selected>Radiobases en operación (2016-S2 – 2026-S1)</option>
            <option value="fx_total">Líneas fijas totales (2022-S2 – 2026-S1)</option>
            <option value="lp_per_rb">Brecha territorial: Lugares Poblados / Radiobase</option>
            <option value="lp_tot">Lugares Poblados geolocalizados (KMZ 2026)</option>
            <option value="op_3">Líneas fijas · TELGUA</option>
            <option value="op_1">Líneas fijas · COMCEL</option>
            <option value="op_0">Líneas fijas · Cablenet</option>
            <option value="op_5">Líneas fijas · Claro</option>
            <option value="op_6">Líneas fijas · GUATEL</option>
            <option value="op_4">Líneas fijas · Teléfonos del Norte</option>
            <option value="op_2">Líneas fijas · A-Tel</option>
            <option value="op_lib">Líneas fijas · Liberty / Columbus</option>
          </select>

          <div class="timeline-inline">
            <button class="play-btn" id="btn-play" title="Reproducir evolución histórica">▶</button>
            <button class="step-btn" id="btn-prev" title="Semestre anterior">◀</button>
            <input type="range" id="period-slider" class="period-slider" min="0" max="17" value="17" />
            <button class="step-btn" id="btn-next" title="Semestre siguiente">▶</button>
            <span class="period-pill num" id="period-pill">2026-S1</span>
          </div>
        </div>
      </div>

      <!-- Unobstructed SVG Map Stage -->
      <div class="map-stage" id="map-stage">
        <div id="compare-banner" class="compare-banner">
          <span id="compare-banner-text">Modo comparación: haz clic en otro municipio</span>
          <button id="cancel-compare">Salir</button>
        </div>

        <div class="map-tools">
          <div class="tool-group">
            <button class="tool-btn" id="btn-zoom-in" title="Acercar">+</button>
            <button class="tool-btn" id="btn-zoom-out" title="Alejar">−</button>
            <button class="tool-btn" id="btn-zoom-reset" title="Restablecer vista completa">
              <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/></svg>
            </button>
          </div>
          <div class="tool-group">
            <button class="tool-btn active" id="btn-toggle-deptos" title="Bordes departamentales">
              <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="12" y1="3" x2="12" y2="21"/><line x1="3" y1="12" x2="21" y2="12"/></svg>
            </button>
            <button class="tool-btn active" id="btn-toggle-labels" title="Nombres de departamentos">Aa</button>
            <button class="tool-btn" id="btn-toggle-cabs" title="Mostrar 340 Cabeceras GPS (KMZ 2026)">
              <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </button>
          </div>
        </div>

        <svg id="gt-map" preserveAspectRatio="xMidYMid meet">
          <defs>
            <pattern id="nodata-hatch" width="6" height="6" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
              <rect width="6" height="6" fill="#e2e8f0" />
              <line x1="0" y1="0" x2="0" y2="6" stroke="#cbd5e1" stroke-width="2.5" />
            </pattern>
          </defs>
          <g id="map-viewport">
            <g id="layer-munis"></g>
            <g id="layer-lakes"></g>
            <g id="layer-deptos"></g>
            <g id="layer-cabs" style="display:none"></g>
            <g id="layer-lp"></g>
            <g id="layer-labels"></g>
          </g>
        </svg>
      </div>

      <!-- Clean Bottom Legend & GPS Footer (Zero map overlap!) -->
      <div class="map-footer">
        <div class="legend-inline">
          <span class="legend-lbl" id="legend-label">Radiobases por municipio</span>
          <div class="legend-bar-wrap">
            <span class="legend-end" id="legend-min">0</span>
            <div class="legend-swatches" id="legend-swatches"></div>
            <span class="legend-end" id="legend-max">3,842</span>
          </div>
          <span class="legend-nodata" id="legend-nodata">
            <span class="nodata-box"></span>
            Sin dato publicado
          </span>
          <span class="granularity-pill" id="legend-granularity" style="display:none;"></span>
        </div>
        <div class="gps-pill" id="gps-hud">GPS: 15.7835° N, 90.2308° W</div>
      </div>
    </div>

    <!-- Right Inspector Panel -->
    <aside class="inspector">
      <div class="inspector-scroll" id="inspector-content"></div>
    </aside>
  </section>

  <!-- VIEW 2: TABLA & RANKING -->
  <section id="view-table" class="view-container">
    <div class="panel-card">
      <div class="toolbar">
        <div class="toolbar-left">
          <h2 style="font-size:15.5px;font-weight:800;margin-right:6px;">Explorador Municipal (340 municipios)</h2>
          <input id="tbl-search" class="search-input" style="width:210px;padding:0 10px;" placeholder="Filtrar municipio o depto..." />
          <select id="tbl-depto" class="ctrl-select">
            <option value="">Todos los departamentos</option>
          </select>
          <select id="tbl-tier" class="ctrl-select">
            <option value="">Todos los niveles ISI</option>
            <option value="2">Alta Saturación (ISI ≥ 75)</option>
            <option value="1">En Consolidación (45–74)</option>
            <option value="0">Baja Saturación / Oportunidad (&lt; 45)</option>
          </select>
          <select id="tbl-period" class="ctrl-select"></select>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <span id="tbl-count" style="font-size:12px;color:var(--muted);font-weight:600;"></span>
          <button class="btn-sm green" id="btn-export-table-xlsx">⬇ Descargar Excel (.xlsx)</button>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table" id="muni-table">
          <thead>
            <tr>
              <th data-sort="rank">#</th>
              <th data-sort="nom">Municipio</th>
              <th data-sort="dep">Departamento</th>
              <th data-sort="bd_sc">Puntaje Brecha</th>
              <th data-sort="ine_br">Brecha Hog. (%)</th>
              <th data-sort="edu_ana">Analfabeta (%)</th>
              <th data-sort="eco_ocu">Ocupación (%)</th>
              <th data-sort="isi">ISI (0–100)</th>
              <th data-sort="tier">Semáforo</th>
              <th data-sort="rb">Radiobases</th>
              <th data-sort="fx">Líneas Fijas</th>
              <th data-sort="g3y">Crec. 3a</th>
              <th>Mapa</th>
            </tr>
          </thead>
          <tbody id="tbl-body"></tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- VIEW 3: PANORAMA NACIONAL & AUDITORÍA -->
  <section id="view-national" class="view-container">
    <div class="nat-banner">
      <div>
        <strong>Alcance metodológico oficial (SIT + KMZ 2026):</strong> Telefonía móvil, banda ancha (BAF/BAM), smartphones (ETM), tráfico y tarifas se publican únicamente a <strong>nivel nacional</strong> (Hojas 01–07 y 10–12). A nivel <strong>municipal y departamental</strong> se integran <strong>Líneas fijas por operador (Hoja 08)</strong>, <strong>Radiobases (Hoja 09)</strong> y los <strong>27,352 sitios GPS</strong> de <code>Lugares Poblados 2026.kmz</code>.
      </div>
      <span class="pill ok">100% Verificado · 0 datos inventados</span>
    </div>

    <div class="nat-kpi-grid" id="nat-kpis"></div>

    <div class="nat-grid-2">
      <div class="panel-card">
        <div class="card-hd">
          <h3>Serie Histórica Nacional (2014-S1 – 2026-S1 · Hoja 01)</h3>
          <select id="nat-series-select" class="ctrl-select" style="height:28px;font-size:11.5px;">
            <option value="moviles">Usuarios móviles activos</option>
            <option value="fijas">Líneas fijas en operación</option>
            <option value="pospago">Móviles pospago</option>
            <option value="prepago">Móviles prepago</option>
            <option value="rb">Radiobases en operación</option>
            <option value="baf">Usuarios Banda Ancha Fija (BAF)</option>
            <option value="etm">Smartphones / ETM</option>
            <option value="tnac_m">Tráfico nacional móvil (min)</option>
          </select>
        </div>
        <div id="nat-chart-container"></div>
      </div>

      <div class="panel-card">
        <div class="card-hd">
          <h3>Participación Nacional por Operador (Hojas 03, 04 y 07)</h3>
          <select id="nat-op-period" class="ctrl-select" style="height:28px;font-size:11.5px;"></select>
        </div>
        <div id="nat-ops-container" style="display:flex;flex-direction:column;gap:12px;"></div>
      </div>
    </div>

    <div class="nat-grid-2">
      <div class="panel-card">
        <div class="card-hd">
          <h3>Tarifas Unitarias Verificables ORL (2025-S2 · Hoja 12)</h3>
          <input id="tarifa-search" class="search-input" style="width:200px;height:28px;padding:0 8px;font-size:11.5px;" placeholder="Filtrar operador o concepto..." />
        </div>
        <div class="table-scroll" style="max-height:260px;">
          <table class="data-table">
            <thead><tr><th style="text-align:left">Operador</th><th style="text-align:left">Concepto tarifario</th><th>Valor (Q)</th><th>Pág. PDF</th></tr></thead>
            <tbody id="tarifas-body"></tbody>
          </table>
        </div>
      </div>

      <div class="panel-card">
        <div class="card-hd">
          <h3>Auditoría de Integridad y Control Territorial (Hojas 13 y 15)</h3>
          <span class="pill ok">Conciliación Exacta</span>
        </div>
        <div class="table-scroll" style="max-height:260px;">
          <table class="data-table">
            <thead><tr><th style="text-align:left">Período</th><th style="text-align:left">Magnitud</th><th>Munis</th><th>Suma Munis</th><th>Total Nac.</th><th>Dif. Local</th></tr></thead>
            <tbody id="audit-body"></tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="panel-card">
      <div class="card-hd">
        <h3>Evolución Brecha Digital por Departamento: Censo 2018 vs ENCOVI 2023 (INE)</h3>
        <span class="pill" style="background:#fff1f2;color:#9f1239;">trazabilidad_brecha_digital.xlsx · 22 departamentos</span>
      </div>
      <div style="font-size:11.5px;color:var(--muted);margin-bottom:8px;">
        Comparación oficial entre el <strong>XII Censo INE 2018</strong> (agregado de 340 municipios) y la <strong>ENCOVI 2023 del INE</strong> (publicada a nivel departamental). Incluye hogares sin internet en casa, uso de internet en personas de 7+ años y mediana de gasto mensual (Q).
      </div>
      <div class="table-scroll" style="max-height:310px;">
        <table class="data-table">
          <thead>
            <tr>
              <th style="text-align:left">Departamento</th>
              <th>Brecha Hog. 2018</th>
              <th>Brecha Hog. 2023</th>
              <th>Cambio (pp)</th>
              <th>Uso Int. 7+ (2018)</th>
              <th>Uso Int. 7+ (2023)</th>
              <th>Cambio Uso</th>
              <th>Pago Int. 2023 (Q)</th>
              <th>Pobreza 2023</th>
            </tr>
          </thead>
          <tbody id="nat-brecha-body"></tbody>
        </table>
      </div>
    </div>

    <div class="panel-card">
      <div class="card-hd">
        <h3>Desarrollo Tecnológico, Educativo y Económico por Departamento (INE · Enfoque ITU)</h3>
        <span class="pill" style="background:#eef2ff;color:#3730a3;">DatosEstadisticos_tecnologia_educacion_economico.xlsx · 340 munis → 22 deptos</span>
      </div>
      <div style="font-size:11.5px;color:var(--muted);margin-bottom:8px;">
        Indicadores oficiales del INE (Población, Tecnología, Educación y Economía) agregados exactamente desde los 340 municipios, más el <strong>Puntaje promedio de Brecha Digital (0–100)</strong> para organismos como la <strong>ITU</strong>, planificación educativa y desarrollo económico territorial.
      </div>
      <div class="table-scroll" style="max-height:310px;">
        <table class="data-table">
          <thead>
            <tr>
              <th style="text-align:left">Departamento</th>
              <th>Población Total</th>
              <th>Alfabeta</th>
              <th>Analfabeta</th>
              <th>% Analfabeta</th>
              <th>Pob. Ocupada</th>
              <th>% Ocupación</th>
              <th>Puntaje Brecha Prom.</th>
            </tr>
          </thead>
          <tbody id="nat-edu-eco-body"></tbody>
        </table>
      </div>
    </div>
  </section>
  <section id="view-guide" class="view-container">
    <div class="guide-shell">
      <div class="guide-hero">
        <div>
          <h2>Cómo leer e interpretar este mapa</h2>
          <p>
            Los datos oficiales de telecomunicaciones de Guatemala suelen venir en tablas gigantescas de Excel con miles de filas. Esta herramienta transforma esos archivos oficiales de la <strong>SIT (2014–2026)</strong> y el mapa oficial de <strong>27,352 comunidades (KMZ 2026)</strong> en un mapa interactivo y accesible —con lectura en voz alta, subtítulos visuales en vivo y dictado por voz— para que cualquier persona pueda entenderlo en segundos.
          </p>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button class="btn-primary-green" id="guide-speak-btn" style="background:#0284c7;">🔊 Escuchar esta guía</button>
          <button class="btn-primary-green" id="guide-goto-map" style="background:#38bdf8;color:#0f172a;">Volver al Mapa →</button>
        </div>
      </div>

      <!-- Panel de Inclusión y Accesibilidad (Personas sordas, sordomudas, baja visión o movilidad reducida) -->
      <div class="a11y-panel-guide">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
          <div>
            <div class="guide-sec-title" style="margin-bottom:2px;">Accesibilidad e Inclusión: Voz, Subtítulos y Comunicación Asistida</div>
            <div style="font-size:12px;color:var(--ink-2);line-height:1.45;">
              Diseñado para incluir a <strong>personas sordas, sordomudas / no verbales, con baja visión o que prefieren navegar sin teclear</strong>: <strong>cada burbuja o tarjeta (con el ícono 🔊) es un botón interactivo</strong> — al tocarla lee <strong>únicamente esa burbuja</strong> con subtítulos grandes en pantalla (vuelve a tocarla para detener).
            </div>
          </div>
        </div>
        <div class="a11y-controls-row">
          <button class="btn-speak-sm" id="guide-a11y-mic">🎙️ Dictar ahora (Web Speech API)</button>
          <button class="btn-speak-sm" id="guide-a11y-tts">🔊 Escuchar guía con subtítulos</button>
          <button class="btn-sm" id="guide-test-peten">Probar frase: "Dame los datos de Petén"</button>
          <button class="btn-sm" id="btn-a11y-large">A+ Texto grande</button>
          <button class="btn-sm" id="btn-a11y-contrast">◐ Alto contraste</button>
          <select id="a11y-rate" class="ctrl-select" style="height:29px;font-size:11.5px;" title="Velocidad de lectura en voz alta">
            <option value="0.85">Velocidad: Pausada (0.85x)</option>
            <option value="1" selected>Velocidad: Normal (1.0x)</option>
            <option value="1.2">Velocidad: Rápida (1.2x)</option>
          </select>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:9px;margin-top:2px;">
          <div class="gloss-card" style="padding:10px 12px;">
            <div class="gc-term" style="font-size:12.5px;">Para personas sordomudas / no verbales</div>
            <div class="gc-plain" style="font-size:11.5px;">Puedes seleccionar cualquier municipio con un toque y presionar <strong>"Escuchar"</strong> para que la aplicación <strong>narre en voz alta los datos ante un grupo o jurado</strong>, mostrando simultáneamente <strong>subtítulos grandes en pantalla</strong> sin depender de hablar ni oír.</div>
          </div>
          <div class="gloss-card" style="padding:10px 12px;">
            <div class="gc-term" style="font-size:12.5px;">Para personas sordas o con hipoacusia</div>
            <div class="gc-plain" style="font-size:11.5px;">Toda la plataforma es <strong>100% visual</strong>: semáforos de color, texto en español sencillo ("En palabras sencillas"), íconos <code>?</code> explicativos y barra de <strong>subtítulos sincronizados</strong> cuando la narración está activa.</div>
          </div>
          <div class="gloss-card" style="padding:10px 12px;">
            <div class="gc-term" style="font-size:12.5px;">Dictado por voz inteligente (Español)</div>
            <div class="gc-plain" style="font-size:11.5px;">Toca el micrófono <strong>Dictar</strong> y di un municipio (ej. <em>"Cobán"</em>), un departamento (<em>"Petén"</em>), o una orden como <em>"Comparar Guatemala con Jalapa"</em>, <em>"Semáforo"</em> o <em>"Descargar Excel"</em>.</div>
          </div>
        </div>
      </div>

      <!-- 1. Recorridos según perfil -->
      <div>
        <div class="guide-sec-title">1. Dime qué quieres lograr y te digo exactamente qué mirar</div>
        <div class="guide-sec-sub">Elige tu objetivo o prueba directamente los ejemplos reales con un clic:</div>
        <div class="persona-grid">
          <div class="persona-card">
            <span class="persona-tag" style="background:var(--accent-soft);color:var(--accent-dark);">Emprendedor / Empresa</span>
            <h3>"Quiero abrir un negocio, tienda u oficina y necesito buen internet"</h3>
            <p>Te conviene un municipio con infraestructura ya madura, muchas antenas activas y respaldo de líneas fijas para que tu operación no se caiga.</p>
            <ol class="persona-steps">
              <li>Escribe el municipio en <strong>Buscar municipio o depto</strong>.</li>
              <li>Mira el <strong>Semáforo ISI</strong>: <strong>Rojo (≥ 75)</strong> o <strong>Ámbar (45–74)</strong> indican buena infraestructura ya instalada.</li>
              <li>Revisa <strong>Operadores de Líneas Fijas</strong> para ver qué empresas tienen cableado ahí.</li>
            </ol>
            <div class="persona-actions">
              <button class="btn-sm" data-demo-muni="301">Probar: Antigua Guatemala →</button>
              <button class="btn-sm" data-demo-muni="1601">Probar: Cobán →</button>
            </div>
          </div>

          <div class="persona-card">
            <span class="persona-tag" style="background:var(--emerald-soft);color:#065f46;">Proveedor ISP / Inversión</span>
            <h3>"Busco municipios poco saturados donde llevar internet o crecer"</h3>
            <p>Te interesan zonas con muchas aldeas/caseríos pero pocas antenas o sin competencia en telefonía/internet fijo ("océano azul").</p>
            <ol class="persona-steps">
              <li>En el selector de indicador elige <strong>Índice de Saturación Económica (ISI)</strong>.</li>
              <li>Explora los municipios pintados en <strong>Verde (&lt; 45)</strong>: tienen menor saturación.</li>
              <li>Revisa el <strong>Crecimiento a 3 años</strong> y si tiene <strong>0 líneas fijas</strong> (hay 31 municipios así en 2026-S1).</li>
            </ol>
            <div class="persona-actions">
              <button class="btn-sm green" data-demo-muni="514">Probar: Sipacate (0 fijas, +657%) →</button>
              <button class="btn-sm" id="guide-demo-zerofx">Ver los 31 sin líneas fijas →</button>
            </div>
          </div>

          <div class="persona-card">
            <span class="persona-tag" style="background:var(--purple-soft);color:var(--purple);">Ciudadano / Investigador / Alcaldía</span>
            <h3>"Quiero conocer mi municipio, compararlo y bajar un informe"</h3>
            <p>Puedes revisar el historial completo de los últimos 10 años, ver las aldeas en el mapa y descargar un archivo de Excel con tablas y mapa listo para imprimir.</p>
            <ol class="persona-steps">
              <li>Haz clic en tu municipio sobre el mapa (o búscalo arriba).</li>
              <li>Presiona <strong>Comparar</strong> y toca un segundo municipio para verlos lado a lado.</li>
              <li>Presiona <strong>Descargar Excel (.xlsx)</strong> para guardar tablas + hoja de mapa visual.</li>
            </ol>
            <div class="persona-actions">
              <button class="btn-sm purple" id="guide-demo-cmp">Ver comparación: Guatemala vs Jalapa →</button>
              <button class="btn-sm green" id="guide-demo-xlsx">Abrir descargas Excel →</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Diccionario sin tecnicismos -->
      <div>
        <div class="guide-sec-title">2. ¿Qué significa cada palabra y cada número?</div>
        <div class="guide-sec-sub">Explicación en español cotidiano de todos los indicadores oficiales que verás en pantalla:</div>
        <div class="glossary-grid">
          <div class="gloss-card" style="grid-column: 1 / -1; background:linear-gradient(135deg,#fff1f2 0%,#ffffff 75%); border-color:#fecdd3;" data-speak-title="Cómo se calcula el puntaje de brecha digital" data-speak="Cómo se calcula el puntaje de brecha digital. Va de cero a cien y se arma con dos datos de cada municipio, en cinco pasos. Uno: uso de internet, porcentaje de personas de siete años o más que usó internet según el Censo 2018 del INE. Dos: antenas por habitante, antenas de telefonía móvil por cada diez mil habitantes según la SIT, primer semestre de 2026. Tres: posición en cada dato, se ordenan los 340 municipios de menor a mayor; el que menos usa internet queda en la posición uno, y el que menos antenas tiene por habitante, también. Cuatro: promedio de las dos posiciones. Cinco: puntaje, el municipio con el promedio más bajo recibe cien y el del más alto queda cerca de cero.">
            <div class="gc-term" style="color:#9f1239;">Cómo se calcula el puntaje de brecha digital <span class="pill danger">Escala 0 a 100 · 5 pasos</span></div>
            <div class="gc-plain">Va de <strong>0 a 100</strong> y se arma con dos datos de cada municipio, en cinco pasos:</div>
            <ol style="margin:6px 0 6px 18px;font-size:12.5px;color:var(--ink-2);line-height:1.55;display:flex;flex-direction:column;gap:4px;">
              <li><strong>Uso de internet:</strong> porcentaje de personas de 7 años o más que usó internet (INE, Censo 2018).</li>
              <li><strong>Antenas por habitante:</strong> antenas de telefonía móvil por cada 10,000 habitantes (SIT, primer semestre de 2026).</li>
              <li><strong>Posición en cada dato:</strong> se ordenan los 340 municipios de menor a mayor. El que menos usa internet queda en la posición 1; el que menos antenas tiene por habitante, también.</li>
              <li><strong>Promedio de las dos posiciones.</strong></li>
              <li><strong>Puntaje:</strong> el municipio con el promedio más bajo recibe <strong>100</strong> y el del más alto queda cerca de <strong>0</strong>.</li>
            </ol>
            <div class="gc-ex"><strong>Ejemplo real verificado:</strong> <strong>Senahú (Alta Verapaz)</strong> ocupa el puesto #1 con <strong>100.0 / 100</strong> (2.6% uso de internet, 5.11 antenas/10,000 hab.), mientras <strong>Santa Catarina Pinula</strong> queda en <strong>0.29 / 100</strong> (58.1% uso, 61.92 antenas/10,000 hab.).</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Brecha Digital en Hogares <span class="pill danger">INE 2018 → 2023</span></div>
            <div class="gc-plain">Porcentaje oficial de hogares que <strong>NO cuentan con acceso a internet en casa</strong>. Usa la <strong>línea de tiempo</strong> para comparar <strong>2018</strong> (XII Censo INE, 340 municipios) con <strong>2023</strong> (ENCOVI 2023 INE, publicada a nivel de los 22 departamentos).</div>
            <div class="gc-ex"><strong>Evolución nacional oficial:</strong> Bajó de <strong>82.74%</strong> en 2018 a <strong>79.43%</strong> en 2023 (<strong>−3.31 pp</strong>), mientras el uso de internet en personas de 7+ años subió de 29.32% a 47.34%.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Educación · % Analfabeta <span class="pill warn">INE · Enfoque ITU</span></div>
            <div class="gc-plain">Indica población <strong>alfabeta</strong>, <strong>analfabeta</strong> y <strong>% de población analfabeta</strong> de cada municipio y departamento (INE). Permite a organismos como la <strong>ITU</strong> cruzar brecha educativa con conectividad digital.</div>
            <div class="gc-ex"><strong>Dato nacional real:</strong> 10,215,017 personas alfabetas y 2,313,920 analfabetas (<strong>15.53%</strong> de la población total de 14,901,286).</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Economía · % Ocupación <span class="pill ok">INE · Enfoque ITU</span></div>
            <div class="gc-plain">Mide la <strong>población ocupada</strong> y el <strong>% de ocupación</strong> sobre la población total por municipio y departamento (INE), clave para evaluar capacidad productiva y demanda económica de conectividad.</div>
            <div class="gc-ex"><strong>Dato nacional real:</strong> 4,968,542 personas ocupadas (<strong>33.34%</strong> de la población total) a nivel nacional.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Radiobases <span class="pill">Antenas celulares</span></div>
            <div class="gc-plain">Son las torres o antenas que dan señal a los teléfonos celulares en un municipio. Mientras más radiobases hay, mayor es la capacidad de la red móvil.</div>
            <div class="gc-ex"><strong>Ejemplo real (2026-S1):</strong> Guatemala tiene 3,842 radiobases; el municipio típico (mediana nacional) tiene 48.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Líneas Fijas <span class="pill" style="background:var(--teal-soft);color:#0f766e;">Red por cable</span></div>
            <div class="gc-plain">Son las líneas telefónicas fijas instaladas en hogares, negocios y oficinas, separadas por empresa (TELGUA, COMCEL, Cablenet, Claro, etc.).</div>
            <div class="gc-ex"><strong>Cómo leerlo:</strong> Si un municipio tiene 0 líneas fijas, sus habitantes dependen casi totalmente de telefonía celular o enlaces inalámbricos.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Lugares Poblados <span class="pill ine">KMZ 2026</span></div>
            <div class="gc-plain">Son todas las ciudades, pueblos, aldeas, caseríos, colonias y fincas registradas oficialmente con su punto GPS dentro de cada municipio (27,352 en todo el país).</div>
            <div class="gc-ex"><strong>Para qué sirve:</strong> Al tocar un municipio, puedes ver exactamente dónde están sus aldeas en el mapa y cuántas comunidades comparten las antenas disponibles.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Lugares / Radiobase <span class="pill warn">Brecha rural</span></div>
            <div class="gc-plain">Divide el número de comunidades entre las antenas del municipio. Responde: <em>"¿cuántas comunidades dependen de una sola antena?"</em></div>
            <div class="gc-ex"><strong>Cómo leerlo:</strong> Menos de 0.5 = cobertura muy densa (urbano). Más de 1.8 = muchas comunidades por cada antena (oportunidad de expansión).</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Semáforo ISI (0 a 100) <span class="pill ok">Decisión rápida</span></div>
            <div class="gc-plain">Resume en una sola nota qué tan saturada o cubierta está la infraestructura del municipio comparándolo contra los otros 339 municipios del país:</div>
            <div class="gc-ex">
              <strong>Verde (0–44):</strong> Baja saturación / alta oportunidad.<br>
              <strong>Ámbar (45–74):</strong> Mercado en consolidación.<br>
              <strong>Rojo (75–100):</strong> Alta saturación / plaza muy madura.
            </div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Concentración HHI <span class="pill ine">Competencia</span></div>
            <div class="gc-plain">Mide si en las líneas fijas compiten varias empresas o manda solo una. Es el indicador oficial que usan reguladores económicos internacionales (DOJ/FTC).</div>
            <div class="gc-ex"><strong>Cómo leerlo:</strong> 10,000 = 1 solo operador controla el 100%. Debajo de 1,800 = mercado competitivo. En Guatemala la mayoría supera 9,000.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Crecimiento 3 años <span class="pill ok">Tendencia</span></div>
            <div class="gc-plain">Compara las radiobases de 2023-S1 contra 2026-S1 para ver si el municipio está recibiendo inversión nueva o si se quedó estancado.</div>
            <div class="gc-ex"><strong>Referencia real:</strong> La mitad de los municipios creció +50% o más en 3 años. Arriba de +65% indica expansión muy acelerada.</div>
          </div>

          <div class="gloss-card">
            <div class="gc-term">Panorama Nacional <span class="pill ine">Solo país</span></div>
            <div class="gc-plain">Datos como usuarios celulares (21.5 millones), banda ancha fija (BAF), smartphones (ETM) y tarifas solo los publica la SIT a nivel de todo el país.</div>
            <div class="gc-ex"><strong>Transparencia:</strong> Por eso los mostramos aparte en <em>Panorama Nacional</em> y nunca inventamos estimaciones por municipio.</div>
          </div>
        </div>
      </div>

      <!-- 3. Manual paso a paso de uso -->
      <div>
        <div class="guide-sec-title">3. Manual rápido: ¿Cómo buscar y usar cada botón?</div>
        <div class="guide-sec-sub">Cinco acciones básicas para sacarle todo el provecho desde computadora o teléfono:</div>
        <div class="steps-grid">
          <div class="step-card">
            <span class="step-badge">1</span>
            <h4>Buscar un lugar</h4>
            <p>Usa la caja <strong>"Buscar municipio o depto"</strong> arriba a la izquierda (no importa si pones tildes). Al elegir un resultado, el mapa se acerca automáticamente y abre su ficha.</p>
          </div>
          <div class="step-card">
            <span class="step-badge">2</span>
            <h4>Cambiar qué pinta el mapa</h4>
            <p>Usa el selector de indicador para cambiar entre <strong>Semáforo ISI</strong>, <strong>Radiobases</strong>, <strong>Líneas fijas</strong>, <strong>Brecha</strong> o un operador específico (TELGUA, COMCEL, Cablenet, Claro...).</p>
          </div>
          <div class="step-card">
            <span class="step-badge">3</span>
            <h4>Ver la historia en movimiento</h4>
            <p>Mueve la barra de años o presiona el botón azul <strong>▶</strong> para ver cómo cambiaron las antenas semestre por semestre desde 2016 hasta 2026. Si un municipio aparece rayado en gris, significa que la SIT no publicó ese dato ese año.</p>
          </div>
          <div class="step-card">
            <span class="step-badge">4</span>
            <h4>Ubicar aldeas y comparar</h4>
            <p>Dentro de un municipio, toca <strong>Lugares GPS</strong> para ver sus aldeas y caseríos sobre el mapa. O toca <strong>Comparar</strong> y luego otro municipio para ver ambos lado a lado.</p>
          </div>
          <div class="step-card">
            <span class="step-badge">5</span>
            <h4>Descargar Excel con mapa</h4>
            <p>Presiona el botón verde <strong>Descargar Excel (.xlsx)</strong> arriba a la derecha. Puedes bajar solo un municipio, un departamento entero, una comparación (2 a 5 municipios) o todo el país — cada archivo trae sus tablas y una hoja <strong>Mapa_Visual</strong>.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>

<!-- MODAL: CENTRO DE DESCARGAS EXCEL (.xlsx) -->
<div class="modal-backdrop" id="excel-modal">
  <div class="modal" role="dialog" aria-modal="true">
    <div class="modal-hd">
      <h2>Centro de Descargas Excel (.xlsx)</h2>
      <button class="modal-close" id="btn-close-excel-modal">✕</button>
    </div>
    <div class="modal-body">
      <p style="font-size:12px;color:var(--muted);line-height:1.45;">
        Genera un libro real de Microsoft Excel (<code>.xlsx</code>) multi-hoja, con encabezados formateados, filtros automáticos, índice económico ISI y trazabilidad oficial SIT. Elige la categoría:
      </p>

      <div class="exp-modes">
        <button class="exp-mode-btn active" data-mode="muni">
          <div class="em-t">Solo un Municipio</div>
          <div class="em-s">Resumen ejecutivo, recomendación ISI, serie histórica completa y lugares poblados GPS.</div>
        </button>
        <button class="exp-mode-btn" data-mode="depto">
          <div class="em-t">Departamento Completo</div>
          <div class="em-s">Totales oficiales departamentales + todos sus municipios con operadores e índice ISI.</div>
        </button>
        <button class="exp-mode-btn" data-mode="compare">
          <div class="em-t">Comparación de Municipios</div>
          <div class="em-s">Compara de 2 a 5 municipios lado a lado (métricas, operadores, ISI y series).</div>
        </button>
        <button class="exp-mode-btn" data-mode="national">
          <div class="em-t">Nacional (340 Municipios)</div>
          <div class="em-s">Base consolidada completa de los 340 municipios + hoja metodológica ISI/HHI.</div>
        </button>
      </div>

      <div class="exp-config" id="exp-config-area"></div>
      <div class="exp-sheets-preview" id="exp-sheets-preview"></div>
    </div>
    <div class="modal-ft">
      <button class="btn-sm" id="btn-cancel-excel">Cancelar</button>
      <button class="btn-primary-green" id="btn-do-excel-download">⬇ Generar y Descargar .xlsx</button>
    </div>
  </div>
</div>

<div id="map-tooltip"></div>

<!-- Live Accessible Closed-Caption & Voice Feedback Bar -->
<div id="a11y-caption-bar" role="status" aria-live="polite">
  <div class="cap-left">
    <div class="cap-tag"><span class="cap-dot" id="cap-dot"></span><span id="cap-mode-label">Lectura con subtítulos</span></div>
    <div class="cap-text" id="cap-text"></div>
  </div>
  <button class="cap-stop" id="cap-stop-btn">Detener</button>
</div>

<script>
const SIT = __SIT_DATA_PAYLOAD__;
</script>
<script>
(function() {
  // ===== PURE CLIENT-SIDE NATIVE MULTI-SHEET .XLSX GENERATOR (ZERO DEPENDENCIES, 100% OFFLINE) =====
  const XLSXWriter = (function() {
    const CRC_TABLE = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
      let c = i;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      CRC_TABLE[i] = c >>> 0;
    }
    function crc32(bytes) {
      let c = 0xFFFFFFFF;
      for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
      return (c ^ 0xFFFFFFFF) >>> 0;
    }
    const enc = new TextEncoder();
    function xmlEsc(s) {
      return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g,'');
    }
    function colLetter(n) {
      let s = ''; n += 1;
      while (n > 0) { const r = (n - 1) % 26; s = String.fromCharCode(65 + r) + s; n = Math.floor((n - 1) / 26); }
      return s;
    }
    function makeZip(entries) {
      // entries: [{name, bytes}]
      const locals = [];
      const centrals = [];
      let offset = 0;
      const now = new Date();
      const dosTime = ((now.getHours() & 31) << 11) | ((now.getMinutes() & 63) << 5) | ((now.getSeconds() >> 1) & 31);
      const dosDate = (((Math.max(1980, now.getFullYear()) - 1980) & 127) << 9) | (((now.getMonth() + 1) & 15) << 5) | (now.getDate() & 31);

      for (const e of entries) {
        const nameB = enc.encode(e.name);
        const dataB = e.bytes;
        const crc = crc32(dataB);
        const lh = new Uint8Array(30 + nameB.length);
        const lv = new DataView(lh.buffer);
        lv.setUint32(0, 0x04034b50, true);
        lv.setUint16(4, 20, true);
        lv.setUint16(6, 0x0800, true); // UTF-8 flag
        lv.setUint16(8, 0, true);      // STORE
        lv.setUint16(10, dosTime, true);
        lv.setUint16(12, dosDate, true);
        lv.setUint32(14, crc, true);
        lv.setUint32(18, dataB.length, true);
        lv.setUint32(22, dataB.length, true);
        lv.setUint16(26, nameB.length, true);
        lv.setUint16(28, 0, true);
        lh.set(nameB, 30);
        locals.push(lh, dataB);

        const ch = new Uint8Array(46 + nameB.length);
        const cv = new DataView(ch.buffer);
        cv.setUint32(0, 0x02014b50, true);
        cv.setUint16(4, 20, true);
        cv.setUint16(6, 20, true);
        cv.setUint16(8, 0x0800, true);
        cv.setUint16(10, 0, true);
        cv.setUint16(12, dosTime, true);
        cv.setUint16(14, dosDate, true);
        cv.setUint32(16, crc, true);
        cv.setUint32(20, dataB.length, true);
        cv.setUint32(24, dataB.length, true);
        cv.setUint16(28, nameB.length, true);
        cv.setUint16(30, 0, true);
        cv.setUint16(32, 0, true);
        cv.setUint16(34, 0, true);
        cv.setUint16(36, 0, true);
        cv.setUint32(38, 0, true);
        cv.setUint32(42, offset, true);
        ch.set(nameB, 46);
        centrals.push(ch);

        offset += lh.length + dataB.length;
      }

      const cdStart = offset;
      let cdSize = 0;
      for (const c of centrals) cdSize += c.length;

      const eocd = new Uint8Array(22);
      const ev = new DataView(eocd.buffer);
      ev.setUint32(0, 0x06054b50, true);
      ev.setUint16(4, 0, true);
      ev.setUint16(6, 0, true);
      ev.setUint16(8, entries.length, true);
      ev.setUint16(10, entries.length, true);
      ev.setUint32(12, cdSize, true);
      ev.setUint32(16, cdStart, true);
      ev.setUint16(20, 0, true);

      const totalLen = offset + cdSize + 22;
      const out = new Uint8Array(totalLen);
      let pos = 0;
      for (const b of locals) { out.set(b, pos); pos += b.length; }
      for (const b of centrals) { out.set(b, pos); pos += b.length; }
      out.set(eocd, pos);
      return out;
    }

    function buildSheetXML(rows, headerRowIdx = 0, hasDrawing = false) {
      const colWidths = [];
      for (const r of rows) {
        r.forEach((cell, cIdx) => {
          const len = String(cell ?? '').length;
          colWidths[cIdx] = Math.min(48, Math.max(colWidths[cIdx] || 10, len + 3));
        });
      }
      const colsXml = colWidths.length
        ? `<cols>${colWidths.map((w, i) => `<col min="${i+1}" max="${i+1}" width="${w}" customWidth="1"/>`).join('')}</cols>`
        : '';

      const rowXmls = [];
      let maxCols = 1;
      rows.forEach((r, rIdx) => {
        if (r.length > maxCols) maxCols = r.length;
        const rNum = rIdx + 1;
        const isHdr = rIdx === headerRowIdx;
        const cells = [];
        r.forEach((val, cIdx) => {
          if (val === null || val === undefined || val === '') return;
          const ref = colLetter(cIdx) + rNum;
          if (typeof val === 'number' && Number.isFinite(val)) {
            const st = isHdr ? 1 : (Number.isInteger(val) ? 2 : 3);
            cells.push(`<c r="${ref}" s="${st}"><v>${val}</v></c>`);
          } else {
            const st = isHdr ? 1 : 0;
            cells.push(`<c r="${ref}" t="inlineStr" s="${st}"><is><t>${xmlEsc(val)}</t></is></c>`);
          }
        });
        rowXmls.push(`<row r="${rNum}"${isHdr ? ' ht="22" customHeight="1"' : ''}>${cells.join('')}</row>`);
      });

      const autoFilter = (rows.length > headerRowIdx + 1 && headerRowIdx >= 0)
        ? `<autoFilter ref="A${headerRowIdx+1}:${colLetter(maxCols-1)}${rows.length}"/>`
        : '';
      const drawingTag = hasDrawing ? `<drawing r:id="rId1"/>` : '';

      return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  ${colsXml}
  <sheetData>${rowXmls.join('')}</sheetData>
  ${autoFilter}
  ${drawingTag}
</worksheet>`;
    }

    function buildDrawingXML(imgIdx, widthPx, heightPx, startRow = 2, startCol = 0) {
      // 1 px = 9525 EMU at 96 DPI; scale cleanly to ~880px display width in Excel
      const scale = 880 / Math.max(1, widthPx);
      const cx = Math.round(widthPx * scale * 9525);
      const cy = Math.round(heightPx * scale * 9525);
      return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <xdr:oneCellAnchor>
    <xdr:from><xdr:col>${startCol}</xdr:col><xdr:colOff>95250</xdr:colOff><xdr:row>${startRow}</xdr:row><xdr:rowOff>95250</xdr:rowOff></xdr:from>
    <xdr:ext cx="${cx}" cy="${cy}"/>
    <xdr:pic>
      <xdr:nvPicPr>
        <xdr:cNvPr id="${imgIdx + 1}" name="MapaSIT_${imgIdx}"/>
        <xdr:cNvPicPr><a:picLocks noChangeAspect="1"/></xdr:cNvPicPr>
      </xdr:nvPicPr>
      <xdr:blipFill>
        <a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1"/>
        <a:stretch><a:fillRect/></a:stretch>
      </xdr:blipFill>
      <xdr:spPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </xdr:spPr>
    </xdr:pic>
    <xdr:clientData/>
  </xdr:oneCellAnchor>
</xdr:wsDr>`;
    }

    function createXLSXBlob(sheets) {
      const safeSheets = sheets.map((s, idx) => ({
        name: s.name.replace(/[\\/*?:[\]]/g, '').slice(0, 31) || `Hoja${idx+1}`,
        rows: s.rows,
        headerRowIdx: s.headerRowIdx ?? 0,
        image: s.image || null
      }));

      const drawingOverrides = [];
      let drawCount = 0;
      safeSheets.forEach((s) => {
        if (s.image) {
          drawCount++;
          s._drawIdx = drawCount;
          drawingOverrides.push(`<Override PartName="/xl/drawings/drawing${drawCount}.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>`);
        }
      });

      const contentTypes = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  ${drawCount > 0 ? '<Default Extension="png" ContentType="image/png"/>' : ''}
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  ${safeSheets.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}
  ${drawingOverrides.join('')}
</Types>`;

      const rootRels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>`;

      const workbookXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    ${safeSheets.map((s, i) => `<sheet name="${xmlEsc(s.name)}" sheetId="${i+1}" r:id="rId${i+1}"/>`).join('')}
  </sheets>
</workbook>`;

      const wbRels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  ${safeSheets.map((_, i) => `<Relationship Id="rId${i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i+1}.xml"/>`).join('')}
  <Relationship Id="rId${safeSheets.length+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>`;

      const stylesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF0F172A"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFE2E8F0"/></left><right style="thin"><color rgb="FFE2E8F0"/></right><top style="thin"><color rgb="FFE2E8F0"/></top><bottom style="thin"><color rgb="FFE2E8F0"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="4">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center"/></xf>
    <xf numFmtId="3" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1"/>
    <xf numFmtId="4" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1"/>
  </cellXfs>
</styleSheet>`;

      const files = [
        { name: '[Content_Types].xml', bytes: enc.encode(contentTypes) },
        { name: '_rels/.rels', bytes: enc.encode(rootRels) },
        { name: 'xl/workbook.xml', bytes: enc.encode(workbookXml) },
        { name: 'xl/_rels/workbook.xml.rels', bytes: enc.encode(wbRels) },
        { name: 'xl/styles.xml', bytes: enc.encode(stylesXml) },
      ];
      safeSheets.forEach((s, i) => {
        files.push({ name: `xl/worksheets/sheet${i+1}.xml`, bytes: enc.encode(buildSheetXML(s.rows, s.headerRowIdx, !!s.image)) });
        if (s.image) {
          const dIdx = s._drawIdx;
          const sheetRels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing${dIdx}.xml"/>
</Relationships>`;
          const drawRels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image${dIdx}.png"/>
</Relationships>`;
          files.push({ name: `xl/worksheets/_rels/sheet${i+1}.xml.rels`, bytes: enc.encode(sheetRels) });
          files.push({ name: `xl/drawings/drawing${dIdx}.xml`, bytes: enc.encode(buildDrawingXML(dIdx, s.image.widthPx, s.image.heightPx, s.image.startRow ?? 2, s.image.startCol ?? 0)) });
          files.push({ name: `xl/drawings/_rels/drawing${dIdx}.xml.rels`, bytes: enc.encode(drawRels) });
          files.push({ name: `xl/media/image${dIdx}.png`, bytes: s.image.bytes });
        }
      });

      return new Blob([makeZip(files)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    }

    function downloadXLSX(filename, sheets) {
      const blob = createXLSXBlob(sheets);
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename.endsWith('.xlsx') ? filename : filename + '.xlsx';
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    }
    return { downloadXLSX, createXLSXBlob };
  })();

  // ===== UTILITIES & ECONOMIC RECOMMENDATION ENGINE =====
  const fmtInt = (v) => (v === null || v === undefined) ? 'Sin dato' : Number(v).toLocaleString('es-GT');
  const fmtDec = (v, d=2) => (v === null || v === undefined) ? '—' : Number(v).toLocaleString('es-GT', {minimumFractionDigits: d, maximumFractionDigits: d});
  const norm = (s) => (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));

  function getEcoRecommendation(m) {
    const e = m.eco;
    const rb = m.rb['2026-S1']?.v ?? 0;
    const fx = m.fx['2026-S1']?.t ?? 0;
    const lp = m.lp_sum.tot;
    const gTxt = e.g3y !== null ? `${e.g3y >= 0 ? '+' : ''}${e.g3y}% en 3 años` : 'sin base 2023';
    const hhiTxt = e.hhi !== null
      ? (e.hhi > 2500 ? `Altamente concentrado (HHI ${fmtInt(Math.round(e.hhi))})` : `Moderado (HHI ${fmtInt(Math.round(e.hhi))})`)
      : 'Sin servicio de líneas fijas (0 líneas)';

    if (e.tier === 2) {
      return {
        badge: 'Alta Saturación · Polo Maduro',
        badgeCls: 'danger',
        shortLabel: 'Alta Saturación',
        summary: `Infraestructura densa (${fmtInt(rb)} radiobases y ${fmtInt(fx)} líneas fijas para ${fmtInt(lp)} lugares poblados; crecimiento ${gTxt}). El mercado tradicional está altamente cubierto.`,
        forBiz: 'Ideal para comercios, oficinas, call centers, fintech o logística que exigen conectividad sólida y redundante desde el día uno.',
        forTelco: 'Mercado tradicional saturado y competido. Para entrar conviene diferenciarse con fibra empresarial, SLA corporativo o nichos de valor agregado.' + (e.hhi > 8500 ? ' Ojo: en red fija sigue dominando un solo operador.' : ''),
        hhiTxt, gTxt
      };
    } else if (e.tier === 1) {
      const booming = e.g3y !== null && e.g3y >= 65;
      return {
        badge: booming ? 'En Consolidación · Expansión Rápida' : 'Mercado en Consolidación',
        badgeCls: 'warn',
        shortLabel: 'En Consolidación',
        summary: `Cobertura intermedia (${fmtInt(rb)} radiobases para ${fmtInt(lp)} lugares poblados; crecimiento ${gTxt}). Existe demanda activa comprobada con margen claro de mejora en red fija.`,
        forBiz: 'Buena plaza regional para expansión comercial y PYMES. Se recomienda confirmar cobertura de internet fijo en zonas periféricas antes de operar.',
        forTelco: (booming ? 'Fuerte tracción de demanda (+65% en radiobases en 3 años). ' : '') + `Oportunidad táctica para ISP/fibra local: la red fija muestra ${e.hhi === null ? 'ausencia total' : 'muy alta concentración (' + fmtInt(Math.round(e.hhi)) + ')'}.`,
        hhiTxt, gTxt
      };
    } else {
      return {
        badge: 'Baja Saturación · Alta Oportunidad',
        badgeCls: 'ok',
        shortLabel: 'Baja Saturación',
        summary: `Infraestructura limitada frente a su dispersión territorial (${fmtInt(rb)} radiobases y ${fmtInt(fx)} líneas fijas para ${fmtInt(lp)} lugares poblados; ${e.lp_rb ? fmtDec(e.lp_rb, 2) + ' lugares/RB' : 'sin RB'}).`,
        forBiz: 'Si tu negocio depende 100% de internet fijo corporativo, prevé enlace dedicado o satelital antes de invertir. Poca competencia digital local.',
        forTelco: `Oportunidad alta ("océano azul") para WISP, fibra rural, enlaces comunitarios o inversión público-privada: ${fx === 0 ? '0 líneas fijas reportadas en 2026-S1' : 'baja saturación competitiva'} y clara brecha territorial.`,
        hhiTxt, gTxt
      };
    }
  }

  const PRJ = SIT.meta.proj;
  function projLonLat(lon, lat) { return [PRJ.pad + (lon - PRJ.min_lon) * PRJ.cos_lat * PRJ.scale, PRJ.pad + (PRJ.max_lat - lat) * PRJ.scale]; }
  function unprojXY(x, y) { return [PRJ.min_lon + (x - PRJ.pad) / (PRJ.cos_lat * PRJ.scale), PRJ.max_lat - (y - PRJ.pad) / PRJ.scale]; }

  const muniById = new Map(SIT.munis.map(m => [m.id, m]));
  const deptoById = new Map(SIT.deptos.map(d => [d.id, d]));
  const munisByDepto = new Map();
  SIT.deptos.forEach(d => munisByDepto.set(d.id, []));
  SIT.munis.forEach(m => munisByDepto.get(m.did).push(m));

  const PALETTE_RB  = ['#f0f9ff','#bae6fd','#7dd3fc','#38bdf8','#0284c7','#0369a1','#0c4a6e'];
  const PALETTE_FX  = ['#f0fdfa','#99f6e4','#5eead4','#2dd4bf','#0d9488','#0f766e','#115e59'];
  const PALETTE_GAP = ['#fffbeb','#fef3c7','#fde68a','#fbbf24','#f59e0b','#ea580c','#b91c1c'];
  const PALETTE_LP  = ['#f5f3ff','#ede9fe','#ddd6fe','#c4b5fd','#8b5cf6','#6d28d9','#4c1d95'];
  // ISI traffic light ramp: Low saturation (emerald) -> Consolidation (amber) -> High saturation (red)
  const PALETTE_ISI = ['#059669','#34d399','#a7f3d0','#fde68a','#fbbf24','#f87171','#dc2626'];
  const OP_COLORS   = ['#0284c7','#0d9488','#6366f1','#f59e0b','#ec4899','#10b981','#8b5cf6','#64748b','#475569'];
  const LP_GRP_COLORS = ['#f59e0b', '#e11d48', '#4f46e5', '#0d9488', '#65a30d', '#64748b'];

  // Subtle label nudges (dx, dy) in SVG units to prevent central highlands overlap
  const DEPTO_LABEL_NUDGE = {
    300: [0, 12],     // Sacatepéquez slightly down
    400: [-8, -6],    // Chimaltenango slightly up-left
    100: [12, -4],    // Guatemala slightly right
    700: [-6, 10],    // Sololá slightly down
    800: [4, -10],    // Totonicapán slightly up
    1000: [4, 8],     // Suchitepéquez slightly down
    1100: [-10, 4],   // Retalhuleu slightly left
    900: [-14, -4],   // Quetzaltenango slightly left
    600: [6, 6],      // Santa Rosa
  };

  const state = {
    view: 'map',
    metric: 'rb',
    periodIdx: SIT.meta.periods_rb.length - 1,
    deptoFilter: null,
    selectedMuniId: null,
    selectedDeptoId: null,
    muniSubTab: 'datos', // 'datos' | 'lp' | 'audit'
    compareMode: false,
    compareMuniId: null,
    showDeptos: true,
    showLabels: true,
    showCabs: false,
    lpGroupFilter: -1,
    lpSearchQ: '',
    playTimer: null,
    vb: { x: 0, y: 0, w: SIT.meta.svg_w, h: SIT.meta.svg_h },
    tblSort: { col: 'isi', dir: -1 },
    tblPeriod: '2026-S1',
    // Excel modal state
    expMode: 'muni',
    expCompareIds: [101, 901], // default Guatemala vs Quetzaltenango
  };

  function isIne23Mode(metric, period) {
    return (metric === 'ine_brecha' || metric === 'ine_sin') && period === '2023';
  }
  function getPeriodsForMetric(metric) {
    if (metric === 'rb' || metric === 'lp_per_rb') return SIT.meta.periods_rb;
    if (metric === 'ine_brecha' || metric === 'ine_sin') return SIT.meta.periods_ine || ['2018', '2023'];
    if (metric === 'bd_score') return ['2018–2026'];
    if (metric === 'edu_ana' || metric === 'eco_ocu') return ['Censo INE'];
    if (metric === 'isi' || metric === 'lp_tot') return ['2026-S1'];
    return SIT.meta.periods_fx;
  }
  function getActivePeriod() {
    const ps = getPeriodsForMetric(state.metric);
    return ps[Math.min(state.periodIdx, ps.length - 1)];
  }
  function getMetricValue(muni, metric, period) {
    if (metric === 'bd_score') return muni.bd.sc;
    if (metric === 'edu_ana') return muni.soc.pct_ana;
    if (metric === 'eco_ocu') return muni.soc.pct_ocu;
    if (metric === 'ine_brecha') {
      if (period === '2023') {
        const dep = deptoById.get(muni.did);
        return dep && dep.ine23 ? dep.ine23.br : null;
      }
      return muni.ine.br;
    }
    if (metric === 'ine_sin') {
      if (period === '2023') {
        const dep = deptoById.get(muni.did);
        return dep && dep.ine23 ? dep.ine23.sin : null;
      }
      return muni.ine.sin;
    }
    if (metric === 'isi') return muni.eco.isi;
    if (metric === 'rb') return muni.rb[period] ? muni.rb[period].v : null;
    if (metric === 'lp_tot') return muni.lp_sum.tot;
    if (metric === 'lp_per_rb') {
      const rec = muni.rb[period];
      if (!rec || rec.v === 0) return null;
      return Math.round((muni.lp_sum.tot / rec.v) * 100) / 100;
    }
    const rec = muni.fx[period];
    if (!rec) return null;
    if (metric === 'fx_total') return rec.t;
    if (metric === 'op_lib') return rec.v[8] !== null ? rec.v[8] : rec.v[7];
    return rec.v[parseInt(metric.split('_')[1], 10)];
  }
  function getMetricTitle(metric) {
    if (metric === 'bd_score') return 'Puntaje Brecha Digital (0–100)';
    if (metric === 'edu_ana') return 'Educación · % Analfabeta (INE)';
    if (metric === 'eco_ocu') return 'Economía · % Ocupación (INE)';
    if (metric === 'ine_brecha') return 'Brecha Digital Hogares (INE)';
    if (metric === 'ine_sin') return 'Hogares sin Internet (INE)';
    if (metric === 'isi') return 'Índice Saturación ISI (0–100)';
    if (metric === 'rb') return 'Radiobases en operación';
    if (metric === 'fx_total') return 'Líneas fijas totales';
    if (metric === 'lp_tot') return 'Lugares Poblados (KMZ 2026)';
    if (metric === 'lp_per_rb') return 'Lugares Poblados / Radiobase';
    if (metric === 'op_lib') return 'Líneas fijas · Liberty / Columbus';
    return 'Líneas fijas · ' + SIT.meta.op_names[parseInt(metric.split('_')[1], 10)];
  }
  function fmtMetricVal(v, metric) {
    if (v === null || v === undefined) return 'Sin dato';
    if (metric === 'bd_score') return fmtDec(v, 1) + ' / 100';
    if (metric === 'ine_brecha' || metric === 'edu_ana' || metric === 'eco_ocu') return fmtDec(v, 1) + '%';
    if (metric === 'isi') return fmtDec(v, 1);
    if (metric === 'lp_per_rb') return fmtDec(v, 2);
    return fmtInt(v);
  }

  function computeScale(metric, period) {
    if (metric === 'bd_score') {
      const pal = ['#0d9488','#2dd4bf','#a7f3d0','#fde68a','#fb923c','#dc2626','#7f1d1d'];
      const breaks = [0, 15, 30, 50, 70, 85, 100];
      return {
        palette: pal, breaks,
        minLbl: '0 (Menor brecha)', maxLbl: '100 (Atender primero)',
        colorOf: (v) => {
          if (v === null) return 'url(#nodata-hatch)';
          if (v < 15) return pal[0];
          if (v < 30) return pal[1];
          if (v < 50) return pal[2];
          if (v < 70) return pal[3];
          if (v < 85) return pal[4];
          if (v < 94) return pal[5];
          return pal[6];
        }
      };
    }
    if (metric === 'edu_ana') {
      const pal = ['#0f766e','#2dd4bf','#fef08a','#fbbf24','#f97316','#dc2626','#7f1d1d'];
      const breaks = [3, 10, 16, 22, 29, 36, 50];
      return {
        palette: pal, breaks,
        minLbl: '3% (Menor analf.)', maxLbl: '40%+ (Mayor analf.)',
        colorOf: (v) => {
          if (v === null) return 'url(#nodata-hatch)';
          if (v < 10) return pal[0];
          if (v < 16) return pal[1];
          if (v < 22) return pal[2];
          if (v < 29) return pal[3];
          if (v < 36) return pal[4];
          if (v < 42) return pal[5];
          return pal[6];
        }
      };
    }
    if (metric === 'eco_ocu') {
      const pal = ['#fef3c7','#fde68a','#a7f3d0','#34d399','#0d9488','#0369a1','#1e3a8a'];
      const breaks = [15, 24, 28, 32, 36, 40, 50];
      return {
        palette: pal, breaks,
        minLbl: '15% (Menor ocup.)', maxLbl: '45%+ (Mayor ocup.)',
        colorOf: (v) => {
          if (v === null) return 'url(#nodata-hatch)';
          if (v < 24) return pal[0];
          if (v < 28) return pal[1];
          if (v < 32) return pal[2];
          if (v < 36) return pal[3];
          if (v < 40) return pal[4];
          if (v < 44) return pal[5];
          return pal[6];
        }
      };
    }
    if (metric === 'ine_brecha') {
      // Digital divide %: 44.8% (lowest divide -> emerald/teal) up to 99.7% (extreme divide -> deep crimson)
      const pal = ['#0d9488','#2dd4bf','#fde68a','#fbbf24','#f97316','#dc2626','#7f1d1d'];
      const breaks = [44, 65, 78, 86, 92, 96, 100];
      return {
        palette: pal, breaks,
        minLbl: '45% (Menor brecha)', maxLbl: '99.7% (Sin internet)',
        colorOf: (v) => {
          if (v === null) return 'url(#nodata-hatch)';
          if (v < 65) return pal[0];
          if (v < 78) return pal[1];
          if (v < 86) return pal[2];
          if (v < 92) return pal[3];
          if (v < 96) return pal[4];
          if (v < 98) return pal[5];
          return pal[6];
        }
      };
    }
    if (metric === 'isi') {
      const breaks = [0, 22, 35, 45, 60, 75, 88, 100];
      return {
        palette: PALETTE_ISI, breaks,
        minLbl: '0 (Oportunidad)', maxLbl: '100 (Saturado)',
        colorOf: (v) => {
          if (v === null) return 'url(#nodata-hatch)';
          if (v < 22) return PALETTE_ISI[0];
          if (v < 35) return PALETTE_ISI[1];
          if (v < 45) return PALETTE_ISI[2];
          if (v < 60) return PALETTE_ISI[3];
          if (v < 75) return PALETTE_ISI[4];
          if (v < 88) return PALETTE_ISI[5];
          return PALETTE_ISI[6];
        }
      };
    }
    const vals = [];
    if (metric === 'ine_sin' && period === '2023') {
      for (const d of SIT.deptos) if (d.ine23 && d.ine23.sin > 0) vals.push(d.ine23.sin);
    } else {
      for (const m of SIT.munis) {
        const v = getMetricValue(m, metric, period);
        if (v !== null && v > 0) vals.push(v);
      }
    }
    const palette = metric === 'rb' ? PALETTE_RB : ((metric === 'lp_per_rb' || metric === 'ine_sin') ? PALETTE_GAP : (metric === 'lp_tot' ? PALETTE_LP : PALETTE_FX));
    if (!vals.length) return { palette, breaks: [0,1,2,5,10,50,100], minLbl: '0', maxLbl: '0', colorOf: (v) => v===null?'url(#nodata-hatch)':palette[0] };
    vals.sort((a,b) => a - b);
    const maxV = vals[vals.length - 1];
    const q = (p) => vals[Math.min(vals.length - 1, Math.floor(p * vals.length))];
    let breaks;
    if (metric === 'lp_per_rb') breaks = [0, q(0.18), q(0.38), q(0.58), q(0.76), q(0.90), maxV];
    else if (maxV <= 10) breaks = [0, 1, 2, 3, 5, 8, maxV];
    else {
      breaks = [0, Math.max(1, q(0.18)), Math.max(2, q(0.38)), Math.max(3, q(0.58)), Math.max(5, q(0.76)), Math.max(10, q(0.90)), maxV];
      for (let i = 1; i < breaks.length; i++) if (breaks[i] <= breaks[i-1]) breaks[i] = breaks[i-1] + 1;
    }
    return {
      palette, breaks,
      minLbl: '0', maxLbl: fmtMetricVal(maxV, metric),
      colorOf: (v) => {
        if (v === null || v === undefined) return 'url(#nodata-hatch)';
        if (v === 0) return '#f8fafc';
        for (let i = 1; i < breaks.length; i++) if (v <= breaks[i]) return palette[i];
        return palette[palette.length - 1];
      }
    };
  }

  // ===== BUILD SVG MAP =====
  const svg = document.getElementById('gt-map');
  const layerMunis = document.getElementById('layer-munis');
  const layerLakes = document.getElementById('layer-lakes');
  const layerDeptos = document.getElementById('layer-deptos');
  const layerCabs = document.getElementById('layer-cabs');
  const layerLp = document.getElementById('layer-lp');
  const layerLabels = document.getElementById('layer-labels');
  const tooltip = document.getElementById('map-tooltip');
  const gpsHud = document.getElementById('gps-hud');
  const NS_SVG = 'http://www.w3.org/2000/svg';
  const muniPathEls = new Map();
  const deptoPathEls = new Map();

  function initMap() {
    svg.setAttribute('viewBox', `${state.vb.x} ${state.vb.y} ${state.vb.w} ${state.vb.h}`);
    const fragM = document.createDocumentFragment();
    const fragCabs = document.createDocumentFragment();
    for (const m of SIT.munis) {
      const p = document.createElementNS(NS_SVG, 'path');
      p.setAttribute('d', m.d); p.setAttribute('class', 'muni-path'); p.dataset.id = m.id;
      p.addEventListener('mouseenter', (e) => showTooltipMuni(e, m));
      p.addEventListener('mousemove', moveTooltip);
      p.addEventListener('mouseleave', hideTooltip);
      p.addEventListener('click', (e) => { if (wasDragged) return; e.stopPropagation(); handleMuniClick(m.id); });
      muniPathEls.set(m.id, p); fragM.appendChild(p);

      const [cx, cy] = projLonLat(m.gps[0], m.gps[1]);
      const c = document.createElementNS(NS_SVG, 'circle');
      c.setAttribute('cx', cx.toFixed(1)); c.setAttribute('cy', cy.toFixed(1)); c.setAttribute('r', '2.1');
      c.setAttribute('class', 'cab-pin');
      c.addEventListener('mouseenter', (e) => showTooltipMuni(e, m, true));
      c.addEventListener('mousemove', moveTooltip);
      c.addEventListener('mouseleave', hideTooltip);
      c.addEventListener('click', (e) => { if (wasDragged) return; e.stopPropagation(); handleMuniClick(m.id); });
      fragCabs.appendChild(c);
    }
    layerMunis.appendChild(fragM); layerCabs.appendChild(fragCabs);

    const fragL = document.createDocumentFragment();
    for (const lk of SIT.lakes) {
      const p = document.createElementNS(NS_SVG, 'path');
      p.setAttribute('d', lk.d); p.setAttribute('class', 'lake-path'); fragL.appendChild(p);
    }
    layerLakes.appendChild(fragL);

    const fragD = document.createDocumentFragment();
    const fragT = document.createDocumentFragment();
    for (const d of SIT.deptos) {
      const p = document.createElementNS(NS_SVG, 'path');
      p.setAttribute('d', d.d); p.setAttribute('class', 'depto-outline'); deptoPathEls.set(d.id, p); fragD.appendChild(p);

      const nudge = DEPTO_LABEL_NUDGE[d.id] || [0, 0];
      const t = document.createElementNS(NS_SVG, 'text');
      t.setAttribute('x', (d.c[0] + nudge[0]).toFixed(1));
      t.setAttribute('y', (d.c[1] + nudge[1]).toFixed(1));
      t.setAttribute('class', 'depto-label');
      t.textContent = d.nom;
      fragT.appendChild(t);
    }
    layerDeptos.appendChild(fragD); layerLabels.appendChild(fragT);

    const sortedDeptos = [...SIT.deptos].sort((a,b) => a.nom.localeCompare(b.nom, 'es'));
    for (const selId of ['depto-filter', 'tbl-depto']) {
      const sel = document.getElementById(selId);
      for (const d of sortedDeptos) { const opt = document.createElement('option'); opt.value = d.id; opt.textContent = d.nom; sel.appendChild(opt); }
    }
  }

  function renderSelectedMuniLP(highlightPt=null) {
    layerLp.innerHTML = '';
    if (!state.selectedMuniId) return;
    const pts = SIT.lp[String(state.selectedMuniId)] || [];
    const zoomFactor = SIT.meta.svg_w / state.vb.w;
    const baseR = Math.max(0.7, Math.min(2.6, 2.3 / Math.pow(zoomFactor, 0.55)));
    const frag = document.createDocumentFragment();
    const q = norm(state.lpSearchQ);

    for (const pt of pts) {
      const [lon, lat, name, catIdx, grpIdx] = pt;
      if (state.lpGroupFilter !== -1 && grpIdx !== state.lpGroupFilter) continue;
      if (q && !norm(name + ' ' + SIT.meta.lp_cats[catIdx]).includes(q)) continue;
      const [x, y] = projLonLat(lon, lat);
      const circle = document.createElementNS(NS_SVG, 'circle');
      circle.setAttribute('cx', x.toFixed(1)); circle.setAttribute('cy', y.toFixed(1));
      const r = grpIdx === 0 ? baseR * 1.45 : (grpIdx === 1 ? baseR * 1.15 : baseR * 0.85);
      circle.setAttribute('r', r.toFixed(2)); circle.setAttribute('fill', LP_GRP_COLORS[grpIdx]); circle.setAttribute('class', 'lp-dot');
      circle.addEventListener('mouseenter', (e) => showTooltipLP(e, pt));
      circle.addEventListener('mousemove', moveTooltip);
      circle.addEventListener('mouseleave', hideTooltip);
      frag.appendChild(circle);
    }
    if (highlightPt) {
      const [hx, hy] = projLonLat(highlightPt[0], highlightPt[1]);
      const ring = document.createElementNS(NS_SVG, 'circle');
      ring.setAttribute('cx', hx.toFixed(1)); ring.setAttribute('cy', hy.toFixed(1));
      ring.setAttribute('r', (baseR * 2.5).toFixed(2)); ring.setAttribute('class', 'lp-pulse');
      ring.style.transformOrigin = `${hx.toFixed(1)}px ${hy.toFixed(1)}px`;
      frag.appendChild(ring);
    }
    layerLp.appendChild(frag);
  }

  // ===== PAN & ZOOM =====
  let isDragging = false, wasDragged = false, dragStart = null, vbStart = null;
  const stage = document.getElementById('map-stage');

  function applyViewBox() {
    svg.setAttribute('viewBox', `${state.vb.x.toFixed(1)} ${state.vb.y.toFixed(1)} ${state.vb.w.toFixed(1)} ${state.vb.h.toFixed(1)}`);
    const zoomFactor = SIT.meta.svg_w / state.vb.w;
    layerLabels.style.fontSize = Math.max(4.5, 8.0 / Math.pow(zoomFactor, 0.55)) + 'px';
  }
  function animateViewBox(targetVb, duration=280, onDone=null) {
    const startVb = {...state.vb}, t0 = performance.now();
    function step(now) {
      const k = Math.min(1, (now - t0) / duration), ease = 1 - Math.pow(1 - k, 3);
      state.vb.x = startVb.x + (targetVb.x - startVb.x) * ease;
      state.vb.y = startVb.y + (targetVb.y - startVb.y) * ease;
      state.vb.w = startVb.w + (targetVb.w - startVb.w) * ease;
      state.vb.h = startVb.h + (targetVb.h - startVb.h) * ease;
      applyViewBox();
      if (k < 1) requestAnimationFrame(step); else if (onDone) onDone();
    }
    requestAnimationFrame(step);
  }
  function zoomToBBox(bb, padFactor=0.25) {
    const [x1, y1, x2, y2] = bb;
    let bw = Math.max(36, x2 - x1), bh = Math.max(36, y2 - y1);
    let tw = bw * (1 + 2 * padFactor), th = bh * (1 + 2 * padFactor);
    const aspect = SIT.meta.svg_w / SIT.meta.svg_h;
    if (tw / th > aspect) th = tw / aspect; else tw = th * aspect;
    animateViewBox({ x: (x1+x2)/2 - tw/2, y: (y1+y2)/2 - th/2, w: tw, h: th }, 280, () => { if (state.selectedMuniId) renderSelectedMuniLP(); });
  }
  function resetZoom() { animateViewBox({ x: 0, y: 0, w: SIT.meta.svg_w, h: SIT.meta.svg_h }, 280, () => { if (state.selectedMuniId) renderSelectedMuniLP(); }); }
  function zoomAt(factor, clientX, clientY) {
    const rect = svg.getBoundingClientRect();
    const rx = clientX !== undefined ? (clientX - rect.left) / rect.width : 0.5;
    const ry = clientY !== undefined ? (clientY - rect.top) / rect.height : 0.5;
    const nw = Math.max(35, Math.min(SIT.meta.svg_w * 1.15, state.vb.w * factor));
    const nh = nw * (SIT.meta.svg_h / SIT.meta.svg_w);
    state.vb = { x: state.vb.x + (state.vb.w - nw) * rx, y: state.vb.y + (state.vb.h - nh) * ry, w: nw, h: nh };
    applyViewBox(); if (state.selectedMuniId) renderSelectedMuniLP();
  }

  svg.addEventListener('mousemove', (e) => {
    const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    const ctm = svg.getScreenCTM(); if (!ctm) return;
    const sp = pt.matrixTransform(ctm.inverse());
    const [lon, lat] = unprojXY(sp.x, sp.y);
    if (lat >= 13.0 && lat <= 18.5 && lon >= -93.0 && lon <= -87.5) gpsHud.textContent = `GPS: ${lat.toFixed(4)}° N, ${Math.abs(lon).toFixed(4)}° W`;
  });
  // Two-finger pinch zoom for mobile phones & tablets
  let lastPinchDist = null;
  stage.addEventListener('touchmove', (e) => {
    if (e.touches.length === 2) {
      e.preventDefault();
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      const dist = Math.hypot(dx, dy);
      if (lastPinchDist !== null && dist > 10) {
        const cx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const cy = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        zoomAt(lastPinchDist / dist, cx, cy);
      }
      lastPinchDist = dist;
    }
  }, { passive: false });
  stage.addEventListener('touchend', () => { lastPinchDist = null; });

  stage.addEventListener('wheel', (e) => { e.preventDefault(); zoomAt(e.deltaY > 0 ? 1.16 : 0.86, e.clientX, e.clientY); }, { passive: false });
  stage.addEventListener('pointerdown', (e) => {
    if (e.target.closest('.map-tools, .compare-banner')) return;
    isDragging = true; wasDragged = false; stage.classList.add('dragging');
    dragStart = { x: e.clientX, y: e.clientY }; vbStart = { ...state.vb };
  });
  window.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    const dx = e.clientX - dragStart.x, dy = e.clientY - dragStart.y;
    if (Math.abs(dx) > 4 || Math.abs(dy) > 4) wasDragged = true;
    const rect = svg.getBoundingClientRect();
    const scale = Math.max(vbStart.w / rect.width, vbStart.h / rect.height);
    state.vb.x = vbStart.x - dx * scale; state.vb.y = vbStart.y - dy * scale; applyViewBox();
  });
  window.addEventListener('pointerup', () => { isDragging = false; stage.classList.remove('dragging'); setTimeout(() => { wasDragged = false; }, 10); });

  document.getElementById('btn-zoom-in').onclick = () => zoomAt(0.74);
  document.getElementById('btn-zoom-out').onclick = () => zoomAt(1.35);
  document.getElementById('btn-zoom-reset').onclick = () => {
    if (state.deptoFilter) { document.getElementById('depto-filter').value = ''; state.deptoFilter = null; updateMapColors(); }
    resetZoom();
  };
  document.getElementById('btn-toggle-deptos').onclick = function() { state.showDeptos = !state.showDeptos; this.classList.toggle('active', state.showDeptos); layerDeptos.style.display = state.showDeptos ? '' : 'none'; };
  document.getElementById('btn-toggle-labels').onclick = function() { state.showLabels = !state.showLabels; this.classList.toggle('active', state.showLabels); layerLabels.style.display = state.showLabels ? '' : 'none'; };
  document.getElementById('btn-toggle-cabs').onclick = function() { state.showCabs = !state.showCabs; this.classList.toggle('active', state.showCabs); layerCabs.style.display = state.showCabs ? '' : 'none'; };

  // ===== TOOLTIPS =====
  let activeRankMap = new Map();
  function showTooltipMuni(e, m, isCab=false) {
    const p = getActivePeriod(), v = getMetricValue(m, state.metric, p), rk = activeRankMap.get(m.id);
    const tierCol = m.eco.tier === 2 ? '#f87171' : (m.eco.tier === 1 ? '#fbbf24' : '#34d399');
    if (isIne23Mode(state.metric, p)) {
      const dep = deptoById.get(m.did);
      const d23 = dep.ine23;
      const dbrTxt = (d23.dbr >= 0 ? '+' : '') + fmtDec(d23.dbr, 2) + ' pp';
      const dbrCol = d23.dbr <= 0 ? '#34d399' : '#f87171';
      tooltip.innerHTML = `
        <div class="tt-title">${esc(m.nom)} <span style="font-size:10.5px;color:#94a3b8;font-weight:600;">(${esc(m.dep)})</span></div>
        <div class="tt-dept">ENCOVI 2023 (INE) · Dato oficial a nivel departamental</div>
        <div class="tt-val">
          <span style="font-size:11px;color:#cbd5e1;">Depto. ${esc(m.dep)} (2023)</span>
          <span class="tt-num num">${fmtMetricVal(v, state.metric)}</span>
        </div>
        <div style="font-size:10.5px;color:#cbd5e1;margin-top:4px;display:flex;justify-content:space-between;gap:8px;">
          <span>2018→2023: <strong style="color:${dbrCol};">${dbrTxt}</strong></span>
          <span>Muni 2018: <strong>${fmtDec(m.ine.br,1)}%</strong></span>
        </div>
      `;
    } else if (state.metric === 'bd_score') {
      tooltip.innerHTML = `
        <div class="tt-title">${esc(m.nom)}</div>
        <div class="tt-dept">${esc(m.dep)} · Prioridad #${m.bd.rk}/340 (100 = atender primero)</div>
        <div class="tt-val">
          <span style="font-size:11px;color:#cbd5e1;">Puntaje Brecha Digital</span>
          <span class="tt-num num">${fmtDec(m.bd.sc, 1)} / 100</span>
        </div>
        <div style="font-size:10.5px;color:#cbd5e1;margin-top:4px;display:flex;justify-content:space-between;gap:8px;">
          <span>Uso 2018: <strong>${fmtDec(m.bd.uso,1)}%</strong> (#${m.bd.ru})</span>
          <span>Ant/10k: <strong>${fmtDec(m.bd.ant,1)}</strong> (#${m.bd.ra})</span>
        </div>
      `;
    } else if (state.metric === 'edu_ana' || state.metric === 'eco_ocu') {
      tooltip.innerHTML = `
        <div class="tt-title">${esc(m.nom)}</div>
        <div class="tt-dept">${esc(m.dep)} · Pob. ${fmtInt(m.soc.pob)} · INE (Enfoque ITU)</div>
        <div class="tt-val">
          <span style="font-size:11px;color:#cbd5e1;">${esc(getMetricTitle(state.metric))}</span>
          <span class="tt-num num">${fmtMetricVal(v, state.metric)}</span>
        </div>
        <div style="font-size:10.5px;color:#cbd5e1;margin-top:4px;display:flex;justify-content:space-between;gap:8px;">
          <span>Analf.: <strong>${fmtInt(m.soc.ana)}</strong> (${fmtDec(m.soc.pct_ana,1)}%)</span>
          <span>Ocup.: <strong>${fmtInt(m.soc.ocu)}</strong> (${fmtDec(m.soc.pct_ocu,1)}%)</span>
        </div>
      `;
    } else {
      tooltip.innerHTML = `
        <div class="tt-title">${esc(m.nom)}</div>
        <div class="tt-dept">${esc(m.dep)} · INE ${String(m.id).padStart(4,'0')}</div>
        <div class="tt-val">
          <span style="font-size:11px;color:#cbd5e1;">${esc(getMetricTitle(state.metric))} (${p})</span>
          <span class="tt-num num">${fmtMetricVal(v, state.metric)}</span>
        </div>
        <div style="font-size:10.5px;color:#cbd5e1;margin-top:4px;display:flex;justify-content:space-between;gap:8px;">
          <span style="color:${tierCol};font-weight:700;">ISI ${fmtDec(m.eco.isi,1)} · Brecha 2018: ${fmtDec(m.ine.br,1)}%</span>
          ${rk ? `<span style="color:#94a3b8;">#${rk}/${activeRankMap.size}</span>` : ''}
        </div>
      `;
    }
    tooltip.style.display = 'block'; moveTooltip(e);
  }
  function showTooltipLP(e, pt) {
    const [lon, lat, name, catIdx, grpIdx] = pt;
    tooltip.innerHTML = `
      <div class="tt-title" style="color:${LP_GRP_COLORS[grpIdx]}">${esc(name)}</div>
      <div class="tt-dept">Categoría: <strong>${esc(SIT.meta.lp_cats[catIdx])}</strong></div>
      <div style="font-size:11px;color:#cbd5e1;margin-top:4px;font-variant-numeric:tabular-nums;">GPS: ${lat.toFixed(4)}° N, ${Math.abs(lon).toFixed(4)}° W</div>
    `;
    tooltip.style.display = 'block'; moveTooltip(e);
  }
  function moveTooltip(e) {
    const pad = 14; let lx = e.clientX + pad, ly = e.clientY + pad;
    const tw = tooltip.offsetWidth || 225, th = tooltip.offsetHeight || 88;
    if (lx + tw > window.innerWidth - 10) lx = e.clientX - tw - pad;
    if (ly + th > window.innerHeight - 10) ly = e.clientY - th - pad;
    tooltip.style.left = lx + 'px'; tooltip.style.top = ly + 'px';
  }
  function hideTooltip() { tooltip.style.display = 'none'; }

  // ===== UPDATE MAP & KPI STRIP =====
  function updateMapColors() {
    const p = getActivePeriod(), scale = computeScale(state.metric, p);
    const ine23 = isIne23Mode(state.metric, p);
    svg.classList.toggle('depto-level-mode', ine23);
    const scored = [];
    for (const m of SIT.munis) {
      const v = getMetricValue(m, state.metric, p);
      if (v !== null) scored.push({ m, v });
    }
    scored.sort((a,b) => b.v - a.v || a.m.nom.localeCompare(b.m.nom, 'es'));
    activeRankMap = new Map();
    scored.forEach((item, i) => activeRankMap.set(item.m.id, i + 1));

    for (const m of SIT.munis) {
      const el = muniPathEls.get(m.id);
      el.setAttribute('fill', scale.colorOf(getMetricValue(m, state.metric, p)));
      el.classList.toggle('dimmed', state.deptoFilter !== null && m.did !== state.deptoFilter);
      el.classList.toggle('selected', m.id === state.selectedMuniId);
      el.classList.toggle('compare-selected', m.id === state.compareMuniId);
    }
    if (state.compareMuniId && muniPathEls.has(state.compareMuniId)) layerMunis.appendChild(muniPathEls.get(state.compareMuniId));
    if (state.selectedMuniId && muniPathEls.has(state.selectedMuniId)) layerMunis.appendChild(muniPathEls.get(state.selectedMuniId));
    for (const d of SIT.deptos) deptoPathEls.get(d.id).classList.toggle('focused', state.deptoFilter === d.id || state.selectedDeptoId === d.id);

    // Bottom Legend + Granularity indicator for INE 2018 vs 2023
    document.getElementById('legend-label').textContent = getMetricTitle(state.metric);
    document.getElementById('legend-min').textContent = scale.minLbl;
    document.getElementById('legend-max').textContent = scale.maxLbl;
    document.getElementById('legend-swatches').innerHTML = scale.palette.map(c => `<span style="background:${c}"></span>`).join('');
    document.getElementById('legend-nodata').style.display = scored.length < 340 ? 'inline-flex' : 'none';
    const granPill = document.getElementById('legend-granularity');
    if (state.metric === 'ine_brecha' || state.metric === 'ine_sin') {
      granPill.style.display = 'inline-flex';
      if (ine23) {
        granPill.classList.remove('muni-lvl');
        granPill.textContent = 'ENCOVI 2023 (INE) · Nivel departamental (22 deptos)';
      } else {
        granPill.classList.add('muni-lvl');
        granPill.textContent = 'XII Censo 2018 (INE) · Nivel municipal (340 munis)';
      }
    } else if (state.metric === 'bd_score') {
      granPill.style.display = 'inline-flex';
      granPill.classList.remove('muni-lvl');
      granPill.textContent = 'Puntaje 0–100 · Uso Internet 2018 (INE) + Antenas/10k hab 2026 (SIT)';
    } else if (state.metric === 'edu_ana' || state.metric === 'eco_ocu') {
      granPill.style.display = 'inline-flex';
      granPill.classList.add('muni-lvl');
      granPill.textContent = 'INE · Tecnología, Educación y Economía (340 munis · Enfoque ITU)';
    } else {
      granPill.style.display = 'none';
    }

    // KPI Strip
    const scopeMunis = state.deptoFilter !== null ? munisByDepto.get(state.deptoFilter) : SIT.munis;
    const scopeDeptos = state.deptoFilter !== null ? [deptoById.get(state.deptoFilter)] : SIT.deptos;
    const scopeScored = state.deptoFilter !== null ? scored.filter(x => x.m.did === state.deptoFilter) : scored;
    const scopeLabel = state.deptoFilter !== null ? deptoById.get(state.deptoFilter).nom : 'Guatemala (340 munis)';
    const topItem = scopeScored[0];

    let k1Val, k1Sub;
    if (state.metric === 'bd_score') {
      const avgBd = scopeMunis.reduce((s, m) => s + m.bd.sc, 0) / scopeMunis.length;
      k1Val = `${fmtDec(avgBd, 1)} / 100`;
      k1Sub = `Promedio puntaje brecha · 100 = atender primero`;
    } else if (state.metric === 'edu_ana') {
      const pSum = scopeMunis.reduce((s, m) => s + m.soc.pob, 0);
      const aSum = scopeMunis.reduce((s, m) => s + m.soc.ana, 0);
      k1Val = `${fmtDec((aSum / Math.max(1, pSum)) * 100, 2)}%`;
      k1Sub = `${fmtInt(aSum)} analfabetas de ${fmtInt(pSum)} personas (INE)`;
    } else if (state.metric === 'eco_ocu') {
      const pSum = scopeMunis.reduce((s, m) => s + m.soc.pob, 0);
      const oSum = scopeMunis.reduce((s, m) => s + m.soc.ocu, 0);
      k1Val = `${fmtDec((oSum / Math.max(1, pSum)) * 100, 2)}%`;
      k1Sub = `${fmtInt(oSum)} ocupadas de ${fmtInt(pSum)} personas (INE)`;
    } else if (state.metric === 'ine_brecha') {
      if (ine23) {
        const hSum = scopeDeptos.reduce((s, d) => s + d.ine23.h, 0);
        const sinSum = scopeDeptos.reduce((s, d) => s + d.ine23.sin, 0);
        const br23 = (sinSum / Math.max(1, hSum)) * 100;
        const h18 = scopeDeptos.reduce((s, d) => s + d.ine.h, 0);
        const sin18 = scopeDeptos.reduce((s, d) => s + d.ine.sin, 0);
        const dbr = br23 - ((sin18 / Math.max(1, h18)) * 100);
        k1Val = `${fmtDec(br23, 2)}%`;
        k1Sub = `${fmtInt(sinSum)} de ${fmtInt(hSum)} hog. · ${dbr >= 0 ? '+' : ''}${fmtDec(dbr, 2)} pp vs 2018`;
      } else {
        const hSum = scopeMunis.reduce((s, m) => s + m.ine.h, 0);
        const sinSum = scopeMunis.reduce((s, m) => s + m.ine.sin, 0);
        k1Val = `${fmtDec((sinSum / Math.max(1, hSum)) * 100, 2)}%`;
        k1Sub = `${fmtInt(sinSum)} de ${fmtInt(hSum)} hogares · Censo 2018`;
      }
    } else if (state.metric === 'ine_sin') {
      if (ine23) {
        const hSum = scopeDeptos.reduce((s, d) => s + d.ine23.h, 0);
        const sinSum = scopeDeptos.reduce((s, d) => s + d.ine23.sin, 0);
        k1Val = fmtInt(sinSum);
        k1Sub = `${fmtDec((sinSum / Math.max(1, hSum)) * 100, 2)}% de hogares · ENCOVI 2023`;
      } else {
        const hSum = scopeMunis.reduce((s, m) => s + m.ine.h, 0);
        const sinSum = scopeMunis.reduce((s, m) => s + m.ine.sin, 0);
        k1Val = fmtInt(sinSum);
        k1Sub = `${fmtDec((sinSum / Math.max(1, hSum)) * 100, 2)}% de hogares · Censo 2018`;
      }
    } else if (state.metric === 'isi') {
      const avgIsi = scopeMunis.reduce((s, m) => s + m.eco.isi, 0) / scopeMunis.length;
      k1Val = `${fmtDec(avgIsi, 1)} / 100`;
      k1Sub = `Promedio ISI · ${scopeLabel}`;
    } else if (state.metric === 'lp_per_rb') {
      const lpSum = scopeMunis.reduce((s, m) => s + m.lp_sum.tot, 0);
      const rbSum = scopeMunis.reduce((s, m) => s + (m.rb[p]?.v || 0), 0);
      k1Val = rbSum > 0 ? `${fmtDec(lpSum / rbSum, 2)} lug./RB` : '—';
      k1Sub = `${fmtInt(lpSum)} lug. ÷ ${fmtInt(rbSum)} RB`;
    } else {
      let sumScope = scopeScored.reduce((s, x) => s + x.v, 0), extraSp = 0;
      if (state.metric === 'rb') for (const d of SIT.deptos) if (state.deptoFilter === null || d.id === state.deptoFilter) for (const sp of d.sp) if (sp.p === p) extraSp += sp.v;
      k1Val = fmtInt(sumScope + extraSp);
      k1Sub = extraSp > 0 ? `${scopeLabel} (+${extraSp} hist.)` : scopeLabel;
    }

    document.getElementById('kpi-1-lbl').textContent = `${getMetricTitle(state.metric)} · ${p}`;
    document.getElementById('kpi-1-val').textContent = k1Val;
    document.getElementById('kpi-1-sub').textContent = k1Sub;

    document.getElementById('kpi-2-lbl').textContent = 'Cobertura de datos';
    if (ine23) {
      document.getElementById('kpi-2-val').textContent = `${scopeDeptos.length} / ${scopeDeptos.length} deptos`;
      document.getElementById('kpi-2-sub').textContent = 'ENCOVI 2023 · nivel departamental';
    } else {
      document.getElementById('kpi-2-val').textContent = `${scopeScored.length} / ${scopeMunis.length}`;
      document.getElementById('kpi-2-sub').textContent = scopeScored.length === scopeMunis.length ? (state.metric.startsWith('ine_') ? 'Censo 2018 · nivel municipal' : '100% municipios publicados') : `${scopeMunis.length - scopeScored.length} sin dato en ${p}`;
    }

    const k3Card = document.getElementById('kpi-3-card');
    document.getElementById('kpi-3-lbl').textContent = ine23 ? (state.metric === 'ine_sin' ? 'Depto. con más sin internet' : 'Depto. mayor brecha (#1)') : (state.metric === 'bd_score' ? 'Prioridad #1 (Puntaje 100)' : (state.metric === 'edu_ana' ? 'Mayor % analfabeta (#1)' : (state.metric === 'eco_ocu' ? 'Mayor % ocupación (#1)' : ((state.metric === 'lp_per_rb' || state.metric === 'ine_brecha') ? 'Mayor brecha (#1)' : (state.metric === 'ine_sin' ? 'Más hogares sin internet' : 'Municipio líder (#1)')))));
    if (ine23) {
      const topDep = [...scopeDeptos].sort((a,b) => (state.metric === 'ine_sin' ? b.ine23.sin - a.ine23.sin : b.ine23.br - a.ine23.br))[0];
      if (topDep) {
        const dv = state.metric === 'ine_sin' ? topDep.ine23.sin : topDep.ine23.br;
        document.getElementById('kpi-3-val').textContent = topDep.nom;
        document.getElementById('kpi-3-sub').textContent = `${fmtMetricVal(dv, state.metric)} · ENCOVI 2023`;
        k3Card.onclick = () => {
          document.getElementById('depto-filter').value = topDep.id;
          state.deptoFilter = topDep.id; state.selectedMuniId = null; state.selectedDeptoId = topDep.id;
          state.compareMode = false; state.compareMuniId = null; layerLp.innerHTML = '';
          zoomToBBox(topDep.bb, 0.22); updateMapColors(); renderInspector();
        };
      }
    } else if (topItem) {
      document.getElementById('kpi-3-val').textContent = topItem.m.nom;
      document.getElementById('kpi-3-sub').textContent = `${fmtMetricVal(topItem.v, state.metric)} · ${topItem.m.dep}`;
      k3Card.onclick = () => selectAndFocusMuni(topItem.m.id);
    } else {
      document.getElementById('kpi-3-val').textContent = '—'; document.getElementById('kpi-3-sub').textContent = 'Sin datos'; k3Card.onclick = null;
    }

    const t2 = scopeMunis.filter(m => m.eco.tier === 2).length;
    const t1 = scopeMunis.filter(m => m.eco.tier === 1).length;
    const t0 = scopeMunis.filter(m => m.eco.tier === 0).length;
    document.getElementById('kpi-4-lbl').textContent = 'Semáforo Económico ISI';
    document.getElementById('kpi-4-val').textContent = `${t0} Oport. · ${t2} Sat.`;
    document.getElementById('kpi-4-sub').textContent = `${t0} baja sat. · ${t1} consol. · ${t2} alta sat.`;
  }

  // ===== TIMELINE =====
  const metricSel = document.getElementById('metric-select');
  const periodSlider = document.getElementById('period-slider');
  const periodPill = document.getElementById('period-pill');
  const playBtn = document.getElementById('btn-play');
  const prevBtn = document.getElementById('btn-prev');
  const nextBtn = document.getElementById('btn-next');

  function syncSliderToMetric() {
    const oldP = periodPill.textContent, ps = getPeriodsForMetric(state.metric), isSingle = ps.length <= 1;
    periodSlider.min = 0; periodSlider.max = Math.max(0, ps.length - 1);
    const idx = ps.indexOf(oldP);
    state.periodIdx = idx >= 0 ? idx : ps.length - 1;
    periodSlider.value = state.periodIdx;
    periodSlider.disabled = isSingle; playBtn.disabled = isSingle; prevBtn.disabled = isSingle; nextBtn.disabled = isSingle;
    periodPill.textContent = ps[state.periodIdx];
  }
  function setPeriodIdx(idx) {
    const ps = getPeriodsForMetric(state.metric);
    state.periodIdx = Math.max(0, Math.min(ps.length - 1, idx));
    periodSlider.value = state.periodIdx; periodPill.textContent = ps[state.periodIdx];
    updateMapColors(); renderInspector();
  }
  metricSel.addEventListener('change', () => { stopPlay(); state.metric = metricSel.value; syncSliderToMetric(); updateMapColors(); renderInspector(); });
  periodSlider.addEventListener('input', () => { stopPlay(); setPeriodIdx(parseInt(periodSlider.value, 10)); });
  prevBtn.onclick = () => { stopPlay(); setPeriodIdx(state.periodIdx - 1); };
  nextBtn.onclick = () => { stopPlay(); setPeriodIdx(state.periodIdx + 1); };
  function stopPlay() { if (state.playTimer) { clearInterval(state.playTimer); state.playTimer = null; playBtn.classList.remove('playing'); playBtn.textContent = '▶'; } }
  playBtn.onclick = () => {
    if (state.playTimer) { stopPlay(); return; }
    const ps = getPeriodsForMetric(state.metric); if (ps.length <= 1) return;
    if (state.periodIdx >= ps.length - 1) setPeriodIdx(0);
    playBtn.classList.add('playing'); playBtn.textContent = '⏸';
    state.playTimer = setInterval(() => { if (state.periodIdx >= ps.length - 1) stopPlay(); else setPeriodIdx(state.periodIdx + 1); }, ps.length === 2 ? 1400 : 850);
  };

  document.getElementById('depto-filter').addEventListener('change', function() {
    const val = this.value ? parseInt(this.value, 10) : null;
    state.deptoFilter = val;
    if (val !== null) {
      zoomToBBox(deptoById.get(val).bb, 0.22);
      state.selectedMuniId = null; state.selectedDeptoId = val;
      state.compareMode = false; state.compareMuniId = null; layerLp.innerHTML = ''; updateCompareBanner();
    } else { resetZoom(); state.selectedDeptoId = null; }
    updateMapColors(); renderInspector();
  });

  // ===== SEARCH =====
  const searchInput = document.getElementById('map-search');
  const searchClear = document.getElementById('search-clear');
  const searchResults = document.getElementById('search-results');
  const searchIndex = [
    ...SIT.deptos.map(d => ({ type: 'depto', id: d.id, label: d.nom, sub: `${munisByDepto.get(d.id).length} municipios`, key: norm(d.nom) })),
    ...SIT.munis.map(m => ({ type: 'muni', id: m.id, label: m.nom, sub: `${m.dep} · ISI ${fmtDec(m.eco.isi,1)}`, key: norm(m.nom + ' ' + m.dep + ' ' + m.id) }))
  ];

  function renderSearch(q) {
    const nq = norm(q);
    searchClear.style.display = q ? 'block' : 'none';
    if (!nq) { searchResults.classList.remove('open'); return; }
    const hits = searchIndex.filter(it => it.key.includes(nq))
      .sort((a,b) => (a.key.startsWith(nq)?0:1)-(b.key.startsWith(nq)?0:1) || (a.type==='depto'?-1:1) || a.label.localeCompare(b.label,'es'))
      .slice(0, 14);
    searchResults.innerHTML = hits.length
      ? hits.map(h => `<div class="search-item" data-type="${h.type}" data-id="${h.id}"><div><div style="font-weight:700">${esc(h.label)}</div><div class="si-sub">${esc(h.sub)}</div></div><span class="si-tag ${h.type==='depto'?'dept':''}">${h.type==='depto'?'Depto':'Muni'}</span></div>`).join('')
      : `<div class="search-item" style="color:var(--muted);cursor:default">Sin coincidencias</div>`;
    searchResults.querySelectorAll('.search-item[data-id]').forEach(el => {
      el.onclick = () => {
        const type = el.dataset.type, id = parseInt(el.dataset.id, 10);
        searchResults.classList.remove('open');
        searchInput.value = el.querySelector('div > div').textContent; searchClear.style.display = 'block';
        if (type === 'depto') {
          document.getElementById('depto-filter').value = id;
          state.deptoFilter = id; state.selectedMuniId = null; state.selectedDeptoId = id;
          layerLp.innerHTML = ''; zoomToBBox(deptoById.get(id).bb, 0.22); updateMapColors(); renderInspector();
        } else selectAndFocusMuni(id);
      };
    });
    searchResults.classList.add('open');
  }
  searchInput.addEventListener('input', () => renderSearch(searchInput.value));
  searchInput.addEventListener('focus', () => { if (searchInput.value) renderSearch(searchInput.value); });
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && searchInput.value.trim()) {
      e.preventDefault();
      searchResults.classList.remove('open');
      handleVoiceTranscript(searchInput.value.trim());
    }
  });
  searchClear.onclick = () => { searchInput.value = ''; searchClear.style.display = 'none'; searchResults.classList.remove('open'); };
  document.addEventListener('click', (e) => { if (!e.target.closest('.search-wrap')) searchResults.classList.remove('open'); });

  // ===== SELECTION =====
  function updateCompareBanner() {
    const b = document.getElementById('compare-banner');
    if (state.compareMode && !state.compareMuniId && state.selectedMuniId) {
      document.getElementById('compare-banner-text').textContent = `Comparando con ${muniById.get(state.selectedMuniId).nom}: haz clic en otro municipio`;
      b.classList.add('open');
    } else b.classList.remove('open');
  }
  document.getElementById('cancel-compare').onclick = () => { state.compareMode = false; state.compareMuniId = null; updateCompareBanner(); updateMapColors(); renderInspector(); };

  function handleMuniClick(gid) {
    if (state.compareMode && state.selectedMuniId && gid !== state.selectedMuniId) {
      state.compareMuniId = gid; updateCompareBanner(); updateMapColors(); renderInspector(); return;
    }
    state.selectedMuniId = gid; state.selectedDeptoId = null; state.compareMode = false; state.compareMuniId = null;
    state.lpGroupFilter = -1; state.lpSearchQ = '';
    updateCompareBanner(); updateMapColors(); renderSelectedMuniLP(); renderInspector();
    if (window.innerWidth <= 980) {
      document.querySelector('aside.inspector')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
  function selectAndFocusMuni(gid) {
    const m = muniById.get(gid); if (!m) return;
    if (state.view !== 'map') switchView('map');
    if (state.deptoFilter !== null && state.deptoFilter !== m.did) { state.deptoFilter = null; document.getElementById('depto-filter').value = ''; }
    handleMuniClick(gid); zoomToBBox(m.bb, 1.35);
  }

  // ===== SVG CHART =====
  function buildLineChartSVG(labels, values, color, highlightPeriod, unitLabel, compareValues=null, compareColor='#7c3aed') {
    const W = 380, H = 122, padL = 42, padR = 12, padT = 12, padB = 22;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const allNums = [...values, ...(compareValues || [])].filter(v => v !== null && v !== undefined);
    if (!allNums.length) return `<div style="font-size:11.5px;color:var(--muted);padding:8px 0;">Sin datos numéricos.</div>`;
    const maxV = Math.max(1, ...allNums);
    const xOf = (i) => padL + (labels.length === 1 ? plotW/2 : (i / (labels.length - 1)) * plotW);
    const yOf = (v) => padT + plotH - (v / maxV) * plotH;

    let grid = '';
    for (let g = 0; g <= 2; g++) {
      const gv = Math.round((maxV * g) / 2), gy = yOf(gv);
      grid += `<line x1="${padL}" y1="${gy.toFixed(1)}" x2="${W-padR}" y2="${gy.toFixed(1)}" stroke="#e2e8f0" stroke-dasharray="3,3" />`;
      const glbl = gv >= 1e6 ? (gv/1e6).toFixed(1)+'M' : gv >= 1e3 ? (gv/1e3).toFixed(gv>=1e4?0:1)+'k' : String(gv);
      grid += `<text x="${padL-6}" y="${(gy+3.5).toFixed(1)}" text-anchor="end" font-size="9" fill="#64748b">${glbl}</text>`;
    }
    function makeSeries(vals, strokeCol, fillArea) {
      let segs = [], cur = [];
      vals.forEach((v, i) => { if (v !== null && v !== undefined) cur.push([xOf(i), yOf(v), v, labels[i]]); else if (cur.length) { segs.push(cur); cur = []; } });
      if (cur.length) segs.push(cur);
      let out = '';
      for (const seg of segs) {
        if (seg.length > 1) {
          const d = seg.map((pt, idx) => `${idx===0?'M':'L'}${pt[0].toFixed(1)},${pt[1].toFixed(1)}`).join(' ');
          if (fillArea) out += `<path d="${d} L${seg[seg.length-1][0].toFixed(1)},${(padT+plotH).toFixed(1)} L${seg[0][0].toFixed(1)},${(padT+plotH).toFixed(1)} Z" fill="${strokeCol}" fill-opacity="0.11" />`;
          out += `<path d="${d}" fill="none" stroke="${strokeCol}" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round" />`;
        }
        for (const [cx, cy, v, per] of seg) {
          const isHi = per === highlightPeriod;
          out += `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${isHi ? 4.4 : 2.5}" fill="${isHi ? '#f59e0b' : strokeCol}" stroke="#fff" stroke-width="1.2"><title>${per}: ${fmtInt(v)} ${unitLabel}</title></circle>`;
        }
      }
      return out;
    }
    const ticks = labels.length <= 4 ? labels.map((_,i)=>i) : [...new Set([0, Math.floor(labels.length/3), Math.floor(2*labels.length/3), labels.length-1])];
    const xTicks = ticks.map(i => `<text x="${xOf(i).toFixed(1)}" y="${H-5}" text-anchor="middle" font-size="9" fill="#64748b">${labels[i]}</text>`).join('');
    return `<svg class="chart-svg" viewBox="0 0 ${W} ${H}">${grid}${makeSeries(values, color, !compareValues)}${compareValues ? makeSeries(compareValues, compareColor, false) : ''}${xTicks}</svg>`;
  }

  // ===== INSPECTOR RENDERING =====
  function renderInspector() {
    const container = document.getElementById('inspector-content');
    const activePeriod = getActivePeriod();
    if (state.selectedMuniId && state.compareMuniId) { renderComparisonInspector(container, muniById.get(state.selectedMuniId), muniById.get(state.compareMuniId)); enhanceSpeakBubbles(container); return; }
    if (state.selectedMuniId) { renderMuniInspector(container, muniById.get(state.selectedMuniId)); enhanceSpeakBubbles(container); return; }
    if (state.selectedDeptoId) { renderDeptoInspector(container, deptoById.get(state.selectedDeptoId)); enhanceSpeakBubbles(container); return; }

    const ine23 = isIne23Mode(state.metric, activePeriod);
    const scored = SIT.munis.map(m => ({ m, v: getMetricValue(m, state.metric, activePeriod) }))
      .filter(x => x.v !== null).sort((a,b) => b.v - a.v || a.m.nom.localeCompare(b.m.nom, 'es'));
    const top12 = scored.slice(0, 12);
    const top12Deptos = ine23 ? [...SIT.deptos].sort((a,b) => (state.metric === 'ine_sin' ? b.ine23.sin - a.ine23.sin : b.ine23.br - a.ine23.br)).slice(0, 12) : [];

    container.innerHTML = `
      <div class="ins-header">
        <div class="ins-crumbs">
          <span class="pill">${ine23 ? 'ENCOVI 2023 · 22 Departamentos' : 'Vista Nacional · 340 Municipios'}</span>
          <span class="pill ine">${activePeriod}</span>
        </div>
        <div class="ins-title">${ine23 ? 'Brecha Digital 2023 (ENCOVI)' : 'Explora cualquier municipio'}</div>
        <p style="font-size:12px;color:var(--muted);line-height:1.45;">
          ${ine23
            ? `Mostrando <strong>ENCOVI 2023 del INE</strong> (publicada a nivel de los <strong>22 departamentos</strong>). Mueve la línea de tiempo a <strong>2018</strong> para ver el desglose de los 340 municipios del XII Censo, o haz clic en un municipio/departamento para comparar <strong>2018 vs 2023</strong>.`
            : `Haz clic en un municipio del mapa para ver su <strong>Semáforo de Saturación Económica (ISI 0–100)</strong>, recomendación práctica de inversión, operadores oficiales SIT y lugares poblados GPS.`
          }
        </p>
      </div>

      <div class="card" style="background:linear-gradient(135deg,#f8fafc,#f0f9ff);border-color:#bae6fd;">
        <div class="card-hd" style="margin-bottom:5px;">
          <h3>Índice de Saturación Económica (ISI)</h3>
          <button class="btn-sm" id="btn-view-isi-map">Ver en mapa →</button>
        </div>
        <p style="font-size:11.5px;color:var(--ink-2);line-height:1.45;">
          Combina <strong>cobertura móvil por comunidad</strong>, <strong>penetración fija</strong>, <strong>escala de red</strong> y el <strong>Índice HHI de competencia</strong> (metodología OCDE + DOJ/FTC) para detectar plazas saturadas frente a oportunidades de expansión.
        </p>
        <div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;">
          <button class="btn-sm" id="btn-quick-bd" style="border-color:#9f1239;color:#9f1239;background:#fff1f2;">Puntaje Brecha (0–100)</button>
          <button class="btn-sm" id="btn-quick-ine" style="border-color:#dc2626;color:#991b1b;background:#fef2f2;">Brecha Hogares (2018 → 2023)</button>
          <button class="btn-sm" id="btn-quick-edu" style="border-color:#d97706;color:#92400e;background:#fffbeb;">Educación · % Analfabeta (ITU)</button>
          <button class="btn-sm" id="btn-quick-eco" style="border-color:#0369a1;color:#075985;background:#f0f9ff;">Economía · % Ocupación (ITU)</button>
          <button class="btn-sm" id="btn-quick-zerofx">31 munis con 0 líneas fijas</button>
          <button class="btn-sm" id="btn-quick-boom">Top crecimiento RB (3 años)</button>
        </div>
      </div>

      <div class="card">
        <div class="card-hd"><h3>${ine23 ? 'Top 12 Departamentos · ' : 'Top 12 · '}${esc(getMetricTitle(state.metric))}</h3><span>${activePeriod}</span></div>
        <div class="rank-list">
          ${ine23
            ? top12Deptos.map((d, idx) => {
                const v = state.metric === 'ine_sin' ? d.ine23.sin : d.ine23.br;
                const dbrStr = (d.ine23.dbr >= 0 ? '+' : '') + fmtDec(d.ine23.dbr, 2) + ' pp';
                return `<div class="rank-item" data-depto-row="${d.id}">
                  <div class="rank-left">
                    <span class="rank-num">${idx+1}</span>
                    <div style="min-width:0">
                      <div class="rank-name">${esc(d.nom)}</div>
                      <div class="rank-sub">2018: ${fmtDec(d.ine.br,1)}% → 2023: ${fmtDec(d.ine23.br,1)}% (${dbrStr}) · Uso 7+: ${fmtDec(d.ine23.uso,1)}%</div>
                    </div>
                  </div>
                  <span class="rank-val num">${fmtMetricVal(v, state.metric)}</span>
                </div>`;
              }).join('')
            : top12.map((x, idx) => {
                const rec = getEcoRecommendation(x.m);
                return `<div class="rank-item" data-muni="${x.m.id}">
                  <div class="rank-left">
                    <span class="rank-num">${idx+1}</span>
                    <div style="min-width:0">
                      <div class="rank-name">${esc(x.m.nom)}</div>
                      <div class="rank-sub">${esc(x.m.dep)} · ISI ${fmtDec(x.m.eco.isi,1)} (${rec.shortLabel})</div>
                    </div>
                  </div>
                  <span class="rank-val num">${fmtMetricVal(x.v, state.metric)}</span>
                </div>`;
              }).join('')
          }
        </div>
      </div>

      <div class="card">
        <div class="card-hd"><h3>Departamentos (22)</h3><span>Clic para enfocar</span></div>
        <div style="display:flex;flex-wrap:wrap;gap:5px;">
          ${[...SIT.deptos].sort((a,b)=>a.nom.localeCompare(b.nom,'es')).map(d => `<button class="btn-sm" data-depto="${d.id}">${esc(d.nom)}</button>`).join('')}
        </div>
      </div>
    `;
    document.getElementById('btn-view-isi-map').onclick = () => {
      metricSel.value = 'isi'; state.metric = 'isi'; stopPlay(); syncSliderToMetric(); updateMapColors(); renderInspector();
    };
    document.getElementById('btn-quick-bd').onclick = () => {
      metricSel.value = 'bd_score'; state.metric = 'bd_score'; stopPlay(); syncSliderToMetric(); updateMapColors(); renderInspector();
    };
    document.getElementById('btn-quick-ine').onclick = () => {
      metricSel.value = 'ine_brecha'; state.metric = 'ine_brecha'; stopPlay(); syncSliderToMetric(); updateMapColors(); renderInspector();
    };
    document.getElementById('btn-quick-edu').onclick = () => {
      metricSel.value = 'edu_ana'; state.metric = 'edu_ana'; stopPlay(); syncSliderToMetric(); updateMapColors(); renderInspector();
    };
    document.getElementById('btn-quick-eco').onclick = () => {
      metricSel.value = 'eco_ocu'; state.metric = 'eco_ocu'; stopPlay(); syncSliderToMetric(); updateMapColors(); renderInspector();
    };
    document.getElementById('btn-quick-zerofx').onclick = () => {
      switchView('table');
      document.getElementById('tbl-tier').value = '0';
      state.tblSort = { col: 'fx', dir: 1 };
      renderTable();
    };
    document.getElementById('btn-quick-boom').onclick = () => {
      switchView('table');
      document.getElementById('tbl-tier').value = '';
      state.tblSort = { col: 'g3y', dir: -1 };
      renderTable();
    };
    container.querySelectorAll('.rank-item[data-muni]').forEach(el => el.onclick = () => selectAndFocusMuni(parseInt(el.dataset.muni, 10)));
    container.querySelectorAll('.rank-item[data-depto-row]').forEach(el => el.onclick = () => {
      const did = parseInt(el.dataset.deptoRow, 10);
      document.getElementById('depto-filter').value = did;
      state.deptoFilter = did; state.selectedMuniId = null; state.selectedDeptoId = did;
      state.compareMode = false; state.compareMuniId = null; layerLp.innerHTML = '';
      zoomToBBox(deptoById.get(did).bb, 0.22); updateMapColors(); renderInspector();
    });
    container.querySelectorAll('button[data-depto]').forEach(el => el.onclick = () => {
      const did = parseInt(el.dataset.depto, 10);
      document.getElementById('depto-filter').value = did;
      state.deptoFilter = did; state.selectedDeptoId = did;
      zoomToBBox(deptoById.get(did).bb, 0.22); updateMapColors(); renderInspector();
    });
  }

  function renderMuniInspector(container, m) {
    const dep = deptoById.get(m.did);
    const activePeriod = getActivePeriod();
    const pRb = SIT.meta.periods_rb.includes(activePeriod) ? activePeriod : '2026-S1';
    const pFx = SIT.meta.periods_fx.includes(activePeriod) ? activePeriod : '2026-S1';
    const rbRec = m.rb[pRb] || null, fxRec = m.fx[pFx] || null;
    const rec = getEcoRecommendation(m);
    const gmapsUrl = `https://www.google.com/maps?q=${m.gps[1]},${m.gps[0]}`;

    // Build body based on active municipal sub-tab
    let tabBody = '';
    if (state.muniSubTab === 'datos') {
      const rbIdx = SIT.meta.periods_rb.indexOf(pRb), prevRb = rbIdx > 0 ? m.rb[SIT.meta.periods_rb[rbIdx - 1]] : null;
      const fxIdx = SIT.meta.periods_fx.indexOf(pFx), prevFx = fxIdx > 0 ? m.fx[SIT.meta.periods_fx[fxIdx - 1]] : null;
      const deltaHtml = (cur, prev, prevPer) => {
        if (cur === null || cur === undefined || !prev) return '';
        const diff = cur - prev;
        if (diff === 0) return `<span class="delta-flat">(= vs ${prevPer})</span>`;
        return `<span class="${diff>0?'delta-up':'delta-down'}">${diff>0?'+':''}${fmtInt(diff)} vs ${prevPer}</span>`;
      };
      const rbScored = SIT.munis.map(x => [x.id, x.rb[pRb]?.v ?? -1]).filter(x => x[1] >= 0).sort((a,b) => b[1] - a[1]);
      const rbRank = rbRec ? rbScored.findIndex(x => x[0] === m.id) + 1 : null;
      const fxScored = SIT.munis.map(x => [x.id, x.fx[pFx]?.t ?? -1]).filter(x => x[1] >= 0).sort((a,b) => b[1] - a[1]);
      const fxRank = fxRec ? fxScored.findIndex(x => x[0] === m.id) + 1 : null;

      let opsHtml = '';
      if (fxRec) {
        const activeOps = [], zeroOps = [];
        SIT.meta.op_names.forEach((opName, idx) => {
          const val = fxRec.v[idx];
          if (val !== null && val > 0) activeOps.push({ name: opName, val, color: OP_COLORS[idx] });
          else if (val === 0) zeroOps.push(opName);
        });
        activeOps.sort((a,b) => b.val - a.val);
        opsHtml = activeOps.length === 0
          ? `<div style="font-size:11.5px;color:var(--muted);">Reporta <strong>0 líneas fijas</strong> en ${pFx}.</div>`
          : `<div class="op-list">${activeOps.map(op => {
              const pct = fxRec.t > 0 ? (op.val / fxRec.t) * 100 : 0;
              return `<div class="op-row"><div class="op-top"><span class="op-name">${esc(op.name)}</span><span class="op-nums num">${fmtInt(op.val)} <small>(${pct.toFixed(1)}%)</small></span></div><div class="bar-track"><div class="bar-fill" style="width:${Math.max(1.5,pct).toFixed(1)}%;background:${op.color}"></div></div></div>`;
            }).join('')}</div>`;
        if (zeroOps.length) opsHtml += `<div class="op-zero-note"><strong>Con 0 líneas:</strong> ${esc(zeroOps.join(', '))}.</div>`;
      }

      const rbSeries = SIT.meta.periods_rb.map(per => m.rb[per] ? m.rb[per].v : null);
      const fxSeries = SIT.meta.periods_fx.map(per => m.fx[per] ? m.fx[per].t : null);

      // Plain-Spanish narrative strictly derived from this municipality's official numbers
      const topOp = (() => {
        if (!fxRec || fxRec.t === 0) return null;
        let best = null;
        SIT.meta.op_names.forEach((n, i) => { const v = fxRec.v[i]; if (v > 0 && (!best || v > best.v)) best = { n, v, pct: (v / fxRec.t * 100).toFixed(1) }; });
        return best;
      })();
      const rbCount26 = m.rb['2026-S1']?.v ?? 0;
      const fxCount26 = m.fx['2026-S1']?.t ?? 0;
      const lpCount = m.lp_sum.tot;
      const storyLine1 = `<strong>${esc(m.nom)}</strong> cuenta con <strong>${fmtInt(rbCount26)} antenas celulares</strong> para dar cobertura a <strong>${fmtInt(lpCount)} comunidades registradas</strong>${m.eco.lp_rb ? ` (${fmtDec(m.eco.lp_rb, 2)} comunidades por antena)` : ''}.`;
      const storyLine2 = fxCount26 === 0
        ? `En red fija reporta <strong>0 líneas</strong> en 2026-S1 (depende casi por completo de señal móvil o enlaces inalámbricos).`
        : `En red fija suma <strong>${fmtInt(fxCount26)} líneas</strong>${topOp ? `, encabezadas por <strong>${esc(topOp.n)} (${topOp.pct}%)</strong>` : ''}.`;
      const storyLine3 = m.eco.g3y !== null
        ? `En los últimos 3 años sus antenas crecieron <strong>${m.eco.g3y >= 0 ? '+' : ''}${m.eco.g3y}%</strong> (${m.eco.g3y >= 65 ? 'expansión muy acelerada' : (m.eco.g3y >= 50 ? 'por encima de la mediana nacional de +50%' : 'crecimiento moderado frente a la mediana nacional de +50%')}).`
        : '';
      const depObj = deptoById.get(m.did);
      const d23 = depObj.ine23;
      const dbrTxt = (d23.dbr >= 0 ? '+' : '') + fmtDec(d23.dbr, 2) + ' pp';
      const dusoTxt = (d23.duso >= 0 ? '+' : '') + fmtDec(d23.duso, 1) + ' pp';
      const storyLine4 = `Según el XII Censo del INE (2018), de sus <strong>${fmtInt(m.ine.h)} hogares</strong>, <strong>${fmtInt(m.ine.sin)}</strong> no tienen acceso a internet (<strong>${fmtDec(m.ine.br, 1)}%</strong> de brecha digital). A nivel departamental (${esc(m.dep)}), la <strong>ENCOVI 2023</strong> reporta <strong>${fmtDec(d23.br, 1)}%</strong> de hogares sin internet (<strong>${dbrTxt}</strong> frente a 2018).`;

      // National rank by INE digital divide (1 = highest divide)
      const ineRank = [...SIT.munis].sort((a,b) => b.ine.br - a.ine.br).findIndex(x => x.id === m.id) + 1;

      tabBody = `
        <!-- Plain-Spanish Narrative Card -->
        <div class="story-box" data-speak-title="En palabras sencillas · ${esc(m.nom)}">
          <div class="st-hd" style="padding-right:24px;">
            <span>En palabras sencillas (toca para escuchar)</span>
            <button class="guide-link-inline" id="btn-muni-open-guide">Guía</button>
          </div>
          <div>${storyLine1} ${storyLine2} ${storyLine3} ${storyLine4}</div>
        </div>

        <!-- Direct INE Digital Divide 2018 (Municipal) + 2023 (ENCOVI Departamental) Card -->
        <div class="card stat-box" style="background:linear-gradient(135deg,#fff1f2 0%,#ffffff 65%);border-color:#fecdd3;" data-speak-title="Brecha Digital INE 2018–2023 · ${esc(m.nom)}" data-speak="Brecha digital en hogares para ${esc(m.nom)}: en el Censo INE 2018, de ${fmtInt(m.ine.h)} hogares, ${fmtInt(m.ine.sin)} no tenían internet, una brecha del ${fmtDec(m.ine.br,2)} por ciento, puesto ${ineRank} de 340 municipios. En la ENCOVI 2023, publicada a nivel departamental para ${esc(m.dep)}, la brecha en hogares pasó de ${fmtDec(depObj.ine.br,1)} por ciento en 2018 a ${fmtDec(d23.br,1)} por ciento en 2023 (${dbrTxt.replace('pp','puntos porcentuales')}), y el uso de internet en personas de 7 años o más subió de ${fmtDec(depObj.ine.uso,1)} a ${fmtDec(d23.uso,1)} por ciento.">
          <div class="s-lbl" style="color:#9f1239;margin-bottom:4px;padding-right:24px;">
            <span>Brecha Digital · 2018 Municipal<span class="help-q" title="Porcentaje oficial de hogares sin acceso a internet: 2018 según XII Censo INE (340 municipios) y actualización 2023 según ENCOVI 2023 INE (publicada a nivel departamental).">?</span></span>
            <span style="white-space:nowrap;">#${ineRank} / 340</span>
          </div>
          <div style="display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-bottom:6px;">
            <span class="num" style="font-size:23px;font-weight:900;color:#be123c;letter-spacing:-0.02em;">${fmtDec(m.ine.br, 2)}%</span>
            <span style="font-size:11px;color:var(--ink-2);font-weight:600;">sin internet · <strong>${fmtDec(m.ine.pc, 2)}%</strong> con internet</span>
          </div>
          <div style="height:9px;border-radius:99px;overflow:hidden;display:flex;background:#ffe4e6;margin-bottom:7px;">
            <div style="width:${m.ine.pc}%;background:#0d9488;" title="Con internet: ${fmtDec(m.ine.pc,2)}%"></div>
            <div style="width:${m.ine.br}%;background:#e11d48;" title="Sin internet: ${fmtDec(m.ine.br,2)}%"></div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;font-size:11px;margin-bottom:8px;" class="num">
            <div><span style="color:var(--muted);display:block;font-size:9.5px;font-weight:700;">TOTAL HOGARES</span><strong>${fmtInt(m.ine.h)}</strong></div>
            <div><span style="color:#0f766e;display:block;font-size:9.5px;font-weight:700;">CON INTERNET</span><strong>${fmtInt(m.ine.con)}</strong></div>
            <div><span style="color:#be123c;display:block;font-size:9.5px;font-weight:700;">SIN INTERNET</span><strong>${fmtInt(m.ine.sin)}</strong></div>
          </div>
          <div style="border-top:1px dashed #fecdd3;padding-top:7px;font-size:11px;display:flex;flex-direction:column;gap:4px;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
              <span style="font-weight:800;color:#9f1239;font-size:10.5px;">Actualización 2023 · Depto. ${esc(m.dep)} (ENCOVI INE)</span>
              <span class="pill ${d23.dbr <= 0 ? 'ok' : 'danger'}" style="font-size:9.5px;padding:1px 6px;">${dbrTxt}</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;" class="num">
              <div style="background:#fff;border:1px solid #ffe4e6;border-radius:6px;padding:5px 7px;">
                <span style="color:var(--muted);display:block;font-size:9.5px;font-weight:700;">BRECHA HOGARES DEPTO.</span>
                <strong>${fmtDec(depObj.ine.br,1)}% → ${fmtDec(d23.br,1)}%</strong>
              </div>
              <div style="background:#fff;border:1px solid #ffe4e6;border-radius:6px;padding:5px 7px;">
                <span style="color:var(--muted);display:block;font-size:9.5px;font-weight:700;">USO INTERNET 7+ AÑOS</span>
                <strong>${fmtDec(depObj.ine.uso,1)}% → ${fmtDec(d23.uso,1)}%</strong> <span style="color:#0f766e;font-size:9.5px;">(${dusoTxt})</span>
              </div>
            </div>
            <div style="display:flex;justify-content:space-between;gap:6px;font-size:10px;color:var(--muted);margin-top:1px;" class="num">
              <span>Pobreza muni 2023 (SEGEPLAN): <strong>${m.ine.pobr23 !== null ? fmtDec(m.ine.pobr23,1)+'%' : '—'}</strong></span>
              <span>Mediana internet hogar 2023: <strong>Q${fmtInt(d23.q_int)}/mes</strong></span>
            </div>
          </div>
          <div style="border-top:1px dashed #fecdd3;padding-top:7px;margin-top:6px;font-size:11px;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:4px;">
              <span style="font-weight:800;color:#9f1239;font-size:10.5px;">Puntaje de Brecha Digital (0 a 100)<span class="help-q" title="Va de 0 a 100 en 5 pasos: 1) Uso de internet 7+ (INE Censo 2018); 2) Antenas por 10,000 hab (SIT 2026-S1); 3) Posición de 1 a 340 de menor a mayor en cada dato; 4) Promedio de ambas posiciones; 5) El promedio más bajo recibe 100 (atender primero) y el más alto cerca de 0.">?</span></span>
              <span class="num" style="font-weight:900;color:#be123c;font-size:13px;">${fmtDec(m.bd.sc, 2)} / 100 <small style="color:var(--muted);font-weight:700;">(#${m.bd.rk}/340)</small></span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:10px;" class="num">
              <div style="background:#fff;border:1px solid #ffe4e6;border-radius:6px;padding:4px 7px;">Uso int. 7+ (2018): <strong>${fmtDec(m.bd.uso,1)}%</strong> · pos <strong>#${m.bd.ru}</strong></div>
              <div style="background:#fff;border:1px solid #ffe4e6;border-radius:6px;padding:4px 7px;">Antenas/10k (2026): <strong>${fmtDec(m.bd.ant,2)}</strong> · pos <strong>#${m.bd.ra}</strong></div>
            </div>
          </div>
        </div>

        <!-- INE Technology, Education & Economy Card (ITU / Development) -->
        <div class="card stat-box" style="background:linear-gradient(135deg,#f8fafc 0%,#eff6ff 100%);border-color:#bfdbfe;" data-speak-title="Educación y Economía INE · ${esc(m.nom)}" data-speak="Perfil de educación y economía del INE para ${esc(m.nom)}: población total ${fmtInt(m.soc.pob)} personas. En educación cuenta con ${fmtInt(m.soc.alf)} personas alfabetas y ${fmtInt(m.soc.ana)} analfabetas, lo que representa ${fmtDec(m.soc.pct_ana,2)} por ciento de población analfabeta. En economía registra ${fmtInt(m.soc.ocu)} personas ocupadas, equivalente al ${fmtDec(m.soc.pct_ocu,2)} por ciento de ocupación.">
          <div class="s-lbl" style="color:#1e40af;margin-bottom:5px;padding-right:24px;">
            <span>Educación y Economía (INE · Enfoque ITU)</span>
            <span class="num" style="white-space:nowrap;">Pob. ${fmtInt(m.soc.pob)}</span>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;" class="num">
            <div style="background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:7px 9px;">
              <div style="font-size:9.5px;font-weight:800;color:#92400e;text-transform:uppercase;">Educación · Analfabetismo</div>
              <div style="font-size:18px;font-weight:900;color:#b45309;line-height:1.15;">${fmtDec(m.soc.pct_ana, 2)}%</div>
              <div style="height:5px;border-radius:99px;overflow:hidden;background:#fef3c7;margin:4px 0;"><div style="width:${Math.min(100, m.soc.pct_ana)}%;height:100%;background:#d97706;"></div></div>
              <div style="font-size:10px;color:var(--ink-2);">Analf.: <strong>${fmtInt(m.soc.ana)}</strong></div>
              <div style="font-size:10px;color:#0f766e;">Alfab.: <strong>${fmtInt(m.soc.alf)}</strong> (${fmtDec(m.soc.pct_alf7,1)}% de 7+)</div>
            </div>
            <div style="background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:7px 9px;">
              <div style="font-size:9.5px;font-weight:800;color:#075985;text-transform:uppercase;">Economía · Ocupación</div>
              <div style="font-size:18px;font-weight:900;color:#0369a1;line-height:1.15;">${fmtDec(m.soc.pct_ocu, 2)}%</div>
              <div style="height:5px;border-radius:99px;overflow:hidden;background:#e0f2fe;margin:4px 0;"><div style="width:${Math.min(100, m.soc.pct_ocu)}%;height:100%;background:#0284c7;"></div></div>
              <div style="font-size:10px;color:var(--ink-2);">Ocupada: <strong>${fmtInt(m.soc.ocu)}</strong></div>
              <div style="font-size:10px;color:var(--muted);">Pobreza 2023: <strong>${m.ine.pobr23 !== null ? fmtDec(m.ine.pobr23,1)+'%' : '—'}</strong></div>
            </div>
          </div>
        </div>

        <!-- Hero Economic Saturation & Recommendation Card -->
        <div class="eco-card tier-${m.eco.tier}">
          <div class="eco-top">
            <div>
              <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);">Índice de Saturación Económica (ISI)<span class="help-q" title="Nota de 0 a 100 que resume qué tan cubierta está la infraestructura del municipio: Verde (0-44) = alta oportunidad; Ámbar (45-74) = consolidación; Rojo (75-100) = plaza muy madura y saturada.">?</span></div>
              <div class="eco-score-wrap num">
                <span class="eco-score">${fmtDec(m.eco.isi, 1)}</span>
                <span style="font-size:12px;color:var(--muted);font-weight:700;">/ 100</span>
              </div>
            </div>
            <span class="pill ${rec.badgeCls}">${esc(rec.badge)}</span>
          </div>
          <div>
            <div class="eco-gauge-track"><div class="eco-needle" style="left:${Math.max(2, Math.min(98, m.eco.isi))}%"></div></div>
            <div class="eco-scale-lbls"><span>0 · Oportunidad</span><span>45 · Consolidación</span><span>75 · Saturado</span></div>
          </div>
          <div class="eco-summary">${esc(rec.summary)}</div>
          <div class="eco-recs">
            <div class="eco-rec-box" data-speak-title="Recomendación para empresas" data-speak="Recomendación para abrir empresa o comercio en ${esc(m.nom)}: ${esc(rec.forBiz)}"><strong>Si vas a abrir empresa / comercio:</strong> ${esc(rec.forBiz)}</div>
            <div class="eco-rec-box" data-speak-title="Recomendación para ISP / telecom" data-speak="Recomendación para invertir en internet o telecomunicaciones en ${esc(m.nom)}: ${esc(rec.forTelco)}"><strong>Si evalúas invertir en ISP / telecom:</strong> ${esc(rec.forTelco)}</div>
          </div>
          <div class="eco-pillars-mini num">
            <div class="eco-p-item" data-speak-title="Concentración HHI" data-speak="Concentración HHI en telefonía fija para ${esc(m.nom)}: ${m.eco.hhi !== null ? fmtInt(Math.round(m.eco.hhi)) + ' puntos. Valores cercanos a diez mil indican que domina un solo operador; debajo de mil ochocientos indica competencia.' : 'sin red fija reportada en 2026.'}"><div class="pl">Concentración HHI<span class="help-q" title="Mide si compiten varias empresas en líneas fijas (0 a 10,000). Cerca de 10,000 = manda un solo operador; debajo de 1,800 = mercado competitivo.">?</span></div><div class="pv">${m.eco.hhi !== null ? fmtInt(Math.round(m.eco.hhi)) : 'Sin red fija'}</div></div>
            <div class="eco-p-item" data-speak-title="Crecimiento a 3 años" data-speak="Crecimiento de antenas celulares en los últimos tres años en ${esc(m.nom)}: ${m.eco.g3y !== null ? (m.eco.g3y >= 0 ? 'más ' : '') + m.eco.g3y + ' por ciento entre 2023 y 2026. La mediana nacional es más 50 por ciento.' : 'sin dato base en 2023.'}"><div class="pl">Crecimiento RB (3 años)<span class="help-q" title="Porcentaje en que aumentaron las antenas celulares entre 2023-S1 y 2026-S1. Mediana nacional: +50%.">?</span></div><div class="pv">${m.eco.g3y !== null ? (m.eco.g3y >= 0 ? '+' : '') + m.eco.g3y + '%' : '—'}</div></div>
          </div>
        </div>

        <div class="stat-grid-2">
          <div class="stat-box" data-speak-title="Radiobases · ${esc(m.nom)}" data-speak="${esc(m.nom)} registra ${rbRec ? fmtInt(rbRec.v) + ' antenas celulares o radiobases en ' + pRb + ', ocupando el puesto número ' + rbRank + ' de ' + rbScored.length + ' municipios del país.' : 'sin dato publicado de radiobases en ' + pRb}">
            <div class="s-lbl"><span>Radiobases<span class="help-q" title="Torres o antenas celulares activas reportadas oficialmente ante la SIT.">?</span></span><span>${pRb}</span></div>
            <div class="s-val num">${rbRec ? fmtInt(rbRec.v) : 'Sin dato'}</div>
            <div class="s-meta">${rbRec ? `Ranking <strong>#${rbRank}</strong> / ${rbScored.length}` : 'No publicado'}${prevRb ? `<br>${deltaHtml(rbRec?.v, prevRb.v, SIT.meta.periods_rb[rbIdx-1])}` : ''}</div>
          </div>
          <div class="stat-box" data-speak-title="Líneas Fijas · ${esc(m.nom)}" data-speak="${esc(m.nom)} suma ${fxRec ? fmtInt(fxRec.t) + ' líneas fijas oficiales en ' + pFx + ', ocupando el puesto número ' + fxRank + ' de los 340 municipios.' : 'sin dato de líneas fijas.'}">
            <div class="s-lbl"><span>Líneas Fijas<span class="help-q" title="Conexiones telefónicas fijas por cable o fibra reportadas por operador.">?</span></span><span>${pFx}</span></div>
            <div class="s-val num">${fxRec ? fmtInt(fxRec.t) : 'Sin dato'}</div>
            <div class="s-meta">${fxRec ? `Ranking <strong>#${fxRank}</strong> / 340` : '—'}${prevFx ? `<br>${deltaHtml(fxRec?.t, prevFx.t, SIT.meta.periods_fx[fxIdx-1])}` : ''}</div>
          </div>
        </div>

        <div class="card">
          <div class="card-hd"><h3>Operadores de Líneas Fijas</h3><span>${pFx} · Hoja 08</span></div>
          ${opsHtml}
        </div>

        <div class="card">
          <div class="card-hd"><h3>Evolución Radiobases (2016-S2 – 2026-S1)</h3><span>Hoja 09</span></div>
          ${buildLineChartSVG(SIT.meta.periods_rb, rbSeries, '#0284c7', pRb, 'radiobases')}
        </div>

        <div class="card">
          <div class="card-hd"><h3>Evolución Líneas Fijas (2022-S2 – 2026-S1)</h3><span>Hoja 08</span></div>
          ${buildLineChartSVG(SIT.meta.periods_fx, fxSeries, '#0d9488', pFx, 'líneas fijas')}
        </div>
      `;
    } else if (state.muniSubTab === 'lp') {
      tabBody = `
        <div class="geo-strip num">
          <div class="geo-cell"><div class="gl">GPS Cabecera</div><div class="gv">${m.gps[1].toFixed(4)}° N</div><div class="gs">${Math.abs(m.gps[0]).toFixed(4)}° W</div></div>
          <div class="geo-cell"><div class="gl">Lugares Poblados</div><div class="gv">${fmtInt(m.lp_sum.tot)} sitios</div><div class="gs">${m.eco.lp_rb ? fmtDec(m.eco.lp_rb,2)+' lug./RB' : 'KMZ 2026'}</div></div>
          <div class="geo-cell"><div class="gl">Área Oficial</div><div class="gv">${m.area !== null ? fmtDec(m.area,1)+' km²' : 'Segregado'}</div><div class="gs">${m.area !== null ? 'Municipios.kmz' : 'Post-KMZ'}</div></div>
        </div>
        <div class="card">
          <div class="card-hd"><h3>Lugares Poblados en el Mapa (KMZ 2026)</h3><span>${fmtInt(m.lp_sum.tot)} GPS</span></div>
          <div class="lp-chips" id="lp-chips"></div>
          <input id="lp-filter-input" class="search-input" style="height:30px;padding:0 9px;font-size:11.5px;margin-bottom:7px;" placeholder="Buscar aldea, caserío, colonia o finca..." value="${esc(state.lpSearchQ)}" />
          <div class="lp-list" id="lp-list"></div>
          <div class="chart-note">Haz clic en cualquier sitio de la lista para pulsar su punto GPS exacto sobre el mapa.</div>
        </div>
      `;
    } else {
      const altNames = [...new Set(SIT.meta.periods_rb.map(per => m.rb[per]?.on).filter(Boolean))];
      let specialNote = '';
      if ((m.id === 1801 || m.id === 701) && dep.sp.length > 0) {
        specialNote = `<strong>Nota histórica (Hoja 09):</strong> En 2018–2022-S1 la SIT publicó filas separadas para <em>${esc(dep.sp[0].name)}</em> (${dep.sp.map(x=>`${x.p}: ${x.v}`).join(' · ')}). No se suman artificialmente a ${esc(m.nom)}.`;
      }
      tabBody = `
        <div class="card" style="background:linear-gradient(135deg,#fff1f2 0%,#ffffff 75%);border-color:#fecdd3;">
          <div class="card-hd"><h3 style="color:#9f1239;">Cómo se calcula el puntaje de brecha digital</h3><span class="pill danger">${fmtDec(m.bd.sc, 2)} / 100</span></div>
          <p style="font-size:11.5px;color:var(--ink-2);line-height:1.45;margin-bottom:5px;">
            Va de <strong>0 a 100</strong> y se arma con dos datos de cada municipio, en cinco pasos:
          </p>
          <ol style="margin:0 0 7px 16px;font-size:11px;color:var(--ink-2);line-height:1.48;display:flex;flex-direction:column;gap:3px;">
            <li><strong>Uso de internet:</strong> porcentaje de personas de 7 años o más que usó internet (INE, Censo 2018). <em>(${esc(m.nom)}: <strong>${fmtDec(m.bd.uso,1)}%</strong>)</em></li>
            <li><strong>Antenas por habitante:</strong> antenas de telefonía móvil por cada 10,000 habitantes (SIT, primer semestre de 2026). <em>(${esc(m.nom)}: <strong>${fmtDec(m.bd.ant,2)}</strong>)</em></li>
            <li><strong>Posición en cada dato:</strong> se ordenan los 340 municipios de menor a mayor. El que menos usa internet queda en la posición 1; el que menos antenas tiene por habitante, también. <em>(${esc(m.nom)}: pos <strong>${m.bd.ru}</strong> en uso · pos <strong>${m.bd.ra}</strong> en antenas)</em></li>
            <li><strong>Promedio de las dos posiciones:</strong> <em>(<strong>${m.bd.ru}</strong> + <strong>${m.bd.ra}</strong>) ÷ 2 = <strong>${fmtDec(m.bd.avg, 2)}</strong></em></li>
            <li><strong>Puntaje:</strong> el municipio con el promedio más bajo recibe <strong>100</strong> y el del más alto queda cerca de <strong>0</strong>. <em>(${esc(m.nom)}: <strong>${fmtDec(m.bd.sc, 2)} / 100</strong> · prioridad <strong>#${m.bd.rk}</strong> de 340)</em></li>
          </ol>
        </div>

        <div class="card">
          <div class="card-hd"><h3>Fórmula del Índice ISI (0–100) y HHI</h3><span>OCDE + DOJ/FTC</span></div>
          <p style="font-size:11.5px;color:var(--ink-2);line-height:1.45;">
            El <strong>Índice de Saturación de Infraestructura (ISI)</strong> usa normalización por rango percentil <em>P(·)</em> de la metodología <strong>OCDE de Indicadores Compuestos</strong> sobre los 340 municipios:
          </p>
          <div class="formula-box">ISI = 0.25·P(RB/LP) + 0.25·P(%ConInternet_INE) + 0.20·P(Fijas/Hogares) + 0.15·P(RB) + 0.15·P(10000 - HHI)<br>Brecha Digital Hogares = (Hogares sin Internet / Total Hogares) × 100<br>HHI = Σ (cuota_operador_i %)²  [DOJ / FTC]</div>
          <div class="op-list num" style="margin-top:8px;">
            <div class="op-row"><div class="op-top"><span class="op-name">1. Cobertura móvil por comunidad (25%)</span><span class="op-nums">P = ${m.eco.p1}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p1}%;background:#0284c7"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">2. Conectividad real en hogares INE (25%)</span><span class="op-nums">P = ${m.eco.p2}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p2}%;background:#e11d48"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">3. Penetración fija por hogar SIT/INE (20%)</span><span class="op-nums">P = ${m.eco.p3}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p3}%;background:#0d9488"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">4. Escala absoluta de radiobases (15%)</span><span class="op-nums">P = ${m.eco.p4}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p4}%;background:#6366f1"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">5. Diversidad competitiva HHI fija (15%)</span><span class="op-nums">P = ${m.eco.p5}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p5}%;background:#f59e0b"></div></div></div>
          </div>
          <p class="chart-note"><strong>Umbrales:</strong> ISI ≥ 75 = Alta Saturación · 45–74.9 = Consolidación · &lt; 45 = Baja Saturación / Oportunidad. Complementado con crecimiento real de radiobases a 3 años (2023-S1 → 2026-S1).</p>
        </div>

        <div class="audit-box">
          <div><strong>Trazabilidad Oficial (SIT + INE 2018/2023 + SEGEPLAN + KMZ)</strong></div>
          <div class="audit-row"><strong>Brecha Digital 2018 (Municipal):</strong> XII Censo INE (2018) · ${fmtInt(m.ine.h)} hogares (${fmtDec(m.ine.br,2)}% sin internet)</div>
          <div class="audit-row"><strong>Actualización 2023 (Departamental):</strong> ENCOVI 2023 INE (trazabilidad_brecha_digital.xlsx) · ${esc(m.dep)}: ${fmtDec(deptoById.get(m.did).ine23.br,2)}% hogares sin internet · Uso 7+ años: ${fmtDec(deptoById.get(m.did).ine23.uso,1)}%</div>
          <div class="audit-row"><strong>Educación y Economía (INE · ITU):</strong> DatosEstadisticos_tecnologia_educacion_economico.xlsx · Pob. ${fmtInt(m.soc.pob)} · Analf. ${fmtDec(m.soc.pct_ana,2)}% · Ocup. ${fmtDec(m.soc.pct_ocu,2)}%</div>
          <div class="audit-row"><strong>Pobreza Municipal 2023:</strong> SEGEPLAN / Banco Mundial (Mapas de pobreza 2023, cuadro 7.2) · ${m.ine.pobr23 !== null ? fmtDec(m.ine.pobr23,1)+'%' : 'Sin dato'}</div>
          <div class="audit-row"><strong>Radiobases (${pRb}):</strong> ${rbRec ? `${esc(SIT.meta.pdfs[rbRec.pdf])} · Pág. ${rbRec.pg ?? '—'} · Fila XLSX ${rbRec.r ?? '—'}` : 'Sin registro en Hoja 09.'}</div>
          <div class="audit-row"><strong>Líneas fijas (${pFx}):</strong> ${fxRec ? `${esc(SIT.meta.pdfs[fxRec.pdf])} · Pág. ${fxRec.pg ?? '—'} · Fila XLSX ${fxRec.r ?? '—'}` : '—'}</div>
          <div class="audit-row"><strong>Geolocalización:</strong> Lugares Poblados 2026.kmz (${fmtInt(m.lp_sum.tot)} sitios) ${m.area !== null ? '· Municipios.kmz ('+m.area+' km²)' : ''}</div>
          ${altNames.length ? `<div class="audit-row"><strong>Variantes históricas PDF (2016–2022):</strong> ${esc(altNames.join(', '))}</div>` : ''}
          ${specialNote ? `<div class="audit-note">${specialNote}</div>` : ''}
        </div>
      `;
    }

    container.innerHTML = `
      <div class="ins-header">
        <div class="ins-crumbs">
          <button class="pill clickable" id="btn-goto-depto">← ${esc(m.dep)}</button>
          <span class="pill ine">INE ${String(m.id).padStart(4,'0')}</span>
        </div>
        <div class="ins-title">${esc(m.nom)}</div>
        <div class="ins-actions">
          <button class="btn-sm green" id="btn-xlsx-muni">⬇ Excel (.xlsx)</button>
          <button class="btn-sm purple" id="btn-start-compare">Comparar</button>
          <button class="btn-sm" id="btn-focus-muni">Zoom</button>
          <a class="btn-sm" href="${gmapsUrl}" target="_blank" rel="noopener">Google Maps</a>
          <button class="btn-sm" id="btn-close-muni">✕</button>
        </div>
      </div>

      <div class="sub-tabs">
        <button class="sub-tab ${state.muniSubTab==='datos'?'active':''}" data-sub="datos">Decisión &amp; SIT</button>
        <button class="sub-tab ${state.muniSubTab==='lp'?'active':''}" data-sub="lp">Lugares GPS (${fmtInt(m.lp_sum.tot)})</button>
        <button class="sub-tab ${state.muniSubTab==='audit'?'active':''}" data-sub="audit">Fórmula &amp; Auditoría</button>
      </div>

      ${tabBody}
    `;

    container.querySelectorAll('.sub-tab').forEach(btn => {
      btn.onclick = () => { state.muniSubTab = btn.dataset.sub; renderInspector(); };
    });
    document.getElementById('btn-goto-depto').onclick = () => {
      state.selectedMuniId = null; state.selectedDeptoId = m.did; state.deptoFilter = m.did;
      document.getElementById('depto-filter').value = m.did; layerLp.innerHTML = '';
      zoomToBBox(dep.bb, 0.22); updateMapColors(); renderInspector();
    };
    document.getElementById('btn-xlsx-muni').onclick = () => exportMuniXLSX(m);
    document.getElementById('btn-focus-muni').onclick = () => zoomToBBox(m.bb, 1.3);
    document.getElementById('btn-close-muni').onclick = () => { state.selectedMuniId = null; layerLp.innerHTML = ''; updateMapColors(); renderInspector(); };
    document.getElementById('btn-start-compare').onclick = () => { state.compareMode = true; state.compareMuniId = null; updateCompareBanner(); };
    const guideInlineBtn = document.getElementById('btn-muni-open-guide');
    if (guideInlineBtn) guideInlineBtn.onclick = () => switchView('guide');
    const speakMuniBtn = document.getElementById('btn-muni-speak');
    if (speakMuniBtn) speakMuniBtn.onclick = () => speakCurrentContext();

    if (state.muniSubTab === 'lp') {
      function populateLPList() {
        const chipsEl = document.getElementById('lp-chips');
        const grpLabels = ['Urbano/Cab.', 'Aldeas', 'Caseríos', 'Colonias', 'Fincas', 'Otros'];
        chipsEl.innerHTML = `<button class="lp-chip ${state.lpGroupFilter===-1?'active':''}" data-grp="-1">Todos (${m.lp_sum.tot})</button>` +
          m.lp_sum.grp.map((cnt, gIdx) => cnt > 0 ? `<button class="lp-chip ${state.lpGroupFilter===gIdx?'active':''}" data-grp="${gIdx}"><span class="lp-dot-swatch" style="background:${LP_GRP_COLORS[gIdx]}"></span>${grpLabels[gIdx]} (${cnt})</button>` : '').join('');
        chipsEl.querySelectorAll('.lp-chip').forEach(btn => {
          btn.onclick = () => { state.lpGroupFilter = parseInt(btn.dataset.grp, 10); populateLPList(); renderSelectedMuniLP(); };
        });
        const listEl = document.getElementById('lp-list');
        const pts = SIT.lp[String(m.id)] || [];
        const q = norm(state.lpSearchQ);
        const filtered = pts.filter(pt => (state.lpGroupFilter === -1 || pt[4] === state.lpGroupFilter) && (!q || norm(pt[2] + ' ' + SIT.meta.lp_cats[pt[3]]).includes(q)));
        const shown = filtered.slice(0, 140);
        listEl.innerHTML = shown.length
          ? shown.map((pt, i) => `<div class="lp-row" data-idx="${i}"><span class="lp-row-name"><span class="lp-dot-swatch" style="background:${LP_GRP_COLORS[pt[4]]};margin-right:6px;"></span>${esc(pt[2])}</span><span class="lp-row-meta num">${esc(SIT.meta.lp_cats[pt[3]])}</span></div>`).join('') + (filtered.length > 140 ? `<div style="padding:6px;font-size:10.5px;color:var(--muted);text-align:center;">Mostrando 140 de ${filtered.length} (usa el buscador)</div>` : '')
          : `<div style="padding:10px;font-size:11.5px;color:var(--muted);">Sin lugares poblados con este filtro.</div>`;
        listEl.querySelectorAll('.lp-row').forEach(row => { row.onclick = () => renderSelectedMuniLP(shown[parseInt(row.dataset.idx, 10)]); });
      }
      populateLPList();
      document.getElementById('lp-filter-input').oninput = function() { state.lpSearchQ = this.value; populateLPList(); renderSelectedMuniLP(); };
    }
  }

  function renderComparisonInspector(container, m1, m2) {
    const pRb = '2026-S1', pFx = '2026-S1';
    const r1 = getEcoRecommendation(m1), r2 = getEcoRecommendation(m2);
    const fx1 = m1.fx[pFx], fx2 = m2.fx[pFx];
    const lessSat = m1.eco.isi <= m2.eco.isi ? m1 : m2;
    const moreMature = m1.eco.isi >= m2.eco.isi ? m1 : m2;

    container.innerHTML = `
      <div class="ins-header">
        <div class="ins-crumbs">
          <span class="pill" style="background:var(--purple-soft);color:var(--purple);">Comparación Municipal</span>
          <button class="btn-sm" id="btn-exit-cmp">← Volver a ${esc(m1.nom)}</button>
        </div>
        <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-top:2px;">
          <span style="font-weight:800;font-size:15px;color:#b45309;">● ${esc(m1.nom)}</span>
          <span style="font-size:11.5px;color:var(--muted);">vs</span>
          <span style="font-weight:800;font-size:15px;color:#6d28d9;">● ${esc(m2.nom)}</span>
        </div>
        <div class="ins-actions">
          <button class="btn-sm green" id="btn-xlsx-cmp">⬇ Excel con Mapa (.xlsx)</button>
          <button class="btn-sm" id="btn-share-cmp">Copiar enlace</button>
        </div>
      </div>

      <div class="card" style="background:#faf5ff;border-color:#ddd6fe;">
        <div class="card-hd" style="margin-bottom:5px;"><h3>Conclusión Comparativa (ISI)</h3><span>2026-S1</span></div>
        <p style="font-size:11.5px;color:var(--ink-2);line-height:1.45;">
          <strong>${esc(moreMature.nom)}</strong> (ISI ${fmtDec(moreMature.eco.isi,1)}) posee infraestructura más madura y densa para operar negocios digitales; mientras que <strong>${esc(lessSat.nom)}</strong> (ISI ${fmtDec(lessSat.eco.isi,1)}) presenta menor saturación y mayor margen de crecimiento para nuevos servicios de conectividad.
        </p>
      </div>

      <div class="card">
        <div class="card-hd"><h3>Comparativo Directo</h3><span>2026-S1</span></div>
        <table class="cmp-table">
          <thead><tr><th>Indicador</th><th style="color:#b45309">${esc(m1.nom)}</th><th style="color:#6d28d9">${esc(m2.nom)}</th></tr></thead>
          <tbody class="num">
            <tr><td><strong>Brecha Digital INE (%)</strong></td><td style="color:#be123c;font-weight:800;">${fmtDec(m1.ine.br,2)}%</td><td style="color:#be123c;font-weight:800;">${fmtDec(m2.ine.br,2)}%</td></tr>
            <tr><td>Hogares sin Internet (INE)</td><td>${fmtInt(m1.ine.sin)}</td><td>${fmtInt(m2.ine.sin)}</td></tr>
            <tr><td>Total Hogares (INE)</td><td>${fmtInt(m1.ine.h)}</td><td>${fmtInt(m2.ine.h)}</td></tr>
            <tr><td><strong>Índice ISI (0–100)</strong></td><td><strong>${fmtDec(m1.eco.isi,1)}</strong></td><td><strong>${fmtDec(m2.eco.isi,1)}</strong></td></tr>
            <tr><td>Semáforo</td><td>${r1.shortLabel}</td><td>${r2.shortLabel}</td></tr>
            <tr><td>Radiobases (2026-S1)</td><td>${fmtInt(m1.rb[pRb]?.v)}</td><td>${fmtInt(m2.rb[pRb]?.v)}</td></tr>
            <tr><td>Crecimiento RB (3a)</td><td>${m1.eco.g3y!==null?(m1.eco.g3y>=0?'+':'')+m1.eco.g3y+'%':'—'}</td><td>${m2.eco.g3y!==null?(m2.eco.g3y>=0?'+':'')+m2.eco.g3y+'%':'—'}</td></tr>
            <tr><td>Líneas Fijas (2026-S1)</td><td>${fmtInt(fx1?.t)}</td><td>${fmtInt(fx2?.t)}</td></tr>
            <tr><td>HHI Red Fija</td><td>${m1.eco.hhi!==null?fmtInt(Math.round(m1.eco.hhi)):'Sin red'}</td><td>${m2.eco.hhi!==null?fmtInt(Math.round(m2.eco.hhi)):'Sin red'}</td></tr>
            <tr><td>Lugares Poblados</td><td>${fmtInt(m1.lp_sum.tot)}</td><td>${fmtInt(m2.lp_sum.tot)}</td></tr>
            <tr><td>Lugares / Radiobase</td><td>${m1.eco.lp_rb?fmtDec(m1.eco.lp_rb,2):'—'}</td><td>${m2.eco.lp_rb?fmtDec(m2.eco.lp_rb,2):'—'}</td></tr>
          </tbody>
        </table>
      </div>

      <div class="card">
        <div class="card-hd"><h3>Radiobases (2016-S2 – 2026-S1)</h3><span>Ámbar vs Morado</span></div>
        ${buildLineChartSVG(SIT.meta.periods_rb, SIT.meta.periods_rb.map(p=>m1.rb[p]?.v??null), '#d97706', pRb, 'radiobases', SIT.meta.periods_rb.map(p=>m2.rb[p]?.v??null), '#7c3aed')}
      </div>
      <div class="card">
        <div class="card-hd"><h3>Líneas Fijas (2022-S2 – 2026-S1)</h3><span>Ámbar vs Morado</span></div>
        ${buildLineChartSVG(SIT.meta.periods_fx, SIT.meta.periods_fx.map(p=>m1.fx[p]?.t??null), '#d97706', pFx, 'líneas', SIT.meta.periods_fx.map(p=>m2.fx[p]?.t??null), '#7c3aed')}
      </div>
    `;
    document.getElementById('btn-exit-cmp').onclick = () => { state.compareMode = false; state.compareMuniId = null; updateMapColors(); renderInspector(); };
    document.getElementById('btn-xlsx-cmp').onclick = () => exportCompareXLSX([m1.id, m2.id]);
    document.getElementById('btn-share-cmp').onclick = function() {
      const url = `${location.origin}${location.pathname}#metric=${state.metric}&cmp=${m1.id},${m2.id}`;
      navigator.clipboard?.writeText(url);
      this.textContent = 'Enlace copiado ✓';
      setTimeout(() => { this.textContent = 'Copiar enlace'; }, 1800);
    };
  }

  function renderDeptoInspector(container, dep) {
    const activePeriod = getActivePeriod();
    const pRb = SIT.meta.periods_rb.includes(activePeriod) ? activePeriod : '2026-S1';
    const pFx = SIT.meta.periods_fx.includes(activePeriod) ? activePeriod : '2026-S1';
    const depMunis = munisByDepto.get(dep.id);
    const fxRec = dep.fx[pFx], rbRec = dep.rb[pRb];
    const rbDisplay = rbRec ? rbRec.v : depMunis.reduce((s, m) => s + (m.rb[pRb]?.v || 0), 0);
    const avgIsi = depMunis.reduce((s, m) => s + m.eco.isi, 0) / depMunis.length;
    const ine23 = isIne23Mode(state.metric, activePeriod);
    const d23 = dep.ine23;
    const dbrTxt = (d23.dbr >= 0 ? '+' : '') + fmtDec(d23.dbr, 2) + ' pp';
    const dusoTxt = (d23.duso >= 0 ? '+' : '') + fmtDec(d23.duso, 1) + ' pp';
    const listPeriod = ine23 ? '2018' : activePeriod;
    const ranked = depMunis.map(m => ({ m, v: getMetricValue(m, state.metric, listPeriod) }))
      .sort((a,b) => (b.v ?? -1) - (a.v ?? -1) || a.m.nom.localeCompare(b.m.nom, 'es'));

    container.innerHTML = `
      <div class="ins-header">
        <div class="ins-crumbs">
          <span class="pill" style="background:var(--teal-soft);color:#0f766e;">Departamento</span>
          <span class="pill ine">${depMunis.length} municipios · ISI prom. ${fmtDec(avgIsi,1)}</span>
        </div>
        <div class="ins-title">${esc(dep.nom)}</div>
        <div class="ins-actions">
          <button class="btn-sm green" id="btn-xlsx-depto">⬇ Excel Departamento (.xlsx)</button>
          <button class="btn-sm" id="btn-zoom-dep">Zoom</button>
          <button class="btn-sm" id="btn-all-gt">Todo Guatemala</button>
        </div>
      </div>

      <div class="stat-grid-2">
        <div class="stat-box"><div class="s-lbl"><span>Radiobases</span><span>${pRb}</span></div><div class="s-val num">${fmtInt(rbDisplay)}</div><div class="s-meta">Total oficial departamental</div></div>
        <div class="stat-box"><div class="s-lbl"><span>Líneas Fijas</span><span>${pFx}</span></div><div class="s-val num">${fmtInt(fxRec?.t)}</div><div class="s-meta">Total oficial departamental</div></div>
      </div>

      <div class="card stat-box" style="background:linear-gradient(135deg,#fff1f2 0%,#ffffff 65%);border-color:#fecdd3;" data-speak-title="Brecha Digital 2018 → 2023 · ${esc(dep.nom)}" data-speak="Evolución de la brecha digital en hogares del departamento de ${esc(dep.nom)}: en el Censo INE 2018 era del ${fmtDec(dep.ine.br,2)} por ciento (${fmtInt(dep.ine.sin)} de ${fmtInt(dep.ine.h)} hogares sin internet), y en la ENCOVI 2023 del INE es del ${fmtDec(d23.br,2)} por ciento (${fmtInt(d23.sin)} de ${fmtInt(d23.h)} hogares sin internet), un cambio de ${dbrTxt.replace('pp','puntos porcentuales')}. Además, el uso de internet en personas de 7 años o más subió de ${fmtDec(dep.ine.uso,1)} a ${fmtDec(d23.uso,1)} por ciento.">
        <div class="s-lbl" style="color:#9f1239;margin-bottom:5px;padding-right:24px;">
          <span>Brecha Digital Hogares · 2018 → 2023</span>
          <span class="pill ${d23.dbr <= 0 ? 'ok' : 'danger'}" style="font-size:10px;padding:1px 7px;white-space:nowrap;">${dbrTxt}</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:7px;" class="num">
          <div style="background:#fff;border:1px solid #ffe4e6;border-radius:8px;padding:7px 9px;">
            <div style="font-size:9.5px;font-weight:800;color:var(--muted);text-transform:uppercase;">2018 · Censo INE</div>
            <div style="font-size:19px;font-weight:900;color:#be123c;line-height:1.15;">${fmtDec(dep.ine.br, 2)}%</div>
            <div style="font-size:10px;color:var(--ink-2);">${fmtInt(dep.ine.sin)} / ${fmtInt(dep.ine.h)} hog.</div>
          </div>
          <div style="background:#fff;border:1.5px solid #fda4af;border-radius:8px;padding:7px 9px;">
            <div style="font-size:9.5px;font-weight:800;color:#9f1239;text-transform:uppercase;">2023 · ENCOVI INE</div>
            <div style="font-size:19px;font-weight:900;color:#9f1239;line-height:1.15;">${fmtDec(d23.br, 2)}%</div>
            <div style="font-size:10px;color:var(--ink-2);">${fmtInt(d23.sin)} / ${fmtInt(d23.h)} hog.</div>
          </div>
        </div>
        <div style="height:8px;border-radius:99px;overflow:hidden;display:flex;background:#ffe4e6;margin-bottom:6px;">
          <div style="width:${d23.pc}%;background:#0d9488;" title="2023 Con internet: ${fmtDec(d23.pc,2)}%"></div>
          <div style="width:${d23.br}%;background:#e11d48;" title="2023 Sin internet: ${fmtDec(d23.br,2)}%"></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:10.5px;color:var(--ink-2);" class="num">
          <div>Uso internet 7+: <strong>${fmtDec(dep.ine.uso,1)}% → ${fmtDec(d23.uso,1)}%</strong> <span style="color:#0f766e;">(${dusoTxt})</span></div>
          <div>Pago 2023: <strong>Q${fmtInt(d23.q_int)}</strong> int. · <strong>Q${fmtInt(d23.q_cel)}</strong> cel.</div>
        </div>
        <div style="border-top:1px dashed #fecdd3;margin-top:6px;padding-top:5px;font-size:10.5px;display:flex;justify-content:space-between;align-items:center;" class="num">
          <span style="font-weight:700;color:#9f1239;">Puntaje Brecha Digital promedio (0–100):</span>
          <strong style="color:#be123c;font-size:12.5px;">${fmtDec(dep.bd_avg, 1)} / 100</strong>
        </div>
      </div>

      <div class="card stat-box" style="background:linear-gradient(135deg,#f8fafc 0%,#eff6ff 100%);border-color:#bfdbfe;" data-speak-title="Educación y Economía · ${esc(dep.nom)}" data-speak="Educación y economía del departamento de ${esc(dep.nom)} según el INE: población total ${fmtInt(dep.soc.pob)} personas; ${fmtInt(dep.soc.alf)} alfabetas y ${fmtInt(dep.soc.ana)} analfabetas (${fmtDec(dep.soc.pct_ana,2)} por ciento de población analfabeta). En economía registra ${fmtInt(dep.soc.ocu)} personas ocupadas, equivalente al ${fmtDec(dep.soc.pct_ocu,2)} por ciento de ocupación.">
        <div class="s-lbl" style="color:#1e40af;margin-bottom:5px;padding-right:24px;">
          <span>Educación y Economía (INE · Enfoque ITU)</span>
          <span class="num" style="white-space:nowrap;">Pob. ${fmtInt(dep.soc.pob)}</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;" class="num">
          <div style="background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:7px 9px;">
            <div style="font-size:9.5px;font-weight:800;color:#92400e;text-transform:uppercase;">Educación · Analfabeta</div>
            <div style="font-size:18px;font-weight:900;color:#b45309;line-height:1.15;">${fmtDec(dep.soc.pct_ana, 2)}%</div>
            <div style="font-size:10px;color:var(--ink-2);">Analf.: <strong>${fmtInt(dep.soc.ana)}</strong> · Alfab.: <strong>${fmtInt(dep.soc.alf)}</strong></div>
          </div>
          <div style="background:#fff;border:1px solid #dbeafe;border-radius:8px;padding:7px 9px;">
            <div style="font-size:9.5px;font-weight:800;color:#075985;text-transform:uppercase;">Economía · Ocupación</div>
            <div style="font-size:18px;font-weight:900;color:#0369a1;line-height:1.15;">${fmtDec(dep.soc.pct_ocu, 2)}%</div>
            <div style="font-size:10px;color:var(--ink-2);">Ocup.: <strong>${fmtInt(dep.soc.ocu)}</strong> · Pobr. 23: <strong>${fmtDec(d23.pobr,1)}%</strong></div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-hd"><h3>Municipios de ${esc(dep.nom)}</h3><span>${esc(getMetricTitle(state.metric))}${ine23 ? ' (desglose 2018)' : ''}</span></div>
        <div class="rank-list">
          ${ranked.map((x, idx) => `<div class="rank-item" data-muni="${x.m.id}"><div class="rank-left"><span class="rank-num">${idx+1}</span><div><div class="rank-name">${esc(x.m.nom)}</div><div class="rank-sub">ISI ${fmtDec(x.m.eco.isi,1)} · ${getEcoRecommendation(x.m).shortLabel}</div></div></div><span class="rank-val num">${fmtMetricVal(x.v, state.metric)}</span></div>`).join('')}
        </div>
      </div>
    `;
    document.getElementById('btn-xlsx-depto').onclick = () => exportDeptoXLSX(dep.id);
    document.getElementById('btn-all-gt').onclick = () => { document.getElementById('depto-filter').value = ''; state.deptoFilter = null; state.selectedDeptoId = null; resetZoom(); updateMapColors(); renderInspector(); };
    document.getElementById('btn-zoom-dep').onclick = () => zoomToBBox(dep.bb, 0.22);
    container.querySelectorAll('.rank-item[data-muni]').forEach(el => el.onclick = () => selectAndFocusMuni(parseInt(el.dataset.muni, 10)));
    container.querySelectorAll('.rank-item[data-depto-row]').forEach(el => el.onclick = () => {
      const did = parseInt(el.dataset.deptoRow, 10);
      document.getElementById('depto-filter').value = did;
      state.deptoFilter = did; state.selectedMuniId = null; state.selectedDeptoId = did;
      state.compareMode = false; state.compareMuniId = null; layerLp.innerHTML = '';
      zoomToBBox(deptoById.get(did).bb, 0.22); updateMapColors(); renderInspector();
    });
  }

  // ===== OFFSCREEN CANVAS CARTOGRAPHIC MAP RENDERER FOR EXCEL (.XLSX) =====
  const CMP_MAP_COLORS = ['#f59e0b', '#7c3aed', '#0284c7', '#10b981', '#e11d48'];

  async function renderExportMapPNG(spec) {
    // spec: { mode: 'muni'|'depto'|'compare'|'national', muni, depto, munis, period }
    const W = 1280, H = 860;
    const canvas = document.createElement('canvas');
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext('2d');

    // Clean editorial background
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, W, H);

    // Top dark institutional header bar
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, W, 86);
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(0, 86, W, 4);

    let title = 'Mapa Oficial SIT Guatemala', subtitle = 'Datos Oficiales SIT (2014–2026) + Lugares Poblados KMZ 2026';
    if (spec.mode === 'muni') {
      title = `${spec.muni.nom} (${spec.muni.dep}) · Mapa Municipal y Lugares Poblados`;
      subtitle = `INE ${String(spec.muni.id).padStart(4,'0')} · Índice ISI ${fmtDec(spec.muni.eco.isi,1)}/100 · ${fmtInt(spec.muni.lp_sum.tot)} lugares poblados GPS`;
    } else if (spec.mode === 'depto') {
      title = `Departamento de ${spec.depto.nom} · Semáforo Económico ISI (${spec.period})`;
      subtitle = `${munisByDepto.get(spec.depto.id).length} municipios · Radiobases, Líneas Fijas e Índice de Saturación Económica`;
    } else if (spec.mode === 'compare') {
      title = `Comparación Territorial: ${spec.munis.map(m => m.nom).join(' vs ')}`;
      subtitle = `Corte 2026-S1 · Ubicación geográfica, Índice ISI (OCDE + HHI) e infraestructura oficial SIT`;
    } else {
      title = `Guatemala (340 Municipios) · Índice de Saturación Económica ISI (${spec.period})`;
      subtitle = `139 Baja Saturación (Oportunidad) · 161 En Consolidación · 40 Alta Saturación (Polo Maduro)`;
    }

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 26px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
    ctx.fillText(title, 30, 42);
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '500 15px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
    ctx.fillText(subtitle, 30, 68);

    // Map viewport region on left (x: 24..810, y: 110..816)
    const mapX = 24, mapY = 110, mapW = 786, mapH = 706;
    ctx.fillStyle = '#edf4fa';
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 1.5;
    ctx.fillRect(mapX, mapY, mapW, mapH);
    ctx.strokeRect(mapX, mapY, mapW, mapH);

    // Determine bounding box in SVG coordinates
    let bb = [0, 0, SIT.meta.svg_w, SIT.meta.svg_h];
    if (spec.mode === 'muni') {
      const [x1,y1,x2,y2] = spec.muni.bb;
      const bw = Math.max(45, x2 - x1), bh = Math.max(45, y2 - y1);
      bb = [x1 - bw * 0.65, y1 - bh * 0.65, x2 + bw * 0.65, y2 + bh * 0.65];
    } else if (spec.mode === 'depto') {
      const [x1,y1,x2,y2] = spec.depto.bb;
      const bw = Math.max(55, x2 - x1), bh = Math.max(55, y2 - y1);
      bb = [x1 - bw * 0.22, y1 - bh * 0.22, x2 + bw * 0.22, y2 + bh * 0.22];
    }

    const bbW = bb[2] - bb[0], bbH = bb[3] - bb[1];
    const pad = 22;
    const sc = Math.min((mapW - 2*pad) / bbW, (mapH - 2*pad) / bbH);
    const offX = mapX + (mapW - bbW * sc) / 2 - bb[0] * sc;
    const offY = mapY + (mapH - bbH * sc) / 2 - bb[1] * sc;
    const isiScale = computeScale('isi', '2026-S1');
    const cmpMap = new Map();
    if (spec.mode === 'compare') spec.munis.forEach((m, i) => cmpMap.set(m.id, { idx: i, col: CMP_MAP_COLORS[i % CMP_MAP_COLORS.length] }));

    ctx.save();
    ctx.beginPath();
    ctx.rect(mapX + 1, mapY + 1, mapW - 2, mapH - 2);
    ctx.clip();
    ctx.translate(offX, offY);
    ctx.scale(sc, sc);

    // Draw all 340 municipalities
    for (const m of SIT.munis) {
      const path = new Path2D(m.d);
      if (spec.mode === 'muni') {
        ctx.fillStyle = m.id === spec.muni.id ? '#fef3c7' : (m.did === spec.muni.did ? '#e2e8f0' : '#f1f5f9');
      } else if (spec.mode === 'depto') {
        ctx.fillStyle = m.did === spec.depto.id ? isiScale.colorOf(m.eco.isi) : '#e2e8f0';
      } else if (spec.mode === 'compare') {
        ctx.fillStyle = cmpMap.has(m.id) ? cmpMap.get(m.id).col : '#e2e8f0';
      } else {
        ctx.fillStyle = isiScale.colorOf(m.eco.isi);
      }
      ctx.fill(path);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = Math.max(0.35, 0.7 / sc);
      ctx.stroke(path);
    }

    // Lakes
    for (const lk of SIT.lakes) {
      const path = new Path2D(lk.d);
      ctx.fillStyle = '#7dd3fc'; ctx.fill(path);
      ctx.strokeStyle = '#0284c7'; ctx.lineWidth = Math.max(0.4, 0.7 / sc); ctx.stroke(path);
    }

    // Department borders
    for (const d of SIT.deptos) {
      const path = new Path2D(d.d);
      ctx.strokeStyle = (spec.mode === 'depto' && d.id === spec.depto.id) ? '#0f172a' : 'rgba(30,41,59,0.45)';
      ctx.lineWidth = ((spec.mode === 'depto' && d.id === spec.depto.id) ? 2.2 : 1.0) / sc;
      ctx.stroke(path);
    }

    // Mode-specific highlights
    if (spec.mode === 'muni') {
      const mp = new Path2D(spec.muni.d);
      ctx.strokeStyle = '#d97706'; ctx.lineWidth = 3.2 / sc; ctx.stroke(mp);
      // Plot Lugares Poblados GPS points inside selected muni
      const pts = SIT.lp[String(spec.muni.id)] || [];
      for (const pt of pts) {
        const [px, py] = projLonLat(pt[0], pt[1]);
        ctx.beginPath();
        ctx.arc(px, py, (pt[4] === 0 ? 4.8 : (pt[4] === 1 ? 3.5 : 2.5)) / sc, 0, Math.PI * 2);
        ctx.fillStyle = LP_GRP_COLORS[pt[4]];
        ctx.fill();
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 0.8 / sc; ctx.stroke();
      }
    } else if (spec.mode === 'depto') {
      ctx.textAlign = 'center';
      ctx.font = `bold ${Math.max(8, 11 / sc)}px -apple-system, sans-serif`;
      for (const m of munisByDepto.get(spec.depto.id)) {
        ctx.lineWidth = 3 / sc; ctx.strokeStyle = 'rgba(255,255,255,0.92)';
        ctx.strokeText(m.nom, m.c[0], m.c[1]);
        ctx.fillStyle = '#0f172a'; ctx.fillText(m.nom, m.c[0], m.c[1]);
      }
    } else if (spec.mode === 'compare') {
      for (const m of spec.munis) {
        const mp = new Path2D(m.d);
        ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 2.4 / sc; ctx.stroke(mp);
      }
      // Numbered pins on compared municipalities
      spec.munis.forEach((m, i) => {
        const col = CMP_MAP_COLORS[i % CMP_MAP_COLORS.length];
        const r = 13 / sc;
        ctx.beginPath(); ctx.arc(m.c[0], m.c[1], r, 0, Math.PI * 2);
        ctx.fillStyle = col; ctx.fill();
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2.5 / sc; ctx.stroke();
        ctx.fillStyle = '#ffffff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.font = `bold ${14 / sc}px -apple-system, sans-serif`;
        ctx.fillText(String(i + 1), m.c[0], m.c[1]);
      });
    } else {
      // National: crisp department labels
      ctx.textAlign = 'center';
      ctx.font = `bold ${9.5 / sc}px -apple-system, sans-serif`;
      for (const d of SIT.deptos) {
        const nudge = DEPTO_LABEL_NUDGE[d.id] || [0,0];
        ctx.lineWidth = 2.8 / sc; ctx.strokeStyle = 'rgba(255,255,255,0.92)';
        ctx.strokeText(d.nom.toUpperCase(), d.c[0] + nudge[0], d.c[1] + nudge[1]);
        ctx.fillStyle = '#0f172a'; ctx.fillText(d.nom.toUpperCase(), d.c[0] + nudge[0], d.c[1] + nudge[1]);
      }
    }
    ctx.restore();

    // Right Legend & Summary Panel (x: 828..1256, y: 110..816)
    const rx = 828, ry = 110, rw = 428, rh = 706;
    ctx.fillStyle = '#ffffff'; ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.5;
    ctx.fillRect(rx, ry, rw, rh); ctx.strokeRect(rx, ry, rw, rh);

    let cy = ry + 34;
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';

    if (spec.mode === 'compare') {
      ctx.fillStyle = '#0f172a'; ctx.font = 'bold 18px -apple-system, sans-serif';
      ctx.fillText('Municipios Comparados (2026-S1)', rx + 20, cy);
      cy += 24;
      spec.munis.forEach((m, i) => {
        const col = CMP_MAP_COLORS[i % CMP_MAP_COLORS.length];
        const rec = getEcoRecommendation(m);
        ctx.fillStyle = '#f8fafc'; ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1;
        ctx.fillRect(rx + 18, cy, rw - 36, 108); ctx.strokeRect(rx + 18, cy, rw - 36, 108);
        ctx.fillStyle = col;
        ctx.fillRect(rx + 18, cy, 8, 108);
        ctx.beginPath(); ctx.arc(rx + 42, cy + 22, 12, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 13px -apple-system, sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(String(i + 1), rx + 42, cy + 27);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px -apple-system, sans-serif';
        ctx.fillText(`${m.nom} (${m.dep})`, rx + 62, cy + 27);
        ctx.fillStyle = '#334155'; ctx.font = '600 13px -apple-system, sans-serif';
        ctx.fillText(`ISI: ${fmtDec(m.eco.isi,1)} / 100 · ${rec.shortLabel}`, rx + 36, cy + 54);
        ctx.fillStyle = '#475569'; ctx.font = '500 12.5px -apple-system, sans-serif';
        ctx.fillText(`Radiobases: ${fmtInt(m.rb['2026-S1']?.v)}   ·   Líneas Fijas: ${fmtInt(m.fx['2026-S1']?.t)}`, rx + 36, cy + 76);
        ctx.fillText(`Lug. Poblados: ${fmtInt(m.lp_sum.tot)}   ·   Crec. 3a: ${m.eco.g3y!==null?(m.eco.g3y>=0?'+':'')+m.eco.g3y+'%':'—'}`, rx + 36, cy + 96);
        cy += 120;
      });
    } else if (spec.mode === 'muni') {
      const m = spec.muni, rec = getEcoRecommendation(m);
      // Mini locator map of Guatemala
      const lmX = rx + 24, lmY = cy - 10, lmW = rw - 48, lmH = 260;
      ctx.fillStyle = '#f1f5f9'; ctx.fillRect(lmX, lmY, lmW, lmH);
      const lsc = Math.min((lmW - 20) / SIT.meta.svg_w, (lmH - 20) / SIT.meta.svg_h);
      const loX = lmX + (lmW - SIT.meta.svg_w * lsc) / 2, loY = lmY + (lmH - SIT.meta.svg_h * lsc) / 2;
      ctx.save(); ctx.translate(loX, loY); ctx.scale(lsc, lsc);
      for (const d of SIT.deptos) { const p = new Path2D(d.d); ctx.fillStyle = d.id === m.did ? '#bae6fd' : '#e2e8f0'; ctx.fill(p); ctx.strokeStyle='#fff'; ctx.lineWidth=1/lsc; ctx.stroke(p); }
      const mp = new Path2D(m.d); ctx.fillStyle = '#f59e0b'; ctx.fill(mp);
      ctx.restore();
      cy = lmY + lmH + 28;
      ctx.fillStyle = '#0f172a'; ctx.font = 'bold 18px -apple-system, sans-serif';
      ctx.fillText('Indicadores Oficiales (2026-S1)', rx + 20, cy); cy += 26;
      const lines = [
        `Semáforo ISI: ${fmtDec(m.eco.isi,1)} / 100 (${rec.shortLabel})`,
        `Radiobases en operación: ${fmtInt(m.rb['2026-S1']?.v)}`,
        `Líneas fijas totales: ${fmtInt(m.fx['2026-S1']?.t)}`,
        `Lugares poblados (KMZ 2026): ${fmtInt(m.lp_sum.tot)}`,
        `Concentración HHI fija: ${m.eco.hhi!==null?fmtInt(Math.round(m.eco.hhi)):'Sin líneas fijas'}`,
        `Crecimiento RB (3 años): ${m.eco.g3y!==null?(m.eco.g3y>=0?'+':'')+m.eco.g3y+'%':'—'}`,
        `GPS Cabecera: ${m.gps[1].toFixed(4)}° N, ${Math.abs(m.gps[0]).toFixed(4)}° W`
      ];
      ctx.font = '600 13.5px -apple-system, sans-serif'; ctx.fillStyle = '#334155';
      for (const ln of lines) { ctx.fillText(ln, rx + 20, cy); cy += 26; }
      cy += 10;
      ctx.fillStyle = '#0f172a'; ctx.font = 'bold 14px -apple-system, sans-serif';
      ctx.fillText('Leyenda Puntos GPS (Lugares Poblados):', rx + 20, cy); cy += 22;
      const glbls = ['Cabecera/Urbano', 'Aldea', 'Caserío', 'Colonia', 'Finca', 'Otro'];
      glbls.forEach((g, gi) => {
        const gx = rx + 24 + (gi % 2) * 190, gy = cy + Math.floor(gi / 2) * 24;
        ctx.beginPath(); ctx.arc(gx, gy - 4, 5, 0, Math.PI * 2); ctx.fillStyle = LP_GRP_COLORS[gi]; ctx.fill();
        ctx.fillStyle = '#475569'; ctx.font = '500 12.5px -apple-system, sans-serif'; ctx.fillText(g, gx + 12, gy);
      });
    } else {
      // Depto or National ISI Legend
      const scope = spec.mode === 'depto' ? munisByDepto.get(spec.depto.id) : SIT.munis;
      const t0 = scope.filter(m=>m.eco.tier===0).length, t1 = scope.filter(m=>m.eco.tier===1).length, t2 = scope.filter(m=>m.eco.tier===2).length;
      ctx.fillStyle = '#0f172a'; ctx.font = 'bold 18px -apple-system, sans-serif';
      ctx.fillText('Semáforo Económico ISI (0–100)', rx + 20, cy); cy += 28;
      const tiers = [
        { col: '#dc2626', t: `Alta Saturación (≥ 75): ${t2} munis`, s: 'Infraestructura madura y muy cubierta' },
        { col: '#fbbf24', t: `En Consolidación (45–74): ${t1} munis`, s: 'Demanda activa con espacio de mejora' },
        { col: '#10b981', t: `Baja Saturación (< 45): ${t0} munis`, s: 'Alta brecha / oportunidad de expansión' },
      ];
      for (const tr of tiers) {
        ctx.fillStyle = tr.col; ctx.fillRect(rx + 20, cy - 14, 16, 16);
        ctx.fillStyle = '#0f172a'; ctx.font = 'bold 14px -apple-system, sans-serif'; ctx.fillText(tr.t, rx + 44, cy);
        ctx.fillStyle = '#64748b'; ctx.font = '500 12px -apple-system, sans-serif'; ctx.fillText(tr.s, rx + 44, cy + 18);
        cy += 48;
      }
      cy += 16;
      const rbSum = scope.reduce((s,m)=>s+(m.rb[spec.period]?.v||0),0);
      const fxSum = scope.reduce((s,m)=>s+(m.fx[spec.period]?.t||0),0);
      const lpSum = scope.reduce((s,m)=>s+m.lp_sum.tot,0);
      ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px -apple-system, sans-serif';
      ctx.fillText(`Resumen Oficial (${spec.period})`, rx + 20, cy); cy += 26;
      ctx.fillStyle = '#334155'; ctx.font = '600 13.5px -apple-system, sans-serif';
      ctx.fillText(`Municipios incluidos: ${scope.length}`, rx + 20, cy); cy += 25;
      ctx.fillText(`Radiobases en operación: ${fmtInt(rbSum)}`, rx + 20, cy); cy += 25;
      ctx.fillText(`Líneas fijas totales: ${fmtInt(fxSum)}`, rx + 20, cy); cy += 25;
      ctx.fillText(`Lugares poblados (KMZ 2026): ${fmtInt(lpSum)}`, rx + 20, cy); cy += 25;
    }

    // Footer attribution
    ctx.fillStyle = '#64748b'; ctx.font = '500 11.5px -apple-system, sans-serif';
    ctx.fillText('Fuente: SIT Guatemala (Boletines Oficiales 2014–2026) · KMZ Lugares Poblados 2026 · Metodología ISI (OCDE) + HHI (DOJ/FTC)', 24, H - 16);

    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
    const buf = await blob.arrayBuffer();
    return { bytes: new Uint8Array(buf), widthPx: W, heightPx: H, startRow: 2, startCol: 0 };
  }

  // ===== CATEGORICAL EXCEL (.XLSX) BUILDERS (WITH EMBEDDED VISUAL MAP!) =====
  async function exportMuniXLSX(m) {
    const rec = getEcoRecommendation(m);
    const mapImg = await renderExportMapPNG({ mode: 'muni', muni: m, period: '2026-S1' });
    const sMap = [
      ['Mapa Geoespacial Oficial · ' + m.nom + ' (' + m.dep + ')'],
      ['Generado automáticamente desde datos oficiales SIT 2014–2026 + KMZ Lugares Poblados 2026.']
    ];
    const s1 = [
      ['Campo', 'Valor Oficial', 'Fuente / Detalle'],
      ['Código INE', String(m.id).padStart(4,'0'), 'División Político-Administrativa'],
      ['Departamento', m.dep, 'SIT Oficial'],
      ['Municipio', m.nom, 'SIT Oficial'],
      ['Latitud GPS', m.gps[1], m.gps[2]==='kmz'?'Lugares Poblados 2026.kmz':'Centroide geométrico'],
      ['Longitud GPS', m.gps[0], m.gps[2]==='kmz'?'Lugares Poblados 2026.kmz':'Centroide geométrico'],
      ['Área Territorial (km²)', m.area ?? 'No disponible (segregado post-KMZ)', 'Municipios.kmz'],
      ['Lugares Poblados (2026)', m.lp_sum.tot, 'Lugares Poblados 2026.kmz'],
      ['Total Hogares (XII Censo INE 2018)', m.ine.h, 'Censo Población y Vivienda INE 2018 (nivel municipal)'],
      ['Hogares con Internet (2018)', m.ine.con, fmtDec(m.ine.pc, 2) + '% de hogares'],
      ['Hogares sin Internet (2018)', m.ine.sin, fmtDec(m.ine.br, 2) + '% brecha digital municipal'],
      ['% Brecha Digital Hogares 2018 (Municipal)', m.ine.br, 'XII Censo INE 2018'],
      ['Puntaje de Brecha Digital (0 a 100)', m.bd.sc, 'Prioridad #' + m.bd.rk + '/340 · Uso 2018 (' + m.bd.uso + '%, pos ' + m.bd.ru + ') + Antenas/10k 2026 (' + m.bd.ant + ', pos ' + m.bd.ra + ')'],
      ['% Brecha Digital Hogares 2023 (Depto. ' + m.dep + ')', deptoById.get(m.did).ine23.br, 'ENCOVI 2023 INE (publicado a nivel departamental; cambio vs 2018: ' + (deptoById.get(m.did).ine23.dbr >= 0 ? '+' : '') + fmtDec(deptoById.get(m.did).ine23.dbr, 2) + ' pp)'],
      ['% Uso Internet 7+ años 2023 (Depto. ' + m.dep + ')', deptoById.get(m.did).ine23.uso, 'ENCOVI 2023 INE (2018: ' + fmtDec(deptoById.get(m.did).ine.uso, 1) + '%)'],
      ['Población Total (INE)', m.soc.pob, 'DatosEstadisticos_tecnologia_educacion_economico.xlsx'],
      ['Población Alfabeta / Analfabeta (INE)', m.soc.alf + ' / ' + m.soc.ana, fmtDec(m.soc.pct_ana, 2) + '% analfabeta (' + fmtDec(m.soc.pct_alf7, 1) + '% alfabetismo 7+)'],
      ['Población Ocupada (INE)', m.soc.ocu, fmtDec(m.soc.pct_ocu, 2) + '% de ocupación (Enfoque ITU)'],
      ['Población en Pobreza 2023 (%)', m.ine.pobr23 ?? 'Sin dato', 'SEGEPLAN / Banco Mundial (Mapas de pobreza 2023, municipal)'],
      ['Radiobases (2026-S1)', m.rb['2026-S1']?.v ?? null, 'Hoja 09 SIT'],
      ['Líneas Fijas Totales (2026-S1)', m.fx['2026-S1']?.t ?? null, 'Hoja 08 SIT'],
      ['Lugares Poblados por Radiobase', m.eco.lp_rb ?? 'N/A', 'KMZ 2026 / SIT 2026-S1'],
      ['Crecimiento Radiobases 3 años (%)', m.eco.g3y ?? 'N/A', '2023-S1 a 2026-S1'],
      ['Índice HHI Telefonía Fija (DOJ/FTC)', m.eco.hhi ?? 'Sin líneas fijas', 'Suma de cuotas al cuadrado (0-10,000)'],
      ['Índice de Saturación Económica (ISI 0-100)', m.eco.isi, 'Metodología OCDE (4 pilares percentiles)'],
      ['Categoría Semáforo Económico', rec.badge, 'ISI ≥75 Alta | 45-74 Consolidación | <45 Baja'],
      ['Recomendación para Empresas / Comercios', rec.forBiz, 'Basado en ISI + HHI + Crecimiento'],
      ['Recomendación para ISP / Telecom', rec.forTelco, 'Basado en ISI + HHI + Brecha territorial'],
    ];

    const s2 = [['Período', 'Radiobases', 'Líneas Fijas Total', ...SIT.meta.op_names, 'Boletín PDF (RB)', 'Pág. PDF (RB)', 'Fila XLSX (RB)']];
    for (const p of SIT.meta.periods_rb) {
      const rb = m.rb[p], fx = m.fx[p];
      s2.push([
        p, rb ? rb.v : 'Sin dato', fx ? fx.t : 'No aplica',
        ...(fx ? fx.v.map(v => v === null ? 'N/A' : v) : SIT.meta.op_names.map(() => '')),
        rb ? SIT.meta.pdfs[rb.pdf] : '', rb?.pg ?? '', rb?.r ?? ''
      ]);
    }

    const s3 = [['Nombre Lugar Poblado', 'Categoría Oficial', 'Latitud', 'Longitud']];
    for (const pt of (SIT.lp[String(m.id)] || [])) {
      s3.push([pt[2], SIT.meta.lp_cats[pt[3]], pt[1], pt[0]]);
    }

    XLSXWriter.downloadXLSX(`SIT_Municipio_${m.dep}_${m.nom}.xlsx`.replace(/\s+/g,'_'), [
      { name: 'Resumen_y_Recomendacion', rows: s1 },
      { name: 'Mapa_Visual', rows: sMap, headerRowIdx: 0, image: mapImg },
      { name: 'Serie_Historica_SIT', rows: s2 },
      { name: 'Lugares_Poblados_2026', rows: s3 },
    ]);
  }

  async function exportDeptoXLSX(did, period='2026-S1') {
    const dep = deptoById.get(did);
    const depMunis = munisByDepto.get(did);
    const mapImg = await renderExportMapPNG({ mode: 'depto', depto: dep, period });
    const sMap = [
      ['Mapa Departamental · ' + dep.nom + ' (' + period + ')'],
      ['Semáforo Económico ISI (0–100) con los ' + depMunis.length + ' municipios oficiales.']
    ];
    const avgIsi = Math.round((depMunis.reduce((s,m)=>s+m.eco.isi,0)/depMunis.length)*10)/10;
    const s1 = [
      ['Indicador Departamental', 'Valor', 'Detalle'],
      ['Departamento', dep.nom, 'Código INE ' + dep.id],
      ['Cantidad de Municipios', depMunis.length, 'Cobertura completa'],
      ['Período de Corte', period, 'Boletín Oficial SIT'],
      ['Total Radiobases Oficial', dep.rb[period]?.v ?? depMunis.reduce((s,m)=>s+(m.rb[period]?.v||0),0), 'Hoja 09 SIT'],
      ['Total Líneas Fijas Oficial', dep.fx[period]?.t ?? null, 'Hoja 08 SIT'],
      ['Total Hogares Depto (Censo 2018 INE)', dep.ine.h, 'INE Censo 2018 (suma 340 munis)'],
      ['Hogares sin Internet Depto (2018)', dep.ine.sin, fmtDec(dep.ine.br, 2) + '% brecha digital 2018'],
      ['Total Hogares Depto (ENCOVI 2023 INE)', dep.ine23.h, 'INE ENCOVI 2023 (valor expandido departamental)'],
      ['Hogares sin Internet Depto (2023)', dep.ine23.sin, fmtDec(dep.ine23.br, 2) + '% brecha digital 2023 (' + (dep.ine23.dbr >= 0 ? '+' : '') + fmtDec(dep.ine23.dbr, 2) + ' pp vs 2018)'],
      ['Uso de Internet 7+ años (2018 → 2023)', fmtDec(dep.ine.uso, 2) + '% → ' + fmtDec(dep.ine23.uso, 2) + '%', 'Cambio: ' + (dep.ine23.duso >= 0 ? '+' : '') + fmtDec(dep.ine23.duso, 2) + ' pp (Censo 2018 vs ENCOVI 2023)'],
      ['Pago Mensual Mediano Internet / Celular (2023)', 'Q ' + dep.ine23.q_int + ' / Q ' + dep.ine23.q_cel, 'INE ENCOVI 2023 · Pobreza dept.: ' + dep.ine23.pobr + '%'],
      ['Puntaje Brecha Digital Promedio Depto (0-100)', dep.bd_avg, 'Promedio municipal (100 = atender primero)'],
      ['Educación Depto: Alfabeta / Analfabeta (INE)', dep.soc.alf + ' / ' + dep.soc.ana, fmtDec(dep.soc.pct_ana, 2) + '% analfabeta de ' + fmtInt(dep.soc.pob) + ' hab.'],
      ['Economía Depto: Población Ocupada (INE)', dep.soc.ocu, fmtDec(dep.soc.pct_ocu, 2) + '% de ocupación (Enfoque ITU)'],
      ['Total Lugares Poblados (2026)', depMunis.reduce((s,m)=>s+m.lp_sum.tot,0), 'Lugares Poblados 2026.kmz'],
      ['Promedio Índice ISI Departamental', avgIsi, 'Escala 0-100'],
      ['Municipios Alta Saturación (≥75)', depMunis.filter(m=>m.eco.tier===2).length, 'Polo maduro'],
      ['Municipios En Consolidación (45-74)', depMunis.filter(m=>m.eco.tier===1).length, 'Crecimiento moderado'],
      ['Municipios Baja Saturación (<45)', depMunis.filter(m=>m.eco.tier===0).length, 'Oportunidad territorial'],
    ];

    const s2 = [['INE','Municipio','Población','Alfabeta','Analfabeta','% Analfabeta','Pob. Ocupada','% Ocupación','Total Hogares (INE)','Hogares con Internet','Hogares sin Internet','% Brecha Digital INE','Puntaje Brecha (0-100)','Radiobases','Líneas Fijas Total', ...SIT.meta.op_names, 'Lugares Poblados','Lug./RB','Crec. RB 3a (%)','HHI Fijo','ISI (0-100)','Semáforo','Recomendación Empresas','Recomendación ISP/Telecom']];
    for (const m of [...depMunis].sort((a,b)=>b.eco.isi - a.eco.isi)) {
      const fx = m.fx[period], rec = getEcoRecommendation(m);
      s2.push([
        String(m.id).padStart(4,'0'), m.nom, m.soc.pob, m.soc.alf, m.soc.ana, m.soc.pct_ana, m.soc.ocu, m.soc.pct_ocu, m.ine.h, m.ine.con, m.ine.sin, m.ine.br, m.bd.sc, m.rb[period]?.v ?? 'Sin dato', fx?.t ?? 'N/A',
        ...(fx ? fx.v.map(v=>v===null?'N/A':v) : SIT.meta.op_names.map(()=>'')),
        m.lp_sum.tot, m.eco.lp_rb ?? 'N/A', m.eco.g3y ?? 'N/A', m.eco.hhi ?? 'Sin red',
        m.eco.isi, rec.shortLabel, rec.forBiz, rec.forTelco
      ]);
    }

    const s3 = [['Período', 'Radiobases Depto', 'Líneas Fijas Depto']];
    for (const p of SIT.meta.periods_rb) {
      const rbVal = dep.rb[p]?.v ?? depMunis.reduce((s,m)=>s+(m.rb[p]?.v||0),0);
      s3.push([p, rbVal, dep.fx[p]?.t ?? 'No aplica']);
    }

    XLSXWriter.downloadXLSX(`SIT_Departamento_${dep.nom}_${period}.xlsx`.replace(/\s+/g,'_'), [
      { name: 'Resumen_Departamento', rows: s1 },
      { name: 'Mapa_Visual', rows: sMap, headerRowIdx: 0, image: mapImg },
      { name: 'Municipios_Detalle', rows: s2 },
      { name: 'Historico_Depto', rows: s3 },
    ]);
  }

  async function exportCompareXLSX(muniIds) {
    const munis = muniIds.map(id => muniById.get(id)).filter(Boolean);
    if (munis.length < 2) return;
    const mapImg = await renderExportMapPNG({ mode: 'compare', munis, period: '2026-S1' });
    const sMap = [
      ['Mapa Comparativo · ' + munis.map(m => m.nom).join(' vs ')],
      ['Ubicación en Guatemala e indicadores oficiales SIT 2026-S1 + Índice ISI.']
    ];
    const hdr = ['Indicador', ...munis.map(m => `${m.nom} (${m.dep})`)];
    const s1 = [
      hdr,
      ['Código INE', ...munis.map(m => String(m.id).padStart(4,'0'))],
      ['Total Hogares (Censo INE 2018)', ...munis.map(m => m.ine.h)],
      ['Hogares con Internet (2018)', ...munis.map(m => m.ine.con)],
      ['Hogares sin Internet (2018)', ...munis.map(m => m.ine.sin)],
      ['% Brecha Digital Hogares 2018 (Municipal)', ...munis.map(m => m.ine.br)],
      ['Puntaje de Brecha Digital (0-100)', ...munis.map(m => m.bd.sc)],
      ['% Brecha Digital Hogares 2023 (Depto. ENCOVI)', ...munis.map(m => deptoById.get(m.did).ine23.br)],
      ['Población Total (INE)', ...munis.map(m => m.soc.pob)],
      ['Educación: % Población Analfabeta (INE)', ...munis.map(m => m.soc.pct_ana)],
      ['Economía: % Población Ocupada (INE)', ...munis.map(m => m.soc.pct_ocu)],
      ['Población en Pobreza 2023 (% SEGEPLAN)', ...munis.map(m => m.ine.pobr23 ?? 'Sin dato')],
      ['Índice Saturación ISI (0-100)', ...munis.map(m => m.eco.isi)],
      ['Semáforo Económico', ...munis.map(m => getEcoRecommendation(m).badge)],
      ['Radiobases (2026-S1)', ...munis.map(m => m.rb['2026-S1']?.v ?? 0)],
      ['Crecimiento Radiobases 3a (%)', ...munis.map(m => m.eco.g3y ?? 'N/A')],
      ['Líneas Fijas Totales (2026-S1)', ...munis.map(m => m.fx['2026-S1']?.t ?? 0)],
      ['HHI Telefonía Fija (DOJ/FTC)', ...munis.map(m => m.eco.hhi ?? 'Sin red fija')],
      ['Operadores Fijos Activos', ...munis.map(m => m.eco.n_ops)],
      ['Lugares Poblados (KMZ 2026)', ...munis.map(m => m.lp_sum.tot)],
      ['Lugares Poblados por Radiobase', ...munis.map(m => m.eco.lp_rb ?? 'N/A')],
      ['Área KMZ (km²)', ...munis.map(m => m.area ?? 'Post-KMZ')],
      ['Latitud GPS', ...munis.map(m => m.gps[1])],
      ['Longitud GPS', ...munis.map(m => m.gps[0])],
      ...SIT.meta.op_names.map((op, i) => [`Líneas Fijas · ${op} (2026-S1)`, ...munis.map(m => m.fx['2026-S1']?.v[i] ?? 'N/A')]),
      ['Recomendación Empresas', ...munis.map(m => getEcoRecommendation(m).forBiz)],
      ['Recomendación ISP / Telecom', ...munis.map(m => getEcoRecommendation(m).forTelco)],
    ];

    const s2 = [['Período', ...munis.map(m => m.nom)]];
    for (const p of SIT.meta.periods_rb) s2.push([p, ...munis.map(m => m.rb[p]?.v ?? 'Sin dato')]);

    const s3 = [['Período', ...munis.map(m => m.nom)]];
    for (const p of SIT.meta.periods_fx) s3.push([p, ...munis.map(m => m.fx[p]?.t ?? 'Sin dato')]);

    XLSXWriter.downloadXLSX(`SIT_Comparacion_${munis.map(m=>m.nom).join('_vs_')}.xlsx`.replace(/\s+/g,'_').slice(0,80), [
      { name: 'Comparativo_Directo', rows: s1 },
      { name: 'Mapa_Visual', rows: sMap, headerRowIdx: 0, image: mapImg },
      { name: 'Historico_Radiobases', rows: s2 },
      { name: 'Historico_Lineas_Fijas', rows: s3 },
    ]);
  }

  async function exportNationalXLSX(period='2026-S1', customList=null) {
    const list = customList || SIT.munis;
    const mapImg = await renderExportMapPNG({ mode: 'national', period });
    const sMap = [
      ['Mapa Nacional de Guatemala (340 Municipios) · Corte ' + period],
      ['Coloreado según el Índice de Saturación Económica ISI (0–100).']
    ];
    const s1 = [['INE','Departamento','Municipio','Población','Alfabeta','Analfabeta','% Analfabeta','Pob. Ocupada','% Ocupación','Total Hogares (2018)','Hogares con Internet (2018)','Hogares sin Internet (2018)','% Brecha Hogares 2018 (Muni)','Puntaje Brecha (0-100)','% Brecha Hogares 2023 (Depto ENCOVI)','Pobreza 2023 (%)','Radiobases','Líneas Fijas Total', ...SIT.meta.op_names, 'Lugares Poblados 2026','Lug./RB','Área km²','Lat GPS','Lon GPS','Crec. RB 3a (%)','HHI Fijo','ISI (0-100)','Semáforo','Recomendación Empresas','Recomendación ISP']];
    for (const m of list) {
      const fx = m.fx[period], rec = getEcoRecommendation(m), d23 = deptoById.get(m.did).ine23;
      s1.push([
        String(m.id).padStart(4,'0'), m.dep, m.nom, m.soc.pob, m.soc.alf, m.soc.ana, m.soc.pct_ana, m.soc.ocu, m.soc.pct_ocu, m.ine.h, m.ine.con, m.ine.sin, m.ine.br, m.bd.sc, d23.br, m.ine.pobr23 ?? 'Sin dato', m.rb[period]?.v ?? 'Sin dato', fx?.t ?? 'N/A',
        ...(fx ? fx.v.map(v=>v===null?'N/A':v) : SIT.meta.op_names.map(()=>'')),
        m.lp_sum.tot, m.eco.lp_rb ?? 'N/A', m.area ?? '', m.gps[1], m.gps[0],
        m.eco.g3y ?? 'N/A', m.eco.hhi ?? 'Sin red', m.eco.isi, rec.shortLabel, rec.forBiz, rec.forTelco
      ]);
    }
    const s3 = [['Código Depto','Departamento','Población','Alfabeta','Analfabeta','% Analfabeta','Pob. Ocupada','% Ocupación','Puntaje Brecha Prom.','Hogares 2018 (Censo)','Sin Internet 2018','% Brecha 2018','Hogares 2023 (ENCOVI)','Sin Internet 2023','% Brecha 2023','Cambio Brecha (pp)','Uso Int. 7+ 2018 (%)','Uso Int. 7+ 2023 (%)','Cambio Uso (pp)','Pago Int. 2023 (Q)','Pago Cel. 2023 (Q)','Pobreza ENCOVI 2023 (%)']];
    for (const d of SIT.deptos) {
      s3.push([d.id/100, d.nom, d.soc.pob, d.soc.alf, d.soc.ana, d.soc.pct_ana, d.soc.ocu, d.soc.pct_ocu, d.bd_avg, d.ine.h, d.ine.sin, d.ine.br, d.ine23.h, d.ine23.sin, d.ine23.br, d.ine23.dbr, d.ine.uso, d.ine23.uso, d.ine23.duso, d.ine23.q_int, d.ine23.q_cel, d.ine23.pobr]);
    }
    const s2 = [
      ['Componente Metodológico', 'Fórmula / Definición', 'Justificación y Uso Económico'],
      ['Cómo se calcula el Puntaje de Brecha Digital (0 a 100)', 'Va de 0 a 100 en 5 pasos: 1) Uso de internet (% personas 7+ años, INE Censo 2018); 2) Antenas por cada 10,000 habitantes (SIT 2026-S1); 3) Posición 1..340 de menor a mayor en cada dato; 4) Promedio de las dos posiciones; 5) El promedio más bajo recibe 100 y el más alto queda cerca de 0.', 'Priorización territorial: más alto = atender primero. 100% alineado con la hoja Brecha digital de trazabilidad_brecha_digital.xlsx.'],
      ['Educación y Economía (INE · Enfoque ITU)', 'Alfabeta, Analfabeta (% analfabeta = Analfabeta / Población) y Población Ocupada (% ocupación = Ocupada / Población)', 'Fuente oficial: DatosEstadisticos_tecnologia_educacion_economico.xlsx (INE, 340 municipios y 22 departamentos).'],
      ['Brecha Digital en Hogares 2018 (INE)', '(Hogares sin Internet / Total Hogares) × 100', 'Fuente oficial: XII Censo de Población y Vivienda INE (2018), nivel municipal (340 municipios).'],
      ['Brecha Digital en Hogares 2023 (ENCOVI INE)', '(Hogares sin Internet en casa / Total Hogares) × 100', 'Fuente oficial: ENCOVI 2023 del INE (trazabilidad_brecha_digital.xlsx), publicada a nivel departamental (22 departamentos). Sin imputación municipal.'],
      ['Pobreza Municipal 2023 (SEGEPLAN)', 'Población en pobreza (%)', 'SEGEPLAN y Banco Mundial, Mapas de pobreza a nivel municipal 2023, cuadro 7.2.'],
      ['Índice de Saturación de Infraestructura (ISI)', 'ISI = 0.25·P(RB/LP) + 0.25·P(%ConInternet_INE) + 0.20·P(Fijas/Hogares) + 0.15·P(RB) + 0.15·P(10000 - HHI)', 'Normalización percentil (metodología OCDE) sobre 340 municipios integrando SIT 2026 + KMZ 2026 + XII Censo INE. Escala 0 a 100.'],
      ['Índice Herfindahl-Hirschman (HHI)', 'HHI = Σ (cuota_operador_i %)² en líneas fijas 2026-S1', 'Estándar internacional DOJ/FTC para medir concentración y competencia real (>1,800 altamente concentrado; 10,000 monopolio).'],
      ['Crecimiento 3 años Radiobases', '((RB_2026-S1 - RB_2023-S1) / RB_2023-S1) × 100', 'Indica si los operadores están invirtiendo activamente en el municipio o si el mercado está estancado.'],
      ['Umbrales del Semáforo', '≥ 75 Alta Saturación | 45–74.9 Consolidación | < 45 Baja Saturación', 'Traduce los indicadores técnicos a decisiones claras para empresas (conectividad) e inversionistas ISP/telecom (oportunidad).'],
      ['Fuentes Oficiales Verificadas', 'SIT Consolidado 2014–2026 + INE Censo 2018 + ENCOVI 2023 + SEGEPLAN 2023 + KMZ 2026', '100% cifras verificadas con conciliación 0 diferencia local en Hoja 15 y 0 diferencia en trazabilidad 2018.'],
    ];
    XLSXWriter.downloadXLSX(`SIT_Guatemala_${list.length}_Municipios_${period}.xlsx`, [
      { name: 'Municipios_Consolidado', rows: s1 },
      { name: 'Brecha_2018_vs_2023', rows: s3 },
      { name: 'Mapa_Visual', rows: sMap, headerRowIdx: 0, image: mapImg },
      { name: 'Metodologia_ISI_HHI', rows: s2 },
    ]);
  }

  // ===== EXCEL MODAL UI =====
  const excelModal = document.getElementById('excel-modal');
  const expConfigArea = document.getElementById('exp-config-area');
  const expPreview = document.getElementById('exp-sheets-preview');
  const sortedMunisAlpha = [...SIT.munis].sort((a,b) => a.nom.localeCompare(b.nom,'es') || a.dep.localeCompare(b.dep,'es'));
  const sortedDeptosAlpha = [...SIT.deptos].sort((a,b) => a.nom.localeCompare(b.nom,'es'));

  function openExcelModal(forceMode=null) {
    if (forceMode) state.expMode = forceMode;
    else if (state.selectedMuniId && state.compareMuniId) { state.expMode = 'compare'; state.expCompareIds = [state.selectedMuniId, state.compareMuniId]; }
    else if (state.selectedMuniId) state.expMode = 'muni';
    else if (state.selectedDeptoId || state.deptoFilter) state.expMode = 'depto';
    else state.expMode = 'muni';
    excelModal.classList.add('open');
    renderExcelModalBody();
  }

  function renderExcelModalBody() {
    document.querySelectorAll('.exp-mode-btn').forEach(b => b.classList.toggle('active', b.dataset.mode === state.expMode));
    if (state.expMode === 'muni') {
      const defId = state.selectedMuniId || 101;
      expConfigArea.innerHTML = `<div class="exp-field"><label>Selecciona el municipio a exportar:</label><select id="exp-muni-sel">${sortedMunisAlpha.map(m => `<option value="${m.id}" ${m.id===defId?'selected':''}>${esc(m.nom)} (${esc(m.dep)}) — ISI ${fmtDec(m.eco.isi,1)}</option>`).join('')}</select></div>`;
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Resumen_y_Recomendacion</code> (KPIs, GPS, ISI, HHI, Semáforo y recomendación)<br>2. <code>Mapa_Visual</code> (<strong>Mapa cartográfico del municipio + sus puntos GPS incrustado en Excel</strong>)<br>3. <code>Serie_Historica_SIT</code> (Radiobases 2016–2026 + 9 Operadores Fijos 2022–2026 + PDF)<br>4. <code>Lugares_Poblados_2026</code> (Todas las aldeas, caseríos y sitios GPS)`;
    } else if (state.expMode === 'depto') {
      const defDid = state.selectedDeptoId || state.deptoFilter || 100;
      expConfigArea.innerHTML = `
        <div class="exp-field"><label>Selecciona el departamento:</label><select id="exp-depto-sel">${sortedDeptosAlpha.map(d => `<option value="${d.id}" ${d.id===defDid?'selected':''}>${esc(d.nom)} (${munisByDepto.get(d.id).length} municipios)</option>`).join('')}</select></div>
        <div class="exp-field"><label>Período de corte:</label><select id="exp-depto-per">${[...SIT.meta.periods_fx].reverse().map(p => `<option value="${p}">${p}</option>`).join('')}</select></div>
      `;
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Resumen_Departamento</code> (Totales oficiales + distribución Semáforo ISI)<br>2. <code>Mapa_Visual</code> (<strong>Mapa del departamento coloreado por Semáforo ISI incrustado en Excel</strong>)<br>3. <code>Municipios_Detalle</code> (Todos los municipios del depto con operadores, ISI y recomendación)<br>4. <code>Historico_Depto</code> (Serie histórica 2016–2026 del departamento)`;
    } else if (state.expMode === 'compare') {
      expConfigArea.innerHTML = `
        <div class="exp-field"><label>Agregar municipio a la comparación (2 a 5 municipios):</label>
          <div style="display:flex;gap:6px;">
            <select id="exp-cmp-add" style="flex:1">${sortedMunisAlpha.map(m => `<option value="${m.id}">${esc(m.nom)} (${esc(m.dep)})</option>`).join('')}</select>
            <button class="btn-sm" id="btn-cmp-add" style="height:34px;padding:0 12px;">+ Agregar</button>
          </div>
        </div>
        <div class="cmp-chips" id="exp-cmp-chips"></div>
      `;
      function renderChips() {
        const box = document.getElementById('exp-cmp-chips');
        box.innerHTML = state.expCompareIds.map(id => {
          const m = muniById.get(id);
          return `<span class="cmp-chip">${esc(m.nom)} (${esc(m.dep)}) <button data-rm="${id}" title="Quitar">✕</button></span>`;
        }).join('');
        box.querySelectorAll('button[data-rm]').forEach(btn => {
          btn.onclick = () => { state.expCompareIds = state.expCompareIds.filter(x => x !== parseInt(btn.dataset.rm, 10)); renderChips(); };
        });
      }
      renderChips();
      document.getElementById('btn-cmp-add').onclick = () => {
        const id = parseInt(document.getElementById('exp-cmp-add').value, 10);
        if (!state.expCompareIds.includes(id) && state.expCompareIds.length < 5) { state.expCompareIds.push(id); renderChips(); }
      };
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Comparativo_Directo</code> (Tabla lado a lado: ISI, HHI, operadores, lugares poblados y recomendación)<br>2. <code>Mapa_Visual</code> (<strong>Mapa de Guatemala destacando los municipios comparados con etiquetas e ISI</strong>)<br>3. <code>Historico_Radiobases</code> (2016-S2 – 2026-S1 comparados)<br>4. <code>Historico_Lineas_Fijas</code> (2022-S2 – 2026-S1 comparados)`;
    } else {
      expConfigArea.innerHTML = `<div class="exp-field"><label>Período de corte nacional:</label><select id="exp-nat-per">${[...SIT.meta.periods_fx].reverse().map(p => `<option value="${p}">${p} (340 municipios completos)</option>`).join('')}</select></div>`;
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Municipios_Consolidado</code> (340 municipios con operadores, GPS, Lugares Poblados, ISI, HHI y recomendación)<br>2. <code>Mapa_Visual</code> (<strong>Mapa nacional de los 340 municipios coloreado por Semáforo ISI incrustado en Excel</strong>)<br>3. <code>Metodologia_ISI_HHI</code> (Documentación completa de fórmulas y umbrales)`;
    }
  }

  document.getElementById('btn-open-excel-modal').onclick = () => openExcelModal();
  document.getElementById('btn-close-excel-modal').onclick = () => excelModal.classList.remove('open');
  document.getElementById('btn-cancel-excel').onclick = () => excelModal.classList.remove('open');
  excelModal.addEventListener('click', (e) => { if (e.target === excelModal) excelModal.classList.remove('open'); });
  document.querySelectorAll('.exp-mode-btn').forEach(btn => {
    btn.onclick = () => { state.expMode = btn.dataset.mode; renderExcelModalBody(); };
  });
  document.getElementById('btn-do-excel-download').onclick = async () => {
    const btn = document.getElementById('btn-do-excel-download');
    btn.disabled = true; btn.textContent = 'Generando mapa y Excel...';
    try {
      if (state.expMode === 'muni') {
        const id = parseInt(document.getElementById('exp-muni-sel').value, 10);
        await exportMuniXLSX(muniById.get(id));
      } else if (state.expMode === 'depto') {
        const did = parseInt(document.getElementById('exp-depto-sel').value, 10);
        const per = document.getElementById('exp-depto-per').value;
        await exportDeptoXLSX(did, per);
      } else if (state.expMode === 'compare') {
        if (state.expCompareIds.length < 2) { alert('Selecciona al menos 2 municipios para comparar.'); return; }
        await exportCompareXLSX(state.expCompareIds);
      } else {
        await exportNationalXLSX(document.getElementById('exp-nat-per').value);
      }
      excelModal.classList.remove('open');
    } finally {
      btn.disabled = false; btn.textContent = '⬇ Generar y Descargar .xlsx';
    }
  };

  // ===== TABLE VIEW =====
  function initTableView() {
    const pSel = document.getElementById('tbl-period');
    [...SIT.meta.periods_fx].reverse().forEach(p => { const o = document.createElement('option'); o.value = p; o.textContent = `Corte ${p}`; pSel.appendChild(o); });
    pSel.value = state.tblPeriod;
    pSel.onchange = () => { state.tblPeriod = pSel.value; renderTable(); };
    document.getElementById('tbl-search').oninput = renderTable;
    document.getElementById('tbl-depto').onchange = renderTable;
    document.getElementById('tbl-tier').onchange = renderTable;
    document.querySelectorAll('#muni-table thead th[data-sort]').forEach(th => {
      th.onclick = () => {
        const col = th.dataset.sort;
        if (state.tblSort.col === col) state.tblSort.dir *= -1;
        else { state.tblSort.col = col; state.tblSort.dir = (col==='nom'||col==='dep') ? 1 : -1; }
        renderTable();
      };
    });
    document.getElementById('btn-export-table-xlsx').onclick = () => exportNationalXLSX(state.tblPeriod, getFilteredTableRows());
  }

  function getFilteredTableRows() {
    const q = norm(document.getElementById('tbl-search').value);
    const did = document.getElementById('tbl-depto').value ? parseInt(document.getElementById('tbl-depto').value, 10) : null;
    const tierVal = document.getElementById('tbl-tier').value;
    const p = state.tblPeriod;
    let list = SIT.munis.filter(m =>
      (did === null || m.did === did) &&
      (tierVal === '' || m.eco.tier === parseInt(tierVal, 10)) &&
      (!q || norm(m.nom + ' ' + m.dep).includes(q))
    );
    const valOf = (m, col) => {
      switch(col) {
        case 'nom': return m.nom; case 'dep': return m.dep;
        case 'bd_sc': return m.bd.sc;
        case 'ine_br': return m.ine.br; case 'ine_sin': return m.ine.sin;
        case 'edu_ana': return m.soc.pct_ana; case 'eco_ocu': return m.soc.pct_ocu;
        case 'isi': case 'tier': return m.eco.isi;
        case 'rb': return m.rb[p]?.v ?? -1; case 'fx': return m.fx[p]?.t ?? -1;
        case 'g3y': return m.eco.g3y ?? -999;
        default: return m.eco.isi;
      }
    };
    const { col, dir } = state.tblSort;
    list.sort((a,b) => { const va = valOf(a, col), vb = valOf(b, col); return typeof va === 'string' ? va.localeCompare(vb,'es')*dir : (va-vb)*dir || a.nom.localeCompare(b.nom,'es'); });
    return list;
  }

  function renderTable() {
    const p = state.tblPeriod, list = getFilteredTableRows();
    document.getElementById('tbl-count').textContent = `${list.length} de 340 municipios`;
    const tbody = document.getElementById('tbl-body');
    tbody.innerHTML = list.map((m, idx) => {
      const rec = getEcoRecommendation(m);
      return `<tr class="num">
        <td style="color:var(--muted);font-weight:700;">${idx+1}</td>
        <td style="font-weight:700;color:var(--ink);">${esc(m.nom)}</td>
        <td style="color:var(--ink-2);">${esc(m.dep)}</td>
        <td style="font-weight:800;color:#9f1239;">${fmtDec(m.bd.sc,1)}</td>
        <td style="font-weight:800;color:#be123c;">${fmtDec(m.ine.br,1)}%</td>
        <td style="font-weight:700;color:#b45309;">${fmtDec(m.soc.pct_ana,1)}%</td>
        <td style="font-weight:700;color:#0369a1;">${fmtDec(m.soc.pct_ocu,1)}%</td>
        <td style="font-weight:800;">${fmtDec(m.eco.isi,1)}</td>
        <td><span class="pill ${rec.badgeCls}" style="font-size:10px;padding:2px 7px;">${rec.shortLabel}</span></td>
        <td style="font-weight:700;color:var(--accent-dark);">${fmtInt(m.rb[p]?.v)}</td>
        <td style="font-weight:700;color:var(--teal);">${fmtInt(m.fx[p]?.t)}</td>
        <td>${m.eco.g3y !== null ? (m.eco.g3y>=0?'+':'')+m.eco.g3y+'%' : '—'}</td>
        <td><button class="jump-btn" data-jump="${m.id}">Ver mapa →</button></td>
      </tr>`;
    }).join('');
    tbody.querySelectorAll('button[data-jump]').forEach(btn => btn.onclick = () => selectAndFocusMuni(parseInt(btn.dataset.jump, 10)));
  }

  // ===== NATIONAL VIEW =====
  function initNationalView() {
    const latest = SIT.national.serie[SIT.national.serie.length - 1];
    const kpiData = [
      { lbl: `Usuarios móviles (${latest.p})`, val: fmtInt(latest.moviles), sub: `Prepago ${fmtInt(latest.prepago)} · Pospago ${fmtInt(latest.pospago)}` },
      { lbl: `Líneas fijas (${latest.p})`, val: fmtInt(latest.fijas), sub: `${latest.pct_f}% de fijo+móvil (${fmtInt(latest.total_fm)})` },
      { lbl: `Radiobases (${latest.p})`, val: fmtInt(latest.rb), sub: `Suma exacta 340 municipios` },
      { lbl: `Banda Ancha Fija (${latest.p})`, val: fmtInt(latest.baf), sub: `Tráfico BAF: ${fmtDec(latest.tbaf_eb, 2)} exabytes` },
      { lbl: `Smartphones / ETM (${latest.p})`, val: fmtInt(latest.etm), sub: `Tráfico BAM: ${fmtDec(latest.tbam_nac_eb, 2)} EB` },
      { lbl: `Brecha Digital 2018 → 2023 (INE)`, val: `${fmtDec(SIT.meta.ine_totals.br, 1)}% → ${fmtDec(SIT.meta.ine23_totals.br, 1)}%`, sub: `ENCOVI 2023: ${fmtDec(SIT.meta.ine23_totals.dbr, 2)} pp · Uso 7+: ${fmtDec(SIT.meta.ine23_totals.uso, 1)}%` },
      { lbl: `Educación INE · % Analfabeta (ITU)`, val: `${fmtDec(SIT.meta.soc_totals.pct_ana, 2)}%`, sub: `${fmtInt(SIT.meta.soc_totals.ana)} analf. · ${fmtInt(SIT.meta.soc_totals.alf)} alfab.` },
      { lbl: `Economía INE · % Ocupación (ITU)`, val: `${fmtDec(SIT.meta.soc_totals.pct_ocu, 2)}%`, sub: `${fmtInt(SIT.meta.soc_totals.ocu)} ocupadas de ${fmtInt(SIT.meta.soc_totals.pob)} hab.` },
    ];
    document.getElementById('nat-kpis').innerHTML = kpiData.map(k => `<div class="kpi-mini" style="padding:10px 12px;"><span class="lbl">${esc(k.lbl)}</span><span class="val num" style="font-size:19px;">${k.val}</span><span class="sub">${esc(k.sub)}</span></div>`).join('');

    const sSel = document.getElementById('nat-series-select');
    function renderNatChart() {
      const key = sSel.value, labels = SIT.national.serie.map(r => r.p), vals = SIT.national.serie.map(r => r[key]);
      document.getElementById('nat-chart-container').innerHTML = buildLineChartSVG(labels, vals, '#0284c7', latest.p, '') +
        `<div class="chart-note">Serie oficial Hoja 01 (${vals.filter(v=>v!==null).length} períodos publicados). Sin imputación de vacíos.</div>`;
    }
    sSel.onchange = renderNatChart; renderNatChart();

    const opSel = document.getElementById('nat-op-period');
    Object.keys(SIT.national.mobile_ops).sort().reverse().forEach(p => { const o = document.createElement('option'); o.value = p; o.textContent = p; opSel.appendChild(o); });
    function renderNatOps() {
      const p = opSel.value;
      const mob = (SIT.national.mobile_ops[p]?.['Usuarios móviles en operación'] || []).filter(x => x.op !== 'TOTAL');
      const fix = (SIT.national.fixed_ops[p] || []).filter(x => x.op !== 'TOTAL').sort((a,b) => b.v - a.v).slice(0, 5);
      const baf = (SIT.national.internet_etm[p]?.['BAF usuarios'] || []).filter(x => x.op !== 'TOTAL').sort((a,b) => b.v - a.v);
      const blk = (title, items, col) => !items.length ? '' : `<div><div style="font-size:11px;font-weight:800;color:var(--ink-2);margin-bottom:5px;">${esc(title)}</div><div class="op-list">${items.map(it=>`<div class="op-row"><div class="op-top"><span class="op-name">${esc(it.op)}</span><span class="op-nums num">${fmtInt(it.v)} <small>(${fmtDec(it.pct,2)}%)</small></span></div><div class="bar-track"><div class="bar-fill" style="width:${Math.max(1,it.pct)}%;background:${col}"></div></div></div>`).join('')}</div></div>`;
      document.getElementById('nat-ops-container').innerHTML = blk(`Telefonía Móvil (${p} · Hoja 04)`, mob, '#0284c7') + blk(`Telefonía Fija Top 5 (${p} · Hoja 03)`, fix, '#0d9488') + blk(`Banda Ancha Fija - BAF (${p} · Hoja 07)`, baf, '#6366f1');
    }
    opSel.onchange = renderNatOps; renderNatOps();

    const tSearch = document.getElementById('tarifa-search');
    function renderTarifas() {
      const q = norm(tSearch.value), rows = SIT.national.tarifas_latest.filter(r => !q || norm(r.op + ' ' + r.c).includes(q));
      document.getElementById('tarifas-body').innerHTML = rows.map(r => `<tr class="num"><td style="text-align:left;font-weight:600;">${esc(r.op)}</td><td style="text-align:left;white-space:normal;min-width:190px;">${esc(r.c)}</td><td style="font-weight:700;">Q ${fmtDec(r.q,2)}</td><td style="color:var(--muted);">Pág. ${r.pg??'—'}</td></tr>`).join('');
    }
    tSearch.oninput = renderTarifas; renderTarifas();

    document.getElementById('audit-body').innerHTML = [...SIT.national.control_terr].reverse().map(r => `<tr class="num"><td style="text-align:left;font-weight:700;">${esc(r.p)}</td><td style="text-align:left;">${esc(r.mag)}</td><td>${r.nmuni??'—'}</td><td style="font-weight:700;">${fmtInt(r.smuni)}</td><td>${r.tnac!==null?fmtInt(r.tnac):'—'}</td><td>${r.dloc===0?'<span class="pill ok">0</span>':(r.dloc===null?'—':r.dloc)}</td></tr>`).join('');

    const nbBody = document.getElementById('nat-brecha-body');
    if (nbBody) {
      const sortedDeps = [...SIT.deptos].sort((a,b) => b.ine23.br - a.ine23.br);
      const t18 = SIT.meta.ine_totals, t23 = SIT.meta.ine23_totals;
      nbBody.innerHTML = sortedDeps.map(d => {
        const dbrCls = d.ine23.dbr <= 0 ? 'ok' : 'danger';
        const dbrS = (d.ine23.dbr >= 0 ? '+' : '') + fmtDec(d.ine23.dbr, 2) + ' pp';
        const dusoS = (d.ine23.duso >= 0 ? '+' : '') + fmtDec(d.ine23.duso, 1) + ' pp';
        return `<tr class="num">
          <td style="text-align:left;font-weight:700;">${esc(d.nom)}</td>
          <td>${fmtDec(d.ine.br, 2)}%</td>
          <td style="font-weight:800;color:#be123c;">${fmtDec(d.ine23.br, 2)}%</td>
          <td><span class="pill ${dbrCls}">${dbrS}</span></td>
          <td>${fmtDec(d.ine.uso, 1)}%</td>
          <td style="font-weight:700;color:#0f766e;">${fmtDec(d.ine23.uso, 1)}%</td>
          <td style="color:#0f766e;font-weight:700;">${dusoS}</td>
          <td>Q ${fmtInt(d.ine23.q_int)}</td>
          <td>${fmtDec(d.ine23.pobr, 1)}%</td>
        </tr>`;
      }).join('') + `<tr class="num" style="background:#f8fafc;font-weight:800;border-top:2px solid var(--border-strong);">
        <td style="text-align:left;">NACIONAL (22 departamentos)</td>
        <td>${fmtDec(t18.br, 2)}%</td>
        <td style="color:#be123c;">${fmtDec(t23.br, 2)}%</td>
        <td><span class="pill ok">${fmtDec(t23.dbr, 2)} pp</span></td>
        <td>${fmtDec(t18.uso, 1)}%</td>
        <td style="color:#0f766e;">${fmtDec(t23.uso, 1)}%</td>
        <td style="color:#0f766e;">+${fmtDec(t23.duso, 1)} pp</td>
        <td>—</td>
        <td>—</td>
      </tr>`;
    }

    const eduBody = document.getElementById('nat-edu-eco-body');
    if (eduBody) {
      const sDeps = [...SIT.deptos].sort((a,b) => b.soc.pct_ana - a.soc.pct_ana);
      const st = SIT.meta.soc_totals;
      eduBody.innerHTML = sDeps.map(d => `<tr class="num">
        <td style="text-align:left;font-weight:700;">${esc(d.nom)}</td>
        <td>${fmtInt(d.soc.pob)}</td>
        <td>${fmtInt(d.soc.alf)}</td>
        <td>${fmtInt(d.soc.ana)}</td>
        <td style="font-weight:800;color:#b45309;">${fmtDec(d.soc.pct_ana, 2)}%</td>
        <td>${fmtInt(d.soc.ocu)}</td>
        <td style="font-weight:800;color:#0369a1;">${fmtDec(d.soc.pct_ocu, 2)}%</td>
        <td style="font-weight:800;color:#9f1239;">${fmtDec(d.bd_avg, 1)} / 100</td>
      </tr>`).join('') + `<tr class="num" style="background:#f8fafc;font-weight:800;border-top:2px solid var(--border-strong);">
        <td style="text-align:left;">NACIONAL (340 municipios)</td>
        <td>${fmtInt(st.pob)}</td>
        <td>${fmtInt(st.alf)}</td>
        <td>${fmtInt(st.ana)}</td>
        <td style="color:#b45309;">${fmtDec(st.pct_ana, 2)}%</td>
        <td>${fmtInt(st.ocu)}</td>
        <td style="color:#0369a1;">${fmtDec(st.pct_ocu, 2)}%</td>
        <td style="color:#9f1239;">50.1 / 100</td>
      </tr>`;
    }
  }

  function switchView(name) {
    state.view = name;
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.toggle('active', b.dataset.view === name));
    document.querySelectorAll('.view-container').forEach(v => v.classList.toggle('active', v.id === 'view-' + name));
    if (name === 'table') renderTable();
  }
  document.querySelectorAll('.nav-tab').forEach(btn => btn.onclick = () => switchView(btn.dataset.view));

  // ===== GUIDE VIEW INTERACTIVE DEMO BUTTONS =====
  document.getElementById('guide-goto-map').onclick = () => switchView('map');
  document.querySelectorAll('[data-demo-muni]').forEach(btn => {
    btn.onclick = () => {
      metricSel.value = 'isi'; state.metric = 'isi'; stopPlay(); syncSliderToMetric();
      selectAndFocusMuni(parseInt(btn.dataset.demoMuni, 10));
    };
  });
  document.getElementById('guide-demo-zerofx').onclick = () => {
    switchView('table');
    document.getElementById('tbl-tier').value = '0';
    state.tblSort = { col: 'fx', dir: 1 };
    renderTable();
  };
  document.getElementById('guide-demo-cmp').onclick = () => {
    switchView('map');
    metricSel.value = 'isi'; state.metric = 'isi'; stopPlay(); syncSliderToMetric();
    state.selectedMuniId = 101; state.compareMuniId = 2101; state.compareMode = false;
    resetZoom(); updateMapColors(); renderInspector();
  };
  document.getElementById('guide-demo-xlsx').onclick = () => openExcelModal('compare');

  // ===== VOICE DICTATION (SPEECH-TO-TEXT) + TEXT-TO-SPEECH WITH LIVE CAPTIONS =====
  const capBar = document.getElementById('a11y-caption-bar');
  const capDot = document.getElementById('cap-dot');
  const capLabel = document.getElementById('cap-mode-label');
  const capText = document.getElementById('cap-text');
  const capStopBtn = document.getElementById('cap-stop-btn');
  const btnVoiceMic = document.getElementById('btn-voice-mic');
  const btnSearchMic = document.getElementById('search-mic');
  const btnVoiceRead = document.getElementById('btn-voice-read');
  const rateSel = document.getElementById('a11y-rate');

  let activeRecog = null;
  let isSpeaking = false;
  let activeSpeakEl = null;
  let speakRunId = 0;
  let currentUtterance = null;
  let captionTimer = null;

  const btnGuideSpeak = document.getElementById('guide-speak-btn');
  const btnGuideA11yTts = document.getElementById('guide-a11y-tts');

  function updateSpeakButtonsUI(playing) {
    btnVoiceRead.classList.toggle('speaking', playing);
    const vrSpan = btnVoiceRead.querySelector('span');
    if (vrSpan) vrSpan.textContent = playing ? 'Detener' : 'Escuchar';
    if (btnGuideSpeak) {
      btnGuideSpeak.textContent = playing ? '⏹ Detener lectura' : '🔊 Escuchar esta guía';
      btnGuideSpeak.style.background = playing ? '#dc2626' : '#0284c7';
    }
    if (btnGuideA11yTts) {
      btnGuideA11yTts.textContent = playing ? '⏹ Detener lectura' : '🔊 Escuchar guía con subtítulos';
      btnGuideA11yTts.classList.toggle('speaking', playing);
    }
  }

  function showCaption(modeLabel, text, isMic=false) {
    capLabel.textContent = modeLabel;
    capText.textContent = text;
    capDot.classList.toggle('mic', isMic);
    capBar.classList.add('open');
  }
  function stopAllVoice() {
    speakRunId++;
    isSpeaking = false;
    if (captionTimer) { clearTimeout(captionTimer); captionTimer = null; }
    if (currentUtterance) {
      currentUtterance.onend = null;
      currentUtterance.onerror = null;
      currentUtterance = null;
    }
    if (window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
        // Safari/WebKit safety flush to guarantee audio cuts off immediately
        setTimeout(() => {
          if (!isSpeaking && (window.speechSynthesis.speaking || window.speechSynthesis.pending)) {
            try { window.speechSynthesis.pause(); window.speechSynthesis.cancel(); } catch (_) {}
          }
        }, 35);
      } catch(e) {}
    }
    if (activeRecog) { try { activeRecog.stop(); } catch(e) {} activeRecog = null; }
    if (activeSpeakEl) {
      activeSpeakEl.classList.remove('is-speaking');
      const b = activeSpeakEl.querySelector(':scope > .speak-badge-hint');
      if (b) b.textContent = '🔊';
      activeSpeakEl = null;
    }
    btnVoiceMic.classList.remove('active');
    btnSearchMic.classList.remove('listening');
    updateSpeakButtonsUI(false);
    capBar.classList.remove('open');
  }
  capStopBtn.onclick = stopAllVoice;

  // ===== INDIVIDUAL CLICK-TO-SPEAK BUBBLE ENGINE =====
  const BUBBLE_SELECTOR = '.gloss-card, .persona-card, .step-card, .story-box, .eco-rec-box, .eco-p-item, .stat-box, .nat-kpi-grid .kpi-mini';

  function enhanceSpeakBubbles(root=document) {
    root.querySelectorAll(BUBBLE_SELECTOR).forEach(el => {
      if (el.dataset.bubbleReady) return;
      el.dataset.bubbleReady = '1';
      el.classList.add('speak-bubble');
      el.setAttribute('role', 'button');
      el.setAttribute('tabindex', '0');
      if (!el.getAttribute('title')) el.setAttribute('title', 'Toca esta burbuja para escuchar solo este dato');
      if (!el.querySelector(':scope > .speak-badge-hint')) {
        const badge = document.createElement('span');
        badge.className = 'speak-badge-hint';
        badge.setAttribute('aria-hidden', 'true');
        badge.textContent = '🔊';
        el.appendChild(badge);
      }
    });
  }

  function extractBubbleSpeech(el) {
    if (el.dataset.speak) {
      return {
        title: el.dataset.speakTitle || 'Lectura de burbuja',
        text: el.dataset.speak
      };
    }
    const clone = el.cloneNode(true);
    // Remove nested buttons, interactive action bars, tiny '?' marks, and speaker badge so only clean prose is read
    clone.querySelectorAll('button, .speak-badge-hint, .help-q, .persona-actions, .st-hd').forEach(n => n.remove());
    const rawText = (clone.textContent || '').replace(/\s+/g, ' ').trim();
    const headingEl = el.querySelector('h3, h4, .gc-term, .lbl, .s-lbl, .pl, .persona-tag');
    let title = headingEl ? headingEl.textContent.replace(/\?/g,'').replace(/\s+/g,' ').trim() : 'Lectura individual';
    if (title.length > 42) title = title.slice(0, 42) + '…';
    return { title, text: rawText };
  }

  function triggerSpeakBubble(el) {
    // Clicking the currently speaking bubble toggles it off immediately!
    if (activeSpeakEl === el && (isSpeaking || window.speechSynthesis?.speaking)) {
      stopAllVoice();
      return;
    }
    const { title, text } = extractBubbleSpeech(el);
    if (!text) return;
    const sentences = text.split(/(?<=[.!?])\s+/).filter(s => s.trim().length > 0);
    speakSentences(sentences.length ? sentences : [text], `🔊 ${title}`);
    activeSpeakEl = el;
    el.classList.add('is-speaking');
    const b = el.querySelector(':scope > .speak-badge-hint');
    if (b) b.textContent = '⏹';
  }

  document.addEventListener('click', (e) => {
    if (e.target.closest('button, a, input, select, option, textarea')) return;
    const bubble = e.target.closest('.speak-bubble');
    if (!bubble) return;
    e.stopPropagation();
    triggerSpeakBubble(bubble);
  });
  document.addEventListener('keydown', (e) => {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList?.contains('speak-bubble')) {
      e.preventDefault();
      triggerSpeakBubble(e.target);
    }
  });

  function pickSpanishVoice() {
    if (!window.speechSynthesis) return null;
    const vs = window.speechSynthesis.getVoices() || [];
    return vs.find(v => /es[-_]GT/i.test(v.lang))
      || vs.find(v => /es[-_](419|MX|US|CO|CR)/i.test(v.lang))
      || vs.find(v => /^es/i.test(v.lang))
      || null;
  }

  function speakSentences(sentences, title='Lectura con subtítulos') {
    stopAllVoice();
    if (!sentences.length) return;
    const myRun = ++speakRunId;
    isSpeaking = true;
    updateSpeakButtonsUI(true);
    const rate = parseFloat(rateSel?.value || '1');

    if (!window.speechSynthesis) {
      let i = 0;
      function nextCap() {
        if (!isSpeaking || myRun !== speakRunId || i >= sentences.length) {
          if (myRun === speakRunId) stopAllVoice();
          return;
        }
        showCaption(title + ' (solo subtítulos)', sentences[i], false);
        i++;
        captionTimer = setTimeout(nextCap, 4200);
      }
      nextCap();
      return;
    }

    let idx = 0;
    function speakNext() {
      if (!isSpeaking || myRun !== speakRunId || idx >= sentences.length) {
        if (myRun === speakRunId) stopAllVoice();
        return;
      }
      const txt = sentences[idx];
      showCaption(title, txt, false);
      const utt = new SpeechSynthesisUtterance(txt);
      currentUtterance = utt;
      const voice = pickSpanishVoice();
      if (voice) utt.voice = voice;
      utt.lang = voice?.lang || 'es-MX';
      utt.rate = rate;
      utt.onend = () => {
        if (myRun !== speakRunId || !isSpeaking) return;
        idx++;
        speakNext();
      };
      utt.onerror = (ev) => {
        if (myRun !== speakRunId || !isSpeaking) return;
        if (ev && (ev.error === 'canceled' || ev.error === 'interrupted')) return;
        idx++;
        speakNext();
      };
      window.speechSynthesis.speak(utt);
    }
    // Slight 20ms yield after cancel() prevents WebKit from dropping or tangling consecutive utterances
    setTimeout(() => { if (myRun === speakRunId && isSpeaking) speakNext(); }, 20);
  }

  function buildMuniSpeech(m) {
    const rec = getEcoRecommendation(m);
    const dep = deptoById.get(m.did);
    const rb = m.rb['2026-S1']?.v ?? 0;
    const fx = m.fx['2026-S1']?.t ?? 0;
    const lp = m.lp_sum.tot;
    const s = [
      `Resumen oficial de ${m.nom}, departamento de ${m.dep}.`,
      `Según el Censo INE 2018, de ${fmtInt(m.ine.h)} hogares, ${fmtInt(m.ine.sin)} no tienen internet, una brecha digital municipal del ${fmtDec(m.ine.br, 1)} por ciento. En la ENCOVI 2023 a nivel departamental de ${m.dep}, la brecha en hogares es del ${fmtDec(dep.ine23.br, 1)} por ciento.`,
      `En el primer semestre de 2026 registra ${fmtInt(rb)} antenas celulares o radiobases para cubrir ${fmtInt(lp)} comunidades registradas.`,
      fx === 0
        ? `En telefonía fija reporta cero líneas activas, por lo que depende principalmente de señal móvil o enlaces inalámbricos.`
        : `En telefonía fija suma ${fmtInt(fx)} líneas oficiales entre los operadores activos.`,
      m.eco.g3y !== null ? `En los últimos tres años sus antenas crecieron ${m.eco.g3y >= 0 ? 'más ' : ''}${m.eco.g3y} por ciento.` : '',
      `Su Índice de Saturación Económica es de ${fmtDec(m.eco.isi, 1)} sobre 100, clasificado como ${rec.badge}.`,
      `Para empresas o comercios: ${rec.forBiz}`,
      `Para proveedores de internet o inversión en telecomunicaciones: ${rec.forTelco}`
    ].filter(Boolean);
    return s;
  }

  function speakCurrentContext() {
    if (isSpeaking || window.speechSynthesis?.speaking || window.speechSynthesis?.pending) {
      stopAllVoice();
      return;
    }
    if (state.view === 'guide') {
      speakSentences([
        'Bienvenido a la guía inclusiva del Observatorio Geoespacial de la Superintendencia de Telecomunicaciones de Guatemala.',
        'Esta herramienta reúne los datos oficiales de los 340 municipios y 27 mil 352 comunidades de Guatemala en un mapa fácil de entender.',
        'Las radiobases son las antenas celulares que brindan señal móvil. Las líneas fijas son conexiones por cable o fibra de operadores como TELGUA, COMCEL, Cablenet y Claro.',
        'El Semáforo Económico ISI califica a cada municipio de cero a cien: verde significa baja saturación y gran oportunidad para llevar internet; ámbar indica mercado en consolidación; y rojo indica plaza madura con alta infraestructura instalada.',
        'Puedes tocar cualquier municipio en el mapa, presionar Dictar para buscar usando tu voz, o descargar un archivo de Excel con tablas y mapa visual incluido.'
      ], 'Guía en voz alta con subtítulos');
      return;
    }
    if (state.selectedMuniId && state.compareMuniId) {
      const m1 = muniById.get(state.selectedMuniId), m2 = muniById.get(state.compareMuniId);
      speakSentences([
        `Comparación entre ${m1.nom} y ${m2.nom} con datos oficiales del primer semestre de 2026.`,
        `${m1.nom} tiene un Índice de Saturación de ${fmtDec(m1.eco.isi,1)} sobre 100, con ${fmtInt(m1.rb['2026-S1']?.v)} radiobases y ${fmtInt(m1.fx['2026-S1']?.t)} líneas fijas.`,
        `${m2.nom} tiene un Índice de Saturación de ${fmtDec(m2.eco.isi,1)} sobre 100, con ${fmtInt(m2.rb['2026-S1']?.v)} radiobases y ${fmtInt(m2.fx['2026-S1']?.t)} líneas fijas.`
      ], `Comparación ${m1.nom} vs ${m2.nom}`);
      return;
    }
    if (state.selectedMuniId) {
      const m = muniById.get(state.selectedMuniId);
      speakSentences(buildMuniSpeech(m), `Narrativa · ${m.nom}`);
      return;
    }
    if (state.selectedDeptoId) {
      const d = deptoById.get(state.selectedDeptoId);
      speakSentences(buildDeptoSpeech(d), `Departamento · ${d.nom}`);
      return;
    }
    speakSentences([
      'Observatorio Geoespacial de Guatemala con datos oficiales de la SIT hasta el primer semestre de 2026.',
      'A nivel nacional existen 29 mil 186 radiobases, 2 millones 105 mil 12 líneas fijas y 27 mil 352 lugares poblados geolocalizados en los 340 municipios.',
      'Según el Semáforo Económico, 139 municipios presentan baja saturación con alta oportunidad de expansión, 161 están en consolidación y 40 son plazas maduras de alta saturación.',
      'Toca cualquier municipio en el mapa o usa el botón Dictar para decir por ejemplo: Dame los datos de Petén.'
    ], 'Resumen Nacional con subtítulos');
  }

  function buildDeptoSpeech(d, focusMetric=null) {
    const dm = munisByDepto.get(d.id);
    const rb26 = d.rb['2026-S1']?.v ?? dm.reduce((s,m)=>s+(m.rb['2026-S1']?.v||0),0);
    const fx26 = d.fx['2026-S1']?.t ?? dm.reduce((s,m)=>s+(m.fx['2026-S1']?.t||0),0);
    const lpTot = dm.reduce((s,m)=>s+m.lp_sum.tot,0);
    const avgIsi = dm.reduce((s,m)=>s+m.eco.isi,0) / dm.length;
    const t0 = dm.filter(m=>m.eco.tier===0).length, t1 = dm.filter(m=>m.eco.tier===1).length, t2 = dm.filter(m=>m.eco.tier===2).length;
    const topRb = [...dm].sort((a,b)=>(b.rb['2026-S1']?.v||0)-(a.rb['2026-S1']?.v||0))[0];
    const topOport = [...dm].sort((a,b)=>a.eco.isi - b.eco.isi)[0];

    if (focusMetric === 'rb') {
      return [
        `El departamento de ${d.nom} cuenta con ${fmtInt(rb26)} radiobases o antenas celulares en el primer semestre de 2026, distribuidas en sus ${dm.length} municipios.`,
        `El municipio con más antenas en ${d.nom} es ${topRb.nom} con ${fmtInt(topRb.rb['2026-S1']?.v)} radiobases.`
      ];
    }
    if (focusMetric === 'fx_total') {
      return [
        `El departamento de ${d.nom} suma ${fmtInt(fx26)} líneas fijas oficiales en el primer semestre de 2026 entre sus ${dm.length} municipios.`
      ];
    }
    if (focusMetric === 'ine_brecha' || focusMetric === 'ine_sin') {
      const dbrWord = d.ine23.dbr <= 0 ? `bajó ${fmtDec(Math.abs(d.ine23.dbr), 2)} puntos porcentuales` : `subió ${fmtDec(d.ine23.dbr, 2)} puntos porcentuales`;
      return [
        `Evolución de la brecha digital en hogares del departamento de ${d.nom}: en el Censo INE 2018 era del ${fmtDec(d.ine.br, 2)} por ciento (${fmtInt(d.ine.sin)} hogares sin internet), y en la ENCOVI 2023 del INE es del ${fmtDec(d.ine23.br, 2)} por ciento (${fmtInt(d.ine23.sin)} hogares sin internet), es decir, ${dbrWord}.`,
        `El uso de internet en personas de 7 años o más en ${d.nom} pasó de ${fmtDec(d.ine.uso, 1)} por ciento en 2018 a ${fmtDec(d.ine23.uso, 1)} por ciento en 2023.`
      ];
    }
    return [
      `Datos oficiales del departamento de ${d.nom}, integrado por ${dm.length} municipios y ${fmtInt(lpTot)} comunidades registradas.`,
      `En hogares sin internet, pasó de ${fmtDec(d.ine.br, 1)} por ciento en el Censo 2018 a ${fmtDec(d.ine23.br, 1)} por ciento en la ENCOVI 2023 del INE.`,
      `En el primer semestre de 2026 suma ${fmtInt(rb26)} antenas celulares o radiobases y ${fmtInt(fx26)} líneas fijas oficiales.`,
      `Su Índice de Saturación Económica promedio es de ${fmtDec(avgIsi, 1)} sobre 100: tiene ${t0} municipios con baja saturación y alta oportunidad, ${t1} en consolidación y ${t2} de alta saturación.`,
      `El municipio con más radiobases en ${d.nom} es ${topRb.nom} con ${fmtInt(topRb.rb['2026-S1']?.v)}, y el de mayor oportunidad por baja saturación es ${topOport.nom} con índice ${fmtDec(topOport.eco.isi, 1)}.`
    ];
  }

  // Spoken aliases common in Guatemala
  const VOICE_ALIASES = {
    'xela': { type: 'muni', id: 901 },
    'ciudad de guatemala': { type: 'muni', id: 101 },
    'la capital': { type: 'muni', id: 101 },
    'antigua': { type: 'muni', id: 301 },
    'chichi': { type: 'muni', id: 1406 },
    'chichicastenango': { type: 'muni', id: 1406 },
    'petapa': { type: 'muni', id: 117 },
    'barillas': { type: 'muni', id: 1326 },
    'cahabon': { type: 'muni', id: 1612 },
    'lanquin': { type: 'muni', id: 1611 },
    'nebaj': { type: 'muni', id: 1413 },
    'tucuru': { type: 'muni', id: 1606 },
    'comalapa': { type: 'muni', id: 404 },
    'olintepeque': { type: 'muni', id: 903 },
    'ixcan': { type: 'muni', id: 1420 },
    'uspantan': { type: 'muni', id: 1415 },
    'soloma': { type: 'muni', id: 1308 },
    'alotenango': { type: 'muni', id: 314 },
  };

  function stripVoiceFillers(str) {
    let s = ' ' + norm(str) + ' ';
    const fillers = [
      'por favor', 'dame los datos de', 'dame datos de', 'dame informacion de', 'dame la informacion de',
      'dame las radiobases de', 'dame las antenas de', 'dame las lineas fijas de', 'dame el semaforo de',
      'dame el indice de', 'dame el excel de', 'descarga el excel de', 'descargar el excel de',
      'descargar excel de', 'bajar excel de', 'baja el excel de', 'exportar excel de', 'exporta excel de',
      'cuantas radiobases tiene', 'cuantas antenas tiene', 'cuantas lineas fijas tiene', 'cuantos lugares poblados tiene',
      'que tan saturado esta', 'como esta', 'como se encuentra', 'conviene invertir en', 'quiero invertir en',
      'muestrame los datos de', 'muestrame a', 'muestrame', 'mostrar los datos de', 'mostrar', 'ensename',
      'dime los datos de', 'dime de', 'dime', 'quiero ver', 'quiero saber de', 'buscar', 'busca', 'abre', 'abrir', 'ir a',
      'del departamento de', 'el departamento de', 'departamento de', 'depto de',
      'del municipio de', 'el municipio de', 'municipio de', 'en el municipio de', 'en el departamento de',
      'en ', 'de ', 'del ', 'la ', 'el '
    ];
    for (const f of fillers) {
      s = s.replace(new RegExp(' ' + f.trim() + ' ', 'g'), ' ');
    }
    return s.replace(/\s+/g, ' ').trim();
  }

  function findBestEntity(phrase, preferDepto=false) {
    const rawNorm = norm(phrase);
    const cleaned = stripVoiceFillers(phrase);
    const candidates = [cleaned, rawNorm].filter(Boolean);

    // 1. Check exact spoken aliases first
    for (const c of candidates) {
      if (VOICE_ALIASES[c]) {
        const a = VOICE_ALIASES[c];
        return { type: a.type, item: a.type === 'muni' ? muniById.get(a.id) : deptoById.get(a.id) };
      }
    }

    // 2. Exact matches (respecting explicit "departamento de ..." preference)
    for (const c of candidates) {
      if (preferDepto) {
        for (const d of SIT.deptos) if (norm(d.nom) === c) return { type: 'depto', item: d };
      }
      for (const m of SIT.munis) if (norm(m.nom) === c) return { type: 'muni', item: m };
      for (const d of SIT.deptos) if (norm(d.nom) === c) return { type: 'depto', item: d };
    }

    // 3. Word-boundary / phrase substring match (longest entity name found inside spoken sentence!)
    const padded = ' ' + rawNorm + ' ';
    const depInPhrase = SIT.deptos.filter(d => padded.includes(' ' + norm(d.nom) + ' ')).sort((a,b) => b.nom.length - a.nom.length);
    const muniInPhrase = SIT.munis.filter(m => padded.includes(' ' + norm(m.nom) + ' ')).sort((a,b) => b.nom.length - a.nom.length);

    if (preferDepto && depInPhrase.length) return { type: 'depto', item: depInPhrase[0] };
    // Check spoken aliases inside full sentence
    for (const [alias, target] of Object.entries(VOICE_ALIASES)) {
      if (padded.includes(' ' + alias + ' ')) {
        return { type: target.type, item: target.type === 'muni' ? muniById.get(target.id) : deptoById.get(target.id) };
      }
    }
    if (muniInPhrase.length && depInPhrase.length) {
      // If department name is strictly longer (e.g. "Alta Verapaz" vs short word) prefer longer
      if (depInPhrase[0].nom.length > muniInPhrase[0].nom.length) return { type: 'depto', item: depInPhrase[0] };
      return { type: 'muni', item: muniInPhrase[0] };
    }
    if (muniInPhrase.length) return { type: 'muni', item: muniInPhrase[0] };
    if (depInPhrase.length) return { type: 'depto', item: depInPhrase[0] };

    // 4. Partial fallback on cleaned token (>= 4 chars)
    if (cleaned.length >= 4) {
      const mSub = SIT.munis.filter(m => norm(m.nom).includes(cleaned)).sort((a,b) => a.nom.length - b.nom.length);
      if (mSub.length) return { type: 'muni', item: mSub[0] };
      const dSub = SIT.deptos.filter(d => norm(d.nom).includes(cleaned)).sort((a,b) => a.nom.length - b.nom.length);
      if (dSub.length) return { type: 'depto', item: dSub[0] };
    }
    return null;
  }

  function handleVoiceTranscript(raw) {
    const t = norm(raw);
    if (!t) return;

    // Detect requested action & metric WITHOUT exiting early if a place is also named!
    const wantsExcel = t.includes('excel') || t.includes('descarg') || t.includes('export') || t.includes('bajar tabla');
    const wantsDepto = t.includes('departamento') || t.includes('depto');
    const reqIneYear = t.includes('2018') ? '2018' : (t.includes('2023') || t.includes('encovi') ? '2023' : null);
    let reqMetric = null;
    if (t.includes('puntaje') && t.includes('brecha')) reqMetric = 'bd_score';
    else if (t.includes('educacion') || t.includes('analfabet') || t.includes('alfabet')) reqMetric = 'edu_ana';
    else if (t.includes('economia') || t.includes('economico') || t.includes('ocupacion') || t.includes('ocupada') || t.includes('empleo')) reqMetric = 'eco_ocu';
    else if (t.includes('brecha digital') || t.includes('encovi') || (t.includes('brecha') && (t.includes('hogar') || t.includes('ine') || t.includes('internet') || t.includes('censo'))) || t.includes('sin internet')) reqMetric = 'ine_brecha';
    else if (t.includes('hogares sin internet') || t.includes('cuantos hogares')) reqMetric = 'ine_sin';
    else if (t.includes('semaforo') || t.includes('saturad') || t.includes('saturacion') || t.includes('isi') || t.includes('invertir') || t.includes('recomendacion')) reqMetric = 'isi';
    else if (t.includes('radiobase') || t.includes('antena') || t.includes('torre')) reqMetric = 'rb';
    else if (t.includes('linea') && t.includes('fija')) reqMetric = 'fx_total';
    else if (t.includes('brecha')) reqMetric = 'lp_per_rb';
    else if (t.includes('lugares poblados') || t.includes('aldeas') || t.includes('comunidades')) reqMetric = 'lp_tot';

    // 1. Special real-data queries ("municipios sin líneas fijas / cero líneas fijas")
    if ((t.includes('cero') || t.includes('sin') || t.includes('0')) && (t.includes('linea') || t.includes('fija'))) {
      switchView('table');
      document.getElementById('tbl-tier').value = '0';
      state.tblSort = { col: 'fx', dir: 1 };
      renderTable();
      speakSentences([
        'Mostrando los 31 municipios de Guatemala que reportan cero líneas fijas en el primer semestre de 2026.',
        'Todos aparecen ordenados al inicio de la tabla para identificar oportunidades de expansión en red fija.'
      ], 'Consulta por voz · 0 líneas fijas');
      return;
    }

    // 2. Comparison command: "comparar X con Y" or "X versus Y"
    if (t.includes('compar') || t.includes('versus') || t.includes(' vs ') || t.includes('contra')) {
      const cleanedCmp = t.replace(/^(dame la comparacion de|comparar|compara|quiero comparar|descarga el excel de|descargar excel de)\s+/, '');
      const parts = cleanedCmp.split(/\s+(?:con|contra|versus|vs|y)\s+/);
      if (parts.length >= 2) {
        const a = findBestEntity(parts[0], false), b = findBestEntity(parts[1], false);
        if (a?.type === 'muni' && b?.type === 'muni' && a.item.id !== b.item.id) {
          switchView('map');
          if (reqMetric) { metricSel.value = reqMetric; state.metric = reqMetric; stopPlay(); syncSliderToMetric(); }
          state.selectedMuniId = a.item.id; state.compareMuniId = b.item.id; state.compareMode = false;
          resetZoom(); updateMapColors(); renderInspector();
          if (wantsExcel) exportCompareXLSX([a.item.id, b.item.id]);
          speakSentences([
            `Comparando ${a.item.nom} contra ${b.item.nom} con datos oficiales 2026.${wantsExcel ? ' Generando además el archivo de Excel con mapa.' : ''}`,
            `${a.item.nom} tiene Índice ISI de ${fmtDec(a.item.eco.isi,1)}, ${fmtInt(a.item.rb['2026-S1']?.v)} radiobases y ${fmtInt(a.item.fx['2026-S1']?.t)} líneas fijas.`,
            `${b.item.nom} tiene Índice ISI de ${fmtDec(b.item.eco.isi,1)}, ${fmtInt(b.item.rb['2026-S1']?.v)} radiobases y ${fmtInt(b.item.fx['2026-S1']?.t)} líneas fijas.`
          ], `Comparación · ${a.item.nom} vs ${b.item.nom}`);
          return;
        }
      }
    }

    // 3. Whole-country / national summary queries
    if (t.includes('resumen nacional') || t.includes('todo el pais') || t.includes('toda guatemala') || t.includes('panorama nacional')) {
      if (t.includes('panorama')) { switchView('national'); showCaption('Dictado reconocido', 'Abriendo Panorama Nacional SIT', false); return; }
      switchView('map');
      state.deptoFilter = null; state.selectedMuniId = null; state.selectedDeptoId = null;
      document.getElementById('depto-filter').value = '';
      if (reqMetric) { metricSel.value = reqMetric; state.metric = reqMetric; stopPlay(); syncSliderToMetric(); }
      resetZoom(); updateMapColors(); renderInspector();
      speakCurrentContext();
      return;
    }

    // 4. Resolve specific Municipality or Department in the phrase!
    const hit = findBestEntity(raw, wantsDepto);
    if (hit) {
      if (reqMetric) {
        metricSel.value = reqMetric; state.metric = reqMetric; stopPlay(); syncSliderToMetric();
        if (reqIneYear && (reqMetric === 'ine_brecha' || reqMetric === 'ine_sin')) {
          const yIdx = getPeriodsForMetric(reqMetric).indexOf(reqIneYear);
          if (yIdx >= 0) setPeriodIdx(yIdx);
        }
      }
      if (hit.type === 'muni') {
        const m = hit.item;
        searchInput.value = m.nom; searchClear.style.display = 'block';
        selectAndFocusMuni(m.id);
        if (wantsExcel) {
          exportMuniXLSX(m);
          speakSentences([`Descargando el archivo de Excel con mapa visual para el municipio de ${m.nom}, ${m.dep}.`], `Excel · ${m.nom}`);
        } else {
          speakSentences(buildMuniSpeech(m), `Dictado · ${m.nom} (${m.dep})`);
        }
        return;
      } else {
        const d = hit.item;
        switchView('map');
        searchInput.value = d.nom; searchClear.style.display = 'block';
        document.getElementById('depto-filter').value = d.id;
        state.deptoFilter = d.id; state.selectedMuniId = null; state.selectedDeptoId = d.id;
        state.compareMode = false; state.compareMuniId = null;
        layerLp.innerHTML = ''; zoomToBBox(d.bb, 0.22); updateMapColors(); renderInspector();
        if (wantsExcel) {
          exportDeptoXLSX(d.id);
          speakSentences([`Descargando el archivo de Excel departamental con mapa visual para ${d.nom}.`], `Excel · ${d.nom}`);
        } else {
          speakSentences(buildDeptoSpeech(d, reqMetric), `Dictado · Depto. ${d.nom}`);
        }
        return;
      }
    }

    // 5. General view/metric commands when NO specific municipality/department was mentioned
    if (t.includes('guia') || t.includes('manual') || t.includes('ayuda') || t.includes('como interpretar')) { switchView('guide'); speakCurrentContext(); return; }
    if (wantsExcel) { openExcelModal(); showCaption('Dictado reconocido', 'Abriendo centro de descargas Excel (.xlsx)', false); return; }
    if (t.includes('tabla') || t.includes('ranking')) { switchView('table'); showCaption('Dictado reconocido', 'Abriendo explorador y ranking de los 340 municipios', false); return; }
    if (reqMetric) {
      switchView('map'); metricSel.value = reqMetric; state.metric = reqMetric; stopPlay(); syncSliderToMetric();
      if (reqIneYear && (reqMetric === 'ine_brecha' || reqMetric === 'ine_sin')) {
        const yIdx = getPeriodsForMetric(reqMetric).indexOf(reqIneYear);
        if (yIdx >= 0) state.periodIdx = yIdx;
        periodSlider.value = state.periodIdx;
        periodPill.textContent = getActivePeriod();
      }
      updateMapColors(); renderInspector();
      showCaption('Dictado reconocido', `Mostrando mapa de ${getMetricTitle(reqMetric)} (${getActivePeriod()})`, false);
      captionTimer = setTimeout(() => { if (!isSpeaking) capBar.classList.remove('open'); }, 3800);
      return;
    }

    searchInput.value = raw; renderSearch(raw);
    showCaption('Dictado escuchado', `"${raw}" — prueba decir por ejemplo: "Dame los datos de Petén", "Cobán" o "Comparar Guatemala con Jalapa".`, false);
    captionTimer = setTimeout(() => { if (!isSpeaking) capBar.classList.remove('open'); }, 5500);
  }

  function toggleVoiceDictation() {
    if (activeRecog) { stopAllVoice(); return; }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      showCaption('Dictado de voz no soportado en este navegador', 'Usa Google Chrome, Safari o Edge en HTTPS, o escribe tu consulta (ej. "Dame los datos de Petén") en el buscador y presiona Enter.', true);
      captionTimer = setTimeout(() => capBar.classList.remove('open'), 7000);
      return;
    }
    if (location.protocol === 'file:') {
      showCaption('Abre el enlace HTTPS para usar micrófono', 'Los navegadores bloquean el micrófono en archivos locales (file://). Ábrelo en: https://jaredr0.github.io/mapaton-SIT/', true);
      captionTimer = setTimeout(() => capBar.classList.remove('open'), 7500);
      return;
    }

    stopAllVoice();

    // IMPORTANT: Call recog.start() SYNCHRONOUSLY inside click handler!
    // Calling await getUserMedia() before recog.start() expires the user gesture on Safari/Chrome
    // and locks the audio device, causing false "not-allowed" errors even after granting permission.
    const recog = new SR();
    recog.lang = 'es-MX'; // Universally supported Spanish model in Chrome, Safari (macOS/iOS) & Edge
    recog.continuous = false;
    recog.interimResults = true;
    recog.maxAlternatives = 3;
    activeRecog = recog;
    btnVoiceMic.classList.add('active');
    btnSearchMic.classList.add('listening');
    showCaption('Micrófono activo · Escuchando (Español)...', 'Habla ahora: "Dame los datos de Petén", "Cuántas radiobases tiene Cobán", "Comparar Guatemala con Jalapa"...', true);

    let finalTxt = '';
    let lastInterim = '';
    recog.onresult = (e) => {
      let interim = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) finalTxt += e.results[i][0].transcript + ' ';
        else interim += e.results[i][0].transcript;
      }
      lastInterim = interim;
      const live = (finalTxt + interim).trim();
      if (live) showCaption('Escuchando en vivo...', `"${live}"`, true);
    };
    recog.onerror = async (e) => {
      const code = e.error || 'unknown';
      stopAllVoice();
      let msg = '';
      if (code === 'service-not-allowed') {
        msg = 'El servicio de dictado del sistema está desactivado (service-not-allowed). En Mac/iPhone activa Ajustes → Teclado → Dictado, o prueba en Google Chrome.';
      } else if (code === 'not-allowed') {
        let permState = 'unknown';
        try {
          if (navigator.permissions?.query) {
            const st = await navigator.permissions.query({ name: 'microphone' });
            permState = st.state;
          }
        } catch (_) {}
        if (permState === 'granted') {
          msg = 'El sitio ya tiene permiso de micrófono, pero macOS o el navegador bloqueó el servicio de voz (not-allowed). En Mac revisa Ajustes del Sistema → Privacidad y Seguridad → Micrófono (habilita tu navegador) y Ajustes → Teclado → Dictado.';
        } else {
          msg = 'Permiso de micrófono denegado (not-allowed). Permite el micrófono en la configuración del sitio y vuelve a tocar Dictar.';
        }
      } else if (code === 'no-speech') {
        msg = 'No se detectó voz. Toca Dictar de nuevo y habla cerca del micrófono.';
      } else if (code === 'audio-capture') {
        msg = 'No se encontró un micrófono activo (audio-capture). Verifica tu micrófono en Ajustes del Sistema.';
      } else if (code === 'network') {
        msg = 'El reconocimiento de voz requiere conexión a internet (si usas Brave, prueba en Chrome o Safari porque Brave bloquea el servidor de voz).';
      } else {
        msg = `Error de reconocimiento de voz (${code}). También puedes escribir tu frase en el buscador y presionar Enter.`;
      }
      showCaption(`Dictado por voz (${code})`, msg, true);
      captionTimer = setTimeout(() => capBar.classList.remove('open'), 9500);
    };
    recog.onend = () => {
      const heard = (finalTxt || lastInterim).trim();
      activeRecog = null;
      btnVoiceMic.classList.remove('active');
      btnSearchMic.classList.remove('listening');
      if (heard) handleVoiceTranscript(heard);
      else if (!capBar.classList.contains('open')) capBar.classList.remove('open');
    };
    try {
      recog.start();
    } catch (err) {
      stopAllVoice();
      showCaption('Dictado por voz', `No se pudo iniciar el micrófono (${err.message || err}). Recarga la página e intenta de nuevo.`, true);
      captionTimer = setTimeout(() => capBar.classList.remove('open'), 6500);
    }
  }

  btnVoiceMic.onclick = toggleVoiceDictation;
  btnSearchMic.onclick = toggleVoiceDictation;
  btnVoiceRead.onclick = speakCurrentContext;
  document.getElementById('guide-speak-btn').onclick = () => { state.view = 'guide'; speakCurrentContext(); };
  document.getElementById('guide-a11y-mic').onclick = toggleVoiceDictation;
  document.getElementById('guide-a11y-tts').onclick = () => { state.view = 'guide'; speakCurrentContext(); };
  document.getElementById('guide-test-peten').onclick = () => handleVoiceTranscript('Dame los datos de Petén');
  document.getElementById('btn-a11y-large').onclick = function() {
    document.body.classList.toggle('a11y-large');
    this.classList.toggle('green', document.body.classList.contains('a11y-large'));
  };
  document.getElementById('btn-a11y-contrast').onclick = function() {
    document.body.classList.toggle('a11y-contrast');
    this.classList.toggle('green', document.body.classList.contains('a11y-contrast'));
  };

  // Optional URL hash helper for direct municipality deep-linking (e.g. #muni=1601 or #metric=isi)
  initMap();
  const hash = location.hash || '';
  if (hash.includes('metric=bd_score')) { state.metric = 'bd_score'; metricSel.value = 'bd_score'; }
  else if (hash.includes('metric=edu_ana')) { state.metric = 'edu_ana'; metricSel.value = 'edu_ana'; }
  else if (hash.includes('metric=eco_ocu')) { state.metric = 'eco_ocu'; metricSel.value = 'eco_ocu'; }
  else if (hash.includes('metric=ine_brecha')) { state.metric = 'ine_brecha'; metricSel.value = 'ine_brecha'; }
  else if (hash.includes('metric=ine_sin')) { state.metric = 'ine_sin'; metricSel.value = 'ine_sin'; }
  else if (hash.includes('metric=isi')) { state.metric = 'isi'; metricSel.value = 'isi'; }
  syncSliderToMetric();
  const perMatch = hash.match(/period=([0-9A-Za-z-]+)/);
  if (perMatch) {
    const pIdx = getPeriodsForMetric(state.metric).indexOf(perMatch[1]);
    if (pIdx >= 0) { state.periodIdx = pIdx; periodSlider.value = pIdx; periodPill.textContent = perMatch[1]; }
  }
  updateMapColors();
  renderInspector();
  initTableView();
  initNationalView();
  enhanceSpeakBubbles(document);
  if (hash.includes('view=guide')) switchView('guide');
  else if (hash.includes('view=national')) switchView('national');
  const cmpMatch = hash.match(/cmp=(\d+),(\d+)/);
  const mMatch = hash.match(/muni=(\d+)/);
  const dMatch = hash.match(/depto=(\d+)/);
  if (cmpMatch) {
    state.selectedMuniId = parseInt(cmpMatch[1], 10);
    state.compareMuniId = parseInt(cmpMatch[2], 10);
    updateMapColors(); renderInspector();
  } else if (mMatch) {
    selectAndFocusMuni(parseInt(mMatch[1], 10));
  } else if (dMatch) {
    const did = parseInt(dMatch[1], 10);
    if (deptoById.has(did)) {
      document.getElementById('depto-filter').value = did;
      state.deptoFilter = did; state.selectedMuniId = null; state.selectedDeptoId = did;
      zoomToBBox(deptoById.get(did).bb, 0.22); updateMapColors(); renderInspector();
    }
  }
})();
</script>
</body>
</html>
"""

html_out = HTML_TEMPLATE.replace("__SIT_DATA_PAYLOAD__", data_json)
for target_name in ["mapa_sit_guatemala.html", "index.html"]:
    p = os.path.join(OUT_DIR, target_name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Generated {p} ({os.path.getsize(p)/1024:.1f} KB)")
open(os.path.join(OUT_DIR, ".nojekyll"), "w").close()
