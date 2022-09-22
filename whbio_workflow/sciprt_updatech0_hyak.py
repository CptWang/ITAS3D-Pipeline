import numpy as np
import os
import glob
from PIL import Image
import argparse


############ INPUT PARAMETERS ############

parser = argparse.ArgumentParser()
parser.add_argument("--group_name", type=str, help="e.g. s001_o")
args = parser.parse_args()

group_name = args.group_name


############ PROCESS ############

# group_name = 's001_o' #change

seq_folder_list = glob.glob('/gscratch/liulab/weisix/GAN_vid2vid_Hyak/datasets/'+group_name+'/test/ch0/*') 
#('W:\\WX\\WX_test_dod\\whobio_sets\\'+group_name+'\\test\\ch0\\*')
# print(len(seq_folder_list))
# print(seq_folder_list[0])
# ch0_updt_folder = '/gscratch/liulab/weisix/GAN_vid2vid_Hyak/datasets/'+group_name+'/test/ch0' 
#'W:\\WX\\WX_test_dod\\whobio_sets\\'+group_name+'\\test\\ch0_updt'
# os.rename(ch0_folder, ch0_folder+'_s1') #same as ch1
# if not os.path.exists(ch0_updt_folder):
#     os.makedirs(ch0_updt_folder)

p2p_ch0_folder = '/gscratch/liulab/weisix/GAN_HE-CK8/results/'+group_name+'/frame_seq_630_t1/test_latest/images/'
 #'W:\\WX\\WX_test_dod\\whobio_sets\\pix2pix_results\\'+group_name+'\\frame_seq_630_t1\\test_latest\\images\\'

for seq_dir in seq_folder_list:
    # print('-----', seq_dir)
    frame_list = sorted(glob.glob(os.path.join(seq_dir, '*.jpg')))
    # print(len(frame_list))
    
#     print(frame_list[:10])
    for v2vframe in frame_list[:5]: #only substitute first 5 frames for each seq
        frame_name = os.path.basename(v2vframe)[:-4]
    #         print(frame_name)
#         print('v2vframe', v2vframe)
        p2pframe_name = frame_name + '_fake_B.png'
        p2pframe_dir = os.path.join(p2p_ch0_folder, p2pframe_name)
#         print('p2pframe_dir', p2pframe_dir)

        #delete v2vframe
        os.remove(v2vframe)

        #copy p2pframe in jpg
        p2p_img = Image.open(p2pframe_dir)
        p2p_img.save(v2vframe)