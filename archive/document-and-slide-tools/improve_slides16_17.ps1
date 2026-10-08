$ErrorActionPreference = 'Stop'
$ppt = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه_دفاع_نهایی_جلسه.pptx'
$backupDir = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پشتیبان‌ها'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$backup = Join-Path $backupDir ('ارائه_دفاع_نهایی_جلسه_قبل_از_اسلایدهای۱۶و۱۷_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.pptx')
Copy-Item -LiteralPath $ppt -Destination $backup

function Rgb([int]$r,[int]$g,[int]$b) { return $r + 256*$g + 65536*$b }
function Add-Label($slide,[string]$name,[string]$value,[double]$x,[double]$y,[double]$w,[double]$h,[double]$size,[bool]$bold,[int]$color,[bool]$ltr=$false) {
    $shape=$slide.Shapes.AddTextbox(1,$x,$y,$w,$h)
    $shape.Name=$name
    $shape.TextFrame.MarginLeft=0
    $shape.TextFrame.MarginRight=0
    $shape.TextFrame.MarginTop=0
    $shape.TextFrame.MarginBottom=0
    $shape.TextFrame.WordWrap=0
    $text=$shape.TextFrame.TextRange
    $text.Text=$value
    $text.Font.Name=$(if($ltr){'Times New Roman'}else{'B Zar'})
    $text.Font.Size=$size
    $text.Font.Bold=$(if($bold){-1}else{0})
    $text.Font.Color.RGB=$color
    $text.ParagraphFormat.Alignment=$(if($ltr){1}else{3})
    return $shape
}

$navy=Rgb 27 59 85
$ink=Rgb 35 43 50
$green=Rgb 34 111 79
$app=$null; $deck=$null
try {
    $app=New-Object -ComObject PowerPoint.Application
    $deck=$app.Presentations.Open($ppt,$false,$false,$false)
    $s16=$deck.Slides.Item(16)
    $s17=$deck.Slides.Item(17)

    # This page keeps both original charts in full.
    [void](Add-Label $s16 'منطق نگه‌داشت رده‌ها' 'رده‌های کم‌نمونه: نگه‌داشت فریم‌ها' 37 469 435 30 18 $false $green)
    [void](Add-Label $s16 'کنترل اندازه پس از ساخت' 'اندازهٔ اشیا: کنترل پس از ساخت' 488 469 436 30 18 $false $navy)

    # Replace only the generic prose beside the weather chart.
    $s17.Shapes.Item('Rectangle 8').Delete()
    [void](Add-Label $s17 'تیتر استخراج وضعیت' 'استخراج وضعیت از نام ویدیو' 565 120 356 32 20 $true $navy)
    [void](Add-Label $s17 'کد استخراج وضعیت' 'by_cond[r.split("_")[-1]].append(r)' 565 159 356 31 18 $false $ink $true)

    [void](Add-Label $s17 'تیتر تخصیص' 'تخصیص بر پایهٔ کسری سهم' 565 216 356 32 20 $true $navy)
    [void](Add-Label $s17 'توضیح رده‌های نادر' 'رده‌های کم‌نمونه' 565 253 356 30 19 $false $ink)
    [void](Add-Label $s17 'کد کسری رده‌های نادر' 'rt[s] - sr[s]' 565 284 356 27 18 $false $ink $true)
    [void](Add-Label $s17 'توضیح سایر ویدیوها' 'سایر ویدیوها' 565 319 356 30 19 $false $ink)
    [void](Add-Label $s17 'کد کسری فریم‌ها' 'ft[s] - sf[s]' 565 350 356 27 18 $false $ink $true)

    [void](Add-Label $s17 'تیتر نتیجه آزمون' 'سهم شرایط دشوار در آزمون' 565 410 356 32 20 $true $navy)
    [void](Add-Label $s17 'آمار شرایط دشوار' 'شب ۱۵٫۳٪   باران ۹٫۷٪' 565 448 356 31 19 $false $green)

    $deck.Save()
    $s16.Export('C:\Users\amir2\Desktop\cat-claude\slide16_new.png','PNG',1600,900)
    $s17.Export('C:\Users\amir2\Desktop\cat-claude\slide17_new.png','PNG',1600,900)
    Write-Output "backup=$backup"
    Write-Output 'updated_slides=16,17'
}
finally {
    if($deck){$deck.Close()}
    if($app){$app.Quit()}
}
