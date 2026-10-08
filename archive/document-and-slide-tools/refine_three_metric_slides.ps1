$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$logo='D:\projects\car-detection-yolo\thesis\ارائه\شکل‌ها\cover_image2.png'
$app=$null;$pres=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $pres=$app.Presentations.Open($ppt,$false,$false,$false)

 foreach($sn in 6..8){
   $s=$pres.Slides.Item($sn)
   if($s.Shapes.Item('Picture 24')){$s.Shapes.Item('Picture 24').Delete()}
   $s.Shapes.AddPicture($logo,$false,$true,33.84,15.12,42.48,49.68) | Out-Null
 }

 $s=$pres.Slides.Item(6)
 $s.Shapes.Item('TextBox 2').TextFrame2.TextRange.Text='IoU = |P ∩ G| / |P ∪ G|'
 $s.Shapes.Item('TextBox 5').TextFrame2.TextRange.Text=[char]0x200F+'• پذیرش پیش‌بینی: رده صحیح و عبور از آستانه هم‌پوشانی'
 $s.Shapes.Item('TextBox 7').TextFrame2.TextRange.Text=[char]0x200F+'• آستانه متداول هم‌پوشانی: ۰٫۵  [۳، ۹]'

 $s=$pres.Slides.Item(7)
 $s.Shapes.Item('TextBox 12').Top=408
 $s.Shapes.Item('TextBox 12').Height=72
 $s.Shapes.Item('TextBox 12').TextFrame2.TextRange.Text=[char]0x200F+'• آستانه بالاتر: دقت بیشتر، فراخوانی کمتر'+[char]10+[char]0x200F+'• آستانه پایین‌تر: فراخوانی بیشتر، دقت کمتر  [۱۲]'
 $s.Shapes.Item('TextBox 12').TextFrame2.TextRange.Font.Name='B Zar'
 $s.Shapes.Item('TextBox 12').TextFrame2.TextRange.Font.NameComplexScript='B Zar'
 $s.Shapes.Item('TextBox 12').TextFrame2.TextRange.Font.Size=21
 $s.Shapes.Item('TextBox 12').TextFrame2.TextRange.ParagraphFormat.Alignment=2
 $s.Shapes.Item('TextBox 13').Delete()

 $s=$pres.Slides.Item(8)
 $s.Shapes.Item('TextBox 7').TextFrame2.TextRange.Text=[char]0x200F+'میانگین دقت متوسط رده‌ها در آستانه هم‌پوشانی ۰٫۵  [۱۳]'
 $s.Shapes.Item('TextBox 7').TextFrame2.TextRange.Font.Name='B Zar'
 $s.Shapes.Item('TextBox 7').TextFrame2.TextRange.Font.NameComplexScript='B Zar'
 $s.Shapes.Item('TextBox 7').TextFrame2.TextRange.Font.Size=20
 $s.Shapes.Item('TextBox 7').TextFrame2.TextRange.ParagraphFormat.Alignment=3

 $pres.Save()
}
finally{if($pres){$pres.Close()};if($app){$app.Quit()};[gc]::Collect();[gc]::WaitForPendingFinalizers()}
