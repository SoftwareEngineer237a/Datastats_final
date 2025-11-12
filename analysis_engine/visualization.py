# analysis_engine/visualization.py
from app import  db
import os
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

# Plotly (for interactive, special charts)
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot as plotly_save

# NetworkX (for network graphs)
import networkx as nx

# Dendrogram
from scipy.cluster.hierarchy import dendrogram, linkage
from app.models import Graph

# ---------- helpers ----------

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def _img_name(prefix):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{ts}.png"

def _html_name(prefix):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{ts}.html"

def _save_fig(output_dir_img, filename):
    _ensure_dir(output_dir_img)
    outpath = os.path.join(output_dir_img, filename)
    plt.tight_layout()
    plt.savefig(outpath, bbox_inches="tight", dpi=140)
    plt.close()
    return filename

def _save_plotly(fig, output_dir_html, filename):
    _ensure_dir(output_dir_html)
    outpath = os.path.join(output_dir_html, filename)
    plotly_save(fig, filename=outpath, auto_open=False, include_plotlyjs="cdn")
    return filename


# ---------- main dispatcher ----------

def render_chart(df: pd.DataFrame, config: dict, output_img_dir: str, output_html_dir: str, prefix: str, dataset_id=None, user_id=None):
    """
    config keys (common):
      - source: 'dataset' | 'analysis_csv'
      - analysis_csv_path: optional, if source == 'analysis_csv'
      - chart_type: 'bar'|'line'|'pie'|'scatter'|'hist'|'box_violin'|'heatmap'|'radar'|
                    'treemap'|'funnel'|'network'|'waterfall'|'gantt'|'sankey'|'map'|
                    'dendrogram'|'combo'|'3dscatter'
      - subtype: varies per chart_type (see below)
      - interactive: 'on' (use Plotly where available)

      - x, y, y_multi (list), hue/group, size, color, bins, agg, normalize, explode, donut, stacked, orientation
      - misc fields needed by special charts (start/end for gantt, source/target/value for sankey, geo field for map, etc.)
    """
    # If plotting from an analysis CSV result, load it and override df
    if config.get("source") == "analysis_csv":
        csv_path = config.get("analysis_csv_path", "").strip()
        if not csv_path or not os.path.exists(csv_path):
            raise ValueError("Provided analysis CSV path is invalid or does not exist.")
        df = pd.read_csv(csv_path)

    chart_type = config.get("chart_type")
    subtype = config.get("subtype", "")
    interactive = config.get("interactive") == "on"
    result = None

    # dispatch
    if chart_type == "bar":
        result = _bar_chart(df, config, interactive, output_img_dir, output_html_dir, prefix)
    elif chart_type == "line":
        result = _line_chart(df, config, interactive, output_img_dir, output_html_dir, prefix)
    elif chart_type == "pie":
        result = _pie_chart(df, config, output_img_dir, prefix)
    elif chart_type == "scatter":
        result = _scatter_chart(df, config, interactive, output_img_dir, output_html_dir, prefix)
    elif chart_type == "hist":
        result = _hist_chart(df, config, output_img_dir, prefix)
    elif chart_type == "box_violin":
        result = _box_violin(df, config, output_img_dir, prefix)
    elif chart_type == "heatmap":
        result = _heatmap(df, config, output_img_dir, prefix)
    elif chart_type == "radar":
        result = _radar_chart(df, config, output_img_dir, prefix)
    elif chart_type == "treemap":
        result = _treemap(df, config, output_html_dir, prefix)
    elif chart_type == "funnel":
        result = _funnel(df, config, output_html_dir, prefix)
    elif chart_type == "network":
        result = _network(df, config, output_img_dir, prefix)
    elif chart_type == "waterfall":
        result = _waterfall(df, config, output_img_dir, prefix)
    elif chart_type == "gantt":
        result = _gantt(df, config, output_html_dir, prefix)
    elif chart_type == "sankey":
        result = _sankey(df, config, output_html_dir, prefix)
    elif chart_type == "map":
        result = _map_chart(df, config, output_html_dir, prefix)
    elif chart_type == "dendrogram":
        result = _dendrogram(df, config, output_img_dir, prefix)
    elif chart_type == "combo":
        result = _combo_chart(df, config, output_img_dir, prefix)
    elif chart_type == "3dscatter":
        result = _scatter3d(df, config, output_html_dir, prefix)
    else:
        raise ValueError("Unknown chart type.")
    
    if result and (dataset_id or user_id):
        name = f"{chart_type}-{prefix}"
        analysis_type = config.get("analysis_type", "raw")
        file_path = f"img/{result['file']}" if result['kind'] == 'image' else f"html/{result['file']}"
        log_graph_to_db(
            name=name,
            graph_type=chart_type,
            dataset_id=dataset_id,
            analysis_type=analysis_type,
            file_path=file_path,
            user_id=user_id
        )
    return result

