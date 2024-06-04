import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from normlization import Normalization
from data_set2.data_set2_dict import data2_dict
from data_set1.data_set1_dict import data1_dict
from spellchecker import SpellChecker
import string
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk import pos_tag
from nltk.corpus import wordnet


class TextProcessor:
    def __init__(self):
        # self.data_dict = data_dict
        self.specific_words = ['*', ')', '(', '\\', ']', '[', ',', ':', "-", "'s", '&', '¤', '+', '$', ';', '^', '@', '_']
        self.patterns = [r"\b\d+\s+[Yy]ears\b", r"\b\d+\s+[Mm]onths\b", r"\b\d+\s+[Dd]ays\b", r"\b\d+\s+[Ww]eeks\b",r"\b\d+\s+[Yy]ear\b", r"\b\d+\s+[Mm]onth\b", r"\b\d+\s+[Dd]ay\b", r"\b\d+\s+[Ww]eek\b",r'\b\d{4}-\d{1,2}-\d{1,2}\b',r'United\s+\w+', r"Phase \d+/Phase \d+", r'Phase\s+\d+', r'\b\w{4,}\b']
        self.specific_words = set(self.specific_words)
        self.stop_words = set(stopwords.words('english'))
        self.punctuation = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        #self.stemmer = PorterStemmer()
        self.normalize = Normalization()
        nltk.download('stopwords')
        # Combine multiple regex patterns into one for RegexpTokenizer
        combined_pattern = '|'.join(self.patterns)
        self.tokenizer = RegexpTokenizer(combined_pattern)


    def get_wordnet_pos(self,tag_parameter):
        tag = tag_parameter[0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        
        return tag_dict.get(tag, wordnet.NOUN)    
    
    def process_text(self, text):
        # Tokenize the text using RegexpTokenizer
        words = self.tokenizer.tokenize(text)
        
        filtered_words = list(set([
        word for word in words 
        if word.lower() not in self.stop_words 
        and word.lower() not in self.specific_words
        and word not in self.punctuation
        ]))


        normalized_words = list(set([self.normalize.normalize(word) for word in filtered_words]))
        #print(normalized_words[0])
        pos_tags = pos_tag(normalized_words)

        #print(pos_tags[0])
        lemmatized_words = [self.lemmatizer.lemmatize(word,pos=self.get_wordnet_pos(tag)) for word, tag in pos_tags]
        #stemmed_words = [self.stemmer.stem(word) for word in normalized_words]

        #return lemmatized_words
        return ' '.join(lemmatized_words)
    

    def process_single_text(self, text):
        # Tokenize the text using RegexpTokenizer
        words = self.tokenizer.tokenize(text)
        
        filtered_words = list(set([
        word for word in words 
        if word.lower() not in self.stop_words 
        and word.lower() not in self.specific_words
        and word not in self.punctuation
        ]))


        normalized_words = list(set([self.normalize.normalize(word) for word in filtered_words]))
        #print(normalized_words[0])
        pos_tags = pos_tag(normalized_words)

        #print(pos_tags[0])
        lemmatized_words = [self.lemmatizer.lemmatize(word,pos=self.get_wordnet_pos(tag)) for word, tag in pos_tags]
        #stemmed_words = [self.stemmer.stem(word) for word in normalized_words]

        return lemmatized_words
    

    # def process(self):
    #     processed_dict = {}
    #     unique_words = set()

    #     for key, values in self.data_dict.items():
    #         processed_dict[key] = set()
    #         for value in values:
    #             if isinstance(value, str):
    #                 processed_text = self.process_text(value)
    #                 # Add only unique words not already seen
    #                 new_words = set(processed_text) - unique_words
    #                 unique_words.update(new_words)
    #                 processed_dict[key].update(new_words)
    #             elif isinstance(value, list):
    #                 for item in value:
    #                     processed_text = self.process_text(item)
    #                     # Add only unique words not already seen
    #                     new_words = set(processed_text) - unique_words
    #                     unique_words.update(new_words)
    #                     processed_dict[key].update(new_words)

    #     # Convert sets back to lists for consistency with original structure
    #     processed_dict = {key: list(words) for key, words in processed_dict.items()}
    #     return processed_dict


    # def save_to_file(self, output_file, processed_dict):
    #     with open(output_file, 'w', encoding='utf-8') as f:
    #         for key, values in processed_dict.items():
    #             formatted_value = ','.join(f'"{word}"' for word in values)
    #             f.write(f"{formatted_value}\n")

# if __name__ == "__main__":
    # Example dictionary with the provided data
    # data_dict = data2_dict

    # # Specific words to delete
    # specific_words = ["island",'"', 'former', 'republic', '*', ')', '(', '\\', ']', '[', ',', ':', "-", "'s", '&', '¤', '+', '$', ';', '^', '@', '_']

    # patterns = [r'\b\d{4}-\d{1,2}-\d{1,2}\b',r'United\s+\w+', r"Phase \d+/Phase \d+", r'Phase\s+\d+', r'\b\w{3,}\b', r"\b\d+\s+Years\b", r"\b\d+\s+Months\b", r"\b\d+\s+Days\b", r"\b\d+\s+Weeks\b"]

    # # Download required NLTK resources
    # nltk.download('stopwords')

    # # Create an instance of TextProcessor
    # processor = TextProcessor()
    # processor.process_text(text= 'melanoma, BRAF (V600R), 80 year, male')


    # # Process the dictionary
    # processed_dict = processor.process()

    # # Save the result to a text file
    # output_file = 'processed_text.txt'
    # processor.save_to_file(output_file, processed_dict)
    
    # print(f"Processed text has been saved to {output_file}")
