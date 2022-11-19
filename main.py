from bs4 import BeautifulSoup
import requests
import lxml
import csv

URL1 = "https://www.audible.com"

params = {
    "keywords": input("What you wanna search?")
}

header = {
    "Accept-Language": "sr-RS,sr;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}


#function where we search data and choose category which books to scrape and expand our parameters to find all data
# per category
def search_category():
    response = requests.get(url=f"{URL1}/search", params=params, headers=header)

    data = response.text

    soup = BeautifulSoup(data, "lxml")

    search_data = soup.find_all(name="div", class_="categories")

    search_links = [char.find_all(name="a", class_="bc-link") for char in search_data]

    links = []
    counter = 0
    order_cat = {}
    for char in search_links[0]:
        links.append(char.get("href").split("?")[1])
        order_cat[counter] = char.text.strip()
        counter += 1

    print(order_cat)

    list_of = []

    for link in links:
        split_data = link.split("&")
        list_of.append(split_data)

    data_num = input(f"Choose your category: put your favorite number: \n")

    list_num = list_of[int(data_num)]

    for n in list_num:
        key_data = n.split("=")[0]
        value_data = n.split("=")[1]
        params[key_data] = value_data


#function do scrape choosen data and put all into csv
def scrape_data_csv():
    response1 = requests.get(url=f"{URL1}/search", params=params, headers=header)
    data1 = response1.text

    soup1 = BeautifulSoup(data1, "lxml")

    all_data = soup1.find_all(name="div", id="product-list-a11y-skiplink-target")

    info = [char.find_all(name="h3", class_="bc-heading") for char in all_data]

    author_data = [char.find_all(name="li", class_="authorLabel") for char in all_data]

    narrator_data = [char.find_all(name="li", class_="narratorLabel") for char in all_data]

    runtime_data = [char.find_all(name="li", class_="runtimeLabel") for char in all_data]

    release_data = [char.find_all(name="li", class_="releaseDateLabel") for char in all_data]

    language_data = [char.find_all(name="li", class_="languageLabel") for char in all_data]

    titles = [char.text.strip() for char in info[0]]

    authors = [char.find(name="a").text.strip() for char in author_data[0]]

    narrator = [char.find(name="a").text.strip() for char in narrator_data[0]]

    runtime = [char.find(name="span").text.split(":")[1].strip() for char in runtime_data[0]]

    release = [char.find(name="span").text.split(":")[1].strip() for char in release_data[0]]

    language = [char.find(name="span").text.split(":")[1].strip() for char in language_data[0]]

    with open("data.csv", "w", newline="", encoding="utf8") as scrape:
        csv_data = csv.writer(scrape)
        #write header into csv table
        csv_data.writerow(["Titles", "Authors", "Narrator", "Runtime", "Release", "Language"])

        for n in range(len(titles)):
            try:
                #write all scrape sections to csv rows
                csv_data.writerow([titles[n], authors[n], narrator[n], runtime[n], release[n], language[n]])
            except IndexError:
                #these exception might be different type of css selector
                print(f"is no good {n}")
                pass


#execute functions
search_category()
scrape_data_csv()


