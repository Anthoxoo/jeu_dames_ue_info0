# Lors du jeu, si vous voulez capturer un pion, il faut entrer la position finale qu'occupera votre pion et non le pion directement a capturer.

from random import randint

# Constante -> valeur qui ne changera pas, nous donne la valeur de la colonne en fonction de la lettre. Donc on la met en majuscule.
LETTRE_VALEUR = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
}


def creer_grille_debut_partie() -> list[list]:
    return [
        [" ", "n", " ", "n", " ", "n", " ", "n"],
        ["n", " ", "n", " ", "n", " ", "n", " "],
        [" ", "n", " ", "n", " ", "n", " ", "n"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["b", " ", "b", " ", "b", " ", "b", " "],
        [" ", "b", " ", "b", " ", "b", " ", "b"],
        ["b", " ", "b", " ", "b", " ", "b", " "],
    ]


def creer_grille_milieu_partie() -> list[list]:
    return [
        [" ", "n", " ", " ", " ", "n", " ", "n"],
        [" ", " ", "n", " ", "n", " ", " ", " "],
        [" ", " ", " ", "n", " ", " ", " ", "n"],
        [" ", " ", " ", " ", "b", " ", " ", " "],
        [" ", "n", " ", "b", " ", " ", " ", " "],
        ["b", " ", " ", " ", "b", " ", "b", " "],
        [" ", " ", " ", "b", " ", " ", " ", "b"],
        ["b", " ", "b", " ", " ", " ", "b", " "],
    ]


def creer_grille_fin_partie() -> list[list]:
    return [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", "n", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "b", " ", "n", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", "b", " ", " ", " ", "b", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]


def est_dans_grille(ligne: str, colonne: int, grille: list[list]):
    # Si la ligne donnée par l'utilisateur n'est pas dans le dictionnaire (= lettres autorisées)
    if ligne not in LETTRE_VALEUR.keys():
        return False

    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])

    # Prend la valeur associée a la lettre donnée par l'utilisateur
    valeur_lettre = LETTRE_VALEUR[ligne]

    if (0 < valeur_lettre <= nb_lignes) and (0 < colonne <= nb_colonnes):
        return True
    else:
        return False


def est_au_bon_format(message: str) -> bool:
    if len(message) != 2:
        return False

    lettre = message[0]
    chiffre = message[1]

    # Si le code ascii de lettre n'est pas compris entre le code ascii de A et Z inclus
    if not (65 <= ord(lettre) <= 90):
        return False

    # Si le code ascii de chiffre n'est pas compris entre le code ascii de 0 et 9 inclus
    if not (48 <= ord(chiffre) <= 57):
        return False

    return True


def saisie_coordonnees(grille: list[list]) -> tuple:
    while True:  # Boucle tant que l'utilisateur n'a pas rentré une information valide qui menerait à un return -> sortie de fonction
        reponse_utilisateur = str(input("Veuillez entrez des coordonnées : ")).upper()

        if reponse_utilisateur == "FF":
            return (-1, -1)

        if not est_au_bon_format(reponse_utilisateur):
            print("Format invalide : [A-H][1-8]")
            continue  # Recommence la boucle au début (passe tout le code suivant)

        ligne = reponse_utilisateur[0]
        colonne = reponse_utilisateur[1]

        if est_dans_grille(ligne, int(colonne), grille):
            return (LETTRE_VALEUR[ligne] - 1, int(colonne) - 1)

        else:
            print("La position n'est pas dans la grille.")


