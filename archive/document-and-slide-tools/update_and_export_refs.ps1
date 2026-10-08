$ErrorActionPreference='Stop'
$docPath='C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
$outDir='C:\Users\amir2\Desktop\cat-claude\qa_reduced_refs_20260922'
$pdfPath=Join-Path $outDir 'thesis.pdf'
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$word=New-Object -ComObject Word.Application
$word.Visible=$false; $word.DisplayAlerts=0
try {
 $doc=$word.Documents.Open($docPath,$false,$false)
 $doc.Repaginate()
 $updated=0
 foreach($field in $doc.Fields){if($field.Type -eq 37){$field.Update()|Out-Null;$updated++}}
 foreach($story in $doc.StoryRanges){$r=$story;while($null -ne $r){foreach($field in $r.Fields){if($field.Type -eq 37){$field.Update()|Out-Null;$updated++}};$r=$r.NextStoryRange}}
 $doc.Repaginate(); $doc.Save(); $doc.ExportAsFixedFormat($pdfPath,17); $doc.Close($false)
 Write-Output "UPDATED=$updated PDF=$pdfPath"
} finally {$word.Quit();[System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)|Out-Null}