# ---------- implementations ---------- 

def _aggregate_if_needed(df, x, y, agg):
    if not x or not y:
        raise ValueError("x and y must be provided.")
    if agg:
        grouped = df.groupby(x)[y]
        if agg == "sum":
            return grouped.sum().reset_index()
        elif agg == "mean":
            return grouped.mean().reset_index()
        elif agg == "count":
            return grouped.count().reset_index()
        elif agg == "max":
            return grouped.max().reset_index()
        elif agg == "min":
            return grouped.min().reset_index()
        else:
            raise ValueError("Unknown aggregation.")
    return df[[x, y]].dropna()

def _bar_chart(df, cfg, interactive, out_img, out_html, prefix):
    # subtype: vertical | horizontal | stacked | grouped
    x = cfg.get("x")
    y = cfg.get("y")
    hue = cfg.get("group")
    agg = cfg.get("agg")  # None|sum|mean|count|max|min
    subtype = cfg.get("subtype", "vertical")

    if interactive:
        # Plotly
        if subtype in ["vertical", "grouped"]:
            fig = px.bar(df, x=x, y=y, color=hue, barmode="group" if subtype == "grouped" else "relative" if cfg.get("stacked")=="on" else "relative")
        elif subtype == "horizontal":
            fig = px.bar(df, x=y, y=x, color=hue, orientation="h")
        elif subtype == "stacked":
            fig = px.bar(df, x=x, y=y, color=hue, barmode="stack")
        else:
            fig = px.bar(df, x=x, y=y, color=hue)
        name = _html_name(prefix + "_bar")
        return {"kind": "html", "file": _save_plotly(fig, out_html, name), "meta": {}}

    # Matplotlib
    data = _aggregate_if_needed(df, x, y, agg)
    plt.figure(figsize=(10,6))
    if subtype == "horizontal":
        plt.barh(data[x], data[y])
        plt.xlabel(y); plt.ylabel(x)
    elif subtype == "stacked" and hue:
        # simple stacked: pivot by hue
        pivot = df.pivot_table(index=x, columns=hue, values=y, aggfunc=agg or "sum").fillna(0)
        bottom = np.zeros(len(pivot))
        for col in pivot.columns:
            plt.bar(pivot.index, pivot[col], bottom=bottom, label=str(col))
            bottom += pivot[col].values
        plt.legend()
    elif subtype == "grouped" and hue:
        pivot = df.pivot_table(index=x, columns=hue, values=y, aggfunc=agg or "sum").fillna(0)
        idx = np.arange(len(pivot.index))
        w = 0.8 / len(pivot.columns)
        for i, col in enumerate(pivot.columns):
            plt.bar(idx + i*w, pivot[col].values, width=w, label=str(col))
        plt.xticks(idx + w*(len(pivot.columns)-1)/2, pivot.index, rotation=45)
        plt.legend()
    else:
        plt.bar(data[x], data[y])
        plt.xticks(rotation=45)
        plt.ylabel(y); plt.xlabel(x)

    plt.title("Bar Chart")
    name = _img_name(prefix + "_bar")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _line_chart(df, cfg, interactive, out_img, out_html, prefix):
    # subtype: simple | multiple | area
    x = cfg.get("x")
    y = cfg.get("y")
    y_multi = cfg.get("y_multi", []) or []
    agg = cfg.get("agg")
    subtype = cfg.get("subtype", "simple")

    if interactive:
        if subtype == "multiple" and y_multi:
            fig = go.Figure()
            for col in y_multi:
                fig.add_trace(go.Scatter(x=df[x], y=df[col], mode='lines', name=col))
        elif subtype == "area" and y_multi:
            fig = go.Figure()
            for col in y_multi:
                fig.add_trace(go.Scatter(x=df[x], y=df[col], mode='lines', stackgroup='one', name=col))
        else:
            fig = px.line(df, x=x, y=y)
        name = _html_name(prefix + "_line")
        return {"kind": "html", "file": _save_plotly(fig, out_html, name), "meta": {}}

    plt.figure(figsize=(10,6))
    if subtype == "multiple" and y_multi:
        for col in y_multi:
            plt.plot(df[x], df[col], label=str(col))
        plt.legend()
    elif subtype == "area" and y_multi:
        plt.stackplot(df[x], [df[col] for col in y_multi], labels=y_multi)
        plt.legend(loc='upper left')
    else:
        data = _aggregate_if_needed(df, x, y, agg)
        plt.plot(data[x], data[y])
    plt.title("Line Chart"); plt.xlabel(x); plt.ylabel(y or "value")
    name = _img_name(prefix + "_line")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _pie_chart(df, cfg, out_img, prefix):
    # subtype: pie | donut | exploded
    labels_col = cfg.get("x")
    values_col = cfg.get("y")
    subtype = cfg.get("subtype", "pie")
    agg = cfg.get("agg", "sum")

    if not labels_col or not values_col:
        raise ValueError("Pie/Donut requires label (x) and value (y) columns.")

    data = df.groupby(labels_col)[values_col].agg(agg).reset_index()
    labels = data[labels_col].astype(str).values
    values = data[values_col].values

    plt.figure(figsize=(8,8))
    explode = None
    if subtype == "exploded":
        explode = [0.1] + [0]*(len(values)-1)

    wedges, texts, autotexts = plt.pie(values, labels=labels, autopct="%1.1f%%",
                                       startangle=140, pctdistance=0.85 if subtype=="donut" else 0.6,
                                       explode=explode)
    if subtype == "donut":
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf(); fig.gca().add_artist(centre_circle)
    plt.title(subtype.title())
    name = _img_name(prefix + "_pie")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _scatter_chart(df, cfg, interactive, out_img, out_html, prefix):
    # subtype: scatter | bubble
    x = cfg.get("x")
    y = cfg.get("y")
    size = cfg.get("size")
    color = cfg.get("color")
    subtype = cfg.get("subtype", "scatter")

    if interactive:
        scatter_kwargs = dict(x=x, y=y)
        if color and color in df.columns:
            scatter_kwargs['color'] = color
        if subtype == "bubble" and size and size in df.columns:
            scatter_kwargs['size'] = size
        if color and color not in df.columns:
            color = None  # Prevent error
        fig = px.scatter(df, **scatter_kwargs)
        name = _html_name(prefix + "_scatter")
        return {"kind": "html", "file": _save_plotly(fig, out_html, name), "meta": {}}

    plt.figure(figsize=(9,6))
    if subtype == "bubble" and size and size in df.columns:
        s = df[size].fillna(0).values
        s_scaled = 200 * (s - s.min()) / (s.max() - s.min() + 1e-9) + 20
        plt.scatter(df[x], df[y], s=s_scaled, c='C0', alpha=0.7)
    else:
        plt.scatter(df[x], df[y], alpha=0.7)
    plt.xlabel(x); plt.ylabel(y); plt.title("Scatter")
    name = _img_name(prefix + "_scatter")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _hist_chart(df, cfg, out_img, prefix):
    # subtype: hist | cumulative
    col = cfg.get("y") or cfg.get("x")
    subtype = cfg.get("subtype","hist")
    bins = int(cfg.get("bins", 10))

    if not col:
        raise ValueError("Histogram requires a numeric column.")

    plt.figure(figsize=(9,6))
    plt.hist(df[col].dropna().values, bins=bins, cumulative=(subtype=="cumulative"), alpha=0.85)
    plt.xlabel(col); plt.ylabel("Frequency"); plt.title("Histogram" + (" (Cumulative)" if subtype=="cumulative" else ""))
    name = _img_name(prefix + "_hist")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _box_violin(df, cfg, out_img, prefix):
    # subtype: box | violin
    col = cfg.get("y")
    group = cfg.get("group")  # categorical splitter
    subtype = cfg.get("subtype","box")

    plt.figure(figsize=(10,6))
    if subtype == "violin":
        if group:
            sns.violinplot(x=group, y=col, data=df, cut=0)
        else:
            sns.violinplot(y=df[col])
    else:
        if group:
            sns.boxplot(x=group, y=col, data=df)
        else:
            sns.boxplot(y=df[col])
    plt.title(subtype.title())
    name = _img_name(prefix + "_boxviolin")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _heatmap(df, cfg, out_img, prefix):
    # subtype: standard | clustered
    subtype = cfg.get("subtype","standard")
    # if user provided a list of numerical columns, use them; else use all numeric
    cols = cfg.get("y_multi") or df.select_dtypes(include='number').columns.tolist()
    data = df[cols].dropna()
    if data.shape[1] < 2:
        raise ValueError("Heatmap requires at least two numeric columns.")

    if subtype == "clustered":
        # seaborn clustermap returns its own fig; save via fig.savefig
        cg = sns.clustermap(data.corr(), cmap="coolwarm", vmin=-1, vmax=1, annot=len(cols)<=15)
        name = _img_name(prefix + "_clustermap")
        outpath = os.path.join(out_img, name)
        _ensure_dir(out_img)
        cg.fig.savefig(outpath, bbox_inches="tight", dpi=140)
        plt.close(cg.fig)
        return {"kind": "image", "file": name, "meta": {}}
    else:
        plt.figure(figsize=(9,7))
        sns.heatmap(data.corr(), cmap="coolwarm", vmin=-1, vmax=1, annot=len(cols)<=15)
        plt.title("Correlation Heatmap")
        name = _img_name(prefix + "_heatmap")
        return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}

