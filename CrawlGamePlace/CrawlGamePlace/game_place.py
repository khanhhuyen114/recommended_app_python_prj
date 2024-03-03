from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
# Hàm crawl data from Google chrome
def crawlGgchrome(linksearch):
#mở web bằng selenium
    browser = webdriver.Chrome(service = Service("./chromedriver.exe"))
    browser.get(linksearch)
    sleep(2)
#tạo dictionary để lưu data
    data_dict = {}
    data_dict['Name'] = []
    data_dict['Time'] = []
    data_dict['Location'] = []
    data_dict['Rate'] = []
    active = True
    n = []
    while (active):
        try:
            sleep(2)
            #Tìm list địa điểm có xpath = "//div[@jsname = 'GZq3Ke']"
            n = browser.find_elements(By.XPATH, "//div[@jsname = 'GZq3Ke']")
            #Trong mỗi địa điểm, lấy tên, địa chỉ, rating, thời gian mở cửa
            for i in n:
                try:
                    name = i.find_element(By.CLASS_NAME,'OSrXXb')
                    data_dict['Name'].append(name.text)
                except:
                    name = None
                    data_dict['Name'].append(name)
                    pass
                try:
                    i.click()
                    sleep(1)
                    try:
                         rate = browser.find_element(By.XPATH,"//div[@class ='TLYLSe']")
                         data_dict['Rate'].append(rate.text)
                    except:
                        rate = None
                        data_dict['Rate'].append(rate)
                        pass
                    try:
                         loc = browser.find_element(By.XPATH,"//div[@class ='Z1hOCe']")
                         data_dict['Location'].append(loc.text)
                    except:
                        loc = None
                        data_dict['Location'].append(loc)
                        pass
                    try:
                        c = browser.find_element(By.XPATH, "//span[@class='JjSWRd']")
                        c.click()
                        sleep(1)
                        t = '//div[@class="a-h"]'
                        timee = browser.find_element(By.XPATH, t)
                        data_dict['Time'].append(timee.text[:-13])
                    except:
                        timee = None
                        data_dict['Time'].append(timee)
                        pass
                except:
                    continue
            # Next sang trang khác để tìm tiếp
            try:
                next = browser.find_element(By.LINK_TEXT, "Tiếp")
                sleep(1)
                next.click()
                active = True
            except:
                active = False
        except:
            active = False
    # browser.quit()
    # Format lại dữ liệu
    data_format = {}
    data_format['Tên'] = []
    data_format['Thời gian'] = []
    data_format['Địa điểm'] = []
    data_format['Rate'] = []
    data_format['Number_of_Review'] = []
    for i in data_dict['Rate']:
        try:
            i = i.split('\n')
        except:
            pass
        if i == None:
            k = 'loại'
            data_format['Rate'].append(k)
            data_format['Number_of_Review'].append(k)
        else:
            data_format['Rate'].append(i[0])
            data_format['Number_of_Review'].append(i[1])
    for j in data_dict['Time']:
        try:
            j = j.replace('\n', ' ')
            data_format['Thời gian'].append(j)
        except:
            data_format['Thời gian'].append(None)
            continue
    for i, j in zip(data_dict['Name'],data_dict['Location']):
        data_format['Tên'].append(i)
        data_format['Địa điểm'].append(j)
    return data_format
# Đẩy dữ liệu vào data frame
def Data_frame(data_format,keyword):
    data_df = pd.DataFrame(data = data_format)
    data_df['Search Key'] = keyword.replace('+', ' ')
    data_df = data_df[data_df.Rate != 'loại']
    return data_df
# Đẩy data frame vào file excel
def append_df_to_excel(df, excel_path):
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path, index=False)
# list trò chơi
key = ['board+game','bowling+hà+nội','sân+chơi+bóng+chuyền','sân+chơi+bóng+rổ','tham+quan+bảo+tàng' ,'quán+bar+hà+nội','sân+bóng+đá+ở+hà+nội','bể+bơi','cưỡi+ngựa+hà+nội','công+viên+nước','công+viên+hà+nội','quán+cafe+đẹp+ở+hà+nội','sân+cầu+lông+hà+nội','trung+tâm+bóng+bàn+hà+nội','trung+tâm+boxing+hà+nội','địa+điểm+dã+ngoại+gần+hà+nội','quán+cafe+mèo+ở+hà+nội','đạp+vịt','thuê+xe+đạp+hồ+tây','escape+room+hà+nội','sân+golf+ở+hà+nội','go+kart','karaoke+ở+hà+nội','sân+tennis','khu+du+lich+sinh+thái','làng+nghề+cổ+truyền','khu+vui+chơi+trẻ+em','leo+núi+trong+nhà','nhảy+dù+hà+nội','nhà+sách+hà+nội','quán+net+hà+nội','triển+lãm','pub+hà+nội','thủy+cung+hà+nội','taekwondo','trượt+băng','trung+tâm+thương+mại','thư+viện','tô+tượng','sky+walk','súng+sơn','play+station','rạp+phim','phòng+trà+hà+nội']
# Vòng for để crawl dữ liệu từng trò chơi
for j in key:
    search1 = 'https://www.google.com/search?tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=ALiCzsZ4uYPLiEK3lJFeLtym74vzticUgQ:1666455949886&q='
    link = search1 + j
    dictt = crawlGgchrome(link)
    data_df = Data_frame(dictt,j)
    append_df_to_excel(data_df,r'.\Data_gg.xlsx')
