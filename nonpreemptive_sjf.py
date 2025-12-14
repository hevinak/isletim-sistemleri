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
            "priority": parcalar[3],
        }
        processler.append(process)

processler = sorted(processler, key=lambda x: x['arrival'])

zaman = 0
sonuclar = []
zaman_tablosu = []
islenmis = []  #biten process'ler için

while len(islenmis) < len(processler):
    #tüm processler bitene kadar
    hazir_processler = []#şuana kadar gelip işlenmemiş processler için
    
    for p in processler:
        if p['arrival'] <= zaman and p['id'] not in islenmis:#arrival zamandan küçük olan ve işlenmiş listesinde olmayan
            hazir_processler.append(p)

    if hazir_processler:
            # En kısa burst'a sahip olan
        en_kisa = min(hazir_processler, key=lambda x: x['burst'])

        if zaman < en_kisa['arrival']:
            zaman_tablosu.append({
                'process': 'IDLE',
                'baslangic': zaman,
                'bitis': en_kisa['arrival']
            })

            zaman = en_kisa['arrival']

            waiting_time = zaman - en_kisa['arrival']
            baslangic = zaman
            zaman = zaman + en_kisa['burst']
            bitis = zaman
            zaman_tablosu.append({
                    'process': en_kisa['id'],
                    'baslangic': baslangic,
                    'bitis': bitis
                })
            turnaround_time = zaman - en_kisa['arrival']#burst+waiting yani
            sonuclar.append({
                'id': en_kisa['id'],
                'waiting': waiting_time,
                'turnaround': turnaround_time
            })
            islenmis.append(en_kisa['id'])#işlenmiş list'e ekle
    else:
        zaman += 1

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

#kaç satır varsa 1 eksiği kadara bağlam değişimi olmuştur.
baglam_degisim = len(zaman_tablosu) - 1
print(f"Bağlam değiştirme sayısı: { baglam_degisim}")
