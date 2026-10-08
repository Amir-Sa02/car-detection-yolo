$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$app=$null;$pres=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $pres=$app.Presentations.Open($ppt,$false,$false,$false)
 $s=$pres.Slides.Item(29)
 $leftBars=@('Rectangle 7','Rectangle 9','Rectangle 11','Rectangle 13','Rectangle 23','Rectangle 28')
 $leftTexts=@('Rectangle 8','Rectangle 10','Rectangle 12','Rectangle 14','Rectangle 24','Rectangle 29')
 $rightBars=@('Rectangle 15','Rectangle 17','Rectangle 19','Rectangle 21','Rectangle 25','Rectangle 30')
 $rightTexts=@('Rectangle 16','Rectangle 18','Rectangle 20','Rectangle 22','Rectangle 27','Rectangle 31')
 foreach($n in $leftBars){$s.Shapes.Item($n).Left=41.04}
 foreach($n in $leftTexts){$s.Shapes.Item($n).Left=54.72}
 foreach($n in $rightBars){$s.Shapes.Item($n).Left=495.36}
 foreach($n in $rightTexts){$s.Shapes.Item($n).Left=508.32}
 $s.Shapes.Item('Rectangle 8').TextFrame2.TextRange.Text='[1] Khosravian et al., IADD dataset, IET Image Processing, 2023.'
 $pres.Save()
}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
