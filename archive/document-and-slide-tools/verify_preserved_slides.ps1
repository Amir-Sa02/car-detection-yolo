$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$out='C:\Users\amir2\Desktop\cat-claude\preserved_check'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$app=$null;$pres=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $pres=$app.Presentations.Open($ppt,$false,$true,$false)
 foreach($i in 1..5){$pres.Slides.Item($i).Export((Join-Path $out ('old-{0:d2}.png' -f $i)),'PNG',1600,900)}
 foreach($i in 6..10){$pres.Slides.Item($i+3).Export((Join-Path $out ('old-{0:d2}.png' -f $i)),'PNG',1600,900)}
}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
