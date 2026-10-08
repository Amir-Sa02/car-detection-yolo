$ErrorActionPreference='Stop'
$outRoot='C:\Users\amir2\Desktop\cat-claude\network_guides_qa'
New-Item -ItemType Directory -Path $outRoot -Force | Out-Null
$files=Get-ChildItem -LiteralPath 'C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه معماری و پرسش‌های دفاع' -Filter '*.docx' | Sort-Object Name
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
try {
 $i=0
 foreach($f in $files){
  $i++
  $doc=$word.Documents.Open($f.FullName,$false,$true)
  $doc.Repaginate()
  $dest=Join-Path $outRoot ('guide'+$i+'.pdf')
  $doc.ExportAsFixedFormat($dest,17)
  Write-Output ($f.Name+' pages='+$doc.ComputeStatistics(2)+' pdf='+$dest)
  $doc.Close($false)
 }
} finally {
 $word.Quit()
 [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)|Out-Null
}
