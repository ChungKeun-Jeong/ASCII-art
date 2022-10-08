import numpy as np
import cv2
import matplotlib.pylab as plt
from collections import defaultdict
from tkinter import *
from tkinter.filedialog import *
from tkinter import simpledialog
import tkinter.messagebox
import tkinter.ttk


img, fix_img = None, None  # 원본 이미지, 수정한 이미지
rows, cols = None, None  # 세로, 가로
text_img_count = 51  # 준비되어 있는 이미지 개수
size = None  # 한 칸에 들어갈 픽셀 개수 : size x size
img_color = ""  # Gray 또는 Color
img_lock = True  # 크기를 정한 후에 이미지 열 수 있음

text_imgs = []  # 텍스트 이미지들의 리스트 (gray)
color_text_imgs = [] # 텍스트 이미지들의 리스트 (color)


# 흑백 이미지 처리
def gray() :
    global img, fix_img, text_imgs
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    fix_img = np.zeros_like(gray_img)  
    mask = np.zeros_like(gray_img)

    cv2.normalize(gray_img, gray_img, 120, 240, cv2.NORM_MINMAX)

    # key : 평균 값 / value : 텍스트 이미지들
    diffValue_img = defaultdict(list)
    
    # 텍스트 이미지 중에서 같은 평균 값을 가진 것끼리 묶는다.
    for i in range (len(text_imgs)) :
        diffValue_img[int(np.mean(text_imgs[i]))].append(text_imgs[i])    
        
    #print(len(diffValue_img))
    
    
    for i in range(0, rows, size) :  # 세로 한 칸씩 증가
        for j in range(0, cols, size) :  # 가로 한 칸씩 증가
            
            # 새로 만든 픽셀의 평균 값 구하기 1 - 이게 더 빨리 실행됨
            #"""
            pixel_sum = 0
            for k in range(i, i + size) :  # 세로 한 픽셀씩 증가
                for l in range(j, j + size) :  # 가로 한 픽셀씩 증가
                    pixel_sum += gray_img[i, j]      
            pixel_avg = pixel_sum / (size * size)
            #"""
            
            # 새로 만든 픽셀의 평균 값 구하기 2
            """
            mask[i:i+size,j:j+size] = 255

            hist = cv2.calcHist([gray_img], [0], mask, [256], [0, 256])

            pixel_sum = 0
            for v, n in enumerate(hist) :
                pixel_sum += v * n
            
            mask[i:i+size,j:j+size] = 0 
            pixel_avg = int(pixel_sum / (size * size))
            """
            
            # diffValue_img 에서 pixel_avg와 같은 픽셀 값을 가진 이미지를 insert_img에 넣는다.
            insert_img = diffValue_img[pixel_avg]
            
            # 같은 픽셀 값을 가진 이미지가 없으면
            while len(insert_img) == 0 :
                pixel_avg += 1  # 픽셀 값을 증가시켜서 다시 찾는다.
                insert_img = diffValue_img[pixel_avg]
            
            # 같은 픽셀값을 가진 이미지가 여러 개 있을 수 있어서 그 중에서 랜덤으로 골라서 넣는다.
            fix_img[i:i+size, j:j+size] = insert_img[np.random.randint(len(insert_img))]
  
    cv2.imshow('img', img)     
    cv2.imshow('fix_img', fix_img)   
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        

