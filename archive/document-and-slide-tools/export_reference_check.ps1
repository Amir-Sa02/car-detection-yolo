$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$out='C:\Users\amir2\Desktop\cat-claude\reference-final.png'
$app=$null;$pres=$null
try{$app=New-Object -ComObject PowerPoint.Application;$pres=$app.Presentations.Open($ppt,$false,$true,$false);$pres.Slides.Item(29).Export($out,'PNG',1600,900)}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
