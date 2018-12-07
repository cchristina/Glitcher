from PIL import Image, ImageFilter, ImageChops

import numpy as np

import random
from datetime import * 



from random import randint, shuffle
from os import path
import os as os






def pixelate_two(imgA, imgB, cellsize):

    # resizeFactor = (imgB.size[0]*imgA.size[1])/imgA.size[0]
    # imgA.resize(imgB.size)
    imgA.thumbnail((800, 800))
    imgB.thumbnail((800, 800))

    imgC = imgB
    for i in range(imgA.size[0]):
        for j in range (imgB.size[1]):
            box = (i*cellsize, j*cellsize, i*cellsize+cellsize, j*cellsize+cellsize)
            region = imgA.crop(box)
            # if i%3 != j%3 and random.randint(0,9)%3==0: #THIS IS MY RULE
            if random.randint(0,19)>3: #this is new version where all cells are are blended but at different rates
                region = Image.blend(imgA.crop(box), imgB.crop(box), random.uniform(0,1))
                # if i%3 == j%3:
                #     region.filter(ImageFilter.BLUR)
                # img3.paste(region, box)
                imgC.paste(region,box)


    # imgC.save(str(datetime.now())+".png")

    return imgC

def pixelate_two_alt(imgA, imgB, cellsize, savestring):
    imgA.thumbnail((800, 800))
    imgB.thumbnail((800, 800))
    imgC = imgA

    imgC.thumbnail((max(imgA.size[0], imgB.size[0]), max(imgA.size[1], imgB.size[1])))
    for i in range(int(imgA.size[0]/cellsize)):
        for j in range(int(imgB.size[1]/cellsize)):
            box = (i*cellsize, j*cellsize, i*cellsize+cellsize, j*cellsize+cellsize)
            region = imgA.crop(box)

            temp = random.uniform(0,1)
            comb_method = random.randint(0,20)

            if comb_method<3:
                region = ImageChops.difference(imgA.crop(box), imgB.crop(box))

            elif comb_method<7:
                region = Image.blend(imgA.crop(box), imgB.crop(box), temp)

            elif comb_method<10:

                region = ImageChops.subtract_modulo(imgA.crop(box), imgB.crop(box))
            
            elif comb_method<15: 
                region = imgB.crop(box)

            if random.randint(0,4)>-1:
                imgC.paste(region,box)    

        imgC.save(savestring)  
    return imgC


def populate_matrix(cellular_auto, matrix_x, matrix_y):
    for i in range(matrix_x):
        temp_cell = []

        for j in range(matrix_y):
            temp_cell.append(random.randint(0,1))
        
# 
        cellular_auto.append(temp_cell)


def pixelate_two_with_matrix(imgA, imgB, cellsize, frames, seed):


    if (imgA == imgB):
        imgB = imgB.rotate(180)

    cellular_auto = seed



    # populate_matrix(cellular_auto, int(imgA.size[0]/cellsize), int(imgB.size[1]/cellsize) )

 
    imgC = imgA.copy()

  
    imgC.thumbnail((max(imgA.size[0], imgB.size[0])/4, max(imgA.size[1], imgB.size[1])/4))
    imgB.thumbnail((max(imgA.size[0], imgB.size[0])/4, max(imgA.size[1], imgB.size[1])/4))

    for i in range(int(imgA.size[0]/cellsize)):
       

        start_row = random.randint(0,int(imgB.size[1]/cellsize))

        for j in range(int(imgB.size[1]/cellsize)):
            
            start_col = random.randint(0,int(imgB.size[0]/cellsize))

            box = (i*cellsize, j*cellsize, i*cellsize+cellsize, j*cellsize+cellsize)
            region = imgA.crop(box)
            

            temp = pow(random.uniform(-1,1),2)

            if cellular_auto[i][j]:
                # region = Image.blend(imgA.crop(box), imgB.crop(box), temp)
                # region =imgB.crop(box)
                # imgC.paste(region,box)      

                comb_method = random.randint(0,15)

                if comb_method%4==0:        
                    region = ImageChops.difference(imgA.crop(box), imgB.crop(box))

                elif comb_method%4==1:
                    region = Image.blend(imgA.crop(box), imgB.crop(box), temp)

                elif comb_method%4==2:

                    region = ImageChops.subtract_modulo(imgA.crop(box), imgB.crop(box))
                else:
                    region =imgB.crop(box)
                

                imgC.paste(region,box)  
    return imgC



