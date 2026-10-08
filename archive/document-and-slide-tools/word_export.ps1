$ErrorActionPreference='Stop'
$docPath='C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
$pdfPath='C:\Users\amir2\Desktop\cat-claude\qa_map_20260922_1220\thesis.pdf'
$log='C:\Users\amir2\Desktop\cat-claude\qa_map_20260922_1220\word_export.log'
function L($s){Add-Content -LiteralPath $log -Value ("$(Get-Date -Format HH:mm:ss) $s")}
Set-Content -LiteralPath $log -Value 'start'
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
try {
 L 'opening'
 $doc=$word.Documents.Open($docPath,$false,$true)
 L 'opened'
 $doc.Repaginate()
 L ('pages='+$doc.ComputeStatistics(2))
 $doc.SaveAs2($pdfPath,17)
 L 'saved pdf'
 $doc.Close($false)
 L 'closed doc'
} catch { L ('ERROR '+$_.Exception.ToString()); throw } finally { $word.Quit(); L 'quit'; [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)|Out-Null }
