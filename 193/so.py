import requests
from bs4 import BeautifulSoup

cached_so_url = 'https://bit.ly/2IMrXdp'


def get_views_count(view_element):
    title = view_element['title']
    title = title.split(' ')[0]
    count = int(title.replace(',', ''))
    return count


def top_python_questions(url=cached_so_url):
    """Use requests to retrieve the url / html,
       parse the questions out of the html with BeautifulSoup,
       filter them by >= 1m views ("..m views").
       Return a list of (question, num_votes) tuples ordered
       by num_votes descending (see tests for expected output).
    """
    response = requests.get(cached_so_url)
    questions = []
    if response:
        html = BeautifulSoup(response.content, 'html.parser')
        summaries = html.find_all(class_='question-summary')
        for summary in summaries:
            id = summary.get('id')
            hyperlink = summary.find_all('a', class_='question-hyperlink')[0]
            votes = int(summary.find_all(class_='vote-count-post')[0].text)
            views = summary.find_all(class_='views')[0]
            views = get_views_count(views)
            print(f'{id}: {hyperlink.text}, {votes}, {views}')
            if views > 1000000:
                questions.append((hyperlink.text, votes))
        questions.sort(key=lambda c: c[1], reverse=True)
        return questions
