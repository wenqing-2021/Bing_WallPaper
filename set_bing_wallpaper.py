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

def download_images(url):  
    """  
    下载指定网页上的所有图片并保存到本地文件夹  
  
    :param url: 目标网页的URL
    """ 

    # 发送HTTP请求  
    response = requests.get(url)  
    response.raise_for_status()  # 如果请求失败，抛出异常  
  
    # 使用BeautifulSoup解析页面  
    soup = BeautifulSoup(response.text, 'html.parser')  

    today = datetime.date.today()
    data_str = today.today().strftime("%Y-%m-%d")
    # data_str = "2024-07-05"
    print(f"Today is: {data_str}")
  
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
        # print(f"{data_str}, type is {type(data_str)}")
        if data_str == previous_str:
            img_url = img.get('href')
            break

    # 下载图片  
    img_name = os.path.join(SAVE_PATH, "bing_wallpaper.jpg")
    # print(f"url is {img_url}")
    urlretrieve(img_url, img_name)  

    print(f"Downloaded: {img_name}")

    image_path = os.path.join(SAVE_PATH, img_name)
    
    return image_path


if __name__ == "__main__":
    url = "https://bing.wdbyte.com/zh-cn/"  # 替换为你要爬取的网页的URL
    image_path = download_images(url)
    set_windows_desktop_wallpaper(image_path)
