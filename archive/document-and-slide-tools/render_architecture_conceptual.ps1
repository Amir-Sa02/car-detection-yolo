$ErrorActionPreference='Stop'
$targetDoc='C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه معماری و پرسش‌های دفاع\۰۱_آموزش_گام‌به‌گام_معماری_YOLOv11s.docx'
$qaRoot='C:\Users\amir2\Desktop\cat-claude\architecture_conceptual_qa'
New-Item -ItemType Directory -Path $qaRoot -Force | Out-Null
$qaDoc=Join-Path $qaRoot ('verification_'+(Get-Date -Format 'yyyyMMdd_HHmmss')+'.docx')
Copy-Item -LiteralPath $targetDoc -Destination $qaDoc
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
try {
 $doc=$word.Documents.Open($qaDoc,$false,$true)
 $doc.ActiveWindow.View.Type=3
 $doc.Repaginate()
 $ltr=0
 $notRight=0
 $n=0
 foreach($para in $doc.Paragraphs){
  $text=$para.Range.Text.Trim([char[]]@([char]13,[char]7,[char]32,[char]12))
  if($text.Length -gt 0){
   $n++
   if($para.Range.ParagraphFormat.ReadingOrder -ne 0){$ltr++}
   if($para.Range.ParagraphFormat.Alignment -notin @(1,2)){ $notRight++ }
  }
 }
 $doc.ExportAsFixedFormat((Join-Path $qaRoot 'architecture.pdf'),17)
 $info=[ordered]@{pages=$doc.ComputeStatistics(2);equations=$doc.OMaths.Count;meaningful_paragraphs=$n;not_RTL=$ltr;not_right_or_center=$notRight}
 $info | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $qaRoot 'word_audit.json') -Encoding utf8
 $info | ConvertTo-Json
 $doc.Close($false)
} finally {
 $word.Quit()
 [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)|Out-Null
}

