"""Offline regression for narration QA, with no model or billing requests."""
import app
clean=[{"title":"AI membantu pekerjaan","text":"Gunakan AI untuk membantu tugas sederhana."},{"title":"Periksa hasil","text":"Cocokkan jawaban dengan instruksi."},{"title":"Tetap awasi","text":"Jangan kirim data pribadi."}]
assert app.validate_narration(clean)==clean
for title,text in [("0–4 detik | Pembuka","AI bisa membantu."),("Pembuka","Tampilkan layar. Narasi: AI bisa membantu.")]:
 bad=[dict(s) for s in clean];bad[0]={"title":title,"text":text}
 try:app.validate_narration(bad)
 except ValueError:pass
 else:raise AssertionError("Production metadata accepted")
print("PASS: clean narration accepted; timestamps and narration labels rejected (offline regression)")
