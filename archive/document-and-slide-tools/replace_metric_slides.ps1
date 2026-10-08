$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$fig='C:\Users\amir2\Desktop\cat-claude\figure_1_3\image5.png'
$backupDir='D:\projects\car-detection-yolo\thesis\ارائه\پشتیبان‌ها'
$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$backup=Join-Path $backupDir ("ارائه_دفاع_پیش_از_بازطراحی_معیارها_$stamp.pptx")
Copy-Item -LiteralPath $ppt -Destination $backup -Force

$navy=0x4F3817   # RGB(23,56,79) in Office BGR
$blue=0xA37E19   # RGB(25,126,163)
$green=0x539621  # RGB(33,150,83)
$gray=0x665B55   # RGB(85,91,102)

function Add-FaText($slide,$text,$left,$top,$width,$height,$size=22,$color=$navy,$bold=$false,$align=3){
  $sh=$slide.Shapes.AddTextbox(1,$left,$top,$width,$height)
  $sh.TextFrame2.MarginLeft=0; $sh.TextFrame2.MarginRight=0
  $sh.TextFrame2.MarginTop=0; $sh.TextFrame2.MarginBottom=0
  $sh.TextFrame2.WordWrap=-1
  $sh.TextFrame2.AutoSize=0
  $sh.TextFrame2.TextRange.Text=[char]0x200F+$text
  $sh.TextFrame2.TextRange.Font.Name='B Zar'
  $sh.TextFrame2.TextRange.Font.NameComplexScript='B Zar'
  $sh.TextFrame2.TextRange.Font.Size=$size
  $sh.TextFrame2.TextRange.Font.Bold=($(if($bold){-1}else{0}))
  $sh.TextFrame2.TextRange.Font.Fill.ForeColor.RGB=$color
  $sh.TextFrame2.TextRange.ParagraphFormat.Alignment=$align
  return $sh
}
function Add-EnText($slide,$text,$left,$top,$width,$height,$size=25,$color=$navy,$bold=$false){
  $sh=$slide.Shapes.AddTextbox(1,$left,$top,$width,$height)
  $sh.TextFrame2.MarginLeft=0; $sh.TextFrame2.MarginRight=0
  $sh.TextFrame2.MarginTop=0; $sh.TextFrame2.MarginBottom=0
  $sh.TextFrame2.WordWrap=-1
  $sh.TextFrame2.AutoSize=0
  $sh.TextFrame2.TextRange.Text=$text
  $sh.TextFrame2.TextRange.Font.Name='Times New Roman'
  $sh.TextFrame2.TextRange.Font.NameComplexScript='Times New Roman'
  $sh.TextFrame2.TextRange.Font.Size=$size
  $sh.TextFrame2.TextRange.Font.Bold=($(if($bold){-1}else{0}))
  $sh.TextFrame2.TextRange.Font.Fill.ForeColor.RGB=$color
  $sh.TextFrame2.TextRange.ParagraphFormat.Alignment=2
  return $sh
}
function Set-Title($slide,$text){
  $title=$slide.Shapes.Item('Rectangle 25')
  $title.TextFrame2.TextRange.Text=[char]0x200F+$text
  $title.TextFrame2.TextRange.Font.Name='B Zar'
  $title.TextFrame2.TextRange.Font.NameComplexScript='B Zar'
}
function Prepare-Slide($slide,$title,$footer){
  if($slide.Shapes.Item('Table 16')){$slide.Shapes.Item('Table 16').Delete()}
  Set-Title $slide $title
  $slide.Shapes.Item('Rectangle 6').TextFrame2.TextRange.Text=[char]0x200F+$footer
}

