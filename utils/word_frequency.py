from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import re
import spacy
nlp = spacy.load("en_core_web_sm")
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr

def combine_and_clean_one_journal_entry(journal_entry: dict, custom_stop_words: list=None) -> str:
    """
    Combine all text entries within a single journal entry and clean them
    """

    text_data = [journal_entry[text_field] for text_field in vr.text_fields]
    combined_text_data = "\n".join(text_data)
        
    # remove capital letters
    doc = nlp(combined_text_data.lower())
    # remove stop words
    doc = [token for token in doc if not token.is_stop]
    # remove custom stop words
    if custom_stop_words:
        doc = [token for token in doc if token.text not in custom_stop_words]
    # remove punctuation - add space around punct to help identify it
    text = ' '.join(token.text for token in doc)
    doc = nlp(re.sub(r"([.,!?(')])", r' \1 ', text))
    doc = [token for token in doc if not token.is_punct and not token.is_space]
    # lemmitize
    cleaned_text_data = ' '.join(token.lemma_ for token in doc)
        
    return cleaned_text_data

def combine_and_clean_all_journal_entries(journal_data: dict, custom_stop_words: list=None) -> dict:
    """

    """
    cleaned_journal_data = {}
    for entry_id in journal_data.keys():
        journal_entry = journal_data[entry_id]
        cleaned_journal_entry = combine_and_clean_one_journal_entry(journal_entry, custom_stop_words)
        cleaned_journal_data[entry_id] = cleaned_journal_entry

    return cleaned_journal_data

def create_cv_matrix(cleaned_journal_data: dict) -> pd.DataFrame:    
    """
    Fit a CountVectorizer on the cleaned journal data (dictionary with event id as key)
    """

    vectorizer = CountVectorizer()
    # separate keys and journal entries
    event_ids = cleaned_journal_data.keys()
    cleaned_journal_entries = cleaned_journal_data.values()
    X = vectorizer.fit_transform(cleaned_journal_entries)
    # convert to dataframe and add term names
    X_df = pd.DataFrame(X.todense(), columns=vectorizer.get_feature_names_out())
    X_df = pd.concat([pd.Series(event_ids, name="event_id"), X_df], axis=1)

    return X_df

def identify_most_common_words(X_df:pd.DataFrame, min_required_frequency:int=5, n_words:int=10):
    X_df_copy = X_df.copy()
    X_df_copy = X_df_copy.drop(columns=["event_id"])

    word_sum = pd.DataFrame(X_df_copy.sum(axis=0), columns=[vr.word_count_col_name]).sort_values(by=vr.word_count_col_name, ascending=False).reset_index()
    word_sum.columns = [vr.word_col_name, vr.word_count_col_name]
    del X_df_copy

    word_sum = word_sum[word_sum.word_count >= min_required_frequency]
    if word_sum.empty:
        return None

    n_word_filter = min(len(word_sum), n_words)

    return word_sum.iloc[:n_word_filter]

def analyse_word_frequency(journal_data:dict, custom_stop_words:list=None) -> pd.DataFrame:
    # pre-process all journal entries
    cleaned_journal_data = combine_and_clean_all_journal_entries(journal_data, custom_stop_words)
    # count word frequency
    X_df = create_cv_matrix(cleaned_journal_data)
    # identify most common terms
    word_sum = identify_most_common_words(X_df, min_required_frequency=3)
    
    return word_sum


if __name__ == "__main__":
    dummy_data = {
        "a1":{
            "anxiety":2,
            "comments":"Had a cup of tea and it calmed me down.",
            "thoughts":"This cup of tea is nice\nIt stopped me thinking about the train",
            "feelings":"I love tea\nI hate trains",
            "triggers":"Trains"
        },
        "b2":{
            "anxiety":6,
            "comments":"I took the train today.",
            "thoughts":"I don't like all the sounds.",
            "feelings":"I feel unsafe\nI feel restless",
            "triggers":"Trains"
        },
        "c3":{
            "anxiety":1,
            "comments":"All I've done today is drink tea.",
            "thoughts":"Tea is much better than anything else.",
            "feelings":"I feel safe when I have a cup of tea.",
            "triggers":""
        }
    }
    custom_stop_words = ["feel", "feeling", "feelings"]
    cleaned_journal_data = combine_and_clean_all_journal_entries(dummy_data, custom_stop_words)
    X_df = create_cv_matrix(cleaned_journal_data)
    print(X_df)
    word_sum = identify_most_common_words(X_df, min_required_frequency=3)
    print(word_sum)