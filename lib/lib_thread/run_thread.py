import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        # 'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://europe.wsj.com/',
        'http://www.a--bbc.co.uk/',
        'http://euroa--pe.wsj.com/',
        'http://www.a--bbc.co.uk/',
        'http://euroa--pe.wsj.com/',
        'http://www.a--bbc.co.uk/',
        'http://some-made-up-domain.com/']

for i in range(1, 20):
    URLS += URLS
ddd = {}
index = 0

# Retrieve a single page and report the URL and contents
def load_url(url, timeout, key=0):
    print('load -> {}, key: {}'.format(url, key))
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        ddd[key] = conn.read()
        return key

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 10, index): url for index, url in enumerate(URLS)}
    print('done future')
    # for future in concurrent.futures.as_completed(future_to_url):
    for future in future_to_url:
    # for url in URLS:
        # future = executor.submit(load_url, url, 10)
        url = future_to_url[future]
        try:
            key = future.result()
            del ddd[key]
            ddd[key] = None
            # del future_to_url[future]
            # future_to_url[future] = None
            # future_to_url.pop(future, None)
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(ddd[key])))
#         
# import queue

# q = queue.Queue()

# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     try:
#         result = 



print('down')