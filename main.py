import sys

from crawl import extract_page_data, get_html


def main():
    if len(sys.argv) == 2:
        print("starting crawl of:", sys.argv[1])
        page = get_html(sys.argv[1])
        print(page)
        # print(extract_page_data(page, sys.argv[1]))
    elif len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    else:
        print("too many arguments provided")
        sys.exit(1)


main()

if __name__ == "__main__":
    main()
