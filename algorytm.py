import random

# Przykładowe dane wejściowe - zlecenia (czas wykonania, wymagany czas realizacji, kara za minutę opóźnienia)
zlecenia = [(160, 200, 1), (180, 300, 2), (129, 400, 3), (129, 500, 4), (175, 600, 5), (75, 300, 5), (250, 350, 4), (150, 400, 3), (313, 450, 2),
            (284, 500, 1), (119, 550, 2), (108, 600, 3), (129, 650, 4), (192, 700, 5), (205, 750, 1)]



# Definicja funkcji oceny (przystosowania)
def ocena_kary(kolejnosc):
    czas_zakonczenia_maszyna1 = 0
    czas_zakonczenia_maszyna2 = 0
    kara = 0

    for idx in kolejnosc:
        czas_zakonczenia_maszyna1 += zlecenia[idx][0]
        czas_zakonczenia_maszyna2 = max(czas_zakonczenia_maszyna1, czas_zakonczenia_maszyna2) + zlecenia[idx][1]
        opoznienie = max(0, czas_zakonczenia_maszyna2 - zlecenia[idx][1])
        kara += opoznienie * zlecenia[idx][2]

    return kara,


# Inicjalizacja algorytmu genetycznego
def algorytm_genetyczny(populacja, funkcja_oceny, prawdopodobienstwo_krzyzowania=0.7, prawdopodobienstwo_mutacji=0.1,
                        liczba_generacji=100):
    for _ in range(liczba_generacji):
        potomstwo = []
        for _ in range(len(populacja) // 2):
            rodzic1 = random.choice(populacja)
            rodzic2 = random.choice(populacja)
            potomek1, potomek2 = krzyzowanie(rodzic1, rodzic2, prawdopodobienstwo_krzyzowania)
            potomstwo.extend(mutacja(potomek1, prawdopodobienstwo_mutacji))
            potomstwo.extend(mutacja(potomek2, prawdopodobienstwo_mutacji))
        populacja += potomstwo
        populacja = selekcja(populacja, funkcja_oceny)
    return populacja


# Operatory genetyczne
def krzyzowanie(rodzic1, rodzic2, prawdopodobienstwo):
    if random.random() < prawdopodobienstwo:
        punkt_krzyzowania = random.randint(1, len(rodzic1) - 1)
        potomek1 = rodzic1[:punkt_krzyzowania] + [gen for gen in rodzic2 if gen not in rodzic1[:punkt_krzyzowania]]
        potomek2 = rodzic2[:punkt_krzyzowania] + [gen for gen in rodzic1 if gen not in rodzic2[:punkt_krzyzowania]]
        return potomek1, potomek2
    return rodzic1, rodzic2


def mutacja(chromosom, prawdopodobienstwo):
    if random.random() < prawdopodobienstwo:
        idx1, idx2 = random.sample(range(len(chromosom)), 2)
        chromosom[idx1], chromosom[idx2] = chromosom[idx2], chromosom[idx1]
    return [chromosom]


def selekcja(populacja, funkcja_oceny, k=100):
    oceny = [funkcja_oceny(chromosom) for chromosom in populacja]
    najlepsi = sorted(zip(populacja, oceny), key=lambda x: x[1])[:k]
    return [chromosom for chromosom, _ in najlepsi]


# Inicjalizacja populacji początkowej
rozmiar_populacji = 100
populacja_poczatkowa = [random.sample(range(len(zlecenia)), len(zlecenia)) for _ in range(rozmiar_populacji)]

# Uruchomienie algorytmu genetycznego
najlepsza_kolejnosc = algorytm_genetyczny(populacja_poczatkowa, ocena_kary)

print("Najlepsza kolejność zleceń:", najlepsza_kolejnosc[0])
