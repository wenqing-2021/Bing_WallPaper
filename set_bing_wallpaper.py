import os  
import requests  
from bs4 import BeautifulSoup  
from urllib.parse import urljoin  
from urllib.request import urlretrieve  
import datetime
import re
import ctypes
import ctypes.wintypes as wintypes
import os
import argparse

# set the specific path
# SAVE_PATH = "F:\Pictures\WallPaper"

# get the current file path
SAVE_PATH = os.path.dirname(os.path.abspath(__file__))

def set_windows_desktop_wallpaper(fpath: str) -> bool:
    """
    set Windows Desktop Wallpaper.

    BOOL WINAPI SystemParametersInfo(
      _In_    UINT  uiAction,
      _In_    UINT  uiParam,
      _Inout_ PVOID pvParam,
      _In_    UINT  fWinIni
    )

    :param fpath: path to background image file.
    :return:
    """
    fpath = os.path.abspath(fpath)
    SPI = ctypes.windll.User32.SystemParametersInfoW
    SPI_SETDESKWALLPAPER = wintypes.UINT(0x0014)
    SPIF_UPDATEINIFILE = wintypes.UINT(0x0001)

    return SPI(SPI_SETDESKWALLPAPER, 0, fpath, SPIF_UPDATEINIFILE)

def download_images(url, save_name:str = None, date_str:str = None):  
    """  
    下载指定网页上的所有图片并保存到本地文件夹  
  
    :param url: 目标网页的URL
    """ 

    # 发送HTTP请求  
    response = requests.get(url)  
    response.raise_for_status()  # 如果请求失败，抛出异常  
  
    # 使用BeautifulSoup解析页面  
    soup = BeautifulSoup(response.text, 'html.parser')  
  
    # 查找所有的图片链接
    img_links = soup.find_all('a', href=re.compile("https://cn.bing.com/"))
    if len(img_links) < 1:
        print("No image found.")
        return
    img_url = None

    # 下载并保存图片  
    for img in img_links:
        previous_str = re.sub(r"\s+", "", str(img.previous))
        # print(f"{previous_str}, type is {type(previous_str)}")
        # print(f"{date_str}, type is {type(date_str)}")
        if date_str == previous_str:
            img_url = img.get('href')
            break

    # 下载图片  
    img_name = os.path.join(SAVE_PATH, save_name)
    # print(f"url is {img_url}")
    if img_url is None:
        print("No image found.")
        return
    urlretrieve(img_url, img_name)  

    print(f"Downloaded: {img_name}")

    image_path = os.path.join(SAVE_PATH, img_name)
    
    return image_path


if __name__ == "__main__":
    today = datetime.date.today()
    today_str = today.today().strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser()
    parser.add_argument("--desire_date", "-d", type=str, default=today_str, help="The date image you desire. The format is YYYY-MM-DD")
    args = parser.parse_args()

    # check the date format
    desire_date = args.desire_date
    if not re.match(r"\d{4}-\d{2}-\d{2}", desire_date):
        print("The date format is not correct. Please input the date in format like YYYY-MM-DD")
        exit()
    
    # check the date is not beyound today
    if desire_date > today_str:
        print("The date is beyound today. Please input the date before today.")
        exit()
    if desire_date == today_str:
        save_name = "bing_wallpaper" + ".jpg"
    else:
        save_name = desire_date + ".jpg"

    save_name = re.sub(r"-", "_", save_name)
    url = "https://bing.wdbyte.com/zh-cn/"  # 替换为你要爬取的网页的URL
    print(f"Desired Date is: {desire_date}")

    image_path = download_images(url, save_name, desire_date)
    set_windows_desktop_wallpaper(image_path)
