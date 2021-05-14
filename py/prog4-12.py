# -*- coding: utf-8 -*-
"""prog4-12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kp5U3-RBMqbBQRzJCaAi5krPpIGpHjvh
"""

from google.colab import files
files.upload() # kaggle.jsonをアップロード
!mkdir -p ~/.kaggle
!mv kaggle.json ~/.kaggle/
!chmod 600 /root/.kaggle/kaggle.json

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
# t-SNEのクラスをインポート
from sklearn.manifold import TSNE
# 可視化用にインポート
import matplotlib.pyplot as plt
# %matplotlib inline
# UMAPクラスを使用するためのライブラリをインポート
!pip install umap-learn
import umap

# データの準備
def prepare():
    # 英単語の感情ごとの確率値を登録した
    # データセットを読み込む
    !kaggle datasets download -d \
    iwilldoit/emotions-sensor-data-set
    !unzip emotions-sensor-data-set.zip
    features = ['disgust', 'surprise', 
                'neutral', 'anger',
                'sad', 'happy', 'fear']
    df = pd.read_csv('Andbrain_DataSet.csv')
    words = df.loc[:, ['word']].values
    emotions = df.loc[:, features].values
    lbs = []
    for i in range(len(emotions)):
        val = np.max(emotions[i])
        id = list(emotions[i]).index(val)
        lbs.append(id)
    return words, emotions, features, lbs


# t-SNE, UMAPによる次元削減と可視化
def graph_Embedding(emb, emotions, words, features, lbs):
    print('\n----{}-----'.format(emb.__class__.__name__))
    df = pd.DataFrame(emotions, columns=features)
    emb.fit(df)
    fspace = emb.fit_transform(df)
    ndf = pd.DataFrame(fspace, columns=['1', '2'])
    print(ndf.head())
    plt.figure(figsize=(6,6)) 
    n = 0
    col = ['red', 'green', 'blue', 
           'pink', 'black', 'orange', 'purple']
    mks = ['o', '^', '+', '*', 'x', '<', '.']
    chk = [0] * len(features)
    for (dim1,dim2,word,l) in zip(
              fspace[:,0], fspace[:,1], words,lbs):
        if chk[l] == 0:
            plt.plot(dim1,dim2,'x',alpha=0.5, c=col[l],
                     marker=mks[l], label=features[l])
        else:
            plt.plot(dim1,dim2,'x',alpha=0.5, c=col[l],
                     marker=mks[l])
        chk[l] += 1
        n += 1
        if n % 50 == 0:
            plt.annotate(word[0], xy=(dim1, dim2))
    plt.grid()
    plt.xlabel('DIM-1')
    plt.ylabel('DIM-2')
    plt.legend()
    plt.title('Mapping of emotion words by {}'.format(
               emb.__class__.__name__))
    plt.savefig('{}.png'.format(emb.__class__.__name__),\
                dpi=400)
    plt.show()

def main():
    words, emotions, features, lbs = prepare()
    for emb in [TSNE(n_components=2, random_state=0),
                umap.UMAP(n_components=2, random_state=0)]:
        graph_Embedding(emb, emotions, words, features, lbs)

if __name__ == '__main__':
    main()