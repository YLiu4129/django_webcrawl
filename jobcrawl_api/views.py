from django.shortcuts import render
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
# webdriver-manager套件是用來協助selenium套件，在執行Python網頁爬蟲時，自動下載瀏覽器的驅動程式(Webdriver)。
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


# Create your views here.
def main(request):
	return render(request,'index.html')

def crawler(request):

    keywords = request.POST['keyword']
    start_time = time.time()  # 開始時間

    result = []
    options = Options()
    options.add_argument("--headless")  # 不開啟實體瀏覽器背景執行
    options.add_argument("--incognito")  # 開啟無痕模式

    browser = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

    for page in range(1, 2):
        # links.append("https://www.104.com.tw/jobs/search/?keyword=python&order=1&page=" +
        # str(page) + "&jobsource=2018indexpoc&ro=0")
        link = "https://www.104.com.tw/jobs/search/?keyword=python&order=1&page=" + \
               str(page) + "&jobsource=2018indexpoc&ro=0"
        # reqs = (grequests.get(link) for link in links)  # 建立請求集合
        # response = grequests.imap(reqs, grequests.Pool(10))  # 發送請求
        browser.get(link)
        # for r in response:
        soup = BeautifulSoup(browser.page_source, "html")  # 解析HTML原始碼

        blocks = soup.find_all("div", {"class": "b-block__left"})  # 職缺區塊
        # print(blocks)
        for block in blocks:

            job = block.find("a", {"class": "js-job-link"})  # 職缺名稱

            if job is None:
                continue

            company = block.find_all("li")[1]  # 公司名稱
            # print(company.getText())

            salary = block.find("span", {"class": "b-tag--default"})  # 待遇
            if not salary:
                salary = []
            infos = block.find_all('ul', {'class': "b-list-inline b-clearfix job-list-intro b-content"})
            for info in infos:
                address = info.find_all('li')[0]
                years = info.find_all('li')[1]

            job_content = block.find('p', {'class': "job-list-item__info b-clearfix b-content"})

            job_link = block.find('a')['href'][2:]
            job_link = 'http://' + job_link
            # use selenium driver here to avoid jvs problem which bs4 can't solve
            browser.get(job_link)
            # use beautifulsoup to parse selenium driver
            j_soup = BeautifulSoup(browser.page_source, "lxml")
            job_require = j_soup.find('p', {'class': 'mb-5 r3 job-description__content text-break'})

            if job_require:
                result.append(dict(job=job.getText(), company=company.getText().strip().rstrip(), salary=salary.getText(),
                                   address=address.getText(),years=years.getText(), job_content=job_content.getText(),
                                   job_require=job_require.getText(), job_link=job_link))
            else:
                result.append(dict(job=job.getText(), company=company.getText().strip().rstrip(), salary=salary.getText(),
                                   address=address.getText(),years=years.getText(), job_content=job_content.getText(),
                                   job_require='NA', job_link=job_link))
    browser.close()
    # locals(): 取得所有變數並轉成字典
    return render(request, 'result.html', locals())
    #print("花費：" + str(time.time() - start_time) + "秒")