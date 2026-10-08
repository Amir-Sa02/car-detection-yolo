$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$out='C:\Users\amir2\Desktop\cat-claude\ppt_final_check'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$app=$null; $pres=$null
try {
  $app=New-Object -ComObject PowerPoint.Application
  $pres=$app.Presentations.Open($ppt,$false,$true,$false)
  $pres.Slides.Item(20).Export((Join-Path $out 'slide-20.png'),'PNG',1600,900)
  $pres.Slides.Item(27).Export((Join-Path $out 'slide-27.png'),'PNG',1600,900)
}
finally {
  if($pres){$pres.Close()}
  if($app){$app.Quit()}
  [gc]::Collect(); [gc]::WaitForPendingFinalizers()
}
