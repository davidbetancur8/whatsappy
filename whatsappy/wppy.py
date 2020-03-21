import pandas as pd
import numpy as np
import re
import collections
from stop_words import get_stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")


def parse_file(tipo, text_file):
    info = []
    with open(text_file, encoding="utf8") as f:
        for line in f.readlines():
            try:
                if tipo == 1:
                    date = re.search("\[\d+/\d+/\d+, \d+:\d+:\d+\]", line).group(0)
                    date = date[1:-1]
                    name = re.search("(?<=\d\d\] )([^:]*)(?=: )", line).group(0)
                    message = re.search("(?<=: )(.*)($)", line).group(0)
                if tipo == 2:
                    date = re.search("\d+/\d+/\d+ \d+:\d+", line).group(0)
                    name = re.search("(?<=\d\d - )([^:]*)(?=: )", line).group(0)
                    message = re.search("(?<=: )(.*)($)", line).group(0)
                
                info.append([date, name, message])
            except Exception as e:
                pass

    df = pd.DataFrame(info, columns=["date", "name", "message"])
    df.name = df.name.str.strip()
    df.date = df.date.str.strip()

    if tipo == 1:
        df['date'] =  pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S')
    if tipo == 2:
        df['date'] =  pd.to_datetime(df['date'], format='%d/%m/%y %H:%M')
    return df

def plot_word(df, palabra, max_count):
    df_word = df.copy()
    df_word[palabra] = np.where(df['message'].str.contains(palabra, case=False, na=False), 1, 0)
    df_words = df_word.groupby("name")[palabra].sum().sort_values(ascending=False)
    df_words.head(max_count).plot.bar(figsize=(5, 5))
    plt.ylabel(palabra)
    plt.show()

def plot_count(df):
    df_count = df['name'].value_counts()
    df_count.head(10).plot.bar(figsize=(5, 5))
    plt.show()


def agrupar(x):
    todo = []
    for ex in x:
        todo.append(ex)
    todo_str = " ".join(todo)
    return todo_str


def general_cloud(df):
    all_text = df.groupby([True]*len(df)).message.apply(agrupar).values[0]
    stopwords = get_stop_words('es')
    lista_propia = ["<multimedia", "omitido>"]
    for palabra in lista_propia:
        stopwords.append(palabra)
    wordcount = collections.defaultdict(int)
    for word in all_text.lower().split():
        if word not in stopwords:
            wordcount[word] += 1
    
    wc = WordCloud(background_color="white",width=1000, height=1500).generate_from_frequencies(wordcount)
    fig = plt.figure(figsize=(15,15))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
