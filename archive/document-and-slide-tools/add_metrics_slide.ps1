$ErrorActionPreference = 'Stop'

$ppt = 'D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$backupDir = 'D:\projects\car-detection-yolo\thesis\ارائه\پشتیبان‌ها'
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backup = Join-Path $backupDir ("ارائه_دفاع_پیش_از_افزودن_معیارها_$stamp.pptx")
Copy-Item -LiteralPath $ppt -Destination $backup -Force

function OfficeRgb([int]$r, [int]$g, [int]$b) {
    return $r + 256 * $g + 65536 * $b
}

$navy = OfficeRgb 20 61 91
$blue = OfficeRgb 25 126 155
$green = OfficeRgb 31 139 76
$lightBlue = OfficeRgb 221 240 247
$lightGreen = OfficeRgb 225 241 232
$gray = OfficeRgb 87 100 111
$white = OfficeRgb 255 255 255

function Add-FaText($slide, [double]$x, [double]$y, [double]$w, [double]$h,
                    [string]$text, [double]$size, [int]$color, [bool]$bold=$false,
                    [int]$align=3) {
    $shape = $slide.Shapes.AddTextbox(1, $x, $y, $w, $h)
    $shape.TextFrame2.MarginLeft = 0
    $shape.TextFrame2.MarginRight = 0
    $shape.TextFrame2.MarginTop = 0
    $shape.TextFrame2.MarginBottom = 0
    $shape.TextFrame2.WordWrap = -1
    $shape.TextFrame2.TextRange.Text = [char]0x200F + $text
    $shape.TextFrame2.TextRange.Font.Name = 'B Zar'
    try { $shape.TextFrame2.TextRange.Font.NameComplexScript = 'B Zar' } catch {}
    $shape.TextFrame2.TextRange.Font.Size = $size
    $shape.TextFrame2.TextRange.Font.Bold = $(if($bold){-1}else{0})
    $shape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $color
    $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = $align
    try { $shape.TextFrame2.TextRange.ParagraphFormat.TextDirection = 2 } catch {}
    return $shape
}

function Add-EnText($slide, [double]$x, [double]$y, [double]$w, [double]$h,
                    [string]$text, [double]$size, [int]$color, [bool]$bold=$false,
                    [int]$align=2) {
    $shape = $slide.Shapes.AddTextbox(1, $x, $y, $w, $h)
    $shape.TextFrame2.MarginLeft = 0
    $shape.TextFrame2.MarginRight = 0
    $shape.TextFrame2.MarginTop = 0
    $shape.TextFrame2.MarginBottom = 0
    $shape.TextFrame2.WordWrap = -1
    $shape.TextFrame2.TextRange.Text = $text
    $shape.TextFrame2.TextRange.Font.Name = 'Times New Roman'
    $shape.TextFrame2.TextRange.Font.Size = $size
    $shape.TextFrame2.TextRange.Font.Bold = $(if($bold){-1}else{0})
    $shape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $color
    $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = $align
    return $shape
}

function Add-Line($slide, [double]$x1, [double]$y1, [double]$x2, [double]$y2,
                  [int]$color, [double]$weight=1.5) {
    $line = $slide.Shapes.AddLine($x1,$y1,$x2,$y2)
    $line.Line.ForeColor.RGB = $color
    $line.Line.Weight = $weight
    return $line
}