def log_graph_to_db(name, graph_type, dataset_id, analysis_type, file_path, user_id):
    graph = Graph(
        name=name,
        graph_type=graph_type,
        dataset_id=dataset_id,
        analysis_type=analysis_type,
        file_path=file_path,
        created_by=user_id
    )
    db.session.add(graph)
    db.session.commit()
    return graph

def _radar_chart(df, cfg, out_img, prefix):
    # Build radar from a single row / aggregated row; expects y_multi numeric columns
    cats = cfg.get("y_multi") or []
    label = cfg.get("group") or "Series"
    if not cats or len(cats) < 3:
        raise ValueError("Radar requires at least 3 numeric columns selected.")

    # Aggregate: mean across df
    values = df[cats].mean().values.tolist()
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(cats), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(8,8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    if cfg.get("filled") == "on":
        ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=9)
    plt.title("Radar Chart")
    name = _img_name(prefix + "_radar")
    return {"kind": "image", "file": _save_fig(out_img, name), "meta": {}}


def _treemap(df, cfg, out_html, prefix):
    # Requires path or labels + values
    label = cfg.get("x"); value = cfg.get("y")
    parent = cfg.get("parent")  # optional for nested
    if not label or not value:
        raise ValueError("Treemap requires label (x) and value (y) columns.")
    if parent and parent in df.columns:
        fig = px.treemap(df, path=[parent, label], values=value)
    else:
        fig = px.treemap(df, path=[label], values=value)
    name = _html_name(prefix + "_treemap")
    return {"kind":"html","file":_save_plotly(fig, out_html, name), "meta":{}}


