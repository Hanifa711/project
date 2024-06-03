import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the Excel file
input_file_path = 'C:\\Users\\Administrator\\Desktop\\in.xlsx'
df = pd.read_excel(input_file_path)

# Assuming the links are in the first column
links = df.iloc[:, 0].tolist()

def extract_page_content(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
         # Extract publication date
        pub_date = ''
        date_tag = soup.find('span', class_='fm-vol-iss-date')
        if date_tag:
            date_text = date_tag.get_text()
            # Use regex to find the date pattern
            match = re.search(r'Published online (\d{4} \w{3} \d{1,2})', date_text)
            if match:
                pub_date = match.group(1)
        # Extract citation author
        authors = []
        author_tags = soup.find_all('meta', attrs={'name': 'citation_author'})
        for tag in author_tags:
            if 'content' in tag.attrs:
                authors.append(tag['content'])
        citation_author = ', '.join(authors)        
      
        # Extract DC Title
        dc_title = ''
        dc_title_tag = soup.find('meta', attrs={'name': 'DC.Title'})
        if dc_title_tag and 'content' in dc_title_tag.attrs:
            dc_title = dc_title_tag['content']
          # Extract content from list item with specific class
        breadcrumb_item = ''
        breadcrumb_tag = soup.find('li', class_='usa-breadcrumb__list-item', attrs={'aria-current': 'page'})
        if breadcrumb_tag:
            breadcrumb_item = breadcrumb_tag.get_text(strip=True)

        
        # Extract og:description
        abstract = ''
        og_description_tag = soup.find('meta', property='og:description')
        if og_description_tag and 'content' in og_description_tag.attrs:
            abstract = og_description_tag['content']

        # Extract citation_doi
        citation_doi = ''
        citation_doi_tag = soup.find('meta', attrs={'name': 'citation_doi'})
        if citation_doi_tag and 'content' in citation_doi_tag.attrs:
            citation_doi = citation_doi_tag['content']
          
        # Extract citation_journal_title
        citation_journal_title = ''
        citation_journal_title_tag = soup.find('meta', attrs={'name': 'citation_journal_title'})
        if citation_journal_title_tag and 'content' in citation_journal_title_tag.attrs:
            citation_journal_title = citation_journal_title_tag['content']

        # Extract citation_journal_title
        citation_pmid = ''
        citation_pmid_tag = soup.find('meta', attrs={'name': 'citation_pmid'})
        if citation_pmid_tag and 'content' in citation_pmid_tag.attrs:
            citation_pmid = citation_pmid_tag['content']    
        return {
            'URL': url,
            'Title': dc_title,
            'doi':citation_doi,
            'pmcid': breadcrumb_item,
            'pubmed_id':citation_pmid,
            'abstract':abstract,
            'publish_time': pub_date,
            'authors': citation_author,            
            'journal_title':citation_journal_title,
        }
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return None

# Define the crawling limit
crawling_limit = 1000
output_data = []
crawled_count = 0

for link in links:
    if crawled_count >= crawling_limit:
        break
    result = extract_page_content(link)
    if result:
        output_data.append(result)
        crawled_count += 1
        print(crawled_count)

# Convert to DataFrame
output_df = pd.DataFrame(output_data)

# Save to Excel
output_file_path = 'path_to_output_excel_file5.xlsx'
output_df.to_excel(output_file_path, index=False)

print(f"Saved {crawled_count} pages to {output_file_path}")