$app = $null
$pres = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $pres = $app.Presentations.Open($ppt, $false, $false, $false)

    # Duplicate a user-designed slide so the new slide inherits the exact logo,
    # title position, footer style, and lower blue gradient used in the first ten slides.
    $range = $pres.Slides.Item(4).Duplicate()
    $slide = $range.Item(1)
    $slide.MoveTo(20)

    foreach($name in @('Table 20','Rectangle 7')) {
        try { $slide.Shapes.Item($name).Delete() } catch {}
    }
    $slide.Shapes.Item('Rectangle 18').TextFrame2.TextRange.Text = [char]0x200F + 'معیارهای ارزیابی آشکارساز'
    $slide.Shapes.Item('Rectangle 18').TextFrame2.TextRange.Font.Name = 'B Zar'
    try { $slide.Shapes.Item('Rectangle 18').TextFrame2.TextRange.Font.NameComplexScript = 'B Zar' } catch {}
    $slide.Shapes.Item('Rectangle 6').TextFrame2.TextRange.Text = [char]0x200F + 'صفحه ۱۴ از ۲۱'

    # Central divider
    Add-Line $slide 480 86 480 402 $lightBlue 2.0 | Out-Null

    # Right column: IoU, Precision, Recall, F1
    Add-FaText $slide 505 78 410 30 'از هم‌پوشانی کادرها تا امتیاز F1' 23 $navy $true 3 | Out-Null
    $gt = $slide.Shapes.AddShape(1, 625, 118, 145, 76)
    $gt.Fill.ForeColor.RGB = $green; $gt.Fill.Transparency = 0.72
    $gt.Line.ForeColor.RGB = $green; $gt.Line.Weight = 2.25
    $pred = $slide.Shapes.AddShape(1, 700, 145, 145, 76)
    $pred.Fill.ForeColor.RGB = $blue; $pred.Fill.Transparency = 0.72
    $pred.Line.ForeColor.RGB = $blue; $pred.Line.Weight = 2.25
    Add-FaText $slide 600 101 180 20 'کادر واقعی' 17 $green $true 2 | Out-Null
    Add-FaText $slide 760 222 120 20 'کادر پیش‌بینی' 17 $blue $true 2 | Out-Null
    Add-EnText $slide 520 228 395 30 'IoU = |Bpred ∩ Bgt| / |Bpred ∪ Bgt|' 24 $navy $true 2 | Out-Null
    Add-FaText $slide 865 252 45 20 '[۹]' 16 $gray $false 2 | Out-Null
    Add-EnText $slide 515 276 400 27 'Precision = TP / (TP + FP)' 22 $navy $false 2 | Out-Null
    Add-EnText $slide 515 306 400 27 'Recall = TP / (TP + FN)' 22 $navy $false 2 | Out-Null
    Add-EnText $slide 515 336 400 29 'F1 = 2 × Precision × Recall / (Precision + Recall)' 20 $navy $false 2 | Out-Null
    Add-FaText $slide 522 373 390 25 'TP: درست  |  FP: تشخیص اضافه  |  FN: شیء یافت‌نشده' 17 $gray $false 2 | Out-Null

    # Left column: AP and mAP
    Add-FaText $slide 44 78 410 30 'از منحنی دقت–فراخوانی تا mAP' 23 $navy $true 3 | Out-Null
    # compact precision–recall sketch
    Add-Line $slide 70 205 70 118 $gray 1.5 | Out-Null
    Add-Line $slide 70 205 225 205 $gray 1.5 | Out-Null
    Add-Line $slide 70 130 105 134 $blue 3.0 | Out-Null
    Add-Line $slide 105 134 140 145 $blue 3.0 | Out-Null
    Add-Line $slide 140 145 170 163 $blue 3.0 | Out-Null
    Add-Line $slide 170 163 200 190 $blue 3.0 | Out-Null
    Add-Line $slide 200 190 222 202 $blue 3.0 | Out-Null
    Add-FaText $slide 32 108 65 20 'دقت' 16 $gray $false 2 | Out-Null
    Add-FaText $slide 174 207 70 20 'فراخوانی' 16 $gray $false 2 | Out-Null
    Add-EnText $slide 238 138 215 32 'APc = ∫₀¹ Pc(R) dR' 23 $navy $true 2 | Out-Null
    Add-FaText $slide 245 176 205 26 'مساحت زیر منحنی هر رده [۱۳]' 17 $gray $false 2 | Out-Null
    Add-EnText $slide 47 238 405 33 'mAP@0.5 = (1 / N) Σ APc@0.5' 23 $navy $true 2 | Out-Null
    Add-FaText $slide 55 271 390 27 'میانگین دقت متوسط رده‌ها در آستانه IoU برابر ۰٫۵  [۱۳]' 17 $gray $false 2 | Out-Null
    Add-EnText $slide 42 307 415 32 'mAP@0.5:0.95 = (1 / 10) Σ mAP@t' 22 $navy $true 2 | Out-Null
    Add-FaText $slide 50 340 400 28 'میانگین ده آستانه از ۰٫۵۰ تا ۰٫۹۵  [۱۳، ۱۴]' 17 $gray $false 2 | Out-Null
    Add-FaText $slide 48 375 405 27 'عدد پس از @ آستانه هم‌پوشانی است، نه آستانه اطمینان.' 18 $green $true 2 | Out-Null

    $pres.Save()
    Write-Output "backup=$backup"
    Write-Output "output=$ppt"
    Write-Output "slides=$($pres.Slides.Count)"
}
finally {
    if($pres){$pres.Close()}
    if($app){$app.Quit()}
    [gc]::Collect(); [gc]::WaitForPendingFinalizers()
}