def animate_two(imgA, imgB, cellsize, frames, savestring):

    cellular_auto = []
    populate_matrix(cellular_auto, int(imgA.size[0]/cellsize), int(imgB.size[1]/cellsize) )

    images = []
    for frame in range(frames):
        # pixelate_two_with_matrix(imgA, imgB, cellsize, frames, cellular_auto).save(str(frame)+".png")
        cellular_auto= np.roll(cellular_auto, 1, axis=0)
        cellular_auto = np.roll(cellular_auto, 2, axis=1)
        # images.append(Image.open(str(frame)+".png"))
        new_image = pixelate_two_with_matrix(imgA, imgB, cellsize, frames, cellular_auto)
        images.append(new_image)

    
    images[0].save(savestring,
               save_all=True,
               append_images=images[1:],
               duration=100,
               loop=0)




def shuffle_pic(fpath, savestring, recdepth):

       

    savetext = savestring
    with open(fpath, "rb") as pic, open(savetext , "wb") as newpic: 
        newpic.write(pic.read(1024))
        size = path.getsize(fpath)


        test = []

        
        for byte in pic:
            test.append(byte)

        test2=test[0:13]
        test3=test[13:-12]
        shuffle(test3)
        test4=test[-12:]
        test5 = test2+test3+test4

        for i, byte in enumerate(test5):
           
            if randint(0,4) >3:# and i!=0:
                try:
                    newpic.write(byte)
                except: 
                    newpic.write(test[i])

            else:
                newpic.write(test[i])
    try:
        img = Image.open(savetext)
        print("opened", savetext, " succesfully")
        print(type(img))
        img.save(savetext[:-4] + ".jpg")
        # print(savetext[:-4] + ".jpg", "********************")
        # print("resaving as something and removing original")
        # # os.remove(savetext)
        # print(savetext[:-4] + ".jpg")
        # retImg= Image.open(savetext[:-4] + ".jpg")

        # print("\n\n\n\n", type(retImg), "\n\n\n\n")

        return (savetext[:-4] + ".jpg")

    except:
        print("failure to open", savetext , "deleting file")
        # os.remove(savetext)
        if recdepth < 10:
            print(recdepth)
            shuffle_pic(fpath, savetext[:-4]+str(recdepth)+savetext[-4:], recdepth+1)
        else:
            print("sorry, please try again")
            retImg = Image.open(fpath)
            print("\n\n\n\n", type(retImg), "\n\n\n\n")
            return retImg
    


def doub_vert_stripes(img, stripes, savestring):
    new_img = img.resize((img.size[0]*2, img.size[1]))
    stripe_size = int(img.size[0]*2/stripes)

    for i in range(0,img.size[0],stripe_size):

        crop_box = (i,0, i+2*stripe_size, img.size[1])
        paste_box = (2*i, 0,  int((i*2)+2*stripe_size), img.size[1] )
        region = img.crop(crop_box)

        new_img.paste(region, paste_box)
    new_img.save(savestring+".png") 
    return new_img  



def doub_hor_stripes(img, stripes, savestring):
    new_img = img.resize((img.size[0], img.size[1]*2))
    stripe_size = int(img.size[1]*2/stripes)

    for i in range(0,img.size[1],stripe_size):

        crop_box = (0, i, img.size[0], i+2*stripe_size)
        paste_box = (0, 2*i, img.size[0], int((i*2)+2*stripe_size))
        region = img.crop(crop_box)

        new_img.paste(region, paste_box)
    new_img.save(savestring+".png")



    return new_img   


def doub_grid(img, stripes, savestring):
    newimg = doub_hor_stripes(doub_vert_stripes(img, stripes, savestring), stripes, savestring)
    newimg.thumbnail((800,800))
    return newimg

    # return doub_hor_stripes(doub_vert_stripes(img, stripes, savestring), stripes, savestring).thumbnail((800,800))


# if __name__ == '__main__':q
    
    # pixelate_two(img1, img2, 16)