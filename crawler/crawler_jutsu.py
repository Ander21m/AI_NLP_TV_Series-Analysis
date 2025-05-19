import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'narutospider'
    start_urls =['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self,response):
        for title in response.css('.smw-columnlist-container')[0].css('a::attr(href)').extract():
            extract_value = scrapy.Request("https://naruto.fandom.com/"+title,
                           callback= self.parse_jutsu)
            yield extract_value

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page,self.parse)

    def parse_jutsu(self,response):
        jutsu_name = response.css('span.mw-page-title-main::text').extract()[0]
        jutsu_name = jutsu_name.strip()

        div_selection = response.css('div.mw-parser-output')[0]
        div_html = div_selection.extract()

        soup = BeautifulSoup(div_html).find("div")

        jutsu_type =""
        if soup.find('aside'):
            aside = soup.find('aside')

            for cell in aside.find_all('div',{'class' : 'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == "Classification":
                        jutsu_type = cell.find('div').text.strip()

        soup.find("aside").decompose()

        jutsu_des = soup.text.strip()
        jutsu_des = jutsu_des.split("Trivia")[0].strip()

        return dict(
            jutsu_name = jutsu_name,
            jutsu_type = jutsu_type,
            jutsu_des = jutsu_des
        )



