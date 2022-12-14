from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from classes import Post,Comment
from PIL import Image
from makevid import make_fin_video
import time,random,pyttsx3,os,datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#words()

def log(str):
    current_time = datetime.datetime.now()
    h,m,s = current_time.hour,current_time.minute,current_time.second
    print(f'[{h}:{m}:{s}] {str} ...')

def extr_links(str):
    if "https://" in str:
        start=str.index('https://')
        end=str.index('.com')
        nstr = str.replace(str[start:end+4],'')
        return nstr
    else:
        return str

def txt_to_speech(str,filename):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) 
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    nstr = extr_links(str)
    engine.save_to_file(nstr,f'static/ss_audioes/{filename}.mp3')
    engine.runAndWait()

#'planets'

def turn_dark_mode(driver):
    btn = driver.find_element(By.CLASS_NAME,"header-user-dropdown")
    driver.implicitly_wait(30)
    btn.click()
    try:
        dark = driver.find_element(By.CLASS_NAME,"icon-night")
        dark.click()
        btn.click()
    except:
        settings = driver.find_element(By.XPATH,"//span[text()='Settings']")
        settings.click()
        dark = driver.find_element(By.XPATH,"//span[text()='Dark Mode']")
        dark.click()
        btn.click()
    
def make_driver():
    chrome_options = Options()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument("--headless")
    #chrome_options.binary_location="chrome.exe"
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    os.system('bash func.sh')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    #driver = webdriver.Chrome('static/chromedriver.exe',options=chrome_options)
    log("Starting the web driver")
    return driver

def scrap(url):
    #selenium headless
    global driver
    driver = make_driver()
    driver.get(url)
    turn_dark_mode(driver)
    driver.set_window_size(540,960)

    divs = driver.find_elements(By.CLASS_NAME,'Post')
    h3 = driver.find_elements(By.TAG_NAME,'h3')
    postlist = [Post(i,j) for i in h3 for j in divs]
    log("Storing posts in posts list")
    return postlist

def choose_post(query):
    url1 = f'https://www.reddit.com/r/AskReddit/search/?q={query}&restrict_sr=1&sr_nsfw=0&sort=comments'
    url2 = f'https://www.reddit.com/r/NoStupidQuestions/search/?q={query}&restrict_sr=1&sr_nsfw=0&sort=comments'
    plist = [i for i in scrap(url1) if i.cmt_count and len(i.ptxt)<160]
    if len(plist)<1:
            plist = [i for i in scrap(url2) if i.cmt_count and len(i.ptxt)<160]
    post = random.sample(plist,1)
    print(len(plist))
    log(f"Choosing Random Post")
    return post[0]

def check(cmt):
    if cmt.cont is not None and len(cmt.cont)>30:
        return True
    else:
        return False

def get_posts_cont(hed_div,driver):
    heading = driver.find_element(By.TAG_NAME,'h1')
    paras = hed_div.find_elements(By.TAG_NAME,'p')
    if paras:
        return heading.text + ''.join([i.text for i in paras])
    else:
        return heading.text

def mine_comments(query):
    #try:
    ran_post = choose_post(query)
    driver.get(ran_post.plink)
    comments = driver.find_elements(By.CLASS_NAME,'Comment')
    hed_div = driver.find_element(By.CLASS_NAME,'Post')
    #print(type(hed_div))
    fintext = get_posts_cont(hed_div,driver)
    fin_list = [Comment(i) for i in comments if check(Comment(i))]
    fl = [i for i in fin_list if i.upvote_count()]
    log("Scrapping comments")
    return fl,fintext,hed_div

def charcheck(cmt_lst,thres):
    t = thres//5
    l = [len(i.cont) for i in cmt_lst]
    temp = {l.index(i):abs(i-t) for i in l}
    sv = sorted([temp[i] for i in temp])
    ndict = {i:j for j in sv for i in temp if j==temp[i]}
    fl = [cmt_lst[i] for i in ndict]
    if len(fl)>12:
        return random.sample(fl,6)
    else:
        return fl[:6]#previously it was 5

def take_screenshot(query):
    ftuple = mine_comments(query)
    cmt_lst = ftuple[0]
    post_cont = ftuple[1]
    post_div = ftuple[2]
    post_div.screenshot('static/ss_imgs/a-post.png')
    log("Saving Post screenshot")
    txt_to_speech(post_cont,'a-post')
    log("Converting Post text to audio")
    thres = 970 - len(post_cont)
    finlist = charcheck(cmt_lst,thres)
    
    for i,j in enumerate(finlist):
        div = j.cdiv
        div.screenshot(f'static/ss_imgs/cmt{i}.png')
        #print(j.upvote_count())
        log("Saving screenshot of the comment ")
        cont = j.cont
        txt_to_speech(cont,f'cmt{i}')
        log("Converting the text of comment to audio")

def convert_img(path):
    img = Image.open(path)
    for i in range(img.width):
        for j in range(img.height):
            p = img.getpixel((i,j))
            newp = (p[0],p[1],p[2],233)
            img.putpixel((i,j),newp)
    img.save(path)

def final(query):
    start = time.time()
    log("Starting process")
    take_screenshot(query)
    for i in os.listdir('static/ss_imgs'):
        convert_img(f'static/ss_imgs/{i}')
    make_fin_video(query)
    end = time.time()
    fintime = end - start
    finstr = f"Completed in {round(fintime/60,2)} minutes"
    log(finstr)
    
'''if __name__ == '__main__':
    query = input('Enter the query : ')
    take_screenshot(query)'''
