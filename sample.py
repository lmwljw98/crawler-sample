from bs4 import BeautifulSoup
import requests


def getRepoCount(id):
    r = requests.get("https://github.com/" + id)
    source = r.text
    soup = BeautifulSoup(source, "lxml")

    repo_a_tag = soup.find("a", {"title": "Repositories"})
    repoCount = repo_a_tag.find("span")

    return int(repoCount.text.strip())


def getFrequencyByStar(id):
    print("---Show language frequency by stars---")

    r = requests.get("https://github.com/" + id + "?tab=stars")
    source = r.text
    soup = BeautifulSoup(source, "lxml")

    star_menu = soup.find("div", {"class": "select-menu-list"})
    star_category_link = star_menu.find_all("a")
    star_category_lang = star_menu.find_all("span", {"class": "select-menu-item-text js-select-button-text"})

    frequency_star = dict()
    total_stars = 0

    for i in range(1, len(star_category_link)):
        # print(star_category_link[i]['href'])

        r2 = requests.get(star_category_link[i]['href'])
        source2 = r2.text
        soup2 = BeautifulSoup(source2, "lxml")

        star_count = soup2.find("div", {"class": "TableObject-item TableObject-item--primary"})
        print(star_category_lang[i].text + ": " + star_count.find("strong").text + " stars")
        frequency_star[star_category_lang[i].text] = int(star_count.find("strong").text)
        total_stars += int(star_count.find("strong").text)
    
    print(frequency_star)
    # print("Total Stars:", total_stars)
    for j in frequency_star.keys():
        print(j, format((frequency_star[j] / total_stars) * 100, ".2f") + "%")
    return frequency_star # return dictionary for stars


def getFrequencyByRepo(id, repoCount):
    print("---Show language frequency by repositories---")

    if repoCount % 30 == 0:
        pages = repoCount // 30
    else:
        pages = repoCount // 30 + 1

    # print("Pages:", pages)

    frequency = dict()
    lang_count = 0

    for page in range(1, pages + 1):
        r = requests.get("https://github.com/" + id + "?page=" + str(page) + "&tab=repositories")
        source = r.text
        soup = BeautifulSoup(source, "lxml")

        myLanguage = soup.find_all("span", {"itemprop": "programmingLanguage"})
        lang_count += len(myLanguage)

        for i in range(len(myLanguage)):
            if myLanguage[i].text.strip() not in frequency:
                frequency[myLanguage[i].text.strip()] = 1
            else:
                frequency[myLanguage[i].text.strip()] += 1

    print(frequency)

    for j in frequency.keys():
        print(j, format((frequency[j] / lang_count) * 100, ".2f") + "%")
    
    return frequency # return dictionary for repositories


if __name__ == "__main__":
    id = input("Github ID: ")

    repoCount = getRepoCount(id)
    getFrequencyByRepo(id, repoCount)
    print()
    getFrequencyByStar(id)

