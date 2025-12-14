print("Hangi dosyayı okumak istersiniz?")
print("1 - odev1_case1.txt")
print("2 - odev1_case2.txt")

secim = input("Seçiminiz (1 veya 2): ")

if secim == "1":
    dosya_adi = "odev1_case1.txt"
elif secim == "2":
    dosya_adi = "odev1_case2.txt"
else:
    print("Geçersiz seçim! Varsayılan olarak case1 açılıyor.")
    dosya_adi = "odev1_case1.txt"

        
processler = []
ilk_satir = True
        
with open(dosya_adi) as dosya:
    for satir in dosya:
        if ilk_satir:
            ilk_satir = False
            continue
        parcalar = satir.strip().split(",")
        process = {
            "id": parcalar[0],
            "arrival": int(parcalar[1]),
            "burst": int(parcalar[2]),
            "priority": parcalar[3]
        }
        processler.append(process)

processler = sorted(processler, key=lambda x: x['arrival'])

zaman = 0
sonuclar = []
zaman_tablosu = []

for p in processler:#arrival'a göre sıralamıştık
    if zaman < p['arrival']:
        zaman_tablosu.append({
            "process": "IDLE",
            "baslangic": zaman,
            "bitis": p['arrival']
        })
        zaman = p['arrival']

    waiting_time = zaman - p['arrival']#burda olduğumuz zamandan varışı çıkararak bekleme süresini buluyoruz
    baslangic = zaman
    zaman = zaman + p['burst']
    bitis = zaman
    
    zaman_tablosu.append({
        "process": p['id'],
        "baslangic": baslangic,
        "bitis": bitis
    })

    turnaround_time = zaman - p['arrival']#burda zamanda burst eklenmiş oldu böylece zaman-arrival yaptığımızda waiting time + burst time kalıyor. Bu da turnaround time'ı veriyor.
    sonuc = {
        "id": p['id'],
        "waiting": waiting_time,
        "turnaround": turnaround_time
    }
    sonuclar.append(sonuc)

for zt in zaman_tablosu:
    print(f"[ {zt['baslangic']} ] -- {zt['process']} -- [ {zt['bitis']} ]")

waiting_times = [s['waiting'] for s in sonuclar]
max_waiting = max(waiting_times)
ortalama_waiting = sum(waiting_times) / len(waiting_times)

print(f"   Maximum Waiting Time: {max_waiting}")
print(f"   Ortalama Waiting Time: {ortalama_waiting:.2f}")

turnaround_times=[s['turnaround'] for s in sonuclar]
max_turnaround = max(turnaround_times)
ortalama_turnaround = sum(turnaround_times)/ len(turnaround_times)

print(f"   Maximum Turnaround Time: {max_turnaround}")
print(f"   Ortalama Turnaround Time:{ortalama_turnaround:.2f}")

#througput için
sayac = 0

for t in [50, 100, 150, 200]:
    sayac = 0
    
    for s in sonuclar:
        index = sonuclar.index(s)
        arrival = processler[index]['arrival']
        turnaround = s['turnaround']
        bitis_zamani = arrival + turnaround
            
        if bitis_zamani <= t:
            sayac += 1
    
    print(f"T={t} için throughput: {sayac}")

toplam_sure = zaman_tablosu[-1]['bitis']

idle_sure = 0
for zt in zaman_tablosu:
    if zt['process'] == "IDLE":
        idle_sure += (zt['bitis'] - zt['baslangic'])

calisma_sure = toplam_sure - idle_sure
verimlilik = (calisma_sure / toplam_sure) * 100

print(f"Ortalama CPU Verimliliği: {verimlilik:.3f}%")#virgülden sonra 3 basamak

baglam_degisim = len(zaman_tablosu) - 1
print(f"Bağlam değiştirme sayısı: { baglam_degisim}")