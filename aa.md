Exercice 2
EX2.1
Écrire un programme C pour faire communiquer un processus fils avec son processus père. Le processus fils doit écrire un entier dans un fichier, puis le processus père doit récupérer cet entier en le lisant dans le fichier.

Explication et Code :
Le programme ci-dessous illustre la communication entre un processus père et ses processus fils. Le processus père crée deux processus fils. Chaque processus fils écrit un entier différent dans un fichier distinct. Après avoir écrit ces entiers, chaque fils envoie un signal SIGUSR1 au père pour indiquer qu'il a terminé. Le père, après avoir reçu les signaux des deux fils, lit les entiers depuis les fichiers et les affiche.

Le code comprend également la suppression des fichiers après leur lecture, pour éviter de laisser des fichiers temporaires.

C
Copy code
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>

volatile sig_atomic_t flag_child1 = 0;
volatile sig_atomic_t flag_child2 = 0;

void ecrire_fils(int nb, char* name);
void lire_pere(int* nb, char* name);
void handler(int signum);

int main() {
    int nb1, nb2;
    pid_t pid1, pid2;

    // Configuration des gestionnaires de signal pour SIGUSR1
    signal(SIGUSR1, handler);

    // Création du premier fils
    pid1 = fork();
    
    if(pid1 == -1) exit(EXIT_FAILURE); // Erreur lors de la création du processus fils

    if(pid1 == 0) { // Processus fils 1
        ecrire_fils(111, "tmp1.txt"); // Écrire l'entier 111 dans le fichier tmp1.txt
        kill(getppid(), SIGUSR1); // Envoyer le signal SIGUSR1 au père
        exit(EXIT_SUCCESS);
    }
    else { // Processus père
        // Création du deuxième fils
        pid2 = fork();

        if (pid2 == -1) exit(EXIT_FAILURE); // Erreur lors de la création du processus fils 2

        if (pid2 == 0) { // Processus fils 2
            ecrire_fils(222, "tmp2.txt"); // Écrire l'entier 222 dans le fichier tmp2.txt
            kill(getppid(), SIGUSR1); // Envoyer le signal SIGUSR1 au père
            exit(EXIT_SUCCESS);
        } 
        else { // Processus père
            // Attente des signaux des deux fils
            while (!(flag_child1 && flag_child2)) {
                pause(); // Attendre un signal
            }

            // Lecture des valeurs écrites par les fils
            lire_pere(&nb1, "tmp1.txt");
            lire_pere(&nb2, "tmp2.txt");

            printf("Entier récupéré depuis tmp1.txt : %d\n", nb1);
            printf("Entier récupéré depuis tmp2.txt : %d\n", nb2);
        }
    }
    return 0;
}

void ecrire_fils(int nb, char* name) {
    FILE *fichier;
    fichier = fopen(name, "w");
    if (fichier == NULL) exit(EXIT_FAILURE);
    fprintf(fichier, "%d", nb);
    fclose(fichier);
}

void lire_pere(int* nb, char* name) {
    FILE *fichier;
    fichier = fopen(name, "r");
    if (fichier == NULL) exit(EXIT_FAILURE);
    fscanf(fichier, "%d", nb);
    fclose(fichier);
    remove(name); // Suppression du fichier
}

void handler(int signum) {
    if (signum == SIGUSR1) {
        if (flag_child1 == 0)
            flag_child1 = 1;
        else
            flag_child2 = 1;
    }
}
EX2.2
Expliquer comment le programme gère la communication entre le processus père et les processus fils.

Le programme utilise plusieurs concepts pour gérer la communication entre le processus père et les processus fils :

Fork: Le processus père utilise fork() pour créer deux processus fils. Chaque fork() crée un nouveau processus qui exécute le même code que le père mais continue son exécution à partir du point de la création du fork.

Écriture de Fichiers: Chaque processus fils écrit un entier différent dans un fichier distinct (tmp1.txt et tmp2.txt). Ce mécanisme est utilisé pour la communication de données entre les processus.

Signaux: Après avoir écrit dans le fichier, chaque fils envoie un signal SIGUSR1 au processus père. Ce signal sert d'indicateur au père que le fils a terminé son opération.

Handler de Signal: Le père utilise un gestionnaire de signal (handler) pour gérer les signaux SIGUSR1 reçus. Ce gestionnaire met à jour les indicateurs flag_child1 et flag_child2 pour chaque signal reçu.

Lecture de Fichiers: Après avoir reçu les signaux des deux fils, le père lit les entiers depuis les fichiers correspondants. Cela permet de récupérer les données écrites par les fils.

Suppression de Fichiers: Une fois les données lues, les fichiers sont supprimés pour nettoyer les ressources et éviter les fichiers temporaires inutiles.

En combinant ces techniques, le programme réalise une communication efficace entre le processus père et ses processus fils, tout en garantissant la synchronisation et le nettoyage des ressources.
