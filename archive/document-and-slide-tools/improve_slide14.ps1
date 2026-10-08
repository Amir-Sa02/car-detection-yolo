$ErrorActionPreference = 'Stop'
$ppt = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه_دفاع_نهایی_جلسه.pptx'
$backupDir = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پشتیبان‌ها'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$backup = Join-Path $backupDir ('ارائه_دفاع_نهایی_جلسه_قبل_از_اصلاح_اسلاید۱۴_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.pptx')
Copy-Item -LiteralPath $ppt -Destination $backup

function Color-RGB([int]$red, [int]$green, [int]$blue) {
    return ($red + 256 * $green + 65536 * $blue)
}

function Add-PersianText($slide, [string]$name, [string]$content, [double]$x, [double]$y, [double]$w, [double]$h, [double]$size, [bool]$bold, [int]$color) {
    $shape = $slide.Shapes.AddTextbox(1, $x, $y, $w, $h)
    $shape.Name = $name
    $shape.TextFrame.MarginLeft = 0
    $shape.TextFrame.MarginRight = 0
    $shape.TextFrame.MarginTop = 0
    $shape.TextFrame.MarginBottom = 0
    $shape.TextFrame.WordWrap = -1
    $range = $shape.TextFrame.TextRange
    $range.Text = $content
    $range.Font.Name = 'B Zar'
    $range.Font.Size = $size
    $range.Font.Bold = $(if ($bold) { -1 } else { 0 })
    $range.Font.Color.RGB = $color
    $range.ParagraphFormat.Alignment = 3
    return $shape
}

$navy = Color-RGB 27 59 85
$ink = Color-RGB 25 31 38
$green = Color-RGB 34 111 79
$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $deck = $app.Presentations.Open($ppt, $false, $false, $false)
    $slide = $deck.Slides.Item(14)

    $slide.Shapes.Item('TextBox 28').Delete()
    # Preserve the two existing evidence images, logo, title, and page footer.
    [void](Add-PersianText $slide 'غربال اولیه' 'غربال اولیه' 455 98 445 34 22 $true $navy)
    [void](Add-PersianText $slide 'آمار غربال' '۱۳ ویدیو با امتیاز زیر ۰٫۶۳' 455 135 445 33 20 $false $ink)

    [void](Add-PersianText $slide 'نتیجه بازبینی' 'بازبینی برچسب‌ها' 455 186 445 34 22 $true $navy)
    [void](Add-PersianText $slide 'ویدیو معیوب یک' '۰٫۰۰۷: برچسب نادرست' 455 225 445 32 20 $false $ink)
    [void](Add-PersianText $slide 'ویدیو معیوب دو' '۰٫۴۵۱: برچسب ناقص' 455 260 445 32 20 $false $ink)
    [void](Add-PersianText $slide 'ویدیوهای حفظ شده' '۱۱ ویدیوی دشوار: حفظ' 455 295 445 32 20 $false $ink)

    [void](Add-PersianText $slide 'ویدیوهای تکراری' 'بررسی تکرار' 455 348 445 34 22 $true $navy)
    [void](Add-PersianText $slide 'تعداد تکراری' '۳ ویدیوی تکراری: حذف' 455 385 445 33 20 $false $ink)
    [void](Add-PersianText $slide 'حاصل پاکسازی' 'مجموع حذف‌شده: ۵ ویدیو' 455 443 445 36 22 $true $green)

    [void](Add-PersianText $slide 'برچسب شاهد تصویری' 'نمونهٔ برچسب نادرست در ویدیوی ۴۲۶' 41 476 375 28 17 $false $navy)

    $deck.Save()
    $slide.Export('C:\Users\amir2\Desktop\cat-claude\slide14_after.png', 'PNG', 1600, 900)
    Write-Output "backup=$backup"
    Write-Output 'updated_slide=14'
}
finally {
    if ($deck) { $deck.Close() }
    if ($app) { $app.Quit() }
}
