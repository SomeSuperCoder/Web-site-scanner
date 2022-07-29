import sys
import requests
import validators
import copy
import warnings

from bs4 import *
from rich import print


error_text = "[bold red][ERROR][/bold red]"
log_text = "[bold green][LOG][/bold green]"
active_url_gettig_threads = []
main_i = 0
current_urls = []
current_tree_urls = []
temp_urls = []

warnings.filterwarnings("ignore")

def get_depth():
    try:
        return int(sys.argv[sys.argv.index("-d") + 1])
    except ValueError:
        print(f"{error_text} Depth must be a number not a string!")
        raise SystemExit(-1)
    except IndexError:
        print(f"{error_text} You did not specify a value!")
        raise SystemExit(-1)

def get_url():
    try:
        return str(sys.argv[sys.argv.index("-url") + 1])
    except ValueError:
        print(f"{error_text} Error depth must be a number not a string!")
        raise SystemExit(-1)
    except IndexError:
        print(f"{error_text} You did not specify a value!")
        raise SystemExit(-1)


def main():
    global depth
    global url
    global all_urls
    global current_urls
    global current_tree_urls

    depth = get_depth()
    url = get_url()
    print(f"{log_text} [bold]You set the recursion depth to {depth}[/bold]")

    try:
        res = requests.get(url)
    except requests.exceptions.MissingSchema as ex:
        print(f"{error_text} {ex}")
        raise SystemExit(-1)
    except requests.exceptions.ConnectionError:
        print(
            f"{error_text} You seem to have a not existing url or you have no internet connection :sad_but_relieved_face:")
        raise SystemExit(-1)

    soup = BeautifulSoup(res.text, "html.parser")
    initial_a_tags = soup.findAll("a")
    initial_urls = [i["href"] for i in initial_a_tags if validators.url(i["href"])]
    current_tree_urls = copy.copy(initial_urls)
    all_urls = copy.copy(initial_urls)

    print(f"initial urls: {initial_urls}")

    loop_over_list()

def loop_over_list():
    global current_tree_urls
    global depth
    global main_i

    for i in current_tree_urls:
        try:
            res = requests.get(i)
        except requests.exceptions.ConnectionError:
            print(f"{error_text} You seem to have a not existing url or you have no internet connection :sad_but_relieved_face:")
            raise SystemExit(-1)

        soup = BeautifulSoup(res.text, "html.parser")
        try:
            current_urls = [a_tag["href"] for a_tag in soup.findAll("a") if validators.url(a_tag["href"])]
            [temp_urls.append(x) for x in current_urls]
        except KeyError:
            pass

    print(f"{log_text} Loop {main_i} ended!")

    current_tree_urls = temp_urls
    [all_urls.append(x) for x in current_tree_urls]
    if main_i < depth:
        main_i+=1
        loop_over_list()
    else: print(all_urls)


if __name__ == "__main__":
    main()
