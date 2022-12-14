from selenium.webdriver.common.by import By

class Post:
    def __init__(self,post_h3,post_div):
        self.ph3 = post_h3
        self.ptxt = post_h3.text
        self.pdiv = post_div
        self.plink = self.get_link()
        self.cmt_count = self.check_cmt_count()

    def get_link(self):
        a = self.pdiv.find_elements(By.TAG_NAME,'a')
        links = [i.get_attribute('href') for i in a]
        return links[-1]

    def check_cmt_count(self):
        count = self.pdiv.find_elements(By.TAG_NAME,'span')
        if 'k' in count[5].text:
            if count[5].text[:2].isdigit():
                if float(count[5].text[:2])>0:
                    return True
        elif count[5].text.isdigit():
            if float(count[5].text)>100:
                return True
        else:
            return False

class Comment:
    def __init__(self,cdiv):
        self.ctext = cdiv.text
        self.cdiv = cdiv
        self.cont = self.extr_cont()

    def __str__(self):
        return self.cont

    def extr_cont(self):
        text = self.cdiv.find_elements(By.TAG_NAME,'p')
        str = ''.join([i.text for i in text])
        if len(str) > 0:
            return str

    def upvote_count(self):
        txt = self.ctext
        cl = txt.split('\n')
        if 'k' in cl[5]:
            return True
        elif cl[5].isdigit():
            if int(cl[5])>400:
                return True
        else:
            return False
        #return cl[5]
        #txt = self.ctext
        #cl = txt.split('\n')
        #if len(cl)>=5:
            #return cl[4]