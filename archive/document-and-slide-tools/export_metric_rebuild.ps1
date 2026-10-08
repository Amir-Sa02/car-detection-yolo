$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$out='C:\Users\amir2\Desktop\cat-claude\metric_rebuild'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$app=$null;$pres=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $pres=$app.Presentations.Open($ppt,$false,$true,$false)
 foreach($i in 5..9){$pres.Slides.Item($i).Export((Join-Path $out ('slide-{0:d2}.png' -f $i)),'PNG',1600,900)}
}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
