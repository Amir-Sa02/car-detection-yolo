$ErrorActionPreference = 'Stop'
$root = 'C:\Users\amir2\Desktop\cat-claude\supervisor_feedback_after'
New-Item -ItemType Directory -Path $root -Force | Out-Null
$files = @(
    @{Name='before'; Path='C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه-دفاع.pptx'},
    @{Name='after'; Path='C:\Users\amir2\Desktop\cat-claude\ارائه-دفاع_بازخورد_استاد_بازبینی_۲.pptx'}
)
$app = New-Object -ComObject PowerPoint.Application
try {
    foreach ($f in $files) {
        $deck = $app.Presentations.Open($f.Path, $false, $true, $false)
        try {
            foreach ($n in @(4,11,13,15,17,18)) {
                $out = Join-Path $root ($f.Name + '_' + $n + '.png')
                $deck.Slides.Item($n).Export($out, 'PNG', 1600, 900)
                Write-Output $out
            }
        } finally { $deck.Close() }
    }
} finally {
    $app.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
