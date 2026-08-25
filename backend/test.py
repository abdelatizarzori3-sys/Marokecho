import requests, os, json
k = os.getenv('GEMINI_API_KEY')
print('Key:', k[:15]+'...' if k else 'NOT SET')
if k:
  r = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key='+k, json={'contents':[{'parts':[{'text':'hi'}]}]})
  print('Status:', r.status_code)
  print(r.text[:300])
