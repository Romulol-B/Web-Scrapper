import asyncio
import sys

from crawl import crawl_site_async
from json_report import write_json_report


async def main():
    if len(sys.argv) == 4:
        print("starting crawl of:", sys.argv[1])
        print(f"max pages is {sys.argv[2]}")
        print(f"max concurrency is {sys.argv[3]}")
        page_data = await crawl_site_async(
            base_url=sys.argv[1],
            max_concurrency=int(sys.argv[2]),
            max_pages=int(sys.argv[3]),
        )
        write_json_report(page_data)
        sys.exit(0)
    elif len(sys.argv) < 4:
        print("no website provided")
        sys.exit(1)
    else:
        print("too many arguments provided")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
