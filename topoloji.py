import matplotlib.pyplot as plt
import networkx as nx

# Ağ topolojisini oluştur
input_size = 20 # Giriş boyutu (yorum vektörü)
hidden_layer_size = 100  # Gizli katman nöron sayısı
output_size = 3  # Çıkış sınıf sayısı (pozitif, negatif, nötr)

# Şematik görselleştirme için NetworkX grafiği
G = nx.DiGraph()

# Giriş katmanı düğümleri
for i in range(input_size):
    G.add_node(f"Input_{i}", layer=0)

# Gizli katman düğümleri
for j in range(hidden_layer_size):
    G.add_node(f"Hidden_{j}", layer=1)

# Çıkış katmanı düğümleri
for k in range(output_size):
    G.add_node(f"Output_{k}", layer=2)

# Giriş ve gizli katman arasındaki bağlantılar
for i in range(input_size):
    for j in range(hidden_layer_size):
        G.add_edge(f"Input_{i}", f"Hidden_{j}")

# Gizli ve çıkış katmanları arasındaki bağlantılar
for j in range(hidden_layer_size):
    for k in range(output_size):
        G.add_edge(f"Hidden_{j}", f"Output_{k}")

# Katmanları düzenlemedim (doğru düzenlemeyi sağlamak için)
layer_0_nodes = [node for node, data in G.nodes(data=True) if data['layer'] == 0]
layer_1_nodes = [node for node, data in G.nodes(data=True) if data['layer'] == 1]
layer_2_nodes = [node for node, data in G.nodes(data=True) if data['layer'] == 2]

# Katmanlar için düzeni manuel olarak ayarladım
pos = {}
# Giriş katmanı konumları
for i, node in enumerate(layer_0_nodes):
    pos[node] = (0, i)

# Gizli katman konumları
for i, node in enumerate(layer_1_nodes):
    pos[node] = (1, i)

# Çıkış katmanı konumları
for i, node in enumerate(layer_2_nodes):
    pos[node] = (2, i)

# Ağ şeması çizimi
plt.figure(figsize=(12, 8))
nx.draw_networkx(
    G,
    pos,
    with_labels=False,
    node_size=50,
    node_color="skyblue",
    edge_color="gray",
    alpha=0.7
)
plt.title("Yapay Sinir Ağı Şeması", fontsize=16)
plt.axis("off")
plt.savefig("yapay_sinir_agi_semasi.png", dpi=300)  # Görseli kaydet
plt.show()