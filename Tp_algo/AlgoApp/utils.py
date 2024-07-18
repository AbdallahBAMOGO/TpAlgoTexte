import re
import sys

def preprocess_bad_character_heuristic(pattern):
    """
    Prétraitement pour l'heuristique de mauvaise correspondance.
    Retourne une table de décalage pour chaque caractère du motif.
    """
    m = len(pattern)
    bad_char_table = {chr(i): m for i in range(256)}  # Initialisation avec la longueur du motif
    for i in range(m):
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
    Retourne True si le motif est trouvé dans le texte, sinon False.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return False
    
    bad_char_table = preprocess_bad_character_heuristic(pattern)
    good_suffix_table = preprocess_good_suffix_heuristic(pattern)
    
    s = 0  # Décalage du motif par rapport au texte

    while s <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            return True
        else:
            s += max(good_suffix_table[j], bad_char_table.get(text[s + j], m))

    return False

def get_words_from_text(text):
    """
    Extrait les mots d'un texte donné en convertissant tout en minuscules
    et en supprimant la ponctuation.
    """
    #Convertir le texte en minuscules et extraire les mots en utilisant des expressions régulières
    text = text.lower()
    return text.split()  # Retourner la liste des mots pour traitement
    
def get_words_from_text_with_case(text):
    return text.split()

def find_common_words(text1, text2):
    """
    Trouve les mots communs entre deux texte en utilisant l'algorithme de Boyer-Moore.
    """    
    wordc1 = get_words_from_text_with_case(text1)
    wordc2 = get_words_from_text_with_case(text2)
    common_words_with_case = set(wordc1).intersection(wordc2)
    total_words = max(len(wordc1), len(wordc2))
    similarity_percentage_with_case = (len(common_words_with_case) / total_words) * 100 if total_words > 0 else 0

    
     # Extraire les mots des deux textes
    words1 = get_words_from_text(text1)
    words2 = get_words_from_text(text2)    

    # Utiliser un ensemble pour les mots du deuxième fichier pour des recherches rapides
    words2_set = set(words2)

    common_words = set()

    # Vérifier chaque mot du premier texte dans le deuxième texte
    for word in words1:
        if len(word) > 0 and word in words2_set:
            common_words.add(word)
            
    #total_words = max(len(words1), len(words2))
    common_words = list(common_words)        
    similarity_percentage = (len(common_words) / total_words) * 100 if total_words > 0 else 0
    
    
    return common_words, common_words_with_case, similarity_percentage, similarity_percentage_with_case
