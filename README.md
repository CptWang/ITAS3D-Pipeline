# ITAS3D-Pipeline

Please run all the notebooks in Liulab's lab server as all the filepaths are linked to the server drives.

### Step 0: Fuse the raw biopsy

Use ImageJ Bigstitcher or automated script (on desktop of the BigStitcher account on lab server), result in 2x-downsampled fused images (e.g., *xxx-f0.h5* and *xxx-f0.xml*)

### Step 1: Prepare data for GAN image translation

1. From H5 file to 10+ blocks per biopsy (each contains jpeg stacks, nuclei and cyto channel, top and bottom) using notebook [whbio01_a_overlap_dod_enface_preprocess_h5.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio01_dod_enface_preprocess/whbio01_overlap2halfs/whbio01_a_overlap_dod_enface_preprocess_h5.ipynb)
   - Make changes accordingly at 3 places in the second cell (biopsy-specific names and filepaths)
   - Can run multiple scripts for different biopsies at the same time
   - The variable "*hist_clip*" (defining *hi_val* with histogram) start with a default value (*0.9992* for cytoplasm channel, *0.999* for nuclei channel), and can be adjusted as needed based on visual inspection of result or directly hard code *hi_val* and *background* intensity
   - Note that by default the cyto background is not clipped, but nulcei background is clipped at 9% of hi_val. This may be adjusted if needed.
2. Duplicate ch1 as "ch0" for p2p inference
   - Just for the sake of a consistent code structure in GAN training and inference
   - To do this, either manually copy and rename the folder as '*ch0*' or use the last block of code at the end of [whbio01_a_overlap_dod_enface_preprocess_h5.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio01_dod_enface_preprocess/whbio01_overlap2halfs/whbio01_a_overlap_dod_enface_preprocess_h5.ipynb)

### Step 2: Image translation from H&E to CK8

1. Pix2pix + vid2vid inference on Local Linux Workstation

   - [How to connect to the Local Linux Workstation](https://docs.google.com/document/d/1HL2Pus3_wkEAvFM3Jb0C1aqjoZk-gzBv1n1fGs-X0l0/edit)

   - Pix2pix inference acts on only first 5 frames for each seq/block, while vid2vid on the entire stack based on the first 2 levels inferenced by pix2pix

   - Execute the .sh file for pix2pix + vid2vid batch job in terminal

     - Modify the xxx*.sh* file locally for the current case. There are 9 places to be modified in total: 7 places for the # of the patient, and 2 places for today's date. Don’t forget to rename the file name as well. Example *.sh* file for a previously processed case is located at: */home/user/ITAS3D/img_translation/scripts/test_p2p_s140_o_localBatch_7222.sh*
     - Execute the xxx*.sh* file by running the following command (modify the path to file accordingly)

     `bash -i /home/user/ITAS3D/img_translation/scripts/test_p2p_s140_o_localBatch_7222.sh`

     - Add a flag “gpu_ids” to use another GPU on the Linux Workstation if needed (modify the related code in the *.sh* file, example below)

     ```bash
     python ~/ITAS3D/seq_translation/test.py --name seq630_g1_fine_t2 --dataroot /run/user/1000/gvfs/smb-share:server=172.25.29.118,share=e/WX/WX_test_dod/whobio_sets/s140_o --checkpoints_dir ~/Documents/rwang98/GAN_vid2vid_Hyak/checkpoints --dataset_mode w1_test --output_nc 3 --loadSize 1024 --n_scales_spatial 1 --n_downsample_G 2 --use_real_img --results_dir /run/user/1000/gvfs/smb-share:server=172.25.29.118,share=e/WX/WX_test_dod/whobio_sets/vid2vid_results/s140_o --how_many 100000 -- gpu_ids 1 > ~/ITAS3D/seq_translation/log/log_test_s140_o_7222.txt
     ```

2. Remember to delete or archive (with compression) the datasets and results to release storage space if not needed

### Step 3: After image translation inference, preparation for segmentation

1. Assemble the individual 2D levels into 3D biopsy tif files using notebook [whbio03_1_assemble_overlap2halfs.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio03_testlatest2fullseq/whbio03_1_assemble_overlap2halfs.ipynb)
   - Change the variable "*biopsy_group*" before running
   - Assemble top and bottom parts (with middle frames blended) for each block
   - Make folders for each biopsy and move blocks into the folder
   - New added function: stitch CK8 blocks into biopsy (if this doesn't work, alternatively run the next step)
2. [This step has been incorporated into step 8 now, should be skippable] Stitch CK8 blocks into biopsy by running Fiji macro "*stitch_biopsies.ijm*" in Fiji
   - The script is located in "*C:\Users\Administrator\Documents\fiji-win64\Fiji.app\macros*"
   - Remember to change the biopsy group name each time 
   - Run macro after the change of name has been saved
3. For cytoplasm channel, assemble each biopsy (can only be run after step 8, because the *full_seq* folder has to exist) using notebook [whbio04_1_ovlpassemble_cyto_nuc.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio04_assemble_cyto_nuc/whbio04_1_ovlpassemble_cyto_nuc.ipynb)
   - Skip "for individual processing" blocks
   - Change the variables "*biopsy_group*" and "*biopsy_list*" before running

### Step 4: Gland segmentation using traditional CV

1. Run segmentation code with default parameter settings or adjust as the processing proceeds using notebook [seg_1029_s140a.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio05_segmentation/seg_1029_s140a.ipynb)
   - Create a copy of segmentation jupyter notebook for each biopsy so we can tweak the parameters later. This provided notebook can be treated as an example
   - Change the variable "*block_name*" before running
   - The RAM on Weisi's lab server account only allows processing 1 biopsy at a time, so remember to terminate the jupyter kernel session when a biopsy is finished before starting the next one
   - Check saved tif files in each step using Fiji/ImageJ, final epithelium and lumen can be visualized with 2 colors in one stack using the merge color function in Fiji
2. Run active contour to get biopsy-region segmentation using notebook [whbio06_get_biopsy_outline.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio06_get_biopsy_outline.ipynb)
   - Can be done after **Step 3**
   - Remember to change the variable “*biopsy_group_list*” to indicate the biopsy groups to process
3. Save segmentation of lumen, epithelium, gland and biopsy region into *.npz* file (binary format, easier for data sharing) using notebook [whbio07_arrange_npz_send_data.ipynb](https://github.com/CptWang/ITAS3D-Pipeline/blob/main/whbio_workflow/whbio07_arrange_npz_send_data.ipynb)
   - Remember to change the variable “*save_folder*” for the path to save the *.npz* files, as well as “*biopsy_group_name_list*”