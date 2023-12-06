# Used to scrape a number of versions of packages from the Libraries.io site.

import parse_arguments
import os   # for ENV variable
from dotenv import load_dotenv
from pybraries.search import Search
import requests
import pypistats
import pandas as pd

LIBRARIES_API_KEY = os.getenv('LIBRARIES_API_KEY')


# def find_packages(rank_by = "popularity", top_ranks = 10):
#     search = Search()
    
#     print(search.platforms())
    
#     # info = search.project_search(sort='dependent_repos_count',
#     #                              platform='pypi', 
#     #                              repository_sources='pypi', 
#     #                              language='Python')


#     # with open("results.json", "w", encoding="utf-8") as f:
#     #     f.write(str(info))
    
#     return


def get_top_pypi_packages(top_packages_url="https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json",
                    count = 10):
    url_data = requests.get(url)
    
    print(url_data)
    



def main():
    get_top_pypi_packages()


if __name__ == "__main__":
    main()