def _funnel(df, cfg, out_html, prefix):
    stage = cfg.get("x"); value = cfg.get("y")
    if not stage or not value:
        raise ValueError("Funnel requires stage (x) and value (y).")
    fig = px.funnel(df, x=value, y=stage) if cfg.get("orientation")=="horizontal" else px.funnel(df, y=stage, x=value)
    name = _html_name(prefix + "_funnel")
    return {"kind":"html","file":_save_plotly(fig, out_html, name), "meta":{}}


def _network(df, cfg, out_img, prefix):
    src = cfg.get("source_col")
    tgt = cfg.get("target_col")
    w = cfg.get("weight_col")
    G = nx.Graph()
    if src and tgt and src in df.columns and tgt in df.columns:
        for _, row in df[[src, tgt, w] if w and w in df.columns else [src, tgt]].dropna().iterrows():
            if w and w in df.columns:
                G.add_edge(row[src], row[tgt], weight=float(row[w]))
            else:
                G.add_edge(row[src], row[tgt])
    else:
        cols = cfg.get("y_multi") or df.select_dtypes(include='number').columns.tolist()
        corr = df[cols].corr().values
        labels = cols
        for i in range(len(labels)):
            for j in range(i+1, len(labels)):
                if abs(corr[i,j]) >= float(cfg.get("corr_threshold", 0.6)):
                    G.add_edge(labels[i], labels[j], weight=float(corr[i,j]))
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="#7aa2ff", edge_color="#999", font_size=9)
    plt.title("Network Graph")
    name = _img_name(prefix + "_network")
    return {"kind":"image","file":_save_fig(out_img, name),"meta":{}}


