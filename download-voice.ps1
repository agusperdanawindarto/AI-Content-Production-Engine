$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
$dest=Join-Path $PWD 'vendor\voice-id'
New-Item -ItemType Directory -Force $dest | Out-Null
$base='https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium'
$files=@{
'id_ID-news_tts-medium.onnx'='ED8F02AA593F7AF6B19ACBDB8142E0DA0DD72F46194EB33D38E0EB10A52597E8'
'id_ID-news_tts-medium.onnx.json'='1EF677072668A5E172E0759B1D3871F129009D1167F093325A17607F7ADD5AD7'
'MODEL_CARD'='CC134D8C8FCE95D2486A0E5AE60B40C17451A876CF7D36DF0F4110589FC40538'
}
foreach($f in $files.Keys){
  $p=Join-Path $dest $f
  if((Test-Path $p) -and (Get-FileHash $p -Algorithm SHA256).Hash -eq $files[$f]){continue}
  $temp=$p+'.partial'
  curl.exe -fL --max-time 180 --retry 1 "$base/$f" -o $temp
  if($LASTEXITCODE -ne 0){throw "Download failed: $f"}
  if((Get-FileHash $temp -Algorithm SHA256).Hash -ne $files[$f]){throw "Checksum mismatch: $f"}
  Move-Item -Force $temp $p
}
Write-Output 'Indonesian Piper model and model card verified. Preview use only pending voice dataset license review.'
