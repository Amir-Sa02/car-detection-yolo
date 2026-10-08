$ErrorActionPreference = 'Stop'
$source = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه-دفاع.pptx'
$output = 'C:\Users\amir2\Desktop\cat-claude\ارائه-دفاع_کد_اندازه_بازبینی_۲.pptx'
function OleColor([int]$r,[int]$g,[int]$b) { $r + ($g -shl 8) + ($b -shl 16) }
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open($source, $false, $false, $false)
    $slide = $deck.Slides.Item(18)

    $panel = $slide.Shapes.AddShape(5, 7.10 * 72, 1.55 * 72, 5.67 * 72, 3.10 * 72)
    $panel.Name = 'پس‌زمینه کد اندازه اشیا'
    $panel.Fill.ForeColor.RGB = OleColor 241 243 245
    $panel.Line.ForeColor.RGB = OleColor 155 172 184
    $panel.Line.Weight = 1

    $header = $slide.Shapes.AddShape(1, 7.10 * 72, 1.55 * 72, 5.67 * 72, 0.56 * 72)
    $header.Name = 'سربرگ کد اندازه اشیا'
    $header.Fill.ForeColor.RGB = OleColor 64 64 64
    $header.Line.Visible = 0
    $header.TextFrame.MarginLeft = 0.15 * 72
    $header.TextFrame.MarginRight = 0.08 * 72
    $header.TextFrame.MarginTop = 0.02 * 72
    $header.TextFrame.MarginBottom = 0
    $header.TextFrame.TextRange.Text = 'compute_v5_validity.py'
    $header.TextFrame.TextRange.Font.Name = 'Times New Roman'
    $header.TextFrame.TextRange.Font.Size = 19
    $header.TextFrame.TextRange.Font.Color.RGB = OleColor 255 255 255
    $header.TextFrame.TextRange.ParagraphFormat.Alignment = 1

    $code = $slide.Shapes.AddTextbox(1, 7.28 * 72, 2.24 * 72, 5.32 * 72, 2.18 * 72)
    $code.Name = 'کد رده‌بندی اندازه اشیا'
    $code.TextFrame.MarginLeft = 0
    $code.TextFrame.MarginRight = 0
    $code.TextFrame.MarginTop = 0
    $code.TextFrame.MarginBottom = 0
    $code.TextFrame.WordWrap = 0
    $code.TextFrame.TextRange.Text = @(
        'SMALL, LARGE = 0.01, 0.06',
        'a = float(q[3]) * float(q[4])',
        'size[0 if a < SMALL else',
        '     (2 if a >= LARGE else 1)] += 1'
    ) -join "`r"
    $code.TextFrame.TextRange.Font.Name = 'Times New Roman'
    $code.TextFrame.TextRange.Font.Size = 19
    $code.TextFrame.TextRange.Font.Color.RGB = OleColor 30 52 68
    $code.TextFrame.TextRange.ParagraphFormat.Alignment = 1

    $arrow = $slide.Shapes.AddLine(9.94 * 72, 4.73 * 72, 9.94 * 72, 5.18 * 72)
    $arrow.Name = 'فلش از کد اندازه به نتیجه'
    $arrow.Line.ForeColor.RGB = OleColor 31 78 121
    $arrow.Line.Weight = 2.25
    $arrow.Line.EndArrowheadStyle = 3

    $finding = $slide.Shapes.AddTextbox(1, 7.12 * 72, 5.37 * 72, 5.64 * 72, 1.15 * 72)
    $finding.Name = 'یافته اصلی توزیع اندازه'
    $finding.TextFrame.MarginLeft = 0
    $finding.TextFrame.MarginRight = 0
    $finding.TextFrame.MarginTop = 0
    $finding.TextFrame.MarginBottom = 0
    $finding.TextFrame.TextRange.Text = 'حدود ۷۵٪ نمونه‌ها کوچک‌اند'
    $finding.TextFrame.TextRange.Font.Name = 'B Zar'
    $finding.TextFrame.TextRange.Font.Size = 24
    $finding.TextFrame.TextRange.Font.Bold = -1
    $finding.TextFrame.TextRange.Font.Color.RGB = OleColor 24 53 78
    $finding.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    foreach ($shape in $slide.NotesPage.Shapes) {
        try {
            if ($shape.PlaceholderFormat.Type -eq 2) {
                $shape.TextFrame.TextRange.Text = 'کد سمت راست از compute_v5_validity.py گرفته شده است. در برچسب YOLO، q[3] عرض نسبی و q[4] ارتفاع نسبی کادر است؛ حاصل‌ضرب آن‌ها نسبت مساحت کادر به تصویر را می‌دهد. آستانه‌ها در کد ۰٫۰۱ و ۰٫۰۶ هستند: کوچک کمتر از یک درصد، متوسط از یک تا کمتر از شش درصد و بزرگ شش درصد یا بیشتر. نمودار سهم این سه گروه از کل نمونه‌های برچسب‌خورده هر بخش را نشان می‌دهد. سهم اشیای کوچک به‌ترتیب در آموزش، اعتبارسنجی و آزمون حدود ۷۵٫۵، ۷۵٫۱ و ۷۴٫۷ درصد است.'
                break
            }
        } catch {}
    }

    $deck.SaveAs($output, 24)
    Write-Output $output
} finally {
    if ($deck) { $deck.Close() }
    $app.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