$app=$null; $pres=$null
try{
  $app=New-Object -ComObject PowerPoint.Application
  $pres=$app.Presentations.Open($ppt,$false,$false,$false)

  # حذف اسلاید فشرده قبلی.
  for($i=$pres.Slides.Count;$i -ge 1;$i--){
    $hit=$false
    foreach($sh in $pres.Slides.Item($i).Shapes){
      if($sh.HasTextFrame -and $sh.TextFrame.HasText){
        if($sh.TextFrame.TextRange.Text -like '*معیارهای ارزیابی آشکارساز*'){$hit=$true;break}
      }
    }
    if($hit){$pres.Slides.Item($i).Delete()}
  }

  # سه نسخه از قالب اسلاید ۵ و انتقال به جایگاه ۶ تا ۸.
  $s1=$pres.Slides.Item(5).Duplicate().Item(1); $s1.MoveTo(6)
  $s2=$pres.Slides.Item(5).Duplicate().Item(1); $s2.MoveTo(7)
  $s3=$pres.Slides.Item(5).Duplicate().Item(1); $s3.MoveTo(8)

  # ۱) IoU
  Prepare-Slide $s1 'نسبت هم‌پوشانی کادرها' 'صفحه ۳ از ۲۱'
  $pic=$s1.Shapes.AddPicture($fig,$false,$true,54,92,852,281)
  Add-EnText $s1 'IoU = |B_pred ∩ B_gt| / |B_pred ∪ B_gt|' 62 382 520 36 25 $navy $true | Out-Null
  Add-FaText $s1 'نسبت مساحت اشتراک دو کادر به مساحت اجتماع آن‌ها  [۹]' 596 382 322 34 20 $gray $false 3 | Out-Null
  Add-FaText $s1 '• بازه مقدار: صفر تا یک؛ مقدار بزرگ‌تر یعنی انطباق بهتر' 470 431 450 34 21 $navy $false 3 | Out-Null
  Add-FaText $s1 '• پذیرش پیش‌بینی: رده درست و عبور IoU از آستانه تعیین‌شده' 470 470 450 34 21 $navy $false 3 | Out-Null
  Add-FaText $s1 '• آستانه متداول در گزارش mAP@0.5 برابر ۰٫۵  [۳، ۹]' 470 509 450 34 21 $navy $false 3 | Out-Null

  # ۲) Precision و Recall
  Prepare-Slide $s2 'دقت و فراخوانی' 'صفحه ۴ از ۲۱'
  $divider=$s2.Shapes.AddLine(480,104,480,438)
  $divider.Line.ForeColor.RGB=$blue; $divider.Line.Transparency=0.35; $divider.Line.Weight=1.5
  Add-FaText $s2 'دقت' 520 110 390 38 27 $blue $true 3 | Out-Null
  Add-FaText $s2 'سهم پیش‌بینی‌های مثبت که واقعاً درست‌اند' 520 154 390 34 21 $navy $false 3 | Out-Null
  Add-EnText $s2 'Precision = TP / (TP + FP)' 515 211 395 44 28 $navy $true | Out-Null
  Add-FaText $s2 'کاهش تشخیص‌های اضافه، مقدار دقت را افزایش می‌دهد  [۹]' 520 272 390 54 20 $gray $false 3 | Out-Null
  Add-FaText $s2 'فراخوانی' 50 110 390 38 27 $green $true 3 | Out-Null
  Add-FaText $s2 'سهم اشیای واقعی که مدل آن‌ها را پیدا کرده است' 50 154 390 34 21 $navy $false 3 | Out-Null
  Add-EnText $s2 'Recall = TP / (TP + FN)' 50 211 390 44 28 $navy $true | Out-Null
  Add-FaText $s2 'کاهش اشیای ازدست‌رفته، مقدار فراخوانی را افزایش می‌دهد  [۹]' 50 272 390 54 20 $gray $false 3 | Out-Null
  Add-FaText $s2 'رابطه معکوس با تغییر آستانه اطمینان' 170 365 620 38 25 $navy $true 2 | Out-Null
  Add-FaText $s2 'آستانه بالاتر: دقت بیشتر و فراخوانی کمتر  •  آستانه پایین‌تر: فراخوانی بیشتر و دقت کمتر  [۱۲]' 90 414 780 42 21 $navy $false 2 | Out-Null
  Add-FaText $s2 'TP: تشخیص درست    FP: تشخیص اضافه    FN: شیء یافت‌نشده' 155 487 650 34 19 $gray $false 2 | Out-Null

  # ۳) AP و mAP
  Prepare-Slide $s3 'دقت متوسط و میانگین دقت متوسط' 'صفحه ۵ از ۲۱'
  Add-FaText $s3 'دقت متوسط برای هر رده' 575 105 340 34 24 $blue $true 3 | Out-Null
  Add-EnText $s3 'AP(c) = ∫₀¹ P(c,R) dR' 520 153 390 42 27 $navy $true | Out-Null
  Add-FaText $s3 'مساحت زیر منحنی دقت–فراخوانی همان رده  [۱۳]' 530 203 380 34 20 $gray $false 3 | Out-Null
  Add-FaText $s3 'mAP@0.5' 570 273 340 36 25 $green $true 3 | Out-Null
  Add-EnText $s3 'mAP@0.5 = (1 / N) Σ AP(c)@0.5' 500 318 410 48 25 $navy $true | Out-Null
  Add-FaText $s3 'میانگین AP رده‌ها با آستانه IoU برابر ۰٫۵  [۱۳]' 500 374 410 48 20 $gray $false 3 | Out-Null
  Add-FaText $s3 'mAP@0.5:0.95' 55 105 370 36 25 $green $true 3 | Out-Null
  Add-EnText $s3 'mAP@0.5:0.95 = (1 / 10) Σ mAP@t' 38 153 420 52 25 $navy $true | Out-Null
  Add-FaText $s3 'میانگین نتیجه در ده آستانه از ۰٫۵۰ تا ۰٫۹۵ با گام ۰٫۰۵  [۱۳، ۱۴]' 45 214 405 70 20 $gray $false 3 | Out-Null
  Add-FaText $s3 'سنجش سخت‌گیرانه‌تر برای کیفیت مکان‌یابی کادرها' 45 306 405 36 21 $navy $false 3 | Out-Null
  Add-FaText $s3 'عدد پس از @ آستانه هم‌پوشانی است، نه آستانه اطمینان' 118 444 725 42 24 $green $true 2 | Out-Null

  $pres.Save()
}
finally{
  if($pres){$pres.Close()}
  if($app){$app.Quit()}
  [gc]::Collect();[gc]::WaitForPendingFinalizers()
}
Write-Output "BACKUP=$backup"
