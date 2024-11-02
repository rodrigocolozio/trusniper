import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from print_color import print
import argparse
import sys
import re



# functions 
def is_api_link(link):
    api_patterns = [
        r'/api/',
        r'/v[0-9]+/',
        r'\.json$',
        r'\.xml$',
        r'\.aspx$',
        r'\.ashx$',
        r'/graphql',
        r'/gql',
        r'/users?',
        r'/posts?',
        r'/auth',
        r'/data',
        r'/get/',
        r'/list/',
        r'/update/',
        r'/create/',
        r'/delete/',
        r'/edit/',
        r'/fetch/'
    ]
    return any(re.search(pattern, link) for pattern in api_patterns)

def find_links(subdomain):
    try:
        response = requests.get(subdomain, timeout=10)
        if response.status_code != 200:
            print(f"Falha ao acessar {subdomain}", tag='FAIL', tag_color='red', color='white')
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        for tag in soup.find_all(['a', 'link', 'script']):
            link = tag.get('href') or tag.get('src')
            if link:
                full_link = urljoin(subdomain, link)
                links.add(full_link)

        api_links = [link for link in links if is_api_link(link)]
        return list(links), api_links

    except Exception as e:
        print(f"Erro ao processar {subdomain}: {str(e)}", tag='FAIL', tag_color='red', color='white')
        return None

def spider(subdomains):
    all_links = {}
    all_api_links = {}

    for subdomain in subdomains:
        print(f"Processando {subdomain}...")
        result = find_links(subdomain)
        if result:
            links, api_links = result
            if links or api_links:
                all_links[subdomain] = links
                all_api_links[subdomain] = api_links

    return all_links, all_api_links

def read_subdomains_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            subdomains = [line.strip() for line in file if line.strip()]
        return subdomains
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}", tag='FAIL', tag_color='red', color='white')
        return []

def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    subdomains = read_subdomains_from_file(args.file_path)

    if subdomains:
        all_links, all_api_links = spider(subdomains)

        for sub, links in all_links.items():
            if links:  # Exibe apenas se houver links encontrados
                print('----------------------------')
                print(f"Links encontrados em {sub}:\n", tag='LINKS', tag_color='green', color='green')
                for link in links:
                    print(link)

        for sub, api_links in all_api_links.items():
            if api_links:  # Exibe apenas se houver APIs encontradas
                print('------------------------------')
                print(f"Links de APIs encontrados em {sub}:\n", tag='API', tag_color='blue')
                for api_link in api_links:
                    print(api_link)
    else:
        print("Nenhum subdomínio encontrado ou erro ao ler o arquivo.", tag='FAIL', tag_color='red', color='white')

# validar function para salvar arquivo de out put
# criar variáveis que receberão esses valors
# criar a lógica (será no app, será no main?)
def save_output(output, file):
    try:
        with open(output) as data:
            for item in output:
                file.write(item + "\n")
    except Exception as e:
        print(f'Error while creating the output file: {str(e)}')


# application
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL spider to identify APIs consumption")
    parser.add_argument("--url", dest="file_path", required=True, help="Path containing all the domains and subdomais you want to check for API consumption")

    print(
        """
      __________  __  ______________   __________  ____  __   _____
    /_  __/ __ \/ / / / ____/ ____/  /_  __/ __ \/ __ \/ /  / ___/
    / / / /_/ / / / / __/ /___ \     / / / / / / / / / /   \__ 
    / / / _, _/ /_/ / /_______/ /    / / / /_/ / /_/ / /______/ /
    /_/ /_/ |_|\____/_____/_____/    /_/  \____/\____/_____/____/
        \n
    """, color='cyan', format='blink'
    )
    print(
        """
    ===================================================
    =                                                   =
    =                                                   =
    =          :.       TRUSPIDER        .:             =
    =                                                   =
    =                                                   =
    =                                                   =
    =       by: TRUE5                                   =
    =                                                   =
    ====================================================

    Usage ---->   Menu : python3 truspider.py --URL <url_list_PATH>


    truspider v1.2
    Last update: Oct, 20, 2024
    Contact: true5mail _at_ proton.me
    """, color='cyan'
    )
    try:
        main()
    except KeyboardInterrupt:
        print('Stopping program,\n\nByebye :)', color='red')
        sys.exit(0)
