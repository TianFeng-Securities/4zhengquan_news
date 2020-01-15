# 2019.12.26 高华，完结
import pandas as pd
import requests,sys,datetime
from lxml import etree
# 发请求
print("正在初始化。。。")
day_sum_url = "http://finance.sina.com.cn/focus/zqbjh/"  # 总览页的地址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
response = requests.get(url=day_sum_url, headers=headers)  # 获得总览页的返回值
html_text = response.content.decode("utf-8")  # 将返回的结果进行转码并储存
html = etree.HTML(html_text)  # 将文本转换成标准的html
urls = html.xpath("//div/ul[@class=\"list_009\"]/li/a/@href")  # 解析网址
titles = html.xpath("//div/ul[@class=\"list_009\"]/li/a/text()")  # 解析标题
dates = html.xpath("//div/ul[@class=\"list_009\"]/li/span/text()")  # 解析发布日期
df = pd.DataFrame(columns=["时间", "报刊", "标题", "主要内容"])#初始df新建
print("初始化完毕！")
# 对网址循环发请求，返回网址内容
for index, url in enumerate(urls):
    sys.stdout.flush()#刷新上次的打印
    sys.stdout.write(f"\r第{index+1}/{len(urls)}次请求")
    content = requests.get(url, headers=headers).content.decode("utf-8")
    content_html = etree.HTML(content)  # 将内容转换成标准的html
    news = []#存储一个网页所有的内容
    nodes = content_html.xpath("//*[@id=\"artibody\"]/p")
    for node in nodes:
        news.append(node.xpath("string(.)"))
    news = [new.strip() for new in news if new.find("责任编辑") == -1]#去除最后的责任编辑
    real_paper = ["中国证券报", "证券时报", "上海证券报", "证券日报"]#初始的四家报纸顺序
    final_paper = []  # 存储最后的正确顺序的报纸
    news_titles = []  # 存储新闻标题
    news_contents = []  # 存储新闻内容
    #基本的算法思想是遍历字符串列表，当遇到一家报纸的时候，就默认其后面的8条内容就是这家报纸出的
    for new in news:
        if new in real_paper:
            final_paper = final_paper + [new] * 4
            for i in range(1, 9):
                #8条内容中奇数项是标题
                if i % 2 != 0:
                    news_titles.append(news[news.index(new) + i])
                #8条内容中偶数项是内容
                else:
                    news_contents.append(news[news.index(new) + i])
    # 定义时间列表
    date = [datetime.datetime.strptime(dates[index].replace("(","").replace(")",""),'%Y-%m-%d %H:%M:%S').date()] * len(news_titles)
    df_temp = pd.DataFrame({'时间': date, '报刊': final_paper, '标题': news_titles, '主要内容': news_contents})
    df = df.append(df_temp)
df=df.sort_values(by=['时间','报刊'])  # 按照时间先后排序，按照报纸顺序排序
df.to_excel(r"原始数据/四大证券报原始数据.xlsx", encoding='gb2312', index=0)  # 输出到excel
print("\n运行结束")