$ErrorActionPreference = 'Stop'
$source = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه-دفاع.pptx'
$output = 'C:\Users\amir2\Desktop\cat-claude\ارائه-دفاع_تفکیک_نمودارها_بازبینی_۲.pptx'

function OleColor([int]$r, [int]$g, [int]$b) {
    return $r + ($g -shl 8) + ($b -shl 16)
}
function FaNumber([int]$number) {
    return $number.ToString().Replace('0','۰').Replace('1','۱').Replace('2','۲').Replace('3','۳').Replace('4','۴').Replace('5','۵').Replace('6','۶').Replace('7','۷').Replace('8','۸').Replace('9','۹')
}
function SetNotes($slide, [string]$message) {
    foreach ($shape in $slide.NotesPage.Shapes) {
        try {
            if ($shape.PlaceholderFormat.Type -eq 2) {
                $shape.TextFrame.TextRange.Text = $message
                break
            }
        } catch {}
    }
}

$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open($source, $false, $false, $false)
    $sizeSlide = $deck.Slides.Item(18)
    $weatherSlide = $sizeSlide.Duplicate().Item(1)

    # Keep only the object-size chart on slide 18; leave the right side for the user.
    $sizeSlide.Shapes.Item(5).TextFrame.TextRange.Text = 'توزیع اندازه اشیا در سه بخش'
    $sizeChart = $sizeSlide.Shapes.Item(6)
    $sizeChart.Left = 0.52 * 72
    $sizeChart.Top = 1.56 * 72
    $sizeChart.Width = 6.18 * 72
    $sizeChart.Height = 4.64 * 72
    $sizeCaption = $sizeSlide.Shapes.Item(7)
    $sizeCaption.Left = 1.91 * 72
    $sizeCaption.Top = 6.14 * 72
    $sizeSlide.Shapes.Item(9).Delete()
    $sizeSlide.Shapes.Item(8).Delete()
    $sizeSlide.Shapes.Item(3).Delete()
    SetNotes $sizeSlide 'این شکل، سهم سه گروه اندازه اشیا را در بخش‌های آموزش، اعتبارسنجی و آزمون نشان می‌دهد. محور عمودی درصد نمونه‌های برچسب‌خورده در همان بخش است و مقیاس آن خطی است. کوچک یعنی مساحت کادر کمتر از یک درصد تصویر؛ متوسط از یک تا شش درصد و بزرگ از شش درصد به بالا. نزدیکی درصدها در سه بخش، یکی از شواهد هم‌ترازی داده‌هاست.'

    # The new slide 19 uses the original environmental chart on the left.
    $weatherSlide.Shapes.Item(5).TextFrame.TextRange.Text = 'توزیع شرایط محیطی در سه بخش'
    $weatherSlide.Shapes.Item(9).Delete()
    $weatherSlide.Shapes.Item(7).Delete()
    $weatherSlide.Shapes.Item(6).Delete()
    $weatherSlide.Shapes.Item(6).Top = 6.05 * 72

    $panel = $weatherSlide.Shapes.AddShape(5, 7.10 * 72, 1.55 * 72, 5.71 * 72, 3.10 * 72)
    $panel.Fill.ForeColor.RGB = OleColor 241 243 245
    $panel.Line.ForeColor.RGB = OleColor 155 172 184
    $panel.Line.Weight = 1.0
    $panel.Name = 'پس‌زمینه کد محاسبه سهم کل'

    $header = $weatherSlide.Shapes.AddShape(1, 7.10 * 72, 1.55 * 72, 5.71 * 72, 0.56 * 72)
    $header.Fill.ForeColor.RGB = OleColor 64 64 64
    $header.Line.Visible = 0
    $header.Name = 'سربرگ کد محاسبه سهم کل'
    $header.TextFrame.MarginLeft = 0.15 * 72
    $header.TextFrame.MarginRight = 0.10 * 72
    $header.TextFrame.MarginTop = 0.02 * 72
    $header.TextFrame.MarginBottom = 0
    $header.TextFrame.TextRange.Text = 'compute_v5_validity.py'
    $header.TextFrame.TextRange.Font.Name = 'Times New Roman'
    $header.TextFrame.TextRange.Font.Size = 19
    $header.TextFrame.TextRange.Font.Color.RGB = OleColor 255 255 255
    $header.TextFrame.TextRange.ParagraphFormat.Alignment = 1

    $code = $weatherSlide.Shapes.AddTextbox(1, 7.24 * 72, 2.22 * 72, 5.40 * 72, 2.22 * 72)
    $code.Name = 'کد تجمیع شرایط محیطی'
    $code.TextFrame.MarginLeft = 0
    $code.TextFrame.MarginRight = 0
    $code.TextFrame.MarginTop = 0
    $code.TextFrame.MarginBottom = 0
    $code.TextFrame.WordWrap = 0
    $code.TextFrame.TextRange.Text = @(
        'S = {s: analyze(s) for s in SPLITS}',
        'counts = Counter()',
        'for s in SPLITS:',
        '    counts.update(S[s]["cond"])',
        'total = sum(counts.values())',
        'for c, n in counts.items():',
        '    print(c, round(100*n/total, 1))'
    ) -join "`r"
    $code.TextFrame.TextRange.Font.Name = 'Times New Roman'
    $code.TextFrame.TextRange.Font.Size = 18
    $code.TextFrame.TextRange.Font.Color.RGB = OleColor 30 52 68
    $code.TextFrame.TextRange.ParagraphFormat.Alignment = 1

    $arrow = $weatherSlide.Shapes.AddLine(9.92 * 72, 4.72 * 72, 9.92 * 72, 5.12 * 72)
    $arrow.Line.ForeColor.RGB = OleColor 31 78 121
    $arrow.Line.Weight = 2.25
    $arrow.Line.EndArrowheadStyle = 3
    $arrow.Name = 'فلش از کد به سهم کل'

    $shareLabel = $weatherSlide.Shapes.AddTextbox(1, 7.10 * 72, 5.10 * 72, 5.71 * 72, 0.36 * 72)
    $shareLabel.Name = 'عنوان سهم کل تصاویر'
    $shareLabel.TextFrame.MarginLeft = 0
    $shareLabel.TextFrame.MarginRight = 0
    $shareLabel.TextFrame.MarginTop = 0
    $shareLabel.TextFrame.MarginBottom = 0
    $shareLabel.TextFrame.TextRange.Text = 'سهم از کل تصاویر'
    $shareLabel.TextFrame.TextRange.Font.Name = 'B Zar'
    $shareLabel.TextFrame.TextRange.Font.Size = 20
    $shareLabel.TextFrame.TextRange.Font.Bold = -1
    $shareLabel.TextFrame.TextRange.Font.Color.RGB = OleColor 31 78 121
    $shareLabel.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    $bullets = $weatherSlide.Shapes.AddTextbox(1, 7.10 * 72, 5.47 * 72, 5.71 * 72, 1.35 * 72)
    $bullets.Name = 'سهم کل تصاویر'
    $bullets.TextFrame.MarginLeft = 0
    $bullets.TextFrame.MarginRight = 0
    $bullets.TextFrame.MarginTop = 0
    $bullets.TextFrame.MarginBottom = 0
    $bullets.TextFrame.TextRange.Text = @(
        '• روز: ۸۱٫۰٪',
        '• شب و باران: هرکدام ۸٫۸٪',
        '• ابری: ۱٫۴٪'
    ) -join "`r"
    $bullets.TextFrame.TextRange.Font.Name = 'B Zar'
    $bullets.TextFrame.TextRange.Font.Size = 22
    $bullets.TextFrame.TextRange.Font.Color.RGB = OleColor 24 53 78
    $bullets.TextFrame.TextRange.ParagraphFormat.Alignment = 3
    $bullets.TextFrame.TextRange.ParagraphFormat.SpaceAfter = 4

    SetNotes $weatherSlide 'نمودار سمت چپ، سهم شرایط محیطی را جداگانه در آموزش، اعتبارسنجی و آزمون نشان می‌دهد. محور عمودی درصد تصاویر همان بخش است و برای دیده‌شدن سهم کم کد A، لگاریتمی رسم شده است. کد داخل اسلاید از تابع analyze در فایل compute_v5_validity.py استفاده می‌کند؛ خط‌های تجمیع و چاپ درصد کل، برای این اسلاید نوشته شده‌اند و عیناً در فایل اصلی نیستند. این کد شمار تصاویر هر وضعیت را در سه بخش جمع می‌زند و بر ۳۷٬۱۴۲ تصویر تقسیم می‌کند. حرف D روز، N شب، R باران و A وضعیت ابری است؛ نام‌گذاری وضعیت A در پروژه بر پایه بازبینی تصاویر انجام شده است.'

    # Keep every footer consistent with the new 31-slide count.
    for ($i = 1; $i -le $deck.Slides.Count; $i++) {
        foreach ($shape in $deck.Slides.Item($i).Shapes) {
            try {
                $existing = $shape.TextFrame.TextRange.Text
                if ($existing -match '^صفحه\s+[۰-۹]+\s+از\s+[۰-۹]+$') {
                    $shape.TextFrame.TextRange.Text = 'صفحه ' + (FaNumber $i) + ' از ۳۱'
                    $shape.TextFrame.TextRange.Font.Name = 'B Zar'
                    $shape.TextFrame.TextRange.Font.Size = 16
                }
            } catch {}
        }
    }

    $deck.SaveAs($output, 24)
    Write-Output $output
} finally {
    if ($deck) { $deck.Close() }
    $app.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
