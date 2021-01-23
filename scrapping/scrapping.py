import requests
from bs4 import BeautifulSoup


def search(qs):
    global flag2

    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)
    wiki=''
    answer='sorry i ignore the answer \n please give me more precisions'
    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.findAll("a")
    all_links = []
    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))

    flag = False
    for link in all_links:
        if 'https://en.wikipedia.org/wiki/' in link:
            wiki = link
            flag = True
            break

    div0 = soup.find_all('div', class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3 = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0) != 0:
        answer = div0[0].text
    elif len(div1) != 0:
        answer = div1[0].text + "\n" + div1[0].find_next_sibling("div").text
        # print(answer)
        # speak(answer)
        # print(div1[0].find_next_sibling("div").text)
    elif len(div2) != 0:
        answer = div2[0].find_next("span").text + "\n" + div2[0].find_next("div", class_="kCrYT").text
        # print(answer)
        # speak(answer)
        # print(div2[0].find_next("div",class_="kCrYT").text)
    elif len(div3) != 0:
        answer = div3[1].text
    elif flag == True:
        page2 = requests.get(wiki)
        soup = BeautifulSoup(page2.text, 'html.parser')

        title = soup.select("#firstHeading")[0].text
        # print(title)
        paragraphs = soup.select("p")
        for para in paragraphs:
            if bool(para.text.strip()):
                answer = title + "\n" + para.text
                # print(answer)
                # speak(answer)
                break
        # print(paragraphs)
        # just grab the text up to contents as stated in question
        # intro = '\n'.join([ para.text for para in paragraphs[0:2]])
        # print(intro)
    return answer