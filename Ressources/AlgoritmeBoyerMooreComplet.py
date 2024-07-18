def preprocess_bad_character_heuristic(pattern):
    """
    Prétraitement pour l'heuristique de mauvaise correspondance.
    Retourne une table de décalage pour chaque caractère du motif.
    """
    m = len(pattern)
    bad_char_table = {chr(i): m for i in range(256)}  # Initialisation avec la longueur du motif
    for i in range(m - 1):
        bad_char_table[pattern[i]] = m - 1 - i
    return bad_char_table

def preprocess_good_suffix_heuristic(pattern):
    """
    Prétraitement pour l'heuristique de bon suffixe.
    Retourne une table de décalage basée sur les suffixes et préfixes du motif.
    """
    m = len(pattern)
    good_suffix_table = [m] * m
    f = [-1] * m
    k = m - 1

    for j in range(m - 2, -1, -1):
        if j > k and f[j + m - 1 - k] < j - k:
            f[j] = f[j + m - 1 - k]
        else:
            if j < k:
                k = j
            while k >= 0 and pattern[k] == pattern[k + m - 1 - j]:
                k -= 1
            f[j] = j - k

    for j in range(m - 1):
        good_suffix_table[m - 1 - f[j]] = min(m - 1 - f[j], good_suffix_table[m - 1 - j])

    return good_suffix_table

def boyer_moore_search(text, pattern):
    """
    Recherche du motif dans le texte en utilisant l'algorithme de Boyer-Moore.
    Retourne les indices de toutes les occurrences du motif dans le texte.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return []
    
    bad_char_table = preprocess_bad_character_heuristic(pattern)
    good_suffix_table = preprocess_good_suffix_heuristic(pattern)
    
    matches = []
    s = 0  # Décalage du motif par rapport au texte

    while s <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            matches.append(s)
            # Déplacer le motif pour vérifier les chevauchements potentiels
            s += 1  # Changer le décalage à 1 pour permettre les chevauchements
        else:
            s += max(good_suffix_table[j], bad_char_table.get(text[s + j], m))

    return matches

# Exemple d'utilisation
text = "AAA"
pattern = "ABC"
matches = boyer_moore_search(text, pattern)

print("Indices des occurrences :", matches)
