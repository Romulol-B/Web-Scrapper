import sys

from crawl import crawl_page, extract_page_data, get_html


def main():
    if len(sys.argv) == 2:
        print("starting crawl of:", sys.argv[1])
        page_data = crawl_page(sys.argv[1], current_url=sys.argv[1], page_data=None)
        print(page_data)
        print(f"number of pages found:{len(page_data.keys())}")
    elif len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    else:
        print("too many arguments provided")
        sys.exit(1)


main()

if __name__ == "__main__":
    main()
