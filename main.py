import asyncio

import httpx
from fake_useragent import UserAgent

settings = {
    "timeout": 5,
}

headers = {
    "user-agent": UserAgent().random,
    "accept": "text/html"
}

urls = []

result = {
    "success": [],
    "warning": [],
    "error": []
}


def load_urls():
    with open('url.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            urls.append(line)


async def check_urls():
    for url in urls:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=settings['timeout'])

                if response.status_code == 200 or response.status_code == 301:
                    print('{0:<30} {1:>30}'.format(url, '\033[92mSUCCESS\033[0m'))
                    result['success'].append(url)
                else:
                    print('{0:<30} {1:>30}'.format(url, '\033[93mWARNING\033[0m'))
                    result['warning'].append(url)
            except Exception as e:
                print('{0:<30} {1:>30}'.format(url, '\033[91mERROR\033[0m'))
                result['error'].append(url)


def save_data():
    success = "\n".join(result['success'])
    warning = "\n".join(result['warning'])
    error = "\n".join(result['error'])

    open('data/success.txt', 'w').write(success)
    open('data/warning.txt', 'w').write(warning)
    open('data/error.txt', 'w').write(error)


if __name__ == '__main__':
    load_urls()
    print('{0:<30} {1:>20}'.format('Url', 'Status'))
    asyncio.run(check_urls())
    save_data()