# 컬러 이미지 처리
def color() :
    global img, fix_img, color_text_imgs
    
    fix_img = np.zeros_like(img)  
    b, g, r = cv2.split(img)
    
    # key : 평균 값 / value : 텍스트 이미지들
    b_diffValue_img = defaultdict(list)
    g_diffValue_img = defaultdict(list)
    r_diffValue_img = defaultdict(list)
    
    # 텍스트 이미지 중에서 같은 평균 값을 가진 것끼리 묶는다.
    for i in range (len(color_text_imgs)) :
        bb, gg, rr = cv2.split(color_text_imgs[i])
        b_diffValue_img[int(np.mean(bb))].append(color_text_imgs[i])
        g_diffValue_img[int(np.mean(gg))].append(color_text_imgs[i])
        r_diffValue_img[int(np.mean(rr))].append(color_text_imgs[i])
    
    
    for i in range (0, rows, size) :  # 세로 한 칸씩 증가
        for j in range (0, cols, size) :  # 가로 한 칸씩 증가
            
            # 새로 만든 픽셀의 평균 값 구하기 b, g, r 따로
            b_sum = 0
            g_sum = 0
            r_sum = 0
            for k in range(i, i + size) :  # 세로 한 픽셀씩 증가
                for l in range(j, j + size) :  # 가로 한 픽셀씩 증가
                    b_sum += b[i, j]
                    g_sum += g[i, j]
                    r_sum += r[i, j]   
            b_avg = b_sum / (size * size)
            g_avg = g_sum / (size * size)
            r_avg = r_sum / (size * size)
                     
        
            # b,g,r_diffValue_img 에서 b,g,r_avg와 같은 픽셀 값을 가진 이미지를 insert_img에 넣는다.  
            b_img = b_diffValue_img[b_avg]
            g_img = g_diffValue_img[g_avg]
            r_img = r_diffValue_img[r_avg]
            insert_img = b_img + g_img + r_img
                
            b_avg2 = b_avg
            g_avg2 = g_avg
            r_avg2 = r_avg
            
            # 같은 픽셀 값을 가진 이미지가 없으면
            while len(insert_img) == 0 :
                
                # 픽셀 값을 증가시켜서 다시 찾는다.
                b_avg2 += 1  
                g_avg2 += 1
                r_avg2 += 1 
                
                b_img = b_diffValue_img[b_avg2]
                g_img = g_diffValue_img[g_avg2]
                r_img = r_diffValue_img[r_avg2]
                
                insert_img = b_img + g_img + r_img
            
            # 같은 픽셀값을 가진 이미지가 여러 개 있을 수 있어서 그 중에서 랜덤으로 고른다.
            num = np.random.randint(len(insert_img))
            
            # 넣을 이미지를 b,g,r로 쪼갠다.
            bb, gg, rr = cv2.split(insert_img[num])
            
            # 넣을 이미지의 색을 바꾼다.
            for k in range(size) :
                for l in range(size) :
                    
                    # 숫자가 클수록 색이 선명한데 텍스트가 뭉게진다.
                    if rr[k,l] < 200 : rr[k,l] = r_avg
                    if gg[k,l] < 200 : gg[k,l] = g_avg
                    if bb[k,l] < 200 : bb[k,l] = b_avg

            # 다시 합쳐서 넣는다.
            fix_img[i:i+size, j:j+size] = cv2.merge((bb, gg, rr))

    cv2.imshow('img', img)     
    cv2.imshow('fix_img', fix_img)     
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        

