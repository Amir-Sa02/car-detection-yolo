$ErrorActionPreference = 'Stop'
$ppt = 'D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$app = $null
$pres = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $pres = $app.Presentations.Open($ppt, $false, $false, $false)

    # اسلاید معیارها: حذف ترکیب نامأنوس راست‌به‌چپ و نگه‌داشتن ارجاع دقیق.
    $metrics = $pres.Slides.Item(20)
    $label = $metrics.Shapes.Item('TextBox 11')
    $label.Left = 742
    $label.Top = 278
    $label.Width = 168
    $label.TextFrame2.TextRange.Text = [char]0x200F + 'مرجع روابط این بخش: [۹]'
    $label.TextFrame2.TextRange.Font.Name = 'B Zar'
    $label.TextFrame2.TextRange.Font.NameComplexScript = 'B Zar'
    $label.TextFrame2.TextRange.Font.Size = 17
    $label.TextFrame2.TextRange.ParagraphFormat.Alignment = 3

    # اسلاید منابع: پنج ردیف در هر ستون و افزودن منابع ۱۳ و ۱۴.
    $refs = $pres.Slides.Item(27)
    $leftBars  = @('Rectangle 7','Rectangle 9','Rectangle 11','Rectangle 13')
    $leftTexts = @('Rectangle 8','Rectangle 10','Rectangle 12','Rectangle 14')
    $rightBars  = @('Rectangle 15','Rectangle 17','Rectangle 19','Rectangle 21')
    $rightTexts = @('Rectangle 16','Rectangle 18','Rectangle 20','Rectangle 22')
    $textTops = @(80.64, 156.96, 233.28, 309.60, 385.92)
    $barTops  = @(84.24, 160.56, 236.88, 313.20, 389.52)
    for ($i = 0; $i -lt 4; $i++) {
        $refs.Shapes.Item($leftBars[$i]).Top = $barTops[$i]
        $refs.Shapes.Item($leftBars[$i]).Height = 64.8
        $refs.Shapes.Item($leftTexts[$i]).Top = $textTops[$i]
        $refs.Shapes.Item($leftTexts[$i]).Height = 68.4
        $refs.Shapes.Item($rightBars[$i]).Top = $barTops[$i]
        $refs.Shapes.Item($rightBars[$i]).Height = 64.8
        $refs.Shapes.Item($rightTexts[$i]).Top = $textTops[$i]
        $refs.Shapes.Item($rightTexts[$i]).Height = 68.4
    }

    $newLeftBar = $refs.Shapes.Item('Rectangle 13').Duplicate().Item(1)
    $newLeftBar.Top = $barTops[4]
    $newLeftBar.Height = 64.8
    $newLeftText = $refs.Shapes.Item('Rectangle 14').Duplicate().Item(1)
    $newLeftText.Top = $textTops[4]
    $newLeftText.Height = 68.4
    $newLeftText.TextFrame2.TextRange.Text = '[13] Chaman et al., YOLOv11 and YOLOv12 for Real-Time Vehicle Detection, IJTDI, 2025.'
    $newLeftText.TextFrame2.TextRange.Font.Name = 'Times New Roman'
    $newLeftText.TextFrame2.TextRange.Font.NameComplexScript = 'Times New Roman'
    $newLeftText.TextFrame2.TextRange.Font.Size = 19

    $newRightBar = $refs.Shapes.Item('Rectangle 21').Duplicate().Item(1)
    $newRightBar.Top = $barTops[4]
    $newRightBar.Height = 64.8
    $newRightText = $refs.Shapes.Item('Rectangle 22').Duplicate().Item(1)
    $newRightText.Top = $textTops[4]
    $newRightText.Height = 68.4
    $newRightText.TextFrame2.TextRange.Text = '[14] Lin et al., Microsoft COCO: Common Objects in Context, ECCV, 2014.'
    $newRightText.TextFrame2.TextRange.Font.Name = 'Times New Roman'
    $newRightText.TextFrame2.TextRange.Font.NameComplexScript = 'Times New Roman'
    $newRightText.TextFrame2.TextRange.Font.Size = 19

    $pres.Save()
}
finally {
    if ($pres) { $pres.Close() }
    if ($app) { $app.Quit() }
    [gc]::Collect()
    [gc]::WaitForPendingFinalizers()
}
