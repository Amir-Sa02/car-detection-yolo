$ErrorActionPreference='Stop'
$ppt='D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع_نهایی_جلسه.pptx'
$app=$null; $pres=$null
try {
  $app=New-Object -ComObject PowerPoint.Application
  $pres=$app.Presentations.Open($ppt,$false,$false,$false)
  $s=$pres.Slides.Item(20)

  $s.Shapes.Item('Rectangle 3').Top=132
  $s.Shapes.Item('Rectangle 4').Top=158
  $s.Shapes.Item('TextBox 5').Left=610
  $s.Shapes.Item('TextBox 5').Top=109
  $s.Shapes.Item('TextBox 5').Width=180
  $s.Shapes.Item('TextBox 8').Left=746
  $s.Shapes.Item('TextBox 8').Top=228
  $s.Shapes.Item('TextBox 8').Width=150

  $s.Shapes.Item('TextBox 9').Top=250
  $s.Shapes.Item('TextBox 9').TextFrame2.TextRange.Text='IoU = |P ∩ G| / |P ∪ G|'
  $s.Shapes.Item('TextBox 11').Left=730
  $s.Shapes.Item('TextBox 11').Top=278
  $s.Shapes.Item('TextBox 11').Width=180
  $s.Shapes.Item('TextBox 11').TextFrame2.TextRange.Text=[char]0x200F+'P: پیش‌بینی  |  G: واقعی  [۹]'

  $s.Shapes.Item('TextBox 12').Top=299
  $s.Shapes.Item('TextBox 13').Top=329
  $s.Shapes.Item('TextBox 15').Top=359
  $s.Shapes.Item('TextBox 15').TextFrame2.TextRange.Font.Size=19
  $s.Shapes.Item('TextBox 16').Top=391
  $s.Shapes.Item('TextBox 16').TextFrame2.TextRange.Font.Size=16

  $s.Shapes.Item('TextBox 29').TextFrame2.TextRange.Text='AP(c) = ∫₀¹ P(c,R) dR'
  $s.Shapes.Item('TextBox 31').TextFrame2.TextRange.Text='mAP@0.5 = (1 / N) Σ AP(c)@0.5'

  $pres.Save()
}
finally {
  if($pres){$pres.Close()}
  if($app){$app.Quit()}
  [gc]::Collect(); [gc]::WaitForPendingFinalizers()
}