def lister_captures_pion(
    ligne: int, colonne: int, couleur: str, grille: list[list]
) -> list[tuple]:
    captures_possibles = []
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]

    for diff_l, diff_c in directions:
        ligne_arrivee = ligne + diff_l
        colonne_arrivee = colonne + diff_c

        if 0 <= ligne_arrivee < 8 and 0 <= colonne_arrivee < 8:
            ligne_milieu = ligne + (diff_l // 2)
            colonne_milieu = colonne + (diff_c // 2)

            case_arrivee = grille[ligne_arrivee][colonne_arrivee]
            pion_milieu = grille[ligne_milieu][colonne_milieu]

            if case_arrivee == " " and pion_milieu != " " and pion_milieu != couleur:
                captures_possibles.append((ligne_arrivee, colonne_arrivee))

    return captures_possibles


def peut_capturer(ligne: int, colonne: int, couleur: str, grille: list[list]) -> bool:
    return len(lister_captures_pion(ligne, colonne, couleur, grille)) > 0


def analyser_distance_diagonale(
    ligne_base: int, colonne_base: int, ligne_finale: int, colonne_finale: int
) -> int:
    # Renvoie 1 pour un déplacement simple, 2 pour une capture, 0 si le mouvement est illégal
    diff_lignes = abs(ligne_finale - ligne_base)
    diff_colonnes = abs(colonne_finale - colonne_base)

    if diff_lignes == diff_colonnes and diff_lignes in [1, 2]:
        return diff_lignes
    return 0


def est_mouvement_vers_avant(
    couleur_pion: str, ligne_base: int, ligne_finale: int
) -> bool:
    if couleur_pion == "b":
        return ligne_finale < ligne_base  # Les blancs montent (index diminue)
    elif couleur_pion == "n":
        return ligne_finale > ligne_base  # Les noirs descendent (index augmente)
    return False


def obtenir_coordonnees_milieu(
    ligne_base: int, colonne_base: int, ligne_finale: int, colonne_finale: int
) -> tuple[int, int]:

    # Fait la moyenne pour trouver la case survolée lors d'un saut
    ligne_milieu = (ligne_base + ligne_finale) // 2
    colonne_milieu = (colonne_base + colonne_finale) // 2
    return ligne_milieu, colonne_milieu


def selectionner_pion_depart(
    grille: list[list], lettre_couleur: str
) -> tuple[str, int, int]:

    # Gère la boucle de sélection du pion (s'assure que le joueur choisit SA couleur)

    while True:
        print("Quel pion souhaitez-vous déplacer ? (FF pour abandonner)")

        pion_joueur_actif, ligne_base, colonne_base = demander_saisie_pion_a_deplacer(
            grille
        )

        if pion_joueur_actif == "FF":
            return "FF", -1, -1

        possibilités = coups_possible_pour_pion_donne(
            grille, ligne_base, colonne_base, lettre_couleur
        )
        if len(possibilités) == 0:
            print("Le pion que voulez sélectionner n'a pas de coup possible.")

        elif est_meme_couleur(lettre_couleur, pion_joueur_actif):
            return pion_joueur_actif, ligne_base, colonne_base

        elif pion_joueur_actif == " ":
            print("Cette case est vide, veuillez sélectionner un de vos pions.")

        else:
            print("Ce pion adverse ne vous appartient pas.")


def est_meme_couleur(couleur_case_base: str, couleur_case_finale: str):

    if couleur_case_base == couleur_case_finale:
        return True
    else:
        return False


def est_diagonale(
    ligne_base: int, colonne_base: int, ligne_finale: int, colonne_finale: int
) -> bool:

    # On calcule la distance absolue parcourue
    diff_lignes = abs(ligne_finale - ligne_base)
    diff_colonnes = abs(colonne_finale - colonne_base)

    # C'est une diagonale d'une seule case si la différence est de 1 sur les deux axes
    if diff_lignes == 1 and diff_colonnes == 1:
        return True
    return False


def demander_saisie_pion_a_deplacer(
    grille: list[list],
) -> tuple[str, int, int]:
    coordonnees = saisie_coordonnees(grille)

    if coordonnees == (-1, -1):
        return "FF", -1, -1

    ligne, colonne = coordonnees
    pion_joueur_actif = grille[ligne][colonne]

    return pion_joueur_actif, ligne, colonne


def deplacer_pion(
    grille: list[list],
    tour_de_jeu: str,
    nb_pions_captures_noirs: int,
    nb_pions_captures_blancs: int,
) -> int:

    LETTRE_COULEUR = tour_de_jeu[0]
    nb_pion_mange = 0

    pion_joueur_actif, ligne_base, colonne_base = selectionner_pion_depart(
        grille, LETTRE_COULEUR
    )

    # 2. La boucle de déplacement et d'enchaînement
    en_chainement = False

    while True:
        if en_chainement:
            print(
                "Vous devez continuer à capturer. Où souhaitez-vous faire atterrir ce pion ?"
            )
            afficher_grille(
                grille, tour_de_jeu, nb_pions_captures_noirs, nb_pions_captures_blancs
            )
        else:
            if pion_joueur_actif == "FF":
                return -1

            print("Où souhaitez-vous le déplacer ?")

        case_position_finale, ligne_finale, colonne_finale = (
            demander_saisie_pion_a_deplacer(grille)
        )

        # On cherche la distance du déplacement
        distance = analyser_distance_diagonale(
            ligne_base, colonne_base, ligne_finale, colonne_finale
        )

        if distance == 0:
            print("Déplacement incorrect. Diagonale de 1 ou 2 cases uniquement.")
            continue

        if case_position_finale != " ":
            print("Mouvement impossible : la case d'arrivée est occupée.")
            continue

        # Cas 1 : déplacement simple
        if distance == 1:
            if en_chainement:
                print(
                    "Mouvement interdit : lors d'un enchainement, vous êtes obligé de capturer !"
                )
                continue

            if not est_mouvement_vers_avant(LETTRE_COULEUR, ligne_base, ligne_finale):
                print(
                    "Mouvement invalide : un pion simple ne peut avancer que vers l'avant !"
                )
                continue

            grille[ligne_finale][colonne_finale] = pion_joueur_actif
            grille[ligne_base][colonne_base] = " "
            return nb_pion_mange

        # cas 2 : Capture
        if distance == 2:
            # On prend le pion du milieu
            ligne_milieu, colonne_milieu = obtenir_coordonnees_milieu(
                ligne_base, colonne_base, ligne_finale, colonne_finale
            )
            pion_saute = grille[ligne_milieu][colonne_milieu]

            if pion_saute == " " or pion_saute == LETTRE_COULEUR:
                print("Saut invalide : vous devez sauter par-dessus un pion adverse !")
                continue

            grille[ligne_finale][colonne_finale] = pion_joueur_actif
            grille[ligne_base][colonne_base] = " "
            grille[ligne_milieu][colonne_milieu] = " "

            nb_pion_mange += 1
            print(f"pion adverse capturé ! (Total ce tour : {nb_pion_mange})")

            # enchainement
            if peut_capturer(ligne_finale, colonne_finale, LETTRE_COULEUR, grille):
                ligne_base = ligne_finale
                colonne_base = colonne_finale
                en_chainement = True
                continue
            else:
                # Plus rien a manger, on sort de la fonction
                return nb_pion_mange


def directions_simple_par_couleur(tour_de_jeu: str) -> list[tuple]:
    LETTRE_COULEUR = tour_de_jeu[0]

    directions_simples = []
    if LETTRE_COULEUR == "b":
        directions_simples = [(-1, -1), (-1, 1)]
    elif LETTRE_COULEUR == "n":
        directions_simples = [(1, -1), (1, 1)]

    return directions_simples


def deplacer_pion_ia_naive(grille: list[list], tour_de_jeu: str) -> int:
    LETTRE_COULEUR = tour_de_jeu[0]
    nb_pion_mange = 0

    liste_des_coups = coups_possibles(grille, tour_de_jeu)

    if len(liste_des_coups) == 0:
        return 0  # Aucun coup possible, ia bloquée.

    coup_choisi = liste_des_coups[randint(0, len(liste_des_coups) - 1)]

    (ligne_base, colonne_base), (ligne_finale, colonne_finale) = coup_choisi

    distance = analyser_distance_diagonale(
        ligne_base, colonne_base, ligne_finale, colonne_finale
    )

    grille[ligne_finale][colonne_finale] = LETTRE_COULEUR
    grille[ligne_base][colonne_base] = " "

    # Déplacement simple
    if distance == 1:
        print("L'ordinateur a effectué un déplacement simple.")

        return 0

    # Capture, vérifier l'enchainement.
    elif distance == 2:
        ligne_milieu, colonne_milieu = obtenir_coordonnees_milieu(
            ligne_base, colonne_base, ligne_finale, colonne_finale
        )
        grille[ligne_milieu][colonne_milieu] = " "
        nb_pion_mange += 1
        print("L'ordinateur a capturé un pion.")

        while True:
            captures_suivantes = lister_captures_pion(
                ligne_finale, colonne_finale, LETTRE_COULEUR, grille
            )

            if len(captures_suivantes) == 0:
                break

            print("L'ordinateur est en plein enchaînement.")

            prochain_coup = captures_suivantes[randint(0, len(captures_suivantes) - 1)]
            nouvelle_ligne_finale, nouvelle_colonne_finale = prochain_coup

            ligne_milieu, colonne_milieu = obtenir_coordonnees_milieu(
                ligne_finale,
                colonne_finale,
                nouvelle_ligne_finale,
                nouvelle_colonne_finale,
            )
            grille[ligne_milieu][colonne_milieu] = " "

            grille[nouvelle_ligne_finale][nouvelle_colonne_finale] = LETTRE_COULEUR
            grille[ligne_finale][colonne_finale] = " "

            nb_pion_mange += 1
            ligne_finale = nouvelle_ligne_finale
            colonne_finale = nouvelle_colonne_finale

    return nb_pion_mange


def coups_possible_pour_pion_donne(
    grille: list[list[str]], ligne_pion: int, colonne_pion: int, tour_de_jeu: str
) -> list:
    LETTRE_COULEUR = tour_de_jeu[0]
    coups_simples = []
    coups_captures = lister_captures_pion(
        ligne_pion, colonne_pion, LETTRE_COULEUR, grille
    )

    directions_simples = directions_simple_par_couleur(tour_de_jeu)

    for diff_i, diff_j in directions_simples:
        ligne_finale = ligne_pion + diff_i
        colonne_finale = colonne_pion + diff_j

        if 0 <= ligne_finale < 8 and 0 <= colonne_finale < 8:
            if grille[ligne_finale][colonne_finale] == " ":
                coups_simples.append((ligne_finale, colonne_finale))

    return coups_captures if len(coups_captures) > 0 else coups_simples


def coups_possibles(grille: list[list[str]], tour_de_jeu: str) -> list[tuple]:
    LETTRE_COULEUR = tour_de_jeu[0]
    coups_simples = []
    coups_captures = []

    for i in range(8):
        for j in range(8):
            if grille[i][j] == LETTRE_COULEUR:
                destinations_capture = lister_captures_pion(
                    i, j, LETTRE_COULEUR, grille
                )
                for destination in destinations_capture:
                    coups_captures.append(((i, j), destination))

                directions_simples = directions_simple_par_couleur(tour_de_jeu)

                for diff_i, diff_j in directions_simples:
                    ligne_finale = i + diff_i
                    colonne_finale = j + diff_j

                    if 0 <= ligne_finale < 8 and 0 <= colonne_finale < 8:
                        if grille[ligne_finale][colonne_finale] == " ":
                            coups_simples.append(
                                ((i, j), (ligne_finale, colonne_finale))
                            )

    # Priorité à la capture car si on peut manger on doit le faire.
    if len(coups_captures) > 0:
        return coups_captures
    else:
        return coups_simples


def demander_mode_de_jeu() -> str:
    mode_de_jeu = int(
        input(
            "Veuillez sélectionner votre mode de jeu : \n1 - joueur contre joueur\n2 - joueur contre ordinateur\n"
        )
    )

    while mode_de_jeu not in [1, 2]:
        mode_de_jeu = int(
            input(
                "Veuillez sélectionner votre mode de jeu : \n1 - joueur contre joueur\n2 - joueur contre ordinateur\n"
            )
        )

    return "jcj" if mode_de_jeu == 1 else "jco"


def demander_grille() -> list[list]:
    grille_input = int(
        input(
            "Veuillez choisir la grille en fonction de l'avancée du jeu : \n1 - type début de partie\n2 - type milieu de partie\n3 - fin de partie\n"
        )
    )

    while grille_input not in [1, 2, 3]:
        grille_input = int(
            input(
                "Veuillez choisir la grille en fonction de l'avancée du jeu : \n1 - type début de partie\n2 - type milieu de partie\n3 - fin de partie\n"
            )
        )

    if grille_input == 1:
        return creer_grille_debut_partie()
    elif grille_input == 2:
        return creer_grille_milieu_partie()
    else:
        return creer_grille_fin_partie()


def afficher_grille(
    grille: list[list],
    tour_de_jeu: str,
    nb_pions_captures_noirs: int,
    nb_pions_captures_blancs: int,
):

    # print(f"...") permet de mettre une variable dans un print et d'éviter de faire print("..." + variable + "...")

    lettres = ["H", "G", "F", "E", "D", "C", "B", "A"]
    # Permet d'afficher les lettres sur le coté, a chaque itération on pop le tableau (= on enleve le dernier element et on l'affiche).

    print("""
--------------------------------------
| x |  1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
--------------------------------------""")

    for ligne in grille:
        print(f"| {lettres.pop()} | ", end="")

        for element in ligne:
            print(f" {element} |", end="")

        print("")

    print("--------------------------------------")

    print(
        f"Les noirs ont capturés {nb_pions_captures_noirs} pièces.\nLes blancs ont capturés {nb_pions_captures_blancs} pièces.\n "
    )
    print(f"C'est au tour des {tour_de_jeu} de jouer.\n")


def jeu(tour_de_jeu: str):
    nb_pions_captures_par_noirs = 0
    nb_pions_captures_par_blancs = 0

    grille = demander_grille()
    type_jeu = demander_mode_de_jeu()

    while True:
        afficher_grille(
            grille,
            tour_de_jeu,
            nb_pions_captures_par_noirs,
            nb_pions_captures_par_blancs,
        )

        if type_jeu == "jcj" or tour_de_jeu == "blancs":
            nb_pions_manges = deplacer_pion(
                grille,
                tour_de_jeu,
                nb_pions_captures_par_noirs,
                nb_pions_captures_par_blancs,
            )
        else:
            # Faire la liste des coups possibles et appliquer le déplacement.
            nb_pions_manges = deplacer_pion_ia_naive(grille, tour_de_jeu)

        if nb_pions_manges == -1:
            print(
                f"\nLes {tour_de_jeu} ont décidés d'abandonner, ce qui met fin à la partie sur la défaite de {tour_de_jeu} !"
            )
            break

        if tour_de_jeu == "blancs":
            nb_pions_captures_par_blancs += nb_pions_manges
            tour_de_jeu = "noirs"

        else:
            nb_pions_captures_par_noirs += nb_pions_manges
            tour_de_jeu = "blancs"

        if len(coups_possibles(grille, tour_de_jeu)) == 0:
            print(
                f"les {tour_de_jeu} n'ont plus de coups valable, la partie se termine donc avec la défaite des {tour_de_jeu} !"
            )
            break

        if nb_pions_captures_par_blancs >= 12:
            print(
                "Les blancs ont remportés la victoire, ils ont capturés tous les pions adverses."
            )
            break

        elif nb_pions_captures_par_noirs >= 12:
            print(
                "Les noirs ont remportés la victoire, ils ont capturés tous les pions adverses."
            )
            break


def main():
    # Fonction principale, appelle les autres fonctions et stocke les variables ici.
    # On teste d'abord si le code tourne sinon le programme s'arrete
    test()

    tour_de_jeu = "blancs"

    jeu(tour_de_jeu)


###### TESTS #######


def test():  # Fonction de test principale, appelle chacune des petites fonctions de test et effectue un test global

    def test_est_au_bon_format():

        assert est_au_bon_format("A8")
        assert not est_au_bon_format("AA")
        assert not est_au_bon_format("55")
        assert not est_au_bon_format("A12")
        assert not est_au_bon_format("")
        assert est_au_bon_format("Z9")

    def test_est_dans_grille():

        grille = creer_grille_debut_partie()
        assert est_dans_grille("A", 3, grille)
        assert not est_dans_grille("M", 2, grille)
        assert not est_dans_grille("B", 9, grille)
        assert not est_dans_grille("", 3, grille)
        assert not est_dans_grille("", 0, grille)

    def test_est_diagonale():

        assert est_diagonale(3, 3, 4, 4)  # Diagonale Bas-Droite
        assert est_diagonale(3, 3, 2, 2)  # Diagonale Haut-Gauche
        assert est_diagonale(3, 3, 4, 2)  # Diagonale Bas-Gauche
        assert est_diagonale(3, 3, 2, 4)  # Diagonale Haut-Droite
        assert not est_diagonale(3, 3, 3, 3)  # Aucun mouvement (reste sur la même case)
        assert not est_diagonale(3, 3, 5, 5)  # Diagonale de 2 cases
        assert not est_diagonale(1, 1, 8, 8)  # Diagonale de bout en bout du plateau
        assert not est_diagonale(3, 3, 5, 4)  # +2 lignes, +1 colonne
        assert not est_diagonale(3, 3, 2, 5)  # -1 ligne, +2 colonnes

    def test_est_meme_couleur():
        # Cas vrais
        assert est_meme_couleur("n", "n")
        assert est_meme_couleur("b", "b")
        # Cas faux
        assert not est_meme_couleur("n", "b")
        assert not est_meme_couleur("b", " ")
        assert not est_meme_couleur("n", " ")

    def test_analyser_distance_diagonale():
        # Déplacements de 1 case (Doit renvoyer 1)
        assert analyser_distance_diagonale(2, 2, 3, 3) == 1
        assert analyser_distance_diagonale(4, 4, 3, 5) == 1

        # Déplacements de 2 cases (Doit renvoyer 2)
        assert analyser_distance_diagonale(2, 2, 4, 4) == 2
        assert analyser_distance_diagonale(4, 4, 2, 2) == 2

        # Déplacements illégaux (Doit renvoyer 0)
        assert analyser_distance_diagonale(2, 2, 2, 2) == 0  # Sur place
        assert analyser_distance_diagonale(2, 2, 5, 5) == 0  # Diagonale de 3 cases
        assert (
            analyser_distance_diagonale(2, 2, 2, 3) == 0
        )  # Ligne droite (horizontale)
        assert analyser_distance_diagonale(2, 2, 4, 3) == 0  # Mouvement de cavalier

    def test_obtenir_coordonnees_milieu():
        assert obtenir_coordonnees_milieu(2, 2, 4, 4) == (3, 3)
        assert obtenir_coordonnees_milieu(4, 2, 2, 4) == (3, 3)
        assert obtenir_coordonnees_milieu(5, 5, 3, 3) == (4, 4)

    def test_est_mouvement_vers_avant():
        # Test pour les blancs
        assert est_mouvement_vers_avant("b", 5, 4)
        assert est_mouvement_vers_avant("b", 5, 3)
        assert not est_mouvement_vers_avant("b", 5, 6)
        assert not est_mouvement_vers_avant("b", 5, 5)
        # Tests pour les noirs
        assert est_mouvement_vers_avant("n", 2, 3)
        assert est_mouvement_vers_avant("n", 2, 4)
        assert not est_mouvement_vers_avant("n", 2, 1)
        assert not est_mouvement_vers_avant("n", 2, 2)

        assert not est_mouvement_vers_avant("z", 1, 2)

    def test_peut_capturer():
        grille_test = [
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "b", " ", " ", " ", " "],
            [" ", " ", "n", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
        ]
        assert peut_capturer(2, 3, "b", grille_test)
        assert peut_capturer(3, 2, "n", grille_test)
        assert not peut_capturer(0, 0, "b", grille_test)

    # Appel des sous-fonctions de test
    test_est_au_bon_format()
    test_est_dans_grille()
    test_est_diagonale()
    test_est_meme_couleur()
    test_analyser_distance_diagonale()
    test_obtenir_coordonnees_milieu()
    test_est_mouvement_vers_avant()
    test_peut_capturer()

    print(" TESTS OK")


main()