def _waterfall(df, cfg, out_img, prefix):
    # Needs ordered categories (x) and values (y)
    x = cfg.get("x"); y = cfg.get("y")
    if not x or not y:
        raise ValueError("Waterfall requires x and y.")
    data = df[[x,y]].dropna()
    vals = data[y].values
    idx = np.arange(len(vals))
    cum = np.cumsum(vals)
    plt.figure(figsize=(10,6))
    plt.bar(idx, vals, bottom=np.hstack(([0], cum[:-1])), color=["#2ecc71" if v>=0 else "#e74c3c" for v in vals])
    plt.xticks(idx, data[x], rotation=45); plt.title("Waterfall")
    name = _img_name(prefix + "_waterfall")
    return {"kind":"image","file":_save_fig(out_img, name),"meta":{}}


def _gantt(df, cfg, out_html, prefix):
    task = cfg.get("x"); start = cfg.get("start_col"); end = cfg.get("end_col"); group = cfg.get("group")
    if not all([task, start, end]):
        print("DEBUG GANTT:", task, start, end)
        raise ValueError("Gantt requires task (x), start, and end columns.")
    dfg = df[[task, start, end] + ([group] if group and group in df.columns else [])].dropna().copy()
    dfg[start] = pd.to_datetime(dfg[start]); dfg[end] = pd.to_datetime(dfg[end])
    fig = px.timeline(dfg, x_start=start, x_end=end, y=task, color=group if group in dfg.columns else None)
    fig.update_yaxes(autorange="reversed")
    name = _html_name(prefix + "_gantt")
    return {"kind":"html","file":_save_plotly(fig, out_html, name),"meta":{}}


def _sankey(df, cfg, out_html, prefix):
    src = cfg.get("source_col")
    tgt = cfg.get("target_col")
    val = cfg.get("value_col")
    if not all([src, tgt, val]):
        raise ValueError("Sankey requires source, target, and value columns.")
    d = df[[src, tgt, val]].dropna().copy()
    labels = pd.unique(d[[src, tgt]].values.ravel()).tolist()
    label_to_id = {lab:i for i,lab in enumerate(labels)}
    s = d[src].map(label_to_id).tolist()
    t = d[tgt].map(label_to_id).tolist()
    v = d[val].astype(float).tolist()
    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels, pad=20, thickness=16),
        link=dict(source=s, target=t, value=v)
    )])
    name = _html_name(prefix + "_sankey")
    return {"kind":"html","file":_save_plotly(fig, out_html, name),"meta":{}}


