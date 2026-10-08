$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$app=$null;$pres=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $pres=$app.Presentations.Open($ppt,$false,$false,$false)
 $s=$pres.Slides.Item(29)

 $leftBars=@('Rectangle 7','Rectangle 9','Rectangle 11','Rectangle 13','Rectangle 23')
 $leftTexts=@('Rectangle 8','Rectangle 10','Rectangle 12','Rectangle 14','Rectangle 24')
 $rightBars=@('Rectangle 15','Rectangle 17','Rectangle 19','Rectangle 21','Rectangle 25')
 $rightTexts=@('Rectangle 16','Rectangle 18','Rectangle 20','Rectangle 22','Rectangle 27')
 $lb=$s.Shapes.Item('Rectangle 23').Duplicate().Item(1); $leftBars += $lb.Name
 $lt=$s.Shapes.Item('Rectangle 24').Duplicate().Item(1); $leftTexts += $lt.Name
 $rb=$s.Shapes.Item('Rectangle 25').Duplicate().Item(1); $rightBars += $rb.Name
 $rt=$s.Shapes.Item('Rectangle 27').Duplicate().Item(1); $rightTexts += $rt.Name

 $left=@(
 '[1] Khosravian et al., IADD: Multi-domain autonomous driving dataset, IET Image Processing, 2023.',
 '[2] Kaufman et al., Leakage in Data Mining, ACM TKDD, 2012.',
 '[3] Zou et al., Object Detection in 20 Years: A Survey, Proceedings of the IEEE, 2023.',
 '[9] Sapkota et al., YOLO Advances to Its Genesis, Artificial Intelligence Review, 2025.',
 '[10] Ultralytics, YOLO Documentation, 2024.',
 '[13] Chaman et al., YOLOv11 vs. YOLOv12 for Vehicle Detection, IJTDI, 2025.'
 )
 $right=@(
 '[11] Zhang et al., mixup: Beyond Empirical Risk Minimization, ICLR, 2018.',
 '[12] Chaman et al., Real-Time Vehicle Detection with YOLOv11, ETASR, 2025.',
 '[14] Lin et al., Microsoft COCO: Common Objects in Context, ECCV, 2014.',
 '[17] Monga and Evans, Perceptual Image Hashing Via Feature Points, IEEE TIP, 2006.',
 '[18] Loshchilov and Hutter, Decoupled Weight Decay Regularization, ICLR, 2019.',
 '[19] Loshchilov and Hutter, SGDR with Warm Restarts, ICLR, 2017.'
 )
 $tops=@(77.04,139.0,200.96,262.92,324.88,386.84)
 for($i=0;$i -lt 6;$i++){
   foreach($bn in @($leftBars[$i],$rightBars[$i])){$x=$s.Shapes.Item($bn);$x.Top=$tops[$i]+3.6;$x.Height=54}
   $a=$s.Shapes.Item($leftTexts[$i]);$a.Top=$tops[$i];$a.Height=58;$a.TextFrame2.TextRange.Text=$left[$i]
   $b=$s.Shapes.Item($rightTexts[$i]);$b.Top=$tops[$i];$b.Height=58;$b.TextFrame2.TextRange.Text=$right[$i]
   foreach($x in @($a,$b)){
     $x.TextFrame2.TextRange.Font.Name='Times New Roman'
     $x.TextFrame2.TextRange.Font.NameComplexScript='Times New Roman'
     $x.TextFrame2.TextRange.Font.Size=19
     $x.TextFrame2.TextRange.ParagraphFormat.Alignment=1
   }
 }
 $pres.Save()
}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
