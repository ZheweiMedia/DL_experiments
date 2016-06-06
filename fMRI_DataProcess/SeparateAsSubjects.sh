#!/bin/bash


# cat the result of MatLab belongs to the same subject to a file 

# for different groups change the line of cat


cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
IIDarray=(  243875 316041 \
381524 256635 223330 \
257487 332881 393007 \
258448 279226 301767 346233 395573 \
278818 300245 323843 361436 414381 \
283879 305240 326318 358424 417987 \
311921 332859 354814 379008 307555 \
307553 334236 334235 350115 350113 \
381403 246032 265869 306576 372938 \
248233 265533 290438 336704 385092 \
255318 274437 301834 393850 319132 \
376489 361973 388039 343905 361116 \
372823 398098 261316 261319 225058 \
242252 305412 286425 241661 257106 \
339828 264416 281497 308391 347747 \
320432 337377 352722 367848 332584 \
347725 364273 390419 252603 \
224635 280337 352437 402257 255135 \
226625 243008 207341 222174 \
274112 351336 399918 247852 207991 \
223649 281032 353098 404042 290305 \
321928 362541 311906 338289 353986 \
378012 319541 346592 358601 386888 \
260905 277297 301221 341866 398232 \
300529 316049 343137 370437 \
215435 242177 310476 \
379344 217608 196434 247662 \
316979 382683 240043 208974 223353 \
275532 354598 226190 243115 259900 \
297463 367820 249144 264701 284291 \
329780 387206 281149 299318 324478 \
357940 339436 354860 367326 394943 \
401558 264531 228463 245122 305210 \
374515 283305 247533 267918 319578 \
382880 289331 307991 337186 306672 \
333641 376324 316519 337220 354697 \
383934 235258 298266 317378 344443 \
377061 300841 316406 347906 375664 \
361367 317397 336187 266223 \
247983 302589 372302 240902 \
257011 316276 385078 256753 297616 \
259332 281083 341127 394175 279103 \
297702 374201 358935 412933 278493 \
305261 374165 374144 407059 279181 \
301103 319553 358798 414279 282297 \
303032 323821 361486 323163 \
349748 374318 392890 293995 \
341976 )

XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    subj=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $X`
    case "${IIDarray[@]}" in  *$iid*)
        echo $iid
        cat /home/medialab/Zhewei/data/EMCI_Results/EM_Result${iid}.txt >> /home/medialab/Zhewei/data/EMCI_Results/EM_Subj${subj}
    esac
done
