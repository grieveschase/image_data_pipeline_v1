


import cv2, yaml
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import colorsys
from scipy.sparse import coo_matrix
import cv2
import numpy as np
import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import colorsys
from PIL import Image
import skimage
import scipy.misc
import tifffile

def plot_multi_images(img_list):

    fig, axes = plt.subplots(1, len(img_list), figsize=(8, 8))
    for ax, img in zip(axes,img_list):
        if len(img.shape)==3:
            ax.imshow(img)
        else:
            ax.imshow(img,cmap='gray')
    parent = axes[0]
    for i in range(1,len(axes)):
        axes[i].sharex(parent)
        axes[i].sharey(parent)
    plt.show()


def hsv_bound_segmented_mask(image_path:str, hsv_bounds:dict):
    """
        Segments an image based on specified HSV color bounds and returns a binary mask.
        Args:
            image_path (str): The file path to the input image.
            hsv_bounds (dict): A dictionary containing the lower and upper HSV bounds for segmentation.
                The dictionary should have the following structure:
                {
                    "Lower": {"Hue": int, "Saturation": int, "Value": int},
                    "Upper": {"Hue": int, "Saturation": int, "Value": int}
                }
        Returns:
            numpy.ndarray: A binary mask where the pixels within the specified HSV range are white (255) 
                            and all other pixels are black (0).
    """
    
    lwr_Hue = hsv_bounds["Lower"]["Hue"]
    lwr_Saturation = hsv_bounds["Lower"]["Saturation"]
    lwr_Value = hsv_bounds["Lower"]["Value"]
    lower_hsv_bound = np.array([lwr_Hue, lwr_Saturation, lwr_Value])
    
    upper_Hue = hsv_bounds["Upper"]["Hue"]
    upper_Saturation = hsv_bounds["Upper"]["Saturation"]
    upper_Value = hsv_bounds["Upper"]["Value"]
    upper_hsv_bound = np.array([upper_Hue, upper_Saturation, upper_Value])

    
    image = cv2.imread(image_path)
    #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a binary mask using the HSV range
    mask = cv2.inRange(hsv_image, lower_hsv_bound, upper_hsv_bound)
    return mask


def labeled_sparse_mask(mask: np.ndarray):
    """
        Converts a binary mask to a labeled sparse matrix and returns it as a sorted array.
        Parameters:
        mask (np.ndarray): A binary mask where the objects to be labeled are marked with 1s.
        Returns:
        np.ndarray: A 2D array where each row represents a labeled pixel in the format [label, x, y].
                    The array is sorted in ascending order by label, x, and y.
    """
    
    seg_labels_arr = skimage.measure.label(mask, connectivity=1)
    sparse_seg_img = coo_matrix(seg_labels_arr)
    sparse_seg_img_ar = np.concatenate( (sparse_seg_img.data.reshape(-1,1), sparse_seg_img.col.reshape(-1,1), sparse_seg_img.row.reshape(-1,1) ) , axis = 1)
    
    ## Sort sparse_seg_img_ar ascending label, x, y. 
    sorter_ar = np.lexsort((sparse_seg_img_ar[:,2], sparse_seg_img_ar[:,1],sparse_seg_img_ar[:,0]))
    sparse_seg_img_ar = sparse_seg_img_ar[sorter_ar]

    return sparse_seg_img_ar

if __name__ == "__main__":
    

    config_file_path = r"C:\projects\image_data_pipeline_v1\config\cell_img.yaml"
    with open(config_file_path, 'r') as stream:
            config = yaml.safe_load(stream)
    
    #image_path = r"C:\Users\griev\Downloads\10143\000275_16-14.png"
    #image_path = r"C:\Users\griev\Downloads\10143\000025_6-2.png"
    image_path = r"C:\Users\griev\Downloads\10143\000275_16-14.png"
    hsv_bounds = config["HSV_Bounds"]

    print('breakpoint')

    mask = hsv_bound_segmented_mask(image_path, hsv_bounds)
    seg_img_ar = labeled_sparse_mask(mask)
    ###
