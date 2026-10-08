$ErrorActionPreference = 'Stop'
$source = 'C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه-دفاع.pptx'
$output = 'C:\Users\amir2\Desktop\cat-claude\ارائه-دفاع_جدول_شرایط_محیطی_بازبینی.pptx'
function OleColor([int]$r,[int]$g,[int]$b) { $r + ($g -shl 8) + ($b -shl 16) }
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open($source, $false, $false, $false)
    $slide = $deck.Slides.Item(19)
    $slide.Shapes.Item('سهم کل تصاویر').Delete()
    $slide.Shapes.Item('عنوان سهم کل تصاویر').Delete()

    $shape = $slide.Shapes.AddTable(5, 2, 7.10 * 72, 5.16 * 72, 5.71 * 72, 1.66 * 72)
    $shape.Name = 'جدول سهم شرایط محیطی از کل تصاویر'
    $table = $shape.Table
    $rows = @(
        @('سهم از کل تصاویر', 'وضعیت محیطی'),
        @('۸۱٫۰٪', 'روز'),
        @('۸٫۸٪', 'شب'),
        @('۸٫۸٪', 'باران'),
        @('۱٫۴٪', 'ابری')
    )
    for ($r = 1; $r -le 5; $r++) {
        for ($c = 1; $c -le 2; $c++) {
            $cell = $table.Cell($r, $c)
            $cell.Shape.TextFrame.TextRange.Text = $rows[$r - 1][$c - 1]
            $cell.Shape.TextFrame.MarginLeft = 0.03 * 72
            $cell.Shape.TextFrame.MarginRight = 0.03 * 72
            $cell.Shape.TextFrame.MarginTop = 0
            $cell.Shape.TextFrame.MarginBottom = 0
            $cell.Shape.TextFrame.VerticalAnchor = 3
            $cell.Shape.TextFrame.TextRange.Font.Name = 'B Zar'
            $cell.Shape.TextFrame.TextRange.Font.Size = 19
            $cell.Shape.TextFrame.TextRange.ParagraphFormat.Alignment = 2
            if ($r -eq 1) {
                $cell.Shape.Fill.ForeColor.RGB = OleColor 16 73 102
                $cell.Shape.TextFrame.TextRange.Font.Color.RGB = OleColor 255 255 255
                $cell.Shape.TextFrame.TextRange.Font.Bold = -1
            } elseif ($c -eq 2) {
                $cell.Shape.Fill.ForeColor.RGB = OleColor 207 229 240
                $cell.Shape.TextFrame.TextRange.Font.Color.RGB = OleColor 25 56 78
                $cell.Shape.TextFrame.TextRange.Font.Bold = -1
            } else {
                $cell.Shape.Fill.ForeColor.RGB = OleColor 255 255 255
                $cell.Shape.TextFrame.TextRange.Font.Color.RGB = OleColor 25 56 78
            }
            for ($edge = 1; $edge -le 4; $edge++) {
                try {
                    $border = $cell.Borders.Item($edge)
                    $border.ForeColor.RGB = OleColor 56 72 82
                    $border.Weight = 0.75
                } catch {}
            }
        }
    }
    $deck.SaveAs($output, 24)
    Write-Output $output
} finally {
    if ($deck) { $deck.Close() }
    $app.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
