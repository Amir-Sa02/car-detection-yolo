$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$app=$null;$pres=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $pres=$app.Presentations.Open($ppt,$false,$false,$false)
 $s=$pres.Slides.Item(6)
 $s.Shapes.Item('TextBox 4').Top=426
 $s.Shapes.Item('TextBox 4').Height=30
 $s.Shapes.Item('TextBox 4').TextFrame2.TextRange.Text=[char]0x200F+'• بازه صفر تا یک؛ مقدار بزرگ‌تر، انطباق بهتر'
 $s.Shapes.Item('TextBox 5').Top=466
 $s.Shapes.Item('TextBox 5').Height=52
 $s.Shapes.Item('TextBox 5').TextFrame2.TextRange.Text=[char]0x200F+'• پیش‌بینی درست: رده صحیح و هم‌پوشانی حداقل ۰٫۵  [۳، ۹]'
 $s.Shapes.Item('TextBox 7').Delete()
 $pres.Save()
}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
