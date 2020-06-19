from selenium import webdriver

import time

# 2. 构建浏览器对象
browser = webdriver.Chrome('./chromedriver')

# 3. 控制浏览器获取数据
browser.get("https://music.163.com/#/discover/playlist")



while True:
    time.sleep(1)

    # 切换到 iframe 中
    iframe_element = browser.find_element_by_id("g_iframe")
    browser.switch_to.frame(iframe_element)

    # 从网页中提取歌曲
    li_list = browser.find_elements_by_xpath('//ul[@id="m-pl-container"]/li')

    for li in li_list:
        item = {}
        item["title"] = li.find_element_by_xpath('./p[@class="dec"]/a').text
        item["author"] = li.find_element_by_css_selector(".nm.nm-icn.f-thide.s-fc3").text
        item["img"] = li.find_element_by_class_name("j-flag").get_attribute("src")
        print(item)

    next_button = browser.find_element_by_link_text("下一页")
    next_url = next_button.get_attribute("href")
    # next_button.click()
    browser.get(next_url)
    from selenium import webdriver

    import time

    # 2. 构建浏览器对象
    browser = webdriver.Chrome('./chromedriver')

    # 3. 控制浏览器获取数据
    browser.get("https://music.163.com/#/discover/playlist")

    while True:
        time.sleep(1)

        # 切换到 iframe 中
        iframe_element = browser.find_element_by_id("g_iframe")
        browser.switch_to.frame(iframe_element)

        # 从网页中提取歌曲
        li_list = browser.find_elements_by_xpath('//ul[@id="m-pl-container"]/li')

        for li in li_list:
            item = {}
            item["title"] = li.find_element_by_xpath('./p[@class="dec"]/a').text
            item["author"] = li.find_element_by_css_selector(".nm.nm-icn.f-thide.s-fc3").text
            item["img"] = li.find_element_by_class_name("j-flag").get_attribute("src")
            print(item)

        next_button = browser.find_element_by_link_text("下一页")
        next_url = next_button.get_attribute("href")
        # next_button.click()
        browser.get(next_url)
time.sleep(5)
# 4. 退出浏览器
browser.quit()
