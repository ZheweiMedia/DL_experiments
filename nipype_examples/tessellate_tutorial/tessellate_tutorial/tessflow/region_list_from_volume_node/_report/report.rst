Node: tessflow (region_list_from_volume_node (utility)
======================================================

 Hierarchy : tessellate_tutorial.tessflow.region_list_from_volume_node
 Exec ID : region_list_from_volume_node

Original Inputs
---------------

* function_str : def region_list_from_volume(in_file):
    import nibabel as nb
    import numpy as np
    segmentation = nb.load(in_file)
    segmentationdata = segmentation.get_data()
    rois = np.unique(segmentationdata)
    region_list = list(rois)
    region_list.sort()
    region_list.remove(0)
    region_list = list(map(int, region_list))
    return region_list

* ignore_exception : False
* in_file : /home/medialab/Zhewei/nipype_examples/tessellate_tutorial/tessellate_tutorial/tessflow/volconvert/aseg_out.nii

Execution Inputs
----------------

* function_str : def region_list_from_volume(in_file):
    import nibabel as nb
    import numpy as np
    segmentation = nb.load(in_file)
    segmentationdata = segmentation.get_data()
    rois = np.unique(segmentationdata)
    region_list = list(rois)
    region_list.sort()
    region_list.remove(0)
    region_list = list(map(int, region_list))
    return region_list

* ignore_exception : False
* in_file : /home/medialab/Zhewei/nipype_examples/tessellate_tutorial/tessellate_tutorial/tessflow/volconvert/aseg_out.nii

Execution Outputs
-----------------

* region_list : [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 24, 26, 28, 30, 31, 41, 42, 43, 44, 46, 47, 49, 50, 51, 52, 53, 54, 58, 60, 62, 63, 77, 85, 251, 252, 253, 254, 255]

Runtime info
------------

* duration : 6.02226
* hostname : media3

Environment
~~~~~~~~~~~

* DISPLAY : localhost:12.0
* FIX_VERTEX_AREA : 
* FMRI_ANALYSIS_DIR : /usr/local/freesurfer/fsfast
* FREESURFER_HOME : /usr/local/freesurfer
* FSFAST_HOME : /usr/local/freesurfer/fsfast
* FSF_OUTPUT_FORMAT : nii.gz
* FS_OVERRIDE : 0
* FUNCTIONALS_DIR : /usr/local/freesurfer/sessions
* HOME : /home/medialab
* LANG : en_US.UTF-8
* LESSCLOSE : /usr/bin/lesspipe %s %s
* LESSOPEN : | /usr/bin/lesspipe %s
* LOCAL_DIR : /usr/local/freesurfer/local
* LOGNAME : medialab
* LS_COLORS : rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
* MAIL : /var/mail/medialab
* MINC_BIN_DIR : /usr/local/freesurfer/mni/bin
* MINC_LIB_DIR : /usr/local/freesurfer/mni/lib
* MNI_DATAPATH : /usr/local/freesurfer/mni/data
* MNI_DIR : /usr/local/freesurfer/mni
* MNI_PERL5LIB : /usr/local/freesurfer/mni/lib/perl5/5.8.5
* OLDPWD : /home/medialab/Zhewei
* OS : Linux
* PATH : /usr/local/freesurfer/bin:/usr/local/freesurfer/fsfast/bin:/usr/local/freesurfer/tktools:/usr/local/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
* PERL5LIB : /usr/local/freesurfer/mni/lib/perl5/5.8.5
* PWD : /home/medialab/Zhewei/nipype_examples
* QT_QPA_PLATFORMTHEME : appmenu-qt5
* SHELL : /bin/bash
* SHLVL : 1
* SSH_CLIENT : 132.235.14.170 52186 22
* SSH_CONNECTION : 132.235.14.170 52186 132.235.15.103 22
* SSH_TTY : /dev/pts/10
* SUBJECTS_DIR : /usr/local/freesurfer/subjects
* TERM : xterm-256color
* USER : medialab
* XDG_RUNTIME_DIR : /run/user/1000
* XDG_SESSION_ID : 89
* _ : /usr/bin/python3.5

