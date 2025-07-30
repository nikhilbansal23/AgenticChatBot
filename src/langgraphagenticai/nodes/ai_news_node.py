from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self,llm):

        ""
        "Initializes the AINewsNode with a language model."
        ""

        self.tavily = TavilyClient()
        self.llm = llm
        self.state = {}
    
    # Processes the user input and generates a response using the LLM model for AI news.

    def fetch_news(self,state:dict) -> dict:
        """
        Fetches the latest AI news using the Tavily API.
        
        Args:
            state (dict): The current state of the chatbot, including conversation history.
        
        Returns:
            dict: A dictionary containing the fetched news articles.
        """
        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily' : 'd', 'weekly' : 'w', 'monthly' : 'm','yearly' : 'y'}
        days_map = {'daily' : 1, 'weekly' : 7, 'monthly' : 30, 'yearly' : 365}

        response = self.tavily.search(
            query = "Top Artificial Intelligence (AI) technology news India and Globally",
            topic = 'news',
            time_range = time_range_map[frequency],
            include_answer = "advanced",
            max_results = 15,
            days = days_map[frequency],
        )

        state['news_data'] = response.get('results',[])
        self.state['news_data'] = state['news_data']
        return state
    

    # Processes the fetched news articles and summarizes them using the LLM model.
    def summarize_news(self,state:dict) -> dict:
        """
        Summarizes the fetched news articles using the LLM model.
        
        Args:
            state (dict): The current state of the chatbot, including fetched news articles.
        
        Returns:
            dict: A dictionary containing the summarized news articles.
        """
        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])
        # Prepare the articles for summarization
        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles = articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self,state):
        """
        Saves the summarized news articles to a file.
        
        """
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state
        
        

