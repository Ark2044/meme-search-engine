import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

class TextProcessor:
    def __init__(self):
        # Download necessary NLTK resources
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)  # Download omw-1.4 resource

        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """
        Clean and preprocess input text
        
        Args:
            text (str): Input text to clean
        
        Returns:
            str: Cleaned and processed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def tokenize(self, text):
        """
        Tokenize input text
        
        Args:
            text (str): Input text to tokenize
        
        Returns:
            list: List of tokens
        """
        return nltk.word_tokenize(text)

    def remove_stopwords(self, tokens):
        """
        Remove stop words from tokens
        
        Args:
            tokens (list): List of tokens
        
        Returns:
            list: Filtered tokens without stop words
        """
        return [token for token in tokens if token not in self.stop_words]

    def stem_tokens(self, tokens):
        """
        Apply stemming to tokens
        
        Args:
            tokens (list): List of tokens
        
        Returns:
            list: Stemmed tokens
        """
        return [self.stemmer.stem(token) for token in tokens]

    def lemmatize_tokens(self, tokens):
        """
        Apply lemmatization to tokens
        
        Args:
            tokens (list): List of tokens
        
        Returns:
            list: Lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def process_query(self, query, use_stemming=False):
        """
        Full text processing pipeline
        
        Args:
            query (str): Input search query
            use_stemming (bool): Whether to use stemming or lemmatization
        
        Returns:
            list: Processed query tokens
        """
        cleaned_query = self.clean_text(query)
        tokens = self.tokenize(cleaned_query)
        tokens = self.remove_stopwords(tokens)
        
        if use_stemming:
            return self.stem_tokens(tokens)
        else:
            return self.lemmatize_tokens(tokens)
