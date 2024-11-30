from flask import Flask, render_template, request
from utils.text_processor import TextProcessor
from utils.meme_scraper import MemeScraper

app = Flask(__name__)

# Initialize utilities
text_processor = TextProcessor()
meme_scraper = MemeScraper()

@app.route('/')
def index():
    """
    Render the home/index page
    """
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_memes():
    """
    Handle meme search requests
    """
    query = request.args.get('query', '')
    
    if not query:
        return render_template('results.html', memes=[], query=query)
    
    try:
        # Search for memes
        memes = meme_scraper.search_memes(query, text_processor)
        
        return render_template('results.html', 
                               memes=memes, 
                               query=query)
    
    except Exception as e:
        print(f"Search error: {e}")
        return render_template('results.html', 
                               memes=[], 
                               query=query, 
                               error="An error occurred during search")

if __name__ == '__main__':
    app.run(debug=True)