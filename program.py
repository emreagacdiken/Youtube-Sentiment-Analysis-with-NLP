import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np
from tokenlestirme import tokenize_and_train_word2vec, get_average_word2vec

# Eğitim verisini (csv dosyasını) oku
egitim_seti_path = 'egitim_seti.csv'
egitim_seti = pd.read_csv(egitim_seti_path, encoding='utf-16')

# 'Görüş' ve 'Durum' sütunlarını kullan
X = egitim_seti['Görüş']
y = egitim_seti['Durum']

# NaN değerlerini kaldır
X = X.dropna()
y = y[X.index]

# Etiketleri sayısallaştırdım
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Veriyi eğitim ve test setlerine ayırdım
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Word2Vec modelini eğittim
word2vec_model = tokenize_and_train_word2vec(X_train)

# Eğitim ve test verileri için vektörler oluştur
X_train_vectors = np.array([get_average_word2vec(sentence, word2vec_model) for sentence in X_train])
X_test_vectors = np.array([get_average_word2vec(sentence, word2vec_model) for sentence in X_test])

# Yapay Sinir Ağı modeli tanımlanıp eğitildi
mlp_model = MLPClassifier(
    hidden_layer_sizes=(100,),  # 100 nöronlu tek katman
    max_iter=1000, # 1000 iterasyon
    random_state=42, 
    verbose=True, 
    early_stopping=True, 
    n_iter_no_change=10, # 10 iterasyon boyunca değişmeyen durumda dur
    tol=1e-4 # 0.0001 hata toleransı
)

# Modeli eğit ve test seti üzerinde test et
mlp_model.fit(X_train_vectors, y_train)

# Modeli test et ve classification report sonucunu al
y_pred = mlp_model.predict(X_test_vectors)
classification_report_result = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

# Tkinter GUI ile sonuçları arayüzde göster
def display_results_for_file(file_path, title):
    # Dosyadan yorumları oku
    comments = []
    with open(file_path, mode='r', encoding='utf-16') as f:
        reader = csv.DictReader(f)
        for row in reader:
            comments.append(row['text'])

    # Yorumları vektörleştir
    comments_vectors = np.array([get_average_word2vec(comment, word2vec_model) for comment in comments])

    # Yorumların duygusunu tahmin et
    comments_pred = mlp_model.predict(comments_vectors)

    # Tkinter penceresini oluştur
    root = tk.Tk()
    root.title(f"Yorumlar - {title}")

    # Classification report için scrolledtext ekledim
    classification_report_box = scrolledtext.ScrolledText(root, width=100, height=10)
    classification_report_box.pack(padx=10, pady=10, fill=tk.X)
    classification_report_box.insert(tk.END, "Classification Report:\n")
    classification_report_box.insert(tk.END, classification_report_result + "\n")

    # Yorumlar ve tahminler için Treeview tablo oluşturdum
    tree = ttk.Treeview(root, columns=("Yorum", "Duygu"), show="headings", height=20)
    tree.heading("Yorum", text="Yorum")
    tree.heading("Duygu", text="Duygu")
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Yorumların okunabilmesi için kolon genişliklerini ayarladım
    tree.column("Yorum", width=920, anchor="w")
    tree.column("Duygu", width=80, anchor="w")

    # Yorumları ve tahminleri tabloya ekle
    for i in range(min(20, len(comments))):
        tree.insert("", tk.END, values=(f"{i+1}- {comments[i]}", label_encoder.inverse_transform([comments_pred[i]])[0]))

    # GUI başlat
    root.mainloop()

# Dosya seçme ve sonuçları görüntüleyen fonksiyon
def choose_file_and_display(file_idx):
    files = ['youtube_yorumlari_ve_meta_verileri_0.csv', 'youtube_yorumlari_ve_meta_verileri_1.csv', 'youtube_yorumlari_ve_meta_verileri_2.csv']
    file_titles = ['Matematik', 'Yapay Sinir Ağları', 'Yatırım']

    file_path = files[file_idx]
    title = file_titles[file_idx]
    display_results_for_file(file_path, title)

# Ana Tkinter penceresini oluştur
root = tk.Tk()
root.title("Eğitim Konusu Seçin")

# Dosya seçme butonlarını ekle
button_labels = ['Matematik', 'Yapay Sinir Ağları', 'Yatırım']
for idx, label in enumerate(button_labels):
    button = tk.Button(root, text=label, command=lambda idx=idx: choose_file_and_display(idx))
    button.pack(padx=10, pady=10)

# GUI ana döngüsünü başlat
root.mainloop()
