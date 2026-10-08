$ErrorActionPreference = 'Stop'
$source = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه-دفاع.pptx'
$output = 'C:\Users\amir2\Desktop\cat-claude\ارائه-دفاع_بازخورد_استاد_بازبینی_۲.pptx'

$app = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
    $presentation = $app.Presentations.Open($source, $false, $false, $false)

    $challenges = $presentation.Slides.Item(11).Shapes.Item(12)
    $challenges.Left = 5.37 * 72
    $challenges.Top = 1.71 * 72
    $challenges.Width = 6.97 * 72
    $challenges.Height = 3.05 * 72
    $challenges.TextFrame.AutoSize = 0
    $challenges.TextFrame.MarginLeft = 0
    $challenges.TextFrame.MarginRight = 0
    $challenges.TextFrame.MarginTop = 0
    $challenges.TextFrame.MarginBottom = 0
    $lines = @(
        '۱. نشت داده: فریم‌های یک ویدیو در چند بخش [۲]',
        '۲. ویدیوهای تکراری: محتوای یکسان با دو شناسه',
        '۳. برچسب معیوب: کادر ناقص، جابه‌جا یا غایب',
        '۴. ناهم‌ترازی: تفاوت دشواری دو بخش ارزیابی',
        '۵. آزمون رسمیِ بی‌برچسب: ساخت آزمون برچسب‌دار'
    )
    $challenges.TextFrame.TextRange.Text = $lines -join "`r"
    $challenges.TextFrame.TextRange.Font.Name = 'B Zar'
    $challenges.TextFrame.TextRange.Font.Size = 20
    $challenges.TextFrame.TextRange.Font.Color.RGB = 0x222222
    $challenges.TextFrame.TextRange.ParagraphFormat.Alignment = 3
    $challenges.TextFrame.TextRange.ParagraphFormat.SpaceAfter = 2
    for ($i = 1; $i -le $lines.Count; $i++) {
        $paragraph = $challenges.TextFrame.TextRange.Paragraphs($i, 1)
        $colon = $lines[$i - 1].IndexOf(':')
        if ($colon -ge 0) { $paragraph.Characters(1, $colon + 1).Font.Bold = -1 }
    }

    $table = $presentation.Slides.Item(15).Shapes.Item(2).Table
    foreach ($row in @(3,4)) {
        $cell = $table.Cell($row, 3).Shape.TextFrame.TextRange
        $cell.Text = '۱۵٪'
        $cell.Font.Name = 'B Zar'
        $cell.Font.Size = 20
        $cell.ParagraphFormat.Alignment = 2
    }

    $slide = $presentation.Slides.Item(18)
    $note = $slide.Shapes.AddTextbox(1, (1.60 * 72), (6.47 * 72), (10.15 * 72), (0.37 * 72))
    $note.Name = 'سهم کل تصاویر برحسب شرایط محیطی'
    $note.TextFrame.MarginLeft = 0
    $note.TextFrame.MarginRight = 0
    $note.TextFrame.MarginTop = 0
    $note.TextFrame.MarginBottom = 0
    $note.TextFrame.TextRange.Text = 'سهم از کل تصاویر: روز ۸۱٫۰٪، شب ۸٫۸٪، باران ۸٫۸٪، ابری ۱٫۴٪'
    $note.TextFrame.TextRange.Font.Name = 'B Zar'
    $note.TextFrame.TextRange.Font.Size = 20
    $note.TextFrame.TextRange.Font.Color.RGB = 0x253D50
    $note.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    $speakerNotes = @{
        11 = 'بخش آزمون رسمی IADD که برای دانلود در دسترس بود برچسب نداشت. بنابراین از تصاویر برچسب‌دار بخش‌های آموزش و اعتبارسنجی همان مجموعه استفاده کردیم و تقسیم سه‌گانه تازه‌ای در سطح کل ویدیو ساختیم. این کار برچسب‌گذاری مجدد تصاویر نبود. چهار چالش دیگر نیز در همین اسلاید آمده‌اند و روند حل آن‌ها در اسلایدهای بعدی نشان داده می‌شود.'
        15 = 'درصدهای جدول نسبت به کل ۳۷٬۱۴۲ تصویر زیرمجموعه نهایی محاسبه شده‌اند: ۲۶٬۰۰۰ تصویر برای آموزش و برای هر یک از اعتبارسنجی و آزمون ۵٬۵۷۱ تصویر. پس نسبت‌ها تقریباً ۷۰، ۱۵ و ۱۵ درصد است. واحد جداسازی، ویدیو بوده و تعداد ویدیوها الزاماً با همین نسبت تقسیم نشده است.'
        17 = 'محور افقی شش رده شیء و محور عمودی سهم هر رده از کل نمونه‌های همان بخش است؛ درصدها مربوط به شمار کادرهای برچسب‌خورده‌اند، نه شمار تصاویر. محور عمودی لگاریتمی است، چون خودروی سبک حدود ۸۴ درصد نمونه‌ها را دارد ولی سهم بعضی رده‌ها زیر یک درصد است. در مقیاس خطی، ستون‌های رده‌های کم‌نمونه تقریباً دیده نمی‌شدند. نزدیکی سه رنگ در هر رده نشان می‌دهد نسبت رده‌ها میان بخش‌ها تا حدی هم‌تراز شده است؛ با این حال عدم توازن کلی رده‌ها همچنان وجود دارد.'
        18 = 'نمودار سمت چپ درصد تصاویر هر وضعیت محیطی را در هر یک از سه بخش نشان می‌دهد. محور عمودی آن لگاریتمی است تا سهم کم روزهای ابری هم دیده شود. سطر پایین اسلاید، سهم همین وضعیت‌ها را از کل ۳۷٬۱۴۲ تصویر نشان می‌دهد. نمودار سمت راست توزیع اندازه اشیا را بر حسب شمار کادرهای برچسب‌خورده نشان می‌دهد؛ محور عمودی آن خطی است. در این نمودار کوچک یعنی کمتر از یک درصد مساحت تصویر و بزرگ یعنی بیشتر از شش درصد. شباهت توزیع‌ها یکی از شواهد هم‌ترازی است و به تنهایی برابری کامل دشواری صحنه‌ها را ثابت نمی‌کند.'
    }
    foreach ($n in $speakerNotes.Keys) {
        $notesPage = $presentation.Slides.Item([int]$n).NotesPage
        foreach ($shape in $notesPage.Shapes) {
            try {
                if ($shape.PlaceholderFormat.Type -eq 2) {
                    $shape.TextFrame.TextRange.Text = $speakerNotes[$n]
                    break
                }
            } catch {}
        }
    }

    $presentation.SaveAs($output, 24)
    Write-Output $output
} finally {
    if ($presentation) { $presentation.Close() }
    $app.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
