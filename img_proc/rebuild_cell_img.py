import glob
import pandas as pd
import pathlib
import os

print('break')


def create_img_df(IMAGE_DIRECTORY):

    image_file_paths = glob.glob(f"{IMAGE_DIRECTORY}/*.png")
    img_df = pd.DataFrame({"Image_File_Path":image_file_paths})
    img_df["Image_File_Name"] = img_df["Image_File_Path"].apply(lambda x: pathlib.Path(x).stem)

    ## Example Image_File_Name : 000004_5-1
    ## Image_File_Number = 000004
    ## Img_X_Pos = 5
    ## Img_Y_Pos = 1
    img_df["Image_File_Name"] = img_df["Image_File_Name"].str.replace("-","_")
    img_df[["Image_File_Number","Img_X_Pos","Img_Y_Pos"]] = img_df["Image_File_Name"].str.split("_", n=3,expand=True)

    return img_df


IMAGE_DIRECTORY = r"C:\Users\griev\Downloads\10143"

img_df = create_img_df(IMAGE_DIRECTORY)


