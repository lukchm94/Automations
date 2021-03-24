from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
import tkinter as tk

def save_images():
    query = text_label.get()
    count_pics = int(pic_count.get())
    driver = webdriver.Firefox()
    driver.get('https://www.google.com')
    sleep(2)
    frame = driver.find_element_by_xpath('//iframe')
    driver.switch_to.frame(frame)
    driver.find_element_by_xpath("//div[@id='introAgreeButton']").click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath("//input[@name='q']").send_keys(query)
    driver.find_element_by_xpath("//input[@name='q']").send_keys(Keys.ENTER)
    sleep(2)
    driver.find_element_by_link_text('Grafika').click()
    elements = driver.find_elements_by_class_name('rg_i')
    print(len(elements))
    count = 0
    images_url = []
    for e in elements:
        e.click()
        sleep(1)
        element = driver.find_elements_by_class_name('v4dQwb')
        if count == 0:
            big_img = element[0].find_element_by_class_name('n3VNCb')
        else:
            big_img = element[1].find_element_by_class_name('n3VNCb')
        images_url.append(big_img.get_attribute("src"))
        reponse = requests.get(images_url[count])
        if reponse.status_code == 200:
            with open(f"{query}{count + 1}.jpg", "wb") as file:
                file.write(reponse.content)
        count += 1
        if count >= count_pics:
            break
    driver.quit()
    return images_url
    #except:
        #driver.quit()
        #print('There was an error closing FireFox window!\nTry running the app again')

#buiding GUI
window = tk.Tk()
tk.Label(window, text='').grid(row=0)
tk.Label(window, text='').grid(row=3)
tk.Label(window, text='Image to be saved').grid(row=1, pady=4)
tk.Label(window, text='Number of images').grid(row=2, pady=4)
text_label = tk.Entry(window, width=50)
pic_count = tk.Entry(window, width=50)
text_label.grid(row=1, column=2)
pic_count.grid(row=2, column=2)
tk.Button(window,text='Quit', width=10, command=window.quit).grid(row=4,column=2,sticky=tk.W,pady=4)
tk.Button(window, text='Run', width=10, command=save_images).grid(row=4,column=0,sticky=tk.W,pady=4)
window.geometry('600x180')
window.title('Save images from Google by Lukasz Chmielewski, 2021')
window.mainloop()
