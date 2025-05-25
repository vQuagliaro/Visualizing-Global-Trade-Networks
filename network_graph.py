import dash
from dash import html
import dash_cytoscape as cyto
import networkx as nx

# ==== CONFIGURABLE PARAMETERS ====
NODE_SIZE_MIN = 40  # Smallest node bubble
NODE_SIZE_MAX = 110 # Largest node bubble
EDGE_WIDTH_MIN = 2  # Thinnest edge
EDGE_WIDTH_MAX = 12 # Thickest edge

# Define edges (source, target, weight)
edges = [
    ('US', 'CN', 100), ('US', 'DE', 90), ('CN', 'JP', 85), ('US', 'GB', 70), ('DE', 'FR', 60),
    ('CN', 'KR', 80), ('CN', 'US', 75), ('JP', 'AU', 40), ('GB', 'FR', 50), ('US', 'MX', 65),
    ('CA', 'US', 60), ('US', 'CA', 50), ('CN', 'HK', 70), ('KR', 'CN', 60), ('DE', 'IT', 55),
    ('FR', 'ES', 45), ('DE', 'NL', 50), ('DE', 'BE', 40), ('CN', 'SG', 55), ('CN', 'MY', 45)
]

G = nx.DiGraph()
for s, t, w in edges:
    G.add_edge(s, t, weight=w)

# Node size by weighted degree
max_degree = max(G.degree(n, weight='weight') for n in G.nodes())
min_degree = min(G.degree(n, weight='weight') for n in G.nodes())

def scale(val, vmin, vmax, omin, omax):
    """Scale val in [vmin,vmax] to [omin,omax]"""
    if vmax == vmin:
        return (omin + omax) / 2
    return omin + (omax - omin) * (val - vmin) / (vmax - vmin)

node_sizes = {n: scale(G.degree(n, weight='weight'), min_degree, max_degree, NODE_SIZE_MIN, NODE_SIZE_MAX) for n in G.nodes()}

# Cytoscape elements: nodes
elements = [
    {
        'data': {'id': n, 'label': n, 'weight': node_sizes[n]},
        'position': {'x': 100*i, 'y': 100*i},  # Initial positions (can be improved)
        'grabbable': True
    }
    for i, n in enumerate(G.nodes())
]

# Find min/max edge weights for scaling
all_weights = [d['weight'] for _, _, d in G.edges(data=True)]
min_weight = min(all_weights)
max_weight = max(all_weights)

# Cytoscape elements: edges
for u, v, d in G.edges(data=True):
    # Edge width is mapped in stylesheet; just include raw weight here
    elements.append({
        'data': {
            'source': u, 'target': v,
            'weight': d['weight']
        }
    })

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='network-graph',
        elements=elements,
        layout={'name': 'cose'},  # Force-directed, but nodes stay draggable
        style={'width': '100vw', 'height': '90vh', 'background-color': 'white'},
        minZoom=0.3,
        maxZoom=2,
        boxSelectionEnabled=True,
        autoungrabify=False,
        userPanningEnabled=True,
        userZoomingEnabled=True,
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'font-size': 18,
                    'font-family': 'Arial Black',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'background-color': '#2450A7',
                    'color': 'white',
                    'width': 'data(weight)',
                    'height': 'data(weight)',
                    'border-width': 2,
                    'border-color': 'white',
                    'shadow-blur': 7,
                }
            },
            {
                'selector': 'edge',
                'style': {
                    # Dynamically scale edge width via mapData:
                    'width': f'mapData(weight, {min_weight}, {max_weight}, {EDGE_WIDTH_MIN}, {EDGE_WIDTH_MAX})',
                    'line-color': '#B7C0D8',
                    'curve-style': 'bezier',
                }
            }
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
