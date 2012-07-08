import urllib.request


## function to make a get request and get the HTML code of the web page
def get_page(url):
    # This func gets the HTML code from the url
    try:
        opener = urllib.request.build_opener()
        resp = opener.open(url)
        html_page = resp.read()
        print(html_page)
        return str(html_page)
    except:
        return "Unable to fetch the HTML page"


#This func gets the next <a href = "link"
def get_next_link(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    print("url = ", url)
    return url, end_quote
  
#add the value(s) of q to p
def add_to(p,q):
    for e in q:
        if e not in p:
            p.append(e)

#This function fetches all the links in a page. This internally calls get_next_link
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_link(page)
        page = page[endpos:]
        if not url is None and url.find('http://') != -1:
            if url not in links:
                links.append(url)     
        elif url is None:
            break
    return links

#This function controls the no. of links crawled thru the integer link_count
def get_all_links_2(page, link_count):
    links = []
    while link_count>=0 :
        url,endpos = get_next_link(page)
        page = page[endpos:]
        link_count -= 1
        if not url is None and url.find('http://') != -1:
            if url not in links:
                links.append(url)     
        elif url is None:
            break
    return links

##get all the words (contents) from the <html> code of the web page and create an index of those words with the url link 
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
    
##lookup for a keyword in the index
def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return None

# to keep track of the times a particular url is clicked when the corresponding keyword is searched
def click_tracker(index,keyword,url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1]+1

##add the keyword - url to the index list ! 
def add_to_index(index, keyword, url):
    # format of index: [[keyword, [[url, count], [url, count],..]],...]
    for entry in index:
        if entry[0] == keyword:
            for urls in entry[1]:
                if urls[0] == url:
                    return
            entry[1].append([url,0])
            return
    # not found, add new keyword to index
    index.append([keyword, [[url,0]]])


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        link = tocrawl.pop()                            #get the seed/link from tocrawl
        if link not in crawled:
            content = get_page(link)                    #content = <html> content of the page 
            url = get_all_links(content)                # url is a list conatining all the link urls in the current page
            add_page_to_index(index, link, content)
            add_to(tocrawl, url)                         ## add the urls obtained to tocrawl list
            crawled.append(link)
    return index



index = crawl_web('http://xkcd.com/353/')
#print("index = ", index)
print(lookup(index, 'python'))
click_tracker(index, 'python', 'http://xkcd.com/353/')
print(lookup(index, 'python'))


