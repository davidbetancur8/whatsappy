import pandas as pd
import numpy as np
import re
import collections
from stop_words import get_stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("fivethirtyeight")


def parse_file(text_file):
    info = []
    with open(text_file, encoding="utf8") as f:
            for line in f.readlines():
                try:
                    if ":" in line.split("-")[1]:
                        date = line.split("-")[0]
                        name = line.split("-")[1].split(":")[0]
                        message = line.split("-")[1].split(":")[1]
                    else:
                        pass
                    info.append([date, name, message])
                except Exception as e:
                    print(line)
                    print(e)

    df = pd.DataFrame(info, columns=["date", "name", "message"])
    df.name = df.name.str.strip()
    df.date = df.date.str.strip()
    df['date'] =  pd.to_datetime(df['date'], errors="coerce")
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

def plot_hours(df):
    by_dates_df = df.groupby([df.date.dt.hour])["name"].count()
    sns.barplot(by_dates_df.index, by_dates_df.values)
    plt.show()
    return by_dates_df

def agrupar(x):
    todo = []
    for ex in x:
        todo.append(ex)
    todo_str = " ".join(todo)
    return todo_str


def general_cloud(df):
    all_text = df.groupby([True]*len(df)).message.apply(agrupar).values[0]
    all_text = all_text.replace("jajaja", "")
    all_text = all_text.replace("jaja", "")
    stopwords = get_stop_words('es')
    lista_propia = ["<multimedia", "omitido>", "https", "ja"]
    for palabra in lista_propia:
        stopwords.append(palabra)
    wordcount = collections.defaultdict(int)
    for word in all_text.lower().split():
        if word not in stopwords:
            wordcount[word] += 1
    
    wc = WordCloud(background_color="black",width=1000, height=1500).generate_from_frequencies(wordcount)
    fig = plt.figure(figsize=(15,15))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    return wordcount
