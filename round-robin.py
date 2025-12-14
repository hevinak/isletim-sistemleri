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

quantum = int(input("Quantum değerini girin (örnek: 4): "))

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
            "remaining": int(parcalar[2])  
        }
        processler.append(process)

processler = sorted(processler, key=lambda x: x['arrival'])

zaman = 0
tamamlanan = 0
toplam_process = len(processler)
zaman_tablosu = []
completion_times = {}
kuyruk = []
process_index = 0 #kuyruğa eklenen processler için,hangilerini de eklemediğimizi takip edebilmek için


if process_index < len(processler) and processler[process_index]['arrival'] <= zaman:
    kuyruk.append(processler[process_index])
    process_index += 1

while tamamlanan < toplam_process:
    
        if kuyruk:
            su_anki = kuyruk.pop(0)
            calisma_suresi = min(quantum, su_anki['remaining'])#kalan süresi ya da q değerinden en düşük olanı kadar çalıştırıcaz,
            baslangic = zaman
            zaman += calisma_suresi
            bitis = zaman

            zaman_tablosu.append({
                'process': su_anki['id'],
                'baslangic': baslangic,
                'bitis': bitis
            })
            su_anki['remaining'] -= calisma_suresi# Kalan süreyi azalt
        
            while process_index < len(processler) and processler[process_index]['arrival'] <= zaman:
                kuyruk.append(processler[process_index])
                process_index += 1  # işi yaparken gelen processleri kıyruğa ekliyoruz

            if su_anki['remaining'] == 0:
                tamamlanan += 1
                completion_times[su_anki['id']] = zaman
            else:
                kuyruk.append(su_anki)

        else:# Kuyruk boş
         zaman += 1
        
        # yeni process gelirse diye
        while process_index < len(processler) and processler[process_index]['arrival'] <= zaman:
            kuyruk.append(processler[process_index])
            process_index += 1


# Waiting ve Turnaround hesapla
sonuclar = []

for p in processler:
    completion_time = completion_times[p['id']]
    turnaround_time = completion_time - p['arrival']
    waiting_time = turnaround_time - p['burst']
    
    sonuclar.append({
        'id': p['id'],
        'waiting': waiting_time,
        'turnaround': turnaround_time
    })

for zt in zaman_tablosu:
    print(f"[ {zt['baslangic']} ] -- {zt['process']} -- [ {zt['bitis']} ]")

waiting_times = [s['waiting'] for s in sonuclar]
max_waiting = max(waiting_times)
ortalama_waiting = sum(waiting_times) / len(waiting_times)


print(f"   Maximum Waiting Time: {max_waiting}")
print(f"   Ortalama Waiting Time: {ortalama_waiting:.2f} ")

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