def _map_chart(df, cfg, out_html, prefix):
    # choropleth by iso country code or country name; or dot map with lat/lon
    mode = cfg.get("subtype", "choropleth")
    if mode == "choropleth":
        loc = cfg.get("geo_col")
        val = cfg.get("y")
        color = cfg.get("color")
        if not loc or not val:
            raise ValueError("Choropleth requires a location column (geo) and a value column (y).")
        fig = px.choropleth(
            df,
            locations=loc,
            color=val,
            locationmode="country names" if cfg.get("geo_mode") == "names" else "ISO-3"
        )
    else:  # dots
        lat = cfg.get("lat_col")
        lon = cfg.get("lon_col")
        size = cfg.get("size")
        color = cfg.get("color")
        if not all([lat, lon]):
            raise ValueError("Dot map requires latitude and longitude columns.")
        scatter_kwargs = dict(lat=lat, lon=lon)
        if color and color in df.columns:
            scatter_kwargs['color'] = color
        if size and size in df.columns:
            scatter_kwargs['size'] = size
        if cfg.get("x") and cfg.get("x") in df.columns:
            scatter_kwargs['hover_name'] = cfg.get("x")
        fig = px.scatter_geo(df, **scatter_kwargs)
    name = _html_name(prefix + "_map")
    return {"kind": "html", "file": _save_plotly(fig, out_html, name), "meta": {}}


def _dendrogram(df, cfg, out_img, prefix):
    # From numeric columns; uses linkage on standardized data (optional)
    cols = cfg.get("y_multi") or df.select_dtypes(include='number').columns.tolist()
    data = df[cols].dropna()
    if data.shape[0] < 2 or data.shape[1] < 2:
        raise ValueError("Dendrogram requires at least two rows and two numeric columns.")
    # Standardize (optional)
    if cfg.get("standardize") == "on":
        data = (data - data.mean()) / (data.std(ddof=0) + 1e-9)
    Z = linkage(data.values, method=cfg.get("linkage","ward"))
    plt.figure(figsize=(10,6))
    dendrogram(Z, labels=None, leaf_rotation=90)
    plt.title("Hierarchical Clustering Dendrogram")
    name = _img_name(prefix + "_dendrogram")
    return {"kind":"image","file":_save_fig(out_img, name),"meta":{}}


def _combo_chart(df, cfg, out_img, prefix):
    # combo: bar (y1) + line (y2) on twin axis
    x = cfg.get("x"); y1 = cfg.get("y"); y2 = cfg.get("y2")
    if not all([x, y1, y2]):
        raise ValueError("Combo requires x, y (bar) and y2 (line).")
    fig, ax1 = plt.subplots(figsize=(10,6))
    ax1.bar(df[x], df[y1], alpha=0.6, label=y1)
    ax1.set_xlabel(x); ax1.set_ylabel(y1)
    ax2 = ax1.twinx()
    ax2.plot(df[x], df[y2], marker='o', label=y2, linewidth=2)
    ax2.set_ylabel(y2)
    plt.title("Combo Chart (Bar + Line)")
    name = _img_name(prefix + "_combo")
    return {"kind":"image","file":_save_fig(out_img, name),"meta":{}}


def _scatter3d(df, cfg, out_html, prefix):
    x = cfg.get("x"); y = cfg.get("y"); z = cfg.get("z")
    color = cfg.get("color")
    if not all([x, y, z]):
        raise ValueError("3D Scatter requires x, y, and z.")
    fig = px.scatter_3d(df, x=x, y=y, z=z, color=color)
    name = _html_name(prefix + "_3dscatter")
    return {"kind":"html","file":_save_plotly(fig, out_html, name),"meta":{}}