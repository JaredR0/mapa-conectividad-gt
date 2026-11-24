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

  @media (max-width: 1160px) {
    .verified-chip { display: none; }
    .brand-text p { display: none; }
  }
  @media (max-width: 980px) {
    html, body { overflow-y: auto; overflow-x: hidden; height: auto; width: 100%; }
    .app { height: auto; min-height: 100vh; width: 100%; }
    header.topbar { height: auto; padding: 9px 10px; flex-wrap: wrap; gap: 7px; width: 100%; }
    .brand { flex: 1 1 0; min-width: 0; }
    .nav-tabs { order: 3; width: 100%; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .nav-tab { justify-content: center; padding: 7px 4px; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .nav-tab svg { display: none; }
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
    #view-table, #view-national { padding: 10px 10px 26px; overflow: visible; width: 100%; }
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
        Mapa Municipal
      </button>
      <button class="nav-tab" data-view="table">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
        Explorador &amp; Ranking
      </button>
      <button class="nav-tab" data-view="national">
        <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        Panorama Nacional
      </button>
    </nav>

    <div class="header-right">
      <button class="btn-excel-hero" id="btn-open-excel-modal">
        <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        <span><span class="xl-long">Descargar </span>Excel (.xlsx)</span>
      </button>
      <span class="verified-chip" title="Conciliación 0 error con archivo oficial SIT + KMZ 2026">
        <span class="verified-dot"></span>
        SIT Oficial · 0 error
      </span>
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
            <input id="map-search" class="search-input" type="text" autocomplete="off" placeholder="Buscar municipio o depto..." />
            <button id="search-clear" class="search-clear" title="Limpiar">✕</button>
            <div id="search-results" class="search-results"></div>
          </div>
          <select id="depto-filter" class="ctrl-select" title="Filtrar departamento">
            <option value="">Todos los deptos (22)</option>
          </select>
        </div>

        <div class="tb-group">
          <select id="metric-select" class="ctrl-select" title="Seleccionar indicador del mapa">
            <option value="isi">Índice de Saturación Económica (ISI 0–100)</option>
            <option value="rb" selected>Radiobases en operación (2016-S2 – 2026-S1)</option>
            <option value="fx_total">Líneas fijas totales (2022-S2 – 2026-S1)</option>
            <option value="lp_per_rb">Brecha: Lugares Poblados / Radiobase</option>
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
              <th data-sort="isi">ISI (0–100)</th>
              <th data-sort="tier">Semáforo</th>
              <th data-sort="rb">Radiobases</th>
              <th data-sort="fx">Líneas Fijas</th>
              <th data-sort="lp">Lug. Pobl.</th>
              <th data-sort="g3y">Crec. 3a</th>
              <th data-sort="hhi">HHI Fijo</th>
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

    function buildSheetXML(rows, headerRowIdx = 0) {
      // Compute column widths
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

      return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  ${colsXml}
  <sheetData>${rowXmls.join('')}</sheetData>
  ${autoFilter}
</worksheet>`;
    }

    function createXLSXBlob(sheets) {
      // sheets: [{name, rows, headerRowIdx}]
      const safeSheets = sheets.map((s, idx) => ({
        name: s.name.replace(/[\\/*?:[\]]/g, '').slice(0, 31) || `Hoja${idx+1}`,
        rows: s.rows,
        headerRowIdx: s.headerRowIdx ?? 0
      }));

      const contentTypes = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  ${safeSheets.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}
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

      // Styles: 0=default text, 1=navy bold header, 2=integer #,##0, 3=decimal #,##0.00
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
        files.push({ name: `xl/worksheets/sheet${i+1}.xml`, bytes: enc.encode(buildSheetXML(s.rows, s.headerRowIdx)) });
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

  function getPeriodsForMetric(metric) {
    if (metric === 'rb' || metric === 'lp_per_rb') return SIT.meta.periods_rb;
    if (metric === 'isi' || metric === 'lp_tot') return ['2026-S1'];
    return SIT.meta.periods_fx;
  }
  function getActivePeriod() {
    const ps = getPeriodsForMetric(state.metric);
    return ps[Math.min(state.periodIdx, ps.length - 1)];
  }
  function getMetricValue(muni, metric, period) {
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
    if (metric === 'isi') return fmtDec(v, 1);
    if (metric === 'lp_per_rb') return fmtDec(v, 2);
    return fmtInt(v);
  }

  function computeScale(metric, period) {
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
    for (const m of SIT.munis) {
      const v = getMetricValue(m, metric, period);
      if (v !== null && v > 0) vals.push(v);
    }
    const palette = metric === 'rb' ? PALETTE_RB : (metric === 'lp_per_rb' ? PALETTE_GAP : (metric === 'lp_tot' ? PALETTE_LP : PALETTE_FX));
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
    const rec = getEcoRecommendation(m);
    const tierCol = m.eco.tier === 2 ? '#f87171' : (m.eco.tier === 1 ? '#fbbf24' : '#34d399');
    tooltip.innerHTML = `
      <div class="tt-title">${esc(m.nom)}</div>
      <div class="tt-dept">${esc(m.dep)} · INE ${String(m.id).padStart(4,'0')}</div>
      <div class="tt-val">
        <span style="font-size:11px;color:#cbd5e1;">${esc(getMetricTitle(state.metric))} (${p})</span>
        <span class="tt-num num">${fmtMetricVal(v, state.metric)}</span>
      </div>
      <div style="font-size:10.5px;color:#cbd5e1;margin-top:4px;display:flex;justify-content:space-between;gap:8px;">
        <span style="color:${tierCol};font-weight:700;">ISI ${fmtDec(m.eco.isi,1)} · ${rec.shortLabel}</span>
        ${rk ? `<span style="color:#94a3b8;">#${rk}/${activeRankMap.size}</span>` : ''}
      </div>
    `;
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

    // Bottom Legend
    document.getElementById('legend-label').textContent = getMetricTitle(state.metric);
    document.getElementById('legend-min').textContent = scale.minLbl;
    document.getElementById('legend-max').textContent = scale.maxLbl;
    document.getElementById('legend-swatches').innerHTML = scale.palette.map(c => `<span style="background:${c}"></span>`).join('');
    document.getElementById('legend-nodata').style.display = scored.length < 340 ? 'inline-flex' : 'none';

    // KPI Strip
    const scopeMunis = state.deptoFilter !== null ? munisByDepto.get(state.deptoFilter) : SIT.munis;
    const scopeScored = state.deptoFilter !== null ? scored.filter(x => x.m.did === state.deptoFilter) : scored;
    const scopeLabel = state.deptoFilter !== null ? deptoById.get(state.deptoFilter).nom : 'Guatemala (340 munis)';
    const topItem = scopeScored[0];

    let k1Val, k1Sub;
    if (state.metric === 'isi') {
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
    document.getElementById('kpi-2-val').textContent = `${scopeScored.length} / ${scopeMunis.length}`;
    document.getElementById('kpi-2-sub').textContent = scopeScored.length === scopeMunis.length ? '100% municipios publicados' : `${scopeMunis.length - scopeScored.length} sin dato en ${p}`;

    const k3Card = document.getElementById('kpi-3-card');
    document.getElementById('kpi-3-lbl').textContent = state.metric === 'lp_per_rb' ? 'Mayor brecha' : 'Municipio líder (#1)';
    if (topItem) {
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
    state.playTimer = setInterval(() => { if (state.periodIdx >= ps.length - 1) stopPlay(); else setPeriodIdx(state.periodIdx + 1); }, 850);
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
    if (state.selectedMuniId && state.compareMuniId) { renderComparisonInspector(container, muniById.get(state.selectedMuniId), muniById.get(state.compareMuniId)); return; }
    if (state.selectedMuniId) { renderMuniInspector(container, muniById.get(state.selectedMuniId)); return; }
    if (state.selectedDeptoId) { renderDeptoInspector(container, deptoById.get(state.selectedDeptoId)); return; }

    const scored = SIT.munis.map(m => ({ m, v: getMetricValue(m, state.metric, activePeriod) }))
      .filter(x => x.v !== null).sort((a,b) => b.v - a.v || a.m.nom.localeCompare(b.m.nom, 'es'));
    const top12 = scored.slice(0, 12);

    container.innerHTML = `
      <div class="ins-header">
        <div class="ins-crumbs">
          <span class="pill">Vista Nacional · 340 Municipios</span>
          <span class="pill ine">${activePeriod}</span>
        </div>
        <div class="ins-title">Explora cualquier municipio</div>
        <p style="font-size:12px;color:var(--muted);line-height:1.45;">
          Haz clic en un municipio del mapa para ver su <strong>Semáforo de Saturación Económica (ISI 0–100)</strong>, recomendación práctica de inversión, operadores oficiales SIT y lugares poblados GPS.
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
      </div>

      <div class="card">
        <div class="card-hd"><h3>Top 12 · ${esc(getMetricTitle(state.metric))}</h3><span>${activePeriod}</span></div>
        <div class="rank-list">
          ${top12.map((x, idx) => {
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
          }).join('')}
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
    container.querySelectorAll('.rank-item[data-muni]').forEach(el => el.onclick = () => selectAndFocusMuni(parseInt(el.dataset.muni, 10)));
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

      tabBody = `
        <!-- Hero Economic Saturation & Recommendation Card -->
        <div class="eco-card tier-${m.eco.tier}">
          <div class="eco-top">
            <div>
              <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);">Índice de Saturación Económica (ISI)</div>
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
            <div class="eco-rec-box"><strong>Si vas a abrir empresa / comercio:</strong> ${esc(rec.forBiz)}</div>
            <div class="eco-rec-box"><strong>Si evalúas invertir en ISP / telecom:</strong> ${esc(rec.forTelco)}</div>
          </div>
          <div class="eco-pillars-mini num">
            <div class="eco-p-item"><div class="pl">Concentración HHI</div><div class="pv">${m.eco.hhi !== null ? fmtInt(Math.round(m.eco.hhi)) : 'Sin red fija'}</div></div>
            <div class="eco-p-item"><div class="pl">Crecimiento RB (3 años)</div><div class="pv">${m.eco.g3y !== null ? (m.eco.g3y >= 0 ? '+' : '') + m.eco.g3y + '%' : '—'}</div></div>
          </div>
        </div>

        <div class="stat-grid-2">
          <div class="stat-box">
            <div class="s-lbl"><span>Radiobases</span><span>${pRb}</span></div>
            <div class="s-val num">${rbRec ? fmtInt(rbRec.v) : 'Sin dato'}</div>
            <div class="s-meta">${rbRec ? `Ranking <strong>#${rbRank}</strong> / ${rbScored.length}` : 'No publicado'}${prevRb ? `<br>${deltaHtml(rbRec?.v, prevRb.v, SIT.meta.periods_rb[rbIdx-1])}` : ''}</div>
          </div>
          <div class="stat-box">
            <div class="s-lbl"><span>Líneas Fijas</span><span>${pFx}</span></div>
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
        <div class="card">
          <div class="card-hd"><h3>Fórmula del Índice ISI (0–100) y HHI</h3><span>OCDE + DOJ/FTC</span></div>
          <p style="font-size:11.5px;color:var(--ink-2);line-height:1.45;">
            El <strong>Índice de Saturación de Infraestructura (ISI)</strong> usa normalización por rango percentil <em>P(·)</em> de la metodología <strong>OCDE de Indicadores Compuestos</strong> sobre los 340 municipios:
          </p>
          <div class="formula-box">ISI = 0.35·P(RB/LP) + 0.30·P(Fijas/LP) + 0.20·P(RB) + 0.15·P(10000 - HHI)<br>HHI = Σ (cuota_operador_i %)²  [DOJ / FTC]</div>
          <div class="op-list num" style="margin-top:8px;">
            <div class="op-row"><div class="op-top"><span class="op-name">1. Cobertura móvil por comunidad (35%)</span><span class="op-nums">P = ${m.eco.p1}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p1}%;background:#0284c7"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">2. Penetración fija por comunidad (30%)</span><span class="op-nums">P = ${m.eco.p2}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p2}%;background:#0d9488"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">3. Escala absoluta de radiobases (20%)</span><span class="op-nums">P = ${m.eco.p3}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p3}%;background:#6366f1"></div></div></div>
            <div class="op-row"><div class="op-top"><span class="op-name">4. Diversidad competitiva HHI fija (15%)</span><span class="op-nums">P = ${m.eco.p4}</span></div><div class="bar-track"><div class="bar-fill" style="width:${m.eco.p4}%;background:#f59e0b"></div></div></div>
          </div>
          <p class="chart-note"><strong>Umbrales:</strong> ISI ≥ 75 = Alta Saturación · 45–74.9 = Consolidación · &lt; 45 = Baja Saturación / Oportunidad. Complementado con crecimiento real de radiobases a 3 años (2023-S1 → 2026-S1).</p>
        </div>

        <div class="audit-box">
          <div><strong>Trazabilidad Oficial (Archivo SIT Consolidado)</strong></div>
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
          <button class="btn-sm green" id="btn-xlsx-cmp">⬇ Descargar Excel Comparación (.xlsx)</button>
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
  }

  function renderDeptoInspector(container, dep) {
    const activePeriod = getActivePeriod();
    const pRb = SIT.meta.periods_rb.includes(activePeriod) ? activePeriod : '2026-S1';
    const pFx = SIT.meta.periods_fx.includes(activePeriod) ? activePeriod : '2026-S1';
    const depMunis = munisByDepto.get(dep.id);
    const fxRec = dep.fx[pFx], rbRec = dep.rb[pRb];
    const rbDisplay = rbRec ? rbRec.v : depMunis.reduce((s, m) => s + (m.rb[pRb]?.v || 0), 0);
    const avgIsi = depMunis.reduce((s, m) => s + m.eco.isi, 0) / depMunis.length;
    const ranked = depMunis.map(m => ({ m, v: getMetricValue(m, state.metric, activePeriod) }))
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

      <div class="card">
        <div class="card-hd"><h3>Municipios de ${esc(dep.nom)}</h3><span>${esc(getMetricTitle(state.metric))}</span></div>
        <div class="rank-list">
          ${ranked.map((x, idx) => `<div class="rank-item" data-muni="${x.m.id}"><div class="rank-left"><span class="rank-num">${idx+1}</span><div><div class="rank-name">${esc(x.m.nom)}</div><div class="rank-sub">ISI ${fmtDec(x.m.eco.isi,1)} · ${getEcoRecommendation(x.m).shortLabel}</div></div></div><span class="rank-val num">${fmtMetricVal(x.v, state.metric)}</span></div>`).join('')}
        </div>
      </div>
    `;
    document.getElementById('btn-xlsx-depto').onclick = () => exportDeptoXLSX(dep.id);
    document.getElementById('btn-all-gt').onclick = () => { document.getElementById('depto-filter').value = ''; state.deptoFilter = null; state.selectedDeptoId = null; resetZoom(); updateMapColors(); renderInspector(); };
    document.getElementById('btn-zoom-dep').onclick = () => zoomToBBox(dep.bb, 0.22);
    container.querySelectorAll('.rank-item[data-muni]').forEach(el => el.onclick = () => selectAndFocusMuni(parseInt(el.dataset.muni, 10)));
  }

  // ===== CATEGORICAL EXCEL (.XLSX) BUILDERS =====
  function exportMuniXLSX(m) {
    const rec = getEcoRecommendation(m);
    const s1 = [
      ['Campo', 'Valor Oficial', 'Fuente / Detalle'],
      ['Código INE', String(m.id).padStart(4,'0'), 'División Político-Administrativa'],
      ['Departamento', m.dep, 'SIT Oficial'],
      ['Municipio', m.nom, 'SIT Oficial'],
      ['Latitud GPS', m.gps[1], m.gps[2]==='kmz'?'Lugares Poblados 2026.kmz':'Centroide geométrico'],
      ['Longitud GPS', m.gps[0], m.gps[2]==='kmz'?'Lugares Poblados 2026.kmz':'Centroide geométrico'],
      ['Área Territorial (km²)', m.area ?? 'No disponible (segregado post-KMZ)', 'Municipios.kmz'],
      ['Lugares Poblados (2026)', m.lp_sum.tot, 'Lugares Poblados 2026.kmz'],
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
      { name: 'Serie_Historica_SIT', rows: s2 },
      { name: 'Lugares_Poblados_2026', rows: s3 },
    ]);
  }

  function exportDeptoXLSX(did, period='2026-S1') {
    const dep = deptoById.get(did);
    const depMunis = munisByDepto.get(did);
    const avgIsi = Math.round((depMunis.reduce((s,m)=>s+m.eco.isi,0)/depMunis.length)*10)/10;
    const s1 = [
      ['Indicador Departamental', 'Valor', 'Detalle'],
      ['Departamento', dep.nom, 'Código INE ' + dep.id],
      ['Cantidad de Municipios', depMunis.length, 'Cobertura completa'],
      ['Período de Corte', period, 'Boletín Oficial SIT'],
      ['Total Radiobases Oficial', dep.rb[period]?.v ?? depMunis.reduce((s,m)=>s+(m.rb[period]?.v||0),0), 'Hoja 09 SIT'],
      ['Total Líneas Fijas Oficial', dep.fx[period]?.t ?? null, 'Hoja 08 SIT'],
      ['Total Lugares Poblados (2026)', depMunis.reduce((s,m)=>s+m.lp_sum.tot,0), 'Lugares Poblados 2026.kmz'],
      ['Promedio Índice ISI Departamental', avgIsi, 'Escala 0-100'],
      ['Municipios Alta Saturación (≥75)', depMunis.filter(m=>m.eco.tier===2).length, 'Polo maduro'],
      ['Municipios En Consolidación (45-74)', depMunis.filter(m=>m.eco.tier===1).length, 'Crecimiento moderado'],
      ['Municipios Baja Saturación (<45)', depMunis.filter(m=>m.eco.tier===0).length, 'Oportunidad territorial'],
    ];

    const s2 = [['INE','Municipio','Radiobases','Líneas Fijas Total', ...SIT.meta.op_names, 'Lugares Poblados','Lug./RB','Crec. RB 3a (%)','HHI Fijo','ISI (0-100)','Semáforo','Recomendación Empresas','Recomendación ISP/Telecom']];
    for (const m of [...depMunis].sort((a,b)=>b.eco.isi - a.eco.isi)) {
      const fx = m.fx[period], rec = getEcoRecommendation(m);
      s2.push([
        String(m.id).padStart(4,'0'), m.nom, m.rb[period]?.v ?? 'Sin dato', fx?.t ?? 'N/A',
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
      { name: 'Municipios_Detalle', rows: s2 },
      { name: 'Historico_Depto', rows: s3 },
    ]);
  }

  function exportCompareXLSX(muniIds) {
    const munis = muniIds.map(id => muniById.get(id)).filter(Boolean);
    if (munis.length < 2) return;
    const hdr = ['Indicador', ...munis.map(m => `${m.nom} (${m.dep})`)];
    const s1 = [
      hdr,
      ['Código INE', ...munis.map(m => String(m.id).padStart(4,'0'))],
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
      { name: 'Historico_Radiobases', rows: s2 },
      { name: 'Historico_Lineas_Fijas', rows: s3 },
    ]);
  }

  function exportNationalXLSX(period='2026-S1', customList=null) {
    const list = customList || SIT.munis;
    const s1 = [['INE','Departamento','Municipio','Radiobases','Líneas Fijas Total', ...SIT.meta.op_names, 'Lugares Poblados 2026','Lug./RB','Área km²','Lat GPS','Lon GPS','Crec. RB 3a (%)','HHI Fijo','ISI (0-100)','Semáforo','Recomendación Empresas','Recomendación ISP']];
    for (const m of list) {
      const fx = m.fx[period], rec = getEcoRecommendation(m);
      s1.push([
        String(m.id).padStart(4,'0'), m.dep, m.nom, m.rb[period]?.v ?? 'Sin dato', fx?.t ?? 'N/A',
        ...(fx ? fx.v.map(v=>v===null?'N/A':v) : SIT.meta.op_names.map(()=>'')),
        m.lp_sum.tot, m.eco.lp_rb ?? 'N/A', m.area ?? '', m.gps[1], m.gps[0],
        m.eco.g3y ?? 'N/A', m.eco.hhi ?? 'Sin red', m.eco.isi, rec.shortLabel, rec.forBiz, rec.forTelco
      ]);
    }
    const s2 = [
      ['Componente Metodológico', 'Fórmula / Definición', 'Justificación y Uso Económico'],
      ['Índice de Saturación de Infraestructura (ISI)', 'ISI = 0.35·P(RB/LP) + 0.30·P(Fijas/LP) + 0.20·P(RB) + 0.15·P(10000 - HHI)', 'Normalización percentil (metodología OCDE) sobre 340 municipios sin sesgo por valores extremos. Escala intuitiva 0 a 100.'],
      ['Índice Herfindahl-Hirschman (HHI)', 'HHI = Σ (cuota_operador_i %)² en líneas fijas 2026-S1', 'Estándar internacional DOJ/FTC para medir concentración y competencia real (>1,800 altamente concentrado; 10,000 monopolio).'],
      ['Crecimiento 3 años Radiobases', '((RB_2026-S1 - RB_2023-S1) / RB_2023-S1) × 100', 'Indica si los operadores están invirtiendo activamente en el municipio o si el mercado está estancado.'],
      ['Umbrales del Semáforo', '≥ 75 Alta Saturación | 45–74.9 Consolidación | < 45 Baja Saturación', 'Traduce los indicadores técnicos a decisiones claras para empresas (conectividad) e inversionistas ISP/telecom (oportunidad).'],
      ['Fuentes Oficiales Verificadas', 'SIT Consolidado Histórico 2014–2026 (04NOV2026) + Lugares Poblados 2026.kmz + Municipios.kmz', '100% cifras verificadas con conciliación 0 diferencia local en Hoja 15.'],
    ];
    XLSXWriter.downloadXLSX(`SIT_Guatemala_${list.length}_Municipios_${period}.xlsx`, [
      { name: 'Municipios_Consolidado', rows: s1 },
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
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Resumen_y_Recomendacion</code> (KPIs, GPS, ISI, HHI, Semáforo y recomendación)<br>2. <code>Serie_Historica_SIT</code> (Radiobases 2016–2026 + 9 Operadores Fijos 2022–2026 + PDF)<br>3. <code>Lugares_Poblados_2026</code> (Todas las aldeas, caseríos y sitios GPS del municipio)`;
    } else if (state.expMode === 'depto') {
      const defDid = state.selectedDeptoId || state.deptoFilter || 100;
      expConfigArea.innerHTML = `
        <div class="exp-field"><label>Selecciona el departamento:</label><select id="exp-depto-sel">${sortedDeptosAlpha.map(d => `<option value="${d.id}" ${d.id===defDid?'selected':''}>${esc(d.nom)} (${munisByDepto.get(d.id).length} municipios)</option>`).join('')}</select></div>
        <div class="exp-field"><label>Período de corte:</label><select id="exp-depto-per">${[...SIT.meta.periods_fx].reverse().map(p => `<option value="${p}">${p}</option>`).join('')}</select></div>
      `;
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Resumen_Departamento</code> (Totales oficiales + distribución Semáforo ISI)<br>2. <code>Municipios_Detalle</code> (Todos los municipios del depto con operadores, ISI y recomendación)<br>3. <code>Historico_Depto</code> (Serie histórica 2016–2026 del departamento)`;
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
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Comparativo_Directo</code> (Tabla lado a lado: ISI, HHI, operadores, lugares poblados y recomendación)<br>2. <code>Historico_Radiobases</code> (2016-S2 – 2026-S1 comparados)<br>3. <code>Historico_Lineas_Fijas</code> (2022-S2 – 2026-S1 comparados)`;
    } else {
      expConfigArea.innerHTML = `<div class="exp-field"><label>Período de corte nacional:</label><select id="exp-nat-per">${[...SIT.meta.periods_fx].reverse().map(p => `<option value="${p}">${p} (340 municipios completos)</option>`).join('')}</select></div>`;
      expPreview.innerHTML = `<strong>Hojas incluidas en el archivo .xlsx:</strong><br>1. <code>Municipios_Consolidado</code> (340 municipios con operadores, GPS, Lugares Poblados, ISI, HHI y recomendación)<br>2. <code>Metodologia_ISI_HHI</code> (Documentación completa de fórmulas y umbrales)`;
    }
  }

  document.getElementById('btn-open-excel-modal').onclick = () => openExcelModal();
  document.getElementById('btn-close-excel-modal').onclick = () => excelModal.classList.remove('open');
  document.getElementById('btn-cancel-excel').onclick = () => excelModal.classList.remove('open');
  excelModal.addEventListener('click', (e) => { if (e.target === excelModal) excelModal.classList.remove('open'); });
  document.querySelectorAll('.exp-mode-btn').forEach(btn => {
    btn.onclick = () => { state.expMode = btn.dataset.mode; renderExcelModalBody(); };
  });
  document.getElementById('btn-do-excel-download').onclick = () => {
    if (state.expMode === 'muni') {
      const id = parseInt(document.getElementById('exp-muni-sel').value, 10);
      exportMuniXLSX(muniById.get(id));
    } else if (state.expMode === 'depto') {
      const did = parseInt(document.getElementById('exp-depto-sel').value, 10);
      const per = document.getElementById('exp-depto-per').value;
      exportDeptoXLSX(did, per);
    } else if (state.expMode === 'compare') {
      if (state.expCompareIds.length < 2) { alert('Selecciona al menos 2 municipios para comparar.'); return; }
      exportCompareXLSX(state.expCompareIds);
    } else {
      exportNationalXLSX(document.getElementById('exp-nat-per').value);
    }
    excelModal.classList.remove('open');
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
        case 'nom': return m.nom; case 'dep': return m.dep; case 'isi': case 'tier': return m.eco.isi;
        case 'rb': return m.rb[p]?.v ?? -1; case 'fx': return m.fx[p]?.t ?? -1;
        case 'lp': return m.lp_sum.tot; case 'g3y': return m.eco.g3y ?? -999; case 'hhi': return m.eco.hhi ?? -1;
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
        <td style="font-weight:800;">${fmtDec(m.eco.isi,1)}</td>
        <td><span class="pill ${rec.badgeCls}" style="font-size:10px;padding:2px 7px;">${rec.shortLabel}</span></td>
        <td style="font-weight:700;color:var(--accent-dark);">${fmtInt(m.rb[p]?.v)}</td>
        <td style="font-weight:700;color:var(--teal);">${fmtInt(m.fx[p]?.t)}</td>
        <td>${fmtInt(m.lp_sum.tot)}</td>
        <td>${m.eco.g3y !== null ? (m.eco.g3y>=0?'+':'')+m.eco.g3y+'%' : '—'}</td>
        <td>${m.eco.hhi !== null ? fmtInt(Math.round(m.eco.hhi)) : 'Sin red'}</td>
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
      { lbl: `Lugares Poblados (KMZ)`, val: fmtInt(SIT.meta.total_lp), sub: `Sitios GPS en 340 municipios` },
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
  }

  function switchView(name) {
    state.view = name;
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.toggle('active', b.dataset.view === name));
    document.querySelectorAll('.view-container').forEach(v => v.classList.toggle('active', v.id === 'view-' + name));
    if (name === 'table') renderTable();
  }
  document.querySelectorAll('.nav-tab').forEach(btn => btn.onclick = () => switchView(btn.dataset.view));

  // Optional URL hash helper for direct municipality deep-linking (e.g. #muni=1601 or #metric=isi)
  initMap();
  const hash = location.hash || '';
  if (hash.includes('metric=isi')) { state.metric = 'isi'; metricSel.value = 'isi'; }
  syncSliderToMetric();
  updateMapColors();
  renderInspector();
  initTableView();
  initNationalView();
  const mMatch = hash.match(/muni=(\d+)/);
  if (mMatch) selectAndFocusMuni(parseInt(mMatch[1], 10));
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
