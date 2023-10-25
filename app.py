from flask import Flask, render_template, request
import pandas as pd
import re
import pymorphy2

app = Flask(__name__)

morph = pymorphy2.MorphAnalyzer()

text_id = pd.read_csv('~/mysite/instance/text_id.csv')

word_id = pd.read_csv('~/mysite/instance/word_id.csv')

lemma_id = pd.read_csv('~/mysite/instance/lemma_id.csv')

word_to_lemma = pd.read_csv('~/mysite/instance/word_to_lemma.csv')

word_data = pd.read_csv('~/mysite/instance/word_data.csv')


def search(search_text):
  if search_text == '':
    return [['Неверный запрос']]
  #отдельно храним паттерн и тип паттерна
  queries = []
  types = []
  tokens = search_text.split()

  #регулярки для определения типа паттерна
  for token in tokens:
    queries.append(token)
    if re.match(r'"[а-яёА-ЯЁ]+"$', token.lower()):
      types.append('exact')
    elif re.match(r'[а-яёА-ЯЁ]+$', token):
      types.append('lemma')
    elif re.match(r'[a-zA-Z]+$', token):
      types.append('pos')
    elif re.match(r'"[а-яёА-ЯЁ]+"\+[a-zA-Z]+$', token):
      types.append('exact+pos')
    else:
      return [['Неверный запрос']]

  results_df = pd.DataFrame()

  for pattern, query_type in zip(queries, types):

    if query_type == 'exact':
      word = pattern.strip('"')
      #смотрим есть ли слово в БД
      try:
        token_id = word_id[word_id.word == word].id.values[0]
      except:
        return [['Ничего не нашлось :(']]

       #для доставания нграммы объединяем таблицу с предыдущими записями и новыми (по номеру текста и по позиции слова в тексте)
      if not results_df.empty:
        new_df = word_data[word_data.word_id == token_id]
        results_df.text_pos += 1
        results_df = pd.merge(results_df, new_df, left_on=['text_id','text_pos'], \
                              right_on = ['text_id','text_pos'])
      else:
        results_df = word_data[word_data.word_id == token_id].merge(text_id, \
                                          left_on = 'text_id', right_on = 'id')

    elif query_type == 'lemma':
      word = morph.parse(pattern)[0].normal_form

      try:
        id = lemma_id[lemma_id.lemma == word].id.values[0]
      except:
        return [['Ничего не нашлось :(']]

      token_id = word_to_lemma[word_to_lemma.lemma_id == id].word_id

      if not results_df.empty:
        new_df = word_data[word_data.word_id.isin(token_id)]
        results_df.text_pos += 1
        results_df = pd.merge(results_df, new_df, left_on=['text_id','text_pos'], right_on = ['text_id','text_pos'])
      else:
        results_df = word_data[word_data.word_id.isin(token_id)].merge(text_id, left_on = 'text_id', right_on = 'id')

    elif query_type == 'pos':
      if not results_df.empty:
        new_df = word_data[word_data.tag == pattern]
        results_df.text_pos += 1
        results_df = pd.merge(results_df, new_df, left_on=['text_id','text_pos'], right_on = ['text_id','text_pos'])
      else:
        results_df = word_data[word_data.tag == pattern].merge(text_id, left_on = 'text_id', right_on = 'id')

    elif query_type == 'exact+pos':
      word, pos = pattern.split('+')
      word = word.strip('"').lower()
      try:
        token_id = word_id[word_id.word == word].id.values[0]
      except:
        return [['Ничего не нашлось :(']]

      if not results_df.empty:
        new_df = word_data[(word_data.word_id == token_id) & (word_data.tag == pos)]
        results_df.text_pos += 1
        results_df = pd.merge(results_df, new_df, left_on=['text_id','text_pos'], right_on = ['text_id','text_pos'])
      else:
        results_df = word_data[(word_data.word_id == token_id) & (word_data.tag == pos)].merge(text_id, left_on = 'text_id', right_on = 'id')

    if results_df.empty:
        return [['Ничего не нашлось :(']]
  #results_df.drop_duplicates(subset = ['text_id'], inplace = True)
  results_df.text = results_df.text.apply(lambda x: x.replace('\n', ' <br> '))
  for index, row in results_df.iterrows():
    words = results_df.loc[index, 'text'].split()
    search_index = results_df.loc[index, 'text_pos']
    i = 0
    while i <= search_index and i<=len(words)-1:
        if words[i] == '<br>':
            search_index+=1
        i+=1
    tags_between = words[search_index - len(queries):search_index + 1].count('<br>')
    words.insert(search_index + 1, '</b>')
    words.insert(search_index - len(queries) + 1 - tags_between, '<b>')
    results_df.loc[index, 'text'] = " ".join(words)
  return results_df[['text', 'datetime', 'authors', 'year_of_creation']].values.tolist()


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/res', methods=['GET'])
def user_search():
    query = dict(request.args)['q']
    data = search(query)
    for i, example in enumerate(data):
        example.append(i+1)
    return render_template('index.html', data=data, res = 'Результат запроса:', q=query, qq='Ваш запрос: ')

if __name__ == '__main__':
    app.run(debug=True)