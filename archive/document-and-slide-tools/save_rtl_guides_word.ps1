$ErrorActionPreference='Stop'
$taskRoot='C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه معماری و پرسش‌های دفاع'
$qaRoot='C:\Users\amir2\Desktop\cat-claude\network_guides_rtl_qa'
New-Item -ItemType Directory -Path $qaRoot -Force | Out-Null
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
try {
 $index=0
 foreach($file in (Get-ChildItem -LiteralPath $taskRoot -Filter '*.docx' | Sort-Object Name)) {
  $index++
  $doc=$word.Documents.Open($file.FullName,$false,$true)
  $doc.Repaginate()
  $doc.ExportAsFixedFormat((Join-Path $qaRoot ('guide'+$index+'.pdf')),17)
  $ltr=0
  foreach($para in $doc.Paragraphs){if($para.Range.ParagraphFormat.ReadingOrder -ne 0){$ltr++}}
  Write-Output ($file.Name+' equations='+$doc.OMaths.Count+' paragraphs_not_RTL='+$ltr)
  $doc.Close($false)
 }
} finally {
 $word.Quit()
 [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)|Out-Null
}
