$ErrorActionPreference = 'Stop'
$ppt = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه_دفاع_نهایی_جلسه.pptx'
$preEdit = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پشتیبان‌ها\ارائه_دفاع_نهایی_جلسه_قبل_از_اسلایدهای۱۶و۱۷_20260923_004827.pptx'
$backupDir = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پشتیبان‌ها'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$backup = Join-Path $backupDir ('ارائه_دفاع_نهایی_جلسه_قبل_از_بازسازی_کد_زیرمجموعه_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.pptx')
Copy-Item -LiteralPath $ppt -Destination $backup
Copy-Item -LiteralPath $preEdit -Destination $ppt -Force

$app=$null; $deck=$null
try {
    $app=New-Object -ComObject PowerPoint.Application
    $deck=$app.Presentations.Open($ppt,$false,$false,$false)

    # A separate code page preserves the full-size validation charts on pages 16 and 17.
    $new = $deck.Slides.Item(20).Duplicate().Item(1)
    $new.MoveTo(18)
    $new.Shapes.Item('Rectangle 4').TextFrame.TextRange.Text = 'روش پژوهش'
    $new.Shapes.Item('Rectangle 5').TextFrame.TextRange.Text = 'هستهٔ کد ساخت زیرمجموعه'

    $pairs = @(
        @('ویدیو', 'واحد تقسیم'),
        @('۷۰، ۱۵، ۱۵ درصد', 'سهم هدف تصاویر'),
        @('۸۰', 'بذر تقسیم'),
        @('۲، ۳، ۵', 'رده‌های کم‌نمونه'),
        @('شمار نمونه‌های کم‌نمونه', 'معیار اولویت'),
        @('۲۶٬۰۰۰ تصویر', 'حجم آموزش'),
        @('۵٬۵۷۱ تصویر', 'حجم هر بخش ارزیابی'),
        @('۱۲۸۰ پیکسل', 'سقف ضلع تصویر')
    )
    $table=$new.Shapes.Item('Table 19').Table
    for($row=2;$row -le 9;$row++) {
        $pair=$pairs[$row-2]
        $table.Cell($row,1).Shape.TextFrame.TextRange.Text=$pair[0]
        $table.Cell($row,2).Shape.TextFrame.TextRange.Text=$pair[1]
    }
    $table.Cell(6,1).Shape.TextFrame.TextRange.Font.Size=17
    $table.Cell(3,1).Shape.TextFrame.TextRange.Font.Size=17

    $code = @'
if rare_score(r) > 0:
    s = max(FRAC, key=lambda s: rt[s]-sr[s])
else:
    s = max(FRAC, key=lambda s: ft[s]-sf[s])
assign[r] = s
'@
    $codeShape=$new.Shapes.Item('Rectangle 9')
    $codeShape.TextFrame.TextRange.Text=$code
    $codeShape.TextFrame.TextRange.Font.Name='Times New Roman'
    $codeShape.TextFrame.TextRange.Font.Size=20
    $codeShape.TextFrame.TextRange.ParagraphFormat.Alignment=1

    $summary=$new.Shapes.Item('Rectangle 10')
    $summary.TextFrame.TextRange.Text="گروه‌بندی بر پایهٔ پسوند نام ویدیو`rاولویت ویدیوهای دارای رده‌های کم‌نمونه`rحفظ فریم‌های این رده‌ها؛ کنترل اشتراک ویدیوها"
    $summary.TextFrame.TextRange.Font.Name='B Zar'
    $summary.TextFrame.TextRange.Font.Size=20

    $new.Shapes.Item('Rectangle 11').TextFrame.TextRange.Text='build_subset_v5.py'
    $new.Shapes.Item('Rectangle 11').TextFrame.TextRange.Font.Name='Times New Roman'
    $new.Shapes.Item('Rectangle 11').TextFrame.TextRange.Font.Size=16

    # The added content page is number 12; update only page-counter text.
    foreach($slide in $deck.Slides) {
        foreach($shape in $slide.Shapes) {
            if(-not $shape.HasTextFrame -or -not $shape.TextFrame.HasText) { continue }
            $old=$shape.TextFrame.TextRange.Text
            if($old -match 'صفحه\s*([۰-۹]+)\s*از\s*۲۱') {
                $fa='۰۱۲۳۴۵۶۷۸۹'; $num=''
                foreach($c in $Matches[1].ToCharArray()) { $num += [string]$fa.IndexOf([string]$c) }
                $n=[int]$num
                if($slide.SlideIndex -eq 18) { $n=12 }
                elseif($slide.SlideIndex -gt 18 -and $n -ge 12) { $n++ }
                $newNum=([string]$n).Replace('0','۰').Replace('1','۱').Replace('2','۲').Replace('3','۳').Replace('4','۴').Replace('5','۵').Replace('6','۶').Replace('7','۷').Replace('8','۸').Replace('9','۹')
                $shape.TextFrame.TextRange.Text="صفحه $newNum از ۲۲"
            }
        }
    }

    $deck.Save()
    foreach($i in 16..18) { $deck.Slides.Item($i).Export("C:\Users\amir2\Desktop\cat-claude\subset_slide_$i.png",'PNG',1600,900) }
    Write-Output "backup=$backup"
    Write-Output "slides=$($deck.Slides.Count)"
}
finally {
    if($deck){$deck.Close()}
    if($app){$app.Quit()}
}