# 이미지 열기
def imgOpen() :
    global img, rows, cols, text_imgs, color_text_imgs
    
    # gray 또는 color / 사이즈가 정해진 후에 이미지를 입력받을 수 있다.
    if img_lock == False :
        path = askopenfilename(parent = window, initialdir='img', 
            filetypes = (("JPG 파일", "*.jpg"), ("PNG 파일", "*.png"), ("모든 파일", "*.*")))
        print(path)
        img = cv2.imread(path)
        rows, cols = img.shape[:2]
        
        # 화면 사이즈 맞추기 - 잘리는 텍스트가 없게 하기 위해서 이미지의 크기를 조정한다.
        cut_rows = rows % size  
        cut_cols = cols % size

        rows = rows - cut_rows
        cols = cols - cut_cols

        img = cv2.resize(img, (cols, rows))
        
        text_imgs.clear()
        color_text_imgs.clear()
    
        if img_color == 'GRAY' :
            # 텍스트 이미지 받아오기
            for i in range(text_img_count) :
                text_img = cv2.imread('img/text_imgs/' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
                text_img = cv2.resize(text_img, (size, size))
                text_imgs.append(text_img)
            
            """
            # 텍스트 이미지 출력
            for i in range(text_img_count) :
                plt.subplot(int(text_img_count / 10 + 1), 10, i+1)
                plt.title(int(np.mean(text_imgs[i])))
                plt.axis('off')
                plt.subplots_adjust(hspace = 0.5, wspace = 0.7)
                plt.imshow(text_imgs[i], cmap='gray')
            """
            gray()
            
        elif img_color == 'COLOR' :
            # 텍스트 이미지 받아오기
            for i in range(text_img_count) :
                color_text_img = cv2.imread('img/text_imgs/' + str(i) + '.jpg')
                color_text_img = cv2.resize(color_text_img, (size, size))
                color_text_imgs.append(color_text_img)
            
            """
            # 텍스트 이미지 출력
            for i in range(text_img_count) :
                plt.subplot(int(text_img_count / 10 + 1), 10, i+1)
                plt.title(int(np.mean(color_text_imgs[i])))
                plt.axis('off')
                plt.subplots_adjust(hspace = 0.5, wspace = 0.7)
                plt.imshow(color_text_imgs[i], cmap='gray')
            """
            color()
        

# 이미지 저장
def imgSave() :
    global fix_img
    
    if img_lock == False :
        savePath = asksaveasfilename(parent = window, initialdir='/', 
            filetypes = (("JPG 파일", "*.jpg"), ("PNG 파일", "*.png"), ("모든 파일", "*.*")))
        savePath = savePath + ".jpg"
        cv2.imwrite(savePath, fix_img)
    

# 텍스트 크기 받아오기
def textSize() :
    global size, img_color, sizeBox, colorBox, img_lock
    
    try :
        img_lock = True
        size = int(sizeBox.get())
    except ValueError :
        tkinter.messagebox.showerror("텍스트 크기 오류","정수를 입력하세요")
    else :    
        if size >= 1 and size <= 25 :
            img_color = colorBox.get()
            img_lock = False
            tkinter.messagebox.showinfo("", "이미지를 열어주세요")
        else :
            tkinter.messagebox.showerror("텍스트 크기 오류","(1-25) 사이의 값을 입력하세요")
    
    
window = Tk()
window.title(" ")
window.geometry("220x350")
         
group1 = LabelFrame(window, text="", width = 120, height = 160, padx = 5, pady = 15)
group1.pack_propagate(0)
group1.place(x=50, y=50)

colorItem = ["GRAY", "COLOR"]
colorBox = tkinter.ttk.Combobox(group1, state = "readonly", values = colorItem)
colorBox.grid(column=0, row=0)
colorBox.pack()
colorBox.set(colorItem[0])

blankLabel = Label(group1, text="")
blankLabel.grid(column=1, row=0)
blankLabel.pack()

sizeLabel = Label(group1, text="텍스트 크기 (1-25)")
sizeLabel.grid(column=2, row=0)
sizeLabel.pack()

var = IntVar()
var.set(10)
sizeBox = Spinbox(group1, from_ = 1, to = 25, increment = 1, textvariable = var)
sizeBox.grid(column=3, row=0)
sizeBox.pack()

blankLabel = Label(group1, text="")
blankLabel.grid(column=4, row=0)
blankLabel.pack()

okButton = Button(group1, text="확인", relief = RIDGE, command = textSize)
okButton.pack(anchor = "se")    
    
group2 = LabelFrame(window, text="이미지", width = 120, height = 50, padx = 5, pady = 5)
group2.pack_propagate(0)
group2.place(x=50, y=250)

openButton = Button(group2, text="열기", relief = RIDGE, command = imgOpen)
openButton.pack(side='left')

saveButton = Button(group2, text="저장", relief = RIDGE, command = imgSave)
saveButton.pack(side='right')

window.mainloop()

